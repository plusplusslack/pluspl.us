from plusplus.operations.points import update_points, generate_string
from plusplus.operations.leaderboard import generate_leaderboard
from plusplus.operations.help import help_text
from plusplus.models import db, SlackTeam
from plusplus import config
import re

user_exp = re.compile(r"<@([A-Za-z0-9]+)>(\+\+|\-\-|==)")
thing_exp = re.compile(r"#(.+)(\+\+|\-\-|==)")

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

    user_match = user_exp.match(message)
    thing_match = thing_exp.match(message)
    if user_match:
        # handle user point operations
        found_user = user_match.groups()[0]
        operation = user_match.groups()[1]
        thing = Thing.query.filter_by(item=found_user.lower(), team=team).first()
        if not thing:
            thing = Thing(item=found_user.lower(), points=0, user=True, team_id=team.id)
        message = update_points(thing, operation, is_self=user==found_user)
        team.slack_client().api_call(
            "chat.postMessage",
            channel=channel,
            text=message
        )
        print("Processed " + thing.item)
    elif thing_match:
        # handle thing point operations
        found_thing = thing_match.groups()[0]
        operation = thing_match.groups()[1]
        thing = Thing.query.filter_by(item=found_thing.lower(), team=team).first()
        if not thing:
            thing = Thing(item=found_thing.lower(), points=0, user=False, team_id=team.id)
        message = update_points(thing, operation)
        team.slack_client().api_call(
            "chat.postMessage",
            channel=channel,
            text=message
        )
        print("Processed " + thing.item)
    elif "leaderboard" in message and team.bot_user_id.lower() in message:
        global_board = "global" in message
        team.slack_client().api_call(
            "chat.postMessage",
            channel=channel,
            blocks=generate_leaderboard(team=team, global_leaderboard=global_board)
        )
        print("Processed leaderboard for team " + team.id)
    elif "loserboard" in message and team.bot_user_id.lower() in message:
        global_board = "global" in message
        team.slack_client().api_call(
            "chat.postMessage",
            channel=channel,
            blocks=generate_leaderboard(team=team, losers=True, global_leaderboard=global_board)
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
