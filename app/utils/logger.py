from app.models.user_model import UserLog, db
from flask import request
import datetime


def log_user_event(user, event, tool, log_type='info'):
    """Register a user activity event."""
    ip_address = request.remote_addr or 'Unknown IP'
    log = UserLog(user_id=user.id,
                  username=user.username,
                  event=event,
                  tool=tool,
                  timestamp=datetime.datetime.utcnow(),
                  ip_address=ip_address,
                  log_type=log_type)
    db.session.add(log)
    db.session.commit()
