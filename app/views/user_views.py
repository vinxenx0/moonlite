# views/user_views.py
from app.controllers.logs_controller import log_event
from flask import render_template
from flask_login import login_required
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.models.user_model import Transaction, UserLog, Users

from collections import Counter
from datetime import datetime, timedelta

def calculate_log_statistics(logs):
    """Calculates statistics from user logs."""
    stats = {}

    # Herramientas más utilizadas
    tools = [log.tool for log in logs]
    tool_counts = Counter(tools)
    stats['most_used_tools'] = tool_counts.most_common(3)  # Top 3 herramientas

    # % de avisos por tipo
    log_types = [log.log_type for log in logs]
    total_logs = len(logs)
    log_type_counts = Counter(log_types)
    stats['log_type_percentages'] = {
        log_type: (count / total_logs) * 100 for log_type, count in log_type_counts.items()
    }

    # Número de herramientas diferentes usadas
    stats['unique_tools'] = len(set(tools))

    # Veces que se usa por día, mes, año
    today = datetime.utcnow()
    daily_logs = [log for log in logs if log.timestamp.date() == today.date()]
    monthly_logs = [log for log in logs if log.timestamp.year == today.year and log.timestamp.month == today.month]
    yearly_logs = [log for log in logs if log.timestamp.year == today.year]

    stats['logs_per_day'] = len(daily_logs)
    stats['logs_per_month'] = len(monthly_logs)
    stats['logs_per_year'] = len(yearly_logs)

    return stats

@app.route('/profile/logs')
@login_required
def view_logs():
    breadcrumbs = [{'url': '/profile', 'text': 'Perfil'}, {'url': '/profile/logs', 'text': 'Historial de Actividades'}]
    logs = UserLog.query.filter_by(user_id=current_user.id).order_by(UserLog.timestamp.desc()).all()
    stats = calculate_log_statistics(logs)
    return render_template('user/view_logs.html', logs=logs, stats=stats, breadcrumbs=breadcrumbs)

 
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

