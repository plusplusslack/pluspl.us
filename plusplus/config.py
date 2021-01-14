import os

VERSION = 0.1
NAME = os.environ.get("NAME")
SLACK_CLIENT_ID = os.environ.get('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.environ.get('SLACK_CLIENT_SECRET')
SLACK_SCOPES = "chat:write,im:history,im:write,mpim:history,mpim:write,team:read,channels:history,app_mentions:read,groups:history,groups:read,groups:write"
SLACK_OAUTH_URL = f"https://slack.com/oauth/v2/authorize?client_id={SLACK_CLIENT_ID}&scope={SLACK_SCOPES}"
SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SUPPORT_EMAIL = os.environ.get("SUPPORT_EMAIL")
SENTRY_URL = os.environ.get("SENTRY_URL")
TRAP_BAD_REQUEST_ERRORS = os.environ.get('TRAP_BAD_REQUEST_ERRORS', False)
