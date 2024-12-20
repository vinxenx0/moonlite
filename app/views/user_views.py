# views/user_views.py
from app.controllers.logs_controller import log_event
from flask import render_template
from flask_login import login_required
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.models.user_model import Transaction, UserLog, Users
 
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

@app.route('/profile/transactions')
@login_required
def transaction_history():
    breadcrumbs = [{'url': '/profile', 'text': 'Perfil'}, {'url': '/profile/transactions', 'text': 'Historial de Transacciones'}]
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).all()
    return render_template('user/transactions.html', transactions=transactions, breadcrumbs=breadcrumbs)

@app.route('/profile/logs')
@login_required
def view_logs():
    breadcrumbs = [{'url': '/profile', 'text': 'Perfil'}, {'url': '/profile/logs', 'text': 'Historial de Actividades'}]
    logs = UserLog.query.filter_by(user_id=current_user.id).order_by(UserLog.timestamp.desc()).all()
    return render_template('user/view_logs.html', logs=logs, breadcrumbs=breadcrumbs)

