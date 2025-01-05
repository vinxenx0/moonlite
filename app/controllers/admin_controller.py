# app/controllers/admin_controller.py
from app.controllers.logs_controller import log_event
from flask_login import login_required
from app import app
from flask import flash, redirect, render_template
from app.models.log_model import Log
from app.models.user_model import Users
from datetime import datetime, timedelta
from app.forms import PaymentForm
from app.utils.logger import log_user_event
from flask import render_template, redirect, session, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import app, db
from app.controllers.logs_controller import log_event
from app.models.user_model import Transaction, Users
from app.forms import LoginForm, PasswordResetRequestForm
from app.forms import NewUserRegistrationForm, RegistrationForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
# from app import app, db
from app.forms import RegistrationForm, PasswordResetForm, PasswordChangeForm, EditProfileForm
from flask_mail import Message
from flask import render_template, make_response, redirect, url_for, session

from app.forms import SubscriptionForm
import datetime

#comprobar que es admin quien entra y no solo login


# pagina que lista usuarios y algunos graficos
@app.route('/admin/stats')
@login_required
def admin_stats():
    breadcrumbs = [{
        'url': '/admin',
        'text': 'Admin'
    }, {
        'url': '/admin/stats',
        'text': 'Estadísticas'
    }]
    end_date = datetime.datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    users = Users.query.all()
    users_last_month = Users.query.filter(
        Users.registered_on.between(start_date, end_date)).count()
    total_users = Users.query.count()
    active_users = Users.query.filter_by(active=True).count()
    log_event('STATS', 'Paginas de estadísticas de administrador.')
    return render_template('admin/stats.html',
                           breadcrumbs=breadcrumbs,
                           users=users,
                           users_last_month=users_last_month,
                           total_users=total_users,
                           active_users=active_users)


# logs del sistema
@app.route('/admin/logs')
@login_required
def logs():
    breadcrumbs = [{
        'url': '/admin',
        'text': 'Admin'
    }, {
        'url': '/admin/logs',
        'text': 'Logs'
    }]
    logs = Log.query.all()
    log_event('LOGS', 'Pagina de logs de admin')
    return render_template('admin/logs.html',
                           title='Logs',
                           logs=logs,
                           breadcrumbs=breadcrumbs)


@app.route('/admin/register', methods=['GET', 'POST'])
@login_required
def admin_register():
    breadcrumbs = [{
        'url': '/tools',
        'text': 'Tools'
    }, {
        'url': '/tools/checkdomain',
        'text': 'Check Domain'
    }]
    #if current_user.role == 'admin'
    form = RegistrationForm()
    if form.validate_on_submit():
        config_data = {
            "color_primary": "#ffffff",
            "color_secondary": "#000000",
            "color_tertiary": "#0066cc",
            "web_name": "FLASKAPP",
            "logo_url": "https://web.com/asdfadsf.png"
        }
        user = Users(username=form.username.data,
                     email=form.email.data,
                     role=form.role.data,
                     config=config_data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        log_event('USER ADD', 'Admin nuevo usuario.')
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('user/register.html',
                           title='Registro',
                           form=form,
                           breadcrumbs=breadcrumbs)
