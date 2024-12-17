# app/controllers/user_controller.py

from app.forms import PaymentForm
from flask import render_template, redirect, session, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import app, db, mail
from app.controllers.logs_controller import log_event
from app.models.user_model import Users
from app.forms import LoginForm, PasswordResetRequestForm
from app.forms import NewUserRegistrationForm, RegistrationForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
# from app import app, db
from app.forms import RegistrationForm, PasswordResetForm, PasswordChangeForm, EditProfileForm
from flask_mail import Message
from flask import render_template, make_response, redirect, url_for, session


@app.route('/profile')
@login_required
def profile():
    breadcrumbs = [
        {'url': '/profile', 'text': 'Perfil'}
    ]
    user = Users.query.filter_by(id=current_user.id).first()
    return render_template('user/profile.html', user=user, breadcrumbs=breadcrumbs)

@app.route('/profile/payment', methods=['GET', 'POST'])
@login_required
def edit_payment_methods():
    breadcrumbs = [{'url': '/profile', 'text': 'Perfil'}, {'url': '/profile/payment', 'text': 'Editar Métodos de Pago'}]
    form = PaymentForm()
    user = Users.query.get(current_user.id)

    if form.validate_on_submit():
        # Update payment methods
        user.primary_payment = {
            'method': form.primary_payment_method.data,
            'details': form.primary_payment_details.data
        }
        user.secondary_payment = {
            'method': form.secondary_payment_method.data,
            'details': form.secondary_payment_details.data
        }
        db.session.commit()
        flash('Métodos de pago actualizados.', 'success')
        log_event('PAYMENT_UPDATE', f'Métodos de pago actualizados para el usuario {user.username}.')
        return redirect(url_for('profile'))

    # Prepopulate the form
    if user.primary_payment:
        form.primary_payment_method.data = user.primary_payment.get('method')
        form.primary_payment_details.data = user.primary_payment.get('details')
    if user.secondary_payment:
        form.secondary_payment_method.data = user.secondary_payment.get('method')
        form.secondary_payment_details.data = user.secondary_payment.get('details')

    return render_template('user/edit_payment.html', form=form, breadcrumbs=breadcrumbs)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    breadcrumbs = [
        {'url': '/profile', 'text': 'Perfil'},
        {'url': '/profile/edit', 'text': 'Editar Perfil'}
    ]
    user = Users.query.get(current_user.id)
    if user.role == 'admin':
        can_edit = True
    else:
        can_edit = False
    form = EditProfileForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = form.role.data
        active = form.active.data

        if can_edit:
            user.username = username
            user.set_password(password)
            user.role = role
            user.active = active
            print(user)
            db.session.commit()
            flash('Usuario editado correctamente.', 'success')
            log_event('USER EDIT', 'Usuario editado.')
            return redirect(url_for('profile'))
        else:
            flash('No tienes permisos para editar el perfil.', 'success')
            print('No tienes permisos')
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = user.username
    
    log_event('EDIT USER', 'Pagina editar usuario.')
    return render_template('user/edit_profile.html',
                           user=user,
                           form=form,
                           can_edit=can_edit, breadcrumbs=breadcrumbs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    breadcrumbs = [
        {'url': '/register', 'text': 'Nuevo usuario'}
    ]
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = NewUserRegistrationForm()

    if form.validate_on_submit():
        config_data = {
            "color_primary": "#ffffff",
            "color_secondary": "#000000",
            "color_tertiary": "#0066cc",
            "web_name": form.username.data,
            "logo_url": "https://web.com/asdfadsf.png"
        }
        user = Users(
            username=form.username.data,
            email=form.email.data,
            role='usuario',
            config=config_data
        )
        user.set_password(form.password.data)
        user.token = user.get_token()
        db.session.add(user)
        db.session.commit()
        # flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        #log_event('REGISTRATION', 'Nuevo usuario registrado')
        send_activation_email(user)
        flash(
            'Se ha enviado un correo electrónico de confirmación. Por favor, verifica tu cuenta.',
            'success')
        return redirect(url_for('login'))
    return render_template('user/new_user.html', title='Registro', form=form, breadcrumbs=breadcrumbs)



@app.route('/admin/register', methods=['GET', 'POST'])
@login_required
def admin_register():
    breadcrumbs = [
        {'url': '/tools', 'text': 'Tools'},
        {'url': '/tools/checkdomain', 'text': 'Check Domain'}
    ]
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
        user = Users(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data,
            config=config_data  
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        log_event('USER ADD', 'Admin nuevo usuario.')
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('user/register.html', title='Registro', form=form, breadcrumbs=breadcrumbs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    breadcrumbs = [
        {'url': '/login', 'text': 'Login'}
    ]
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            if not user.active:
                send_activation_email(user)
                flash(
                    'Tu cuenta aún no está activada. Se ha enviado un nuevo correo electrónico de activación.',
                    'warning')
                #log_event('LOGIN', 'Cuenta inactiva, enviado nuevo link.')
                return redirect(url_for('login'))
            
            login_user(user)
            log_event('LOGIN', 'Inicio correcto.')
            
            app.config['COLOR_PRIMARY'] = user.config.get(
                'color_primary', app.config['COLOR_PRIMARY'])
            app.config['COLOR_SECONDARY'] = user.config.get(
                'color_secondary', app.config['COLOR_SECONDARY'])
            app.config['COLOR_TERTIARY'] = user.config.get(
                'color_tertiary', app.config['COLOR_TERTIARY'])
            app.config['WEB_NAME'] = user.config.get('web_name',
                                                     app.config['WEB_NAME'])
            app.config['LOGO_URL'] = user.config.get('logo_url',
                                                     app.config['LOGO_URL'])

            flash('Inicio de sesión exitoso.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            #log_event('LOGIN', 'Configuración global sistema.')
            return redirect(url_for('login'))
        
    #log_event('LOGIN', 'Pagina de login.')
    return render_template('user/login.html', title='Login', form=form, breadcrumbs=breadcrumbs)


@app.route('/logout')
def logout():
    breadcrumbs = [
        {'url': '/logout', 'text': 'Desconectado'}
    ]
    logout_user()
    session.pop('session', None)
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('session') 

    app.config.from_pyfile('../instance/config.py')
    #log_event('LOGOUT', 'Usuario desconectado.')
    flash('Hasta la vista', 'success')
    return render_template('user/logout.html', breadcrumbs=breadcrumbs)


@app.route('/activate/<token>')
def activate(token):
    user = Users.verify_token(token)
    if user:
        user.active = True
        db.session.commit()
        flash('¡Tu cuenta ha sido activada! Ya puedes iniciar sesión.',
              'success')
        log_event('ACTIVATION', 'Cuenta activada con token.')
        return redirect(url_for('login'))
    
    #log_event('CONFIG', 'Token de activación incorrecto')
    flash('El enlace de activación es inválido o ha expirado.', 'danger')
    return redirect(url_for('login'))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    breadcrumbs = [
        {'url': '/reset_password_request', 'text': 'Reseteo de Contraseña'}
    ]
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_token(
                expires_sec=600)  # 
            send_password_reset_email(user, token)
            flash(
                'Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.',
                'success')
            #log_event('PASSWORD', 'Configuración global sistema.')
            return redirect(url_for('login'))
        else:
            flash(
                'No se encontró ninguna cuenta con ese correo electrónico. Por favor, verifica tu dirección de correo electrónico.',
                'danger')
    return render_template('user/reset_password_request.html',
                           title='Recuperar contraseña',
                           form=form, breadcrumbs=breadcrumbs)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    breadcrumbs = [
        {'url': '/profile', 'text': 'Perfil'},
        {'url': '/change_password', 'text': 'Cambiar Contraseña'}
    ]
    form = PasswordChangeForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.password.data)
            db.session.commit()
            flash('Tu contraseña ha sido cambiada exitosamente.', 'success')
            log_event('PASSWORD', 'Contraseña cambiada.')
            return redirect(url_for('index'))
        else:
            flash(
                'La contraseña antigua no es correcta. Por favor, inténtalo de nuevo.',
                'danger')
            log_event('PASSWORD', 'Contraseña antigua incorrecta.')
    return render_template('user/change_password.html',
                           title='Cambiar Contraseña',
                           form=form, breadcrumbs=breadcrumbs)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    breadcrumbs = [
        {'url': '/reset_password', 'text': 'Cambiar Contraseña'}
    ]
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = Users.verify_token(token)
    if not user:
        flash(
            'El enlace de restablecimiento de contraseña es inválido o ha expirado.',
            'danger')
        #log_event('PASSWORD', 'Enlace restablecer contraseña inválido')
        return redirect(url_for('login'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(
            'Tu contraseña ha sido restablecida. Ahora puedes iniciar sesión con tu nueva contraseña.',
            'success')
        #log_event('PASSWORD', 'Contraseña restablecida.')
        return redirect(url_for('login'))
    return render_template('user/reset_password.html',
                           title='Restablecer contraseña',
                           form=form)


def send_password_reset_email(user, token):
    msg = Message('Recuperar contraseña',
                  sender='vicente@ciberpunk.es',
                  recipients=[user.email])
    print(url_for('reset_password', token=token, _external=True))
    msg.html = render_template('email/reset_password.html', user=user, token=token)
    #msg.body = f'''Para restablecer tu contraseña, visita el siguiente enlace:
#{url_for('reset_password', token=token, _external=True)}
#
#If clicking the link above doesn't work, please copy and paste the URL in a new browser window instead.
#
#El enlace es válido por 10 minutos.
#
#
#'''
    #msg.html = render_template('email/reset_password.html', user=user, token=token)
    #log_event('PASSWORD', 'Email recuperar contraseña enviado.')
    mail.send(msg)


def send_activation_email(user):
    token = user.get_token()
    msg = Message('Confirma tu cuenta',
                  sender='vicente@ciberpunk.es',
                  recipients=[user.email])
    print(url_for('activate', token=token, _external=True))
    #msg.body = f'''Para activar tu cuenta, visita el siguiente enlace:
#{url_for('activate', token=token, _external=True)}
#
#If clicking the link above doesn't work, please copy and paste the URL in a new browser window instead.
#
#El enlace es válido por 1 hora.
#'''
    msg.html = render_template('email/send_activation.html', user=user, token=token)
    mail.send(msg)
    #log_event('ACTIVATION', 'Email de activacion enviado')

#@app.route('/accept_cookies', methods=['POST'])
#def accept_cookies():
#    session['cookies_accepted'] = True
#    session.pop('show_cookies_modal', None)
#    return redirect(request.referrer)


@app.route('/profile/edit_all', methods=['GET', 'POST'])
@login_required
def edit_full_profile():
    breadcrumbs = [{'url': '/profile', 'text': 'Perfil'}, {'url': '/profile/edit_all', 'text': 'Editar Perfil'}]
    user = Users.query.get(current_user.id)
    form = EditProfileForm()
    payment_form = PaymentForm()

    if form.validate_on_submit() and payment_form.validate_on_submit():
        # Actualizar información básica
        user.username = form.username.data
        if form.password.data:
            user.set_password(form.password.data)
        
        # Actualizar métodos de pago
        user.primary_payment = {
            'method': payment_form.primary_payment_method.data,
            'details': payment_form.primary_payment_details.data
        }
        user.secondary_payment = {
            'method': payment_form.secondary_payment_method.data,
            'details': payment_form.secondary_payment_details.data
        }

        # Actualizar rol y estado si es administrador
        if current_user.role == 'admin':
            user.role = form.role.data
            user.active = form.active.data

        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        log_event('PROFILE_UPDATE', f'Perfil de {user.username} actualizado.')
        return redirect(url_for('profile'))

    elif request.method == 'GET':
        # Pre-populate the forms with current user data
        form.username.data = user.username
        payment_form.primary_payment_method.data = user.primary_payment.get('method') if user.primary_payment else ''
        payment_form.primary_payment_details.data = user.primary_payment.get('details') if user.primary_payment else ''
        payment_form.secondary_payment_method.data = user.secondary_payment.get('method') if user.secondary_payment else ''
        payment_form.secondary_payment_details.data = user.secondary_payment.get('details') if user.secondary_payment else ''
        if current_user.role == 'admin':
            form.role.data = user.role
            form.active.data = user.active

    return render_template('user/edit_full_profile.html',
                           form=form, payment_form=payment_form, user=user, breadcrumbs=breadcrumbs)
