# app/models/log_model.py
import datetime
from app import db


class Log(db.Model):
    __tablename__ = "Log"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  # , db.ForeignKey('Users.id'))
    user_name = db.Column(db.String(50))
    page = db.Column(db.String(255), nullable=False)
    event = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime,
                          nullable=False,
                          default=datetime.datetime.utcnow)

    # user = db.relationship('Users', back_populates='logs')

    def __repr__(self):
        return f"Log('{self.event}', '{self.description}', '{self.page}', '{self.timestamp}')"
