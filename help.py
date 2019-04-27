def help_text(team):
    commands = ["• `@(user)++`: add points to a user (e.g. {bot_ping}++) ",
                "• `@(user)--`: take points from a user (e.g. {bot_ping}--)",
                "• `#(thing)++`: give points to a thing (e.g. #jake++)",
                "• `#(thing)--`: take points from a thing (e.g. #jake--)",
                "• {bot_ping} leaderboard: get the current high scoring people and things",
                "• {bot_ping} loserboard: get the current low scoring people and things",
                "• {bot_ping} feedback <feedback>: send feedback about this bot to its owner"]
    for command in commands:
        command.format(bot_ping="@<@{team.bot_user_id}>")

    help_block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Hey hey! Here's a quick rundown on how to use <@{team.bot_user_id}>"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "\n".join(commands)
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Still need help? Send us an email at support@pluspl.us!"
            }
        }
    ]
    return help_block
