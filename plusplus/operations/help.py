from .. import config


def help_text(team):
    commands = ["• *@(user)++*: add points to a user (e.g. {ping}++) ",
                "• *@(user)--*: take points from a user (e.g. {ping}--)",
                "• *@(user)==*: get current point total of a user (e.g. {ping}==)",
                "• *#(thing)++*: give points to a thing (e.g. #jake++)",
                "• *#(thing)--*: take points from a thing (e.g. #jake--)",
                "• *#(thing)==*: get current point total of a thing (e.g. #jake==)",
                "• *{ping} leaderboard*: get the current high scoring people and things",
                "• *{ping} loserboard*: get the current low scoring people and things",
                "• *{ping} reset*: resets the local leaderboard to 0",
                "• *{ping} feedback <feedback>*: send feedback about this bot to its wrangler"]
    formatted_commands = list()
    for command in commands:
        formatted_commands.append(command.format(ping=f"<@{team.bot_user_id}>"))

    help_block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hey hey! Here's a quick rundown on how to use <@{team.bot_user_id}>"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "\n".join(formatted_commands)
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Still need help? Send us an email at {config.SUPPORT_EMAIL}!"
            }
        }
    ]
    return help_block
