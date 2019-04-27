from flask import Flask, redirect, request
from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
from operations import process_match, generate_string
from leaderboard import generate_leaderboard
from models import db, SlackTeam
import re

# get Slack secret
operation_exp = re.compile(r"(<?@|#)(.+)(\+\+|\-\-|==)")

# flask init
app = Flask(__name__)
app.config.from_object('config')

# init slack event adaptor
slack = SlackEventAdapter(app.config['SLACK_SIGNING_SECRET'], "/slack/events", app)

# init SQLAlchemy
with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route('/callback')
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


@slack.on("message")
def handle_message(event_data, req):
    # ignore retries
    if req.headers.get('X-Slack-Retry-Reason'):
        return "Status: OK"
    # ignore bot messages
    if 'subtype' in event_data['event'] and event_data['event']['subtype'] == 'bot_message':
        return "Status: OK"

    event = event_data['event']
    message = event.get('text').lower()
    user = event.get('user').lower()
    channel = event.get('channel')

    # load/update team
    team = SlackTeam.query.filter_by(id=event_data['team_id']).first()
    team.update_last_access()
    db.session.add(team)
    db.session.commit()

    operation_match = operation_exp.match(message)
    if operation_match:
        thing, operation = process_match(operation_match, user, team)
        db.session.add(thing)
        db.session.commit()
        output = generate_string(thing, operation)
        team.api_call(
            "chat.postMessage",
            channel=channel,
            text=output
        )
        print("Processed " + thing.item)
    elif "leaderboard" in message and team.bot_user_id in message:
        team.api_call(
            "chat.postMessage",
            channel=channel,
            blocks=generate_leaderboard()
        )
        print("Processed leaderboard for team " + team.id)
    elif "loserboard" in message and team.bot_user_id in message:
        team.api_call(
            "chat.postMessage",
            channel=channel,
            blocks=generate_leaderboard(losers=True)
        )
        print("Processed loserboard for team " + team.id)
    return "OK", 200


if __name__ == '__main__':
    app.run(port=3000)
