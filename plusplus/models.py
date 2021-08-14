from flask_sqlalchemy import SQLAlchemy
from slack import WebClient
import csv
import datetime
import io
import uuid

db = SQLAlchemy()


class SlackTeam(db.Model):
    __tablename__ = 'SlackTeam'
    id = db.Column(db.String, primary_key=True, unique=True)
    bot_user_id = db.Column(db.String)
    bot_access_token = db.Column(db.String)
    things = db.relationship("Thing", backref="team")
    last_request = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    banned = db.Column(db.Boolean, default=False)
    team_name = db.Column(db.String)
    team_domain = db.Column(db.String)
    team_email_domain = db.Column(db.String)
    team_archive_url = db.Column(db.String, Unique=True)

    def __init__(self, request_json):
        self.update(request_json)

    def update(self, request_json):
        self.id = request_json['team']['id']
        self.bot_user_id = request_json['bot_user_id']
        self.bot_access_token = request_json['access_token']
        self.get_team_metadata()

    @property
    def slack_client(self):
        return WebClient(self.bot_access_token)

    def update_last_access(self):
        self.last_request = datetime.datetime.utcnow()

    def get_team_metadata(self):
        sc = self.slack_client
        response = sc.team_info()
        self.team_name = response['team']['name']
        self.team_domain = f"https://{response['team']['domain']}.slack.com"
        self.team_email_domain = response['team']['email_domain']

    @property
    def archive_url(self):
        if not self.team_archive_url:
            run = True
            while run:
                candidate = str(uuid.uuid4())
                if SlackTeam.query.filter_by(team_archive_url=candidate).first() is None:
                    self.team_archive_url = candidate
                    run = False
        return self.team_archive_url

    @property
    def archive_csv(self):
        out = io.StringIO()
        csv_writer = csv.writer(out)
        data = [["id", "item", "points", "is_user", "last_modified"]]
        for thing in Thing.query.filter_by(team_id=self.id).all():
            data.append([thing.id, thing.item. thing.points, thing.user, thing.last_modified])
        csv_writer.writerows(data)
        return out.getvalue()


class Thing(db.Model):
    __tablename__ = 'Thing'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    item = db.Column(db.String)
    points = db.Column(db.Integer, default=0)
    user = db.Column(db.Boolean)
    team_id = db.Column(db.String, db.ForeignKey('SlackTeam.id'))
    show_in_global_leaderboard = db.Column(db.Boolean, default=True)
    last_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def increment(self):
        self.points += 1
        self.last_modified = datetime.datetime.utcnow()

    def decrement(self):
        self.points -= 1
        self.last_modified = datetime.datetime.utcnow()
