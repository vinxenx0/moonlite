# app/controllers/main_controller.py

from datetime import datetime
import json
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import app, db
from app.controllers.logs_controller import log_event
from app.controllers.spider_tools import get_page_info
from app.forms import ConfigForm, PageInfoForm
from app.models.usage_model import Activity
from app.models.user_model import Transaction, UserLog, Users
from app.views.user_views import calculate_log_statistics


@app.route('/')
def index():
   
    return redirect(url_for('new_start'))

@app.route('/start', methods=['GET', 'POST'])
def start():
    data = None
    validator = None
    spelling_errors = None
    grammar_errors = None
    breadcrumbs = [] #[{'url': '/start', 'text': 'Bienvenido'}]

    form = PageInfoForm()
    if form.validate_on_submit():
        # Obtener información del usuario
        username = 'Anonymous'
        email = ''
        if current_user.is_authenticated:
            username = current_user.username
            email = current_user.email  # Ajustar según tu formulario

        url = form.url.data
        ip_address = request.remote_addr
        user_agent = request.user_agent.string
        country = 'Spain'  #get_country_from_ip(ip_address)
        language = request.accept_languages.best

        # Obtener fecha y hora actual
        timestamp = datetime.utcnow()

        # Obtener URL de la página actual
        page_url = request.url

        # Guardar la información del usuario en la base de datos
        user_usage = Activity(username=username,
                              email=email,
                              target=url,
                              ip_address=ip_address,
                              user_agent=user_agent,
                              country=country,
                              language=language,
                              timestamp=timestamp,
                              page_url=page_url)
        db.session.add(user_usage)
        db.session.commit()

        #print(get_page_info(url))
        data, validator, spelling_errors, grammar_errors = get_page_info(url)
        #data, validator = get_page_info(url)
        #validator = json.load(validator)

    if current_user.is_authenticated:
        # Check the user's subscription type
        if current_user.subscription_plan == 'Corporate':
            #return redirect(url_for('corporate_start.html'))
            return render_template('corporate_start.html',
                           data=data,
                           validator=validator,
                           form=form,
                           breadcrumbs=breadcrumbs,
                           spelling_errors=spelling_errors,
                           grammar_errors=grammar_errors)
            
        elif current_user.subscription_plan == 'Pro':
            #return redirect(url_for('pro_start.html'))
            return render_template('pro_start.html',
                           data=data,
                           validator=validator,
                           form=form,
                           breadcrumbs=breadcrumbs,
                           spelling_errors=spelling_errors,
                           grammar_errors=grammar_errors)
            
        elif current_user.subscription_plan == 'Free':
            return render_template('start.html',
                           data=data,
                           validator=validator,
                           form=form,
                           breadcrumbs=breadcrumbs,
                           spelling_errors=spelling_errors,
                           grammar_errors=grammar_errors)
            # Default for users without a defined subscription
            #return redirect(url_for('start'))
    # Redirect unauthenticated users to a generic start page
    return render_template('start.html',
                           data=data,
                           validator=validator,
                           form=form,
                           breadcrumbs=breadcrumbs,
                           spelling_errors=spelling_errors,
                           grammar_errors=grammar_errors)


@app.route('/dashboard')
@login_required
def dashboard():
        breadcrumbs = [{'url': '/dashboard', 'text': 'Mi Escritorio'}]
        logs = UserLog.query.filter_by(user_id=current_user.id).order_by(UserLog.timestamp.desc()).all()
        stats = calculate_log_statistics(logs)
        user = Users.query.filter_by(id=current_user.id).first()
        logs = UserLog.query.filter_by(user_id=current_user.id).order_by(UserLog.timestamp.desc()).all()
        transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).all()
        #return redirect(url_for('dashboard'))  # dashboard
        return render_template('dashboard.html', 
                               logs=logs,
                               transactions = transactions,
                               user=user,
                               breadcrumbs=breadcrumbs,
                               stats=stats)


@app.route('/config', methods=['GET', 'POST'])
@login_required
def configuracion():
    breadcrumbs = [
        {
            'url': '/config',
            'text': 'Config'
        },
    ]
    form = ConfigForm()
    if form.validate_on_submit():
        current_user.config = {
            'color_primary': form.color_primary.data,
            'color_secondary': form.color_secondary.data,
            'color_tertiary': form.color_tertiary.data,
            'web_name': form.web_name.data,
            'logo_url': form.logo_url.data
        }
        db.session.commit()

        app.config['COLOR_PRIMARY'] = form.color_primary.data
        app.config['COLOR_SECONDARY'] = form.color_secondary.data
        app.config['COLOR_TERTIARY'] = form.color_tertiary.data
        app.config['WEB_NAME'] = form.web_name.data
        app.config['LOGO_URL'] = form.logo_url.data

        log_event('CONFIG', 'Configuración del sistema actualizada.')

        flash('Configuración actualizada correctamente.', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        if current_user.config:
            form.color_primary.data = current_user.config.get(
                'color_primary', '')
            form.color_secondary.data = current_user.config.get(
                'color_secondary', '')
            form.color_tertiary.data = current_user.config.get(
                'color_tertiary', '')
            form.web_name.data = current_user.config.get('web_name', '')
            form.logo_url.data = current_user.config.get('logo_url', '')
        else:
            # Si el usuario no tiene configuración, inicializar el formulario con valores vacíos
            form.color_primary.data = ''
            form.color_secondary.data = ''
            form.color_tertiary.data = ''
            form.web_name.data = ''
            form.logo_url.data = ''

    log_event('CONFIG', 'Visita Configuración del sistema.')
    return render_template('config.html',
                           title='Configuración',
                           form=form,
                           breadcrumbs=breadcrumbs)


@app.route('/test')
def test():
    breadcrumbs = [{'url': '/test', 'text': 'Test'}]
    #return render_template('inc/layout.html')
    return render_template('base.html')
