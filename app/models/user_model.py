# models/user_model.py

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import JSONType
import datetime
from flask import current_app
# from app import db, login_manager
from flask_login import UserMixin
import jwt 
from flask import current_app
from app import db
from flask_login import UserMixin
from sqlalchemy import Enum
import datetime
from flask_login import UserMixin
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import JSONType
import datetime
from flask import current_app
# from app import db, login_manager
from flask_login import UserMixin
import jwt 
from flask import current_app
from app import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
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

    # Subscription data
    subscription_plan = db.Column(Enum('Free', 'Pro', 'Corporate', name='subscription_plans'), default='Free')
    subscription_currency = db.Column(db.String(3), default='USD')  # ISO currency codes (e.g., USD, EUR)
    subscription_expiration = db.Column(db.DateTime, nullable=True)
    subscription_frequency = db.Column(Enum('Monthly', 'Annually', name='subscription_frequency'), default='Monthly')


    # Payment methods
    primary_payment = db.Column(JSONType, nullable=True)  # IBAN, SWIFT, etc.
    secondary_payment = db.Column(JSONType, nullable=True)

    # Relationship to Transactions
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_token(self, expires_sec=3600):
        return jwt.encode({'user_id': self.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_sec)},
                        current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def is_subscription_active(self):
        if not self.subscription_expiration:
            return False
        return self.subscription_expiration > datetime.datetime.utcnow()

    @staticmethod
    def verify_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
        except:
            return None
        return Users.query.get(user_id)

class Transaction(db.Model):
    __tablename__ = 'Transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # payment, refund, etc.
    description = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.transaction_type} - {self.amount}>'
    

class UserLog(db.Model):
    __tablename__ = 'UserLogs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    event = db.Column(db.String(255), nullable=False)  # Description of the event
    tool = db.Column(db.String(255), nullable=False)  # Tool used 
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=False)  # Supports IPv4/IPv6
    log_type = db.Column(Enum('info', 'warn', 'err', name='log_types'), nullable=False)

    def __repr__(self):
        return f'<UserLog {self.event} by {self.username} on {self.tool}- {self.log_type}>'

