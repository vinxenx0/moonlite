# app/controllers/logs_controller.py

from flask_login import current_user
from flask import request
from app import db
from app.models.log_model import Log


def log_event(event, description):
    page = request.path
    user_id = current_user.id if current_user.is_authenticated else None
    user_name = current_user.username if current_user.is_authenticated else None

    log = Log(user_id=user_id,
              user_name=user_name,
              event=event,
              description=description,
              page=page)
    db.session.add(log)
    db.session.commit()
