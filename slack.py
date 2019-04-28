from flask import Blueprint, request, redirect
from flask import current_app as app
from slackclient import SlackClient
from models import db, SlackTeam

slack = Blueprint('slack', __name__)


@slack.route('/callback')
def callback():
    # first check for errors
    if request.args.get('error'):
        return redirect('/not_installed')

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
    return redirect('/installed')


@slack.route('/auth')
def slack_auth():
    return redirect(app.config['SLACK_OAUTH_URL'])
