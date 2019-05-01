from operations import process_match, generate_string
from leaderboard import generate_leaderboard
from help import help_text
from models import db, SlackTeam
import re
import config

operation_exp = re.compile(r"(<?@|#)(.+)(\+\+|\-\-|==)")


def process_incoming_message(event_data, req):
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
    channel_type = event.get('channel_type')

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
        team.slack_client().api_call(
            "chat.postMessage",
            channel=channel,
            text=output
        )
        print("Processed " + thing.item)
    elif "leaderboard" in message and team.bot_user_id.lower() in message:
        team.slack_client().api_call(
            "chat.postMessage",
            channel=channel,
            blocks=generate_leaderboard(team)
        )
        print("Processed leaderboard for team " + team.id)
    elif "loserboard" in message and team.bot_user_id.lower() in message:
        team.slack_client().api_call(
            "chat.postMessage",
            channel=channel,
            blocks=generate_leaderboard(team, losers=True)
        )
        print("Processed loserboard for team " + team.id)
    elif "help" in message and (team.bot_user_id.lower() in message or channel_type=="im"):
        team.slack_client().api_call(
            "chat.postMessage",
            channel=channel,
            blocks=help_text(team)
        )
        print("Processed help for team " + team.id)
    elif "feedback" in message and (team.bot_user_id.lower() in message or channel_type=="im"):
        print(message)
        team.slack_client().api_call(
            "chat.postMessage",
            channel=channel,
            text="Thanks! For a more urgent response, please email " + config.SUPPORT_EMAIL
        )
    return "OK", 200
