# views/user_views.py
from app.controllers.logs_controller import log_event
from flask import render_template
from flask_login import login_required
from app import app
from app.models.user_model import Users

@app.route('/admin/usuarios')
@login_required
def usuarios():
    breadcrumbs = [
    {'url': '/admin', 'text': 'Admin'},
    {'url': '/admin/usuarios', 'text': 'Listado usuarios'}
    ]
  
    users = Users.query.all()
    log_event('ADMIN', 'Lista de usuarios.')
    return render_template('user/usuarios.html', users=users, breadcrumbs=breadcrumbs)

