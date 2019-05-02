from flask import Flask
from slackeventsapi import SlackEventAdapter
from models import db
from operations.slack_handler import process_incoming_message
from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk


# flask init
app = Flask(__name__)
app.config.from_object('config')

# Setup sentry
sentry_sdk.init(
    dsn=app.config['SENTRY_URL'],
    integrations=[FlaskIntegration()]
)

# init slack event adaptor
slack = SlackEventAdapter(app.config['SLACK_SIGNING_SECRET'], "/slack/events", app)

# init SQLAlchemy
with app.app_context():
    db.init_app(app)
    db.create_all()


from slack import slack as slack_blueprint
from views import views as views_blueprint
app.register_blueprint(slack_blueprint, url_prefix='/slack')
app.register_blueprint(views_blueprint)


@slack.on("message")
def handle_message(event_data, req):
    process_incoming_message(event_data, req)


if __name__ == '__main__':
    app.run(port=3000)
