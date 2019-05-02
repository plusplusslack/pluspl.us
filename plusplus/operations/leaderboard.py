from ..models import Thing
import json


def generate_leaderboard(team=None, losers=False, global_leaderboard=False):
    if losers:
        ordering = Thing.points.asc()
        header = "Here's the current loserboard:"
    else:
        ordering = Thing.points.desc()
        header = "Here's the current leaderboardboard:"

    # filter args
    user_args = {"user": True}
    thing_args = {"user": False}
    if not global_leaderboard:
        user_args['team'] = team
        thing_args['team'] = team
        users = Thing.query.filter_by(**user_args).order_by(ordering).limit(10)

    things = Thing.query.filter_by(**thing_args).order_by(ordering).limit(10)

    formatted_things = [f"{thing.item} ({thing.points})" for thing in things]
    numbered_things = generate_numbered_list(formatted_things)
    leaderboard_header = {"type": "section",
                          "text":
                              {"type": "mrkdwn",
                               "text": header
                               }
                          }
    body = {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Things*\n" + numbered_things
                    }
                ]
        }

    if not global_leaderboard:
        formatted_users = [f"<@{user.item.upper()}> ({user.points})" for user in users]
        numbered_users = generate_numbered_list(formatted_users)
        body['fields'].append({
                                  "type": "mrkdwn",
                                  "text": "*Users*\n" + numbered_users
                              })
    leaderboard = [leaderboard_header, body]
    return json.dumps(leaderboard)


def generate_numbered_list(items):
    out = ""
    for i, item in enumerate(items, 1):
        out += f"{i}. {item}\n"
    if len(out) == 0:
        out = "Welp, nothing's here yet."
    return out
