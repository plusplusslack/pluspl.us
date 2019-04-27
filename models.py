from flask_sqlalchemy import SQLAlchemy
from slackclient import SlackClient
import datetime

db = SQLAlchemy()


class SlackTeam(db.Model):
    __tablename__ = 'SlackTeam'
    id = db.Column(db.String, primary_key=True, unique=True)
    bot_user_id = db.Column(db.String)
    bot_access_token = db.Column(db.String)
    things = db.relationship("Thing", backref="team")
    last_request = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, request_json):
        self.id = request_json['team_id']
        self.bot_user_id = request_json['bot']['bot_user_id']
        self.bot_access_token = request_json['bot']['bot_access_token']

    def slack_client(self):
        return SlackClient(self.bot_access_token)

    def api_call(self, **kwargs):
        self.slack_client().api_call(**kwargs)

    def update_last_access(self):
        self.last_request = datetime.datetime.utcnow()


class Thing(db.Model):
    __tablename__ = 'Thing'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    item = db.Column(db.String)
    points = db.Column(db.Integer, default=0)
    user = db.Column(db.Boolean)
    team_id = db.Column(db.String, db.ForeignKey('SlackTeam.id'))

    def increment(self):
        self.points += 1

    def decrement(self):
        self.points -= 1
