from ..models import Thing
import json
import random


def process_match(match, user, team):
    # figure out what is being plus'd or minus'd
    groups = match.groups()
    # strip text to remove accidental whitepsace
    start = groups[0].strip()
    middle = groups[1].strip()
    end = groups[2].strip()

    # parse based on whether it's a user mention or something else
    if start[0] == "<":
        item = middle[:len(middle) - 1]
        is_user = True
    else:
        item = middle
        is_user = False

    # look up thing in database and increment or decrement if necessary
    thing = Thing.query.filter_by(item=item.lower(), team=team).first()
    if not thing:
        thing = Thing(item=item.lower(), points=0, user=is_user, team_id=team.id)
    if item == user and is_user and end != "==":  # don't allow someone to plus themself
        operation = "self"
        pass
    elif end == "++":
        operation = "plus"
        thing.increment()
    elif end == "--":
        operation = "minus"
        thing.decrement()
    else:
        operation = "equals"
    return thing, operation


def generate_string(thing, operation):
    if thing.user:
        item = f"<@{thing.item.upper()}>"
    else:
        item = thing.item
    points = thing.points
    with open("plusplus/strings.json", "r") as strings:
        parsed = json.load(strings)
        if operation in ["plus", "minus"]:
            exclamation = random.choice(parsed[operation])
            points = random.choice(parsed[operation + "_points"]).format(thing=item, points=points)
            return f"{exclamation} {points}"
        elif operation == "self":
            return random.choice(parsed[operation]).format(thing=item)
        elif operation == "equals":
            return random.choice(parsed[operation]).format(thing=item, points=points)
        else:
            return ""  # probably unnecessary, but here as a fallback
