from flask import Blueprint, abort, request, redirect
from flask import current_app as app
from slackclient import SlackClient
from plusplus.models import db, SlackTeam, Thing
from sqlalchemy.exc import IntegrityError
from plusplus import config
import hashlib
import hmac
import json
import requests

slack = Blueprint('slack', __name__)


@slack.route('/callback')
def callback():
    # first check for errors
    if request.args.get('error'):
        print(request.args.get('error'))
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


@slack.route('/components', methods=['POST'])
def slack_components_callback():
    # verify request manually
    req_timestamp = request.headers.get('X-Slack-Request-Timestamp')
    req_signature = request.headers.get('X-Slack-Signature')
    req_data_raw = request.get_data()
    req = str.encode('v0:' + str(req_timestamp) + ':') + req_data_raw
    request_hash = 'v0=' + hmac.new(str.encode(config.SLACK_SIGNING_SECRET), req, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(request_hash, req_signature):
        print("Received invalid signature from Slack.")
        return abort(403)
    # right now the only component being called is the delete button
    # if more are added in the future, this logic will need to change
    req_data = json.loads(request.form["payload"])
    if req_data['actions'][0]['value'] == 'delete_all':
        # delete all objects in db
        team_id = req_data['team']['id']
        Thing.query.filter_by(team_id=team_id).delete()
        db.session.commit()
        print("Deleted items for team: " + team_id)
        # replace message in Slack with who initiated this request
        response_url = req_data['response_url']
        user_id = req_data['user']['id']
        data = {"replace_original": "true", "text": f"<@{user_id}> sucessfully cleared the leaderboard for this team."}
        requests.post(response_url, json=data)
        return "OK"

    return abort(422)
