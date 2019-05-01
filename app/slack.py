from flask import Blueprint, request, redirect
from flask import current_app as app
from slackclient import SlackClient
from models import db, SlackTeam
from sqlalchemy.exc import IntegrityError

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
    if 'error' in data:  # abort if error
        print("ERROR: " + data['error'])
        return redirect('/not_installed')

    # create new team or update data
    try:
        team = SlackTeam(data)
        db.session.add(team)
        db.session.commit()
        print("Created team " + team.id)
    except IntegrityError:
        db.session().rollback()
        team = SlackTeam.query.filter_by(id=data['team_id']).first()
        team.update(data)
        db.session.add(team)
        db.session.commit()
        print("Updated tokens for team " + team.id)
    return redirect('/installed')


@slack.route('/auth')
def slack_auth():
    return redirect(app.config['SLACK_OAUTH_URL'])
