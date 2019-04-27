import os

VERSION = 0.1
NAME = "PlusPlusServer"
SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET')
SLACK_TOKEN = os.environ.get('SLACK_BOT_USER_OAUTH_ACCESS_TOKEN')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SUCCESS_URL = os.environ.get('SUCCESS_URL')
ERROR_URL = os.environ.get('ERROR_URL')
