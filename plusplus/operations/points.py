from plusplus.models import db
import json
import random


def update_points(thing, end, is_self=False):
    if is_self and end != '==':  # don't allow someone to plus themself
        operation = "self"
    elif end == "++":
        operation = "plus"
        thing.increment()
    elif end == "--":
        operation = "minus"
        thing.decrement()
    else:
        operation = "equals"
    db.session.add(thing)
    db.session.commit()
    return generate_string(thing, operation)


def generate_string(thing, operation):
    if thing.user:
        formatted_thing = f"<@{thing.item.upper()}>"
    else:
        formatted_thing = thing.item
    points = thing.points
    points_word = "points" if points > 1 else "point"
    points_string = f"{points} {points_word}"
    out = ""
    with open("plusplus/strings.json", "r") as strings:
        parsed = json.load(strings)
        if operation in ["plus", "minus"]:
            exclamation = random.choice(parsed[operation])
            random_msg = random.choice(parsed[operation + "_points"])
            points = random_msg.format(thing=formatted_thing, points_string=points_string)
            out = f"{exclamation} {points}"
        elif operation == "self":
            out = random.choice(parsed[operation]).format(thing=formatted_thing)
        elif operation == "equals":
            out = random.choice(parsed[operation]).format(thing=formatted_thing, points_string=points_string)
    out += "\n\n:warning: ATTENTION: pluspl.us will be shutdown on August 31, 2021. "
    out += "Please see the help page (https://plusplusserver.herokuapp.com/sunset) for details "
    out += "and information on how to export your team's data. Thanks for using pluspl.us, we'll miss you :wave:"
    return out
