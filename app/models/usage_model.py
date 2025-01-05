# app/models/usage_models.py
from app import db
from datetime import datetime

from app import db


class Activity(db.Model):
    __tablename__ = 'Activity'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    target = db.Column(db.String(256))
    email = db.Column(db.String(120))
    ip_address = db.Column(db.String(15))
    user_agent = db.Column(db.String(256))
    country = db.Column(db.String(64))
    language = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    page_url = db.Column(db.String(256))

    def __repr__(self):

        return f'<UserUsage {self.username}>'
