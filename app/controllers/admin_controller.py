# app/controllers/admin_controller.py
from app.controllers.logs_controller import log_event
from flask_login import login_required
from app import app
from flask import render_template
from app.models.log_model import Log
from app.models.user_model import Users
from datetime import datetime, timedelta

@app.route('/admin/stats')
@login_required
def admin_stats():
    breadcrumbs = [
        {'url': '/admin', 'text': 'Admin'},
        {'url': '/admin/stats', 'text': 'Estadísticas'}
    ]
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    users = Users.query.all()
    users_last_month = Users.query.filter(Users.registered_on.between(start_date, end_date)).count()
    total_users = Users.query.count()
    active_users = Users.query.filter_by(active=True).count()
    log_event('STATS', 'Paginas de estadísticas de administrador.')
    return render_template('admin/stats.html', breadcrumbs=breadcrumbs, users=users, users_last_month=users_last_month, total_users=total_users, active_users=active_users)


@app.route('/admin/logs')
@login_required
def logs():
    breadcrumbs = [
        {'url': '/admin', 'text': 'Admin'},
        {'url': '/admin/logs', 'text': 'Logs'}
    ]
    logs = Log.query.all()
    log_event('LOGS', 'Pagina de logs de admin')
    return render_template('admin/logs.html', title='Logs', logs=logs, breadcrumbs=breadcrumbs)
