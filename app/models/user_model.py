# models/user_model.py

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import JSONType
import datetime
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin
import jwt 
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin



class Users(UserMixin, db.Model):
    __tablename__='Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), index=True, unique=True)
    active = db.Column(db.Boolean, default=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    config = db.Column(JSONType)   
    role = db.Column(db.String(20), nullable=False, default='usuario')

    #logs = db.relationship('Log', back_populates='user')
    #logs = db.relationship('Log', back_populates='user', cascade="all, delete-orphan")
 
    
    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_token(self, expires_sec=3600):
        return jwt.encode({'user_id': self.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_sec)},
                        current_app.config['SECRET_KEY'], algorithm='HS256') #.decode('utf-8')

    @staticmethod
    def verify_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
        except:
            return None
        return Users.query.get(user_id)