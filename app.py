from flask import Flask, redirect, request
from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
from models import db, SlackTeam
from slack_handler import process_incoming_message

# flask init
app = Flask(__name__)
app.config.from_object('config')

# init slack event adaptor
slack = SlackEventAdapter(app.config['SLACK_SIGNING_SECRET'], "/slack/events", app)

# init SQLAlchemy
with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route('/slack/callback')
def callback():
    # first check for errors
    if request.args.get('error'):
        return redirect(app.config['ERROR_URL'])
        # Retrieve the auth code from the request params
    auth_code = request.args['code']

    # An empty string is a valid token for this request
    sc = SlackClient("")

    # Request the auth tokens from Slack
    data = sc.api_call(
        "oauth.access",
        client_id=app.config['SLACK_CLIENT_ID'],
        client_secret=app.config['SLACK_CLIENT_SECRET'],
        code=auth_code
    )

    team = SlackTeam(data)
    db.session.add(team)
    db.session.commit()
    return redirect(app.config['SUCCESS_URL'])


@app.route('/slack/auth')
def slack_auth():
    return redirect(app.config['SLACK_OAUTH_URL'])


@slack.on("message")
def handle_message(event_data, req):
    process_incoming_message(event_data, req)


if __name__ == '__main__':
    app.run(port=3000)
