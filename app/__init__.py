# __init__py
import json
import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from logging.handlers import RotatingFileHandler
#from mailhog import Mailhog


app = Flask(__name__)
app.config.from_pyfile('../instance/config.py')

app.config['MAIL_SERVER'] = 'smtp.ionos.es'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vicente@ciberpunk.es'
app.config['MAIL_PASSWORD'] = 'rt6K_22MHj'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
csrf = CSRFProtect(app)
#mailhog = Mailhog()

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configurar el registro
#logging.basicConfig(filename='instance/error.log', level=logging.ERROR)

# Creamos archivo de log
log_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'app.log')
if not os.path.exists(log_path):
    open(log_path, 'w').close()

# Configuración de registros
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = RotatingFileHandler('instance/app.log', maxBytes=102400, backupCount=10)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

#@app.errorhandler(Exception)
#def handle_exception(error):
#    app.logger.error('Unhandled Exception: %s', error)
#    return 'Internal Server Error', 500

# Importar modelos y vistas

from app.controllers import main_controller, user_controller, tools_controller, admin_controller, logs_controller, spider_tools, mobile_tools, image_tools, speller_tool
from app.controllers.logs_controller import log_event
from app.views import user_views, tools_views, logs_views, new_domain_views, new_seo_views, accesibility_views, usability_views #seo_views #domain_tools
from app.models.user_model import Users
#from app.forms import LoginForm, ConfigForm

# Comprobamos si la base de datos SQLite existe, y si no, la creamos
database_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'database.db')
if not os.path.exists(database_path):
    open(database_path, 'w').close()


# Crear la primera instancia de usuario si no existe
with app.app_context():
    db.create_all()
    if not Users.query.first():
        new_user = Users(username='user', email='user@user.com', role='usuario', active=True, 
                        config = {"color_primary": "#ffffff", "color_secondary": "#000000", "color_tertiary": "#0066cc", 
                                  "web_name": "WHITE", "logo_url": "https://web.com/asdfadsf.png"}
                        )
        new_user.set_password('user')
        

        new_admin = Users(username='admin', email='admin@admin.com', role='admin', active=True,
                        config = {"color_primary": "#ffffff", "color_secondary": "#000000", "color_tertiary": "#0066cc", 
                                  "web_name": "WHITE", "logo_url": "https://web.com/asdfadsf.png"}
                        )
        new_admin.set_password('admin')
        db.session.add(new_admin)
        db.session.add(new_user)
        db.session.commit()

#@login_manager.user_loader
#def load_user(user_id):
#    return User.query.get(int(user_id))

@app.context_processor
def inject_sidebar_info():
    return dict(is_admin=current_user.is_authenticated and current_user.role == 'admin')

@app.context_processor
def inject_breadcrumb():
    breadcrumbs = [
        {'url': '/', 'text': 'Inicio'},
        {'url': '/profile', 'text': 'Opcion 1'},
        {'url': '/profile/edit', 'text': 'Sub opcion 1'}
    ]
    return {'breadcrumbs': breadcrumbs}

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#@app.before_request
#def check_show_cookies_modal():
#    if not current_user.is_authenticated and 'cookies_accepted' not in session:
#        session['show_cookies_modal'] = True

