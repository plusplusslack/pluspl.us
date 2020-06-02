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
    with open("plusplus/strings.json", "r") as strings:
        parsed = json.load(strings)
        if operation in ["plus", "minus"]:
            exclamation = random.choice(parsed[operation])
            random_msg = random.choice(parsed[operation + "_points"])
            points = random_msg.format(thing=formatted_thing, points_string=points_string)
            return f"{exclamation} {points}"
        elif operation == "self":
            return random.choice(parsed[operation]).format(thing=formatted_thing)
        elif operation == "equals":
            return random.choice(parsed[operation]).format(thing=formatted_thing, points_string=points_string)
        else:
            return ""  # probably unnecessary, but here as a fallback
