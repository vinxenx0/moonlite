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

def inject_tools():
    tools = [
        # Domains & Email
        {"name": "WHOIS", "description": "Check domain ownership details.", "link": "/tools/domains/whois", "icon": "fas fa-info-circle", "category": "Domains & Email"},
        {"name": "Reverse Domain", "description": "Explore reverse domain lookups.", "link": "/tools/domains/reverse", "icon": "fas fa-globe", "category": "Domains & Email"},
        {"name": "CNAME Lookup", "description": "Check CNAME records.", "link": "/tools/domains/cname", "icon": "fas fa-cog", "category": "Domains & Email"},
        {"name": "IP Lookup", "description": "Find the IP address associated with a domain.", "link": "/tools/domains/ip", "icon": "fas fa-search", "category": "Domains & Email"},
        {"name": "AAAA Lookup", "description": "Retrieve IPv6 records for a domain.", "link": "/tools/domains/aaaa", "icon": "fas fa-link", "category": "Domains & Email"},
        {"name": "Traceroute", "description": "Trace the route packets take to a domain.", "link": "/tools/domains/traceroute", "icon": "fas fa-route", "category": "Domains & Email"},
        {"name": "Nmap", "description": "Perform a network map scan.", "link": "/tools/domains/nmap", "icon": "fas fa-network-wired", "category": "Domains & Email"},
        {"name": "Blacklist Check", "description": "Check if your domain is blacklisted.", "link": "/tools/domains/blacklist", "icon": "fas fa-ban", "category": "Domains & Email"},

        # Mail Server
        {"name": "MX Discover", "description": "Identify mail exchange servers for a domain.", "link": "/tools/domains/mx", "icon": "fas fa-server", "category": "Domains & Email"},
        {"name": "DMARC Lookup", "description": "Check DMARC records for a domain.", "link": "/tools/domains/dmarc", "icon": "fas fa-envelope-open", "category": "Domains & Email"},
        {"name": "SPF Lookup", "description": "Check SPF records to prevent email spoofing.", "link": "/tools/domains/spf", "icon": "fas fa-shield-alt", "category": "Domains & Email"},
        {"name": "DKIM Lookup", "description": "Verify DKIM signatures for email authentication.", "link": "/tools/domains/dkim", "icon": "fas fa-signature", "category": "Domains & Email"},
        {"name": "TXT Lookup", "description": "Retrieve TXT records for a domain.", "link": "/tools/domains/txt", "icon": "fas fa-file-alt", "category": "Domains & Email"},
        {"name": "DNS Key Lookup", "description": "Check DNSSEC key records.", "link": "/tools/domains/dnskey", "icon": "fas fa-key", "category": "Domains & Email"},

        # Accessibility & Usability
        {"name": "WCAG-AA/AAA", "description": "Evaluate website accessibility compliance.", "link": "/tools/accesibility/wcag", "icon": "fas fa-universal-access", "category": "Accessibility & Usability"},
        {"name": "Spelling Check", "description": "Detect spelling issues on your site.", "link": "/tools/accesibility/ortografia", "icon": "fas fa-spell-check", "category": "Accessibility & Usability"},
        {"name": "Core Web Vitals", "description": "Analyze website performance metrics.", "link": "/tools/accesibility/core-web-vitals", "icon": "fas fa-vials", "category": "Accessibility & Usability"},
        {"name": "Responsive Design", "description": "Check website responsiveness.", "link": "/tools/accesibility/responsive", "icon": "fas fa-mobile-alt", "category": "Accessibility & Usability"},
        {"name": "Lazy Loading", "description": "Optimize image loading for speed.", "link": "/tools/accesibility/lazy-loading", "icon": "fas fa-clock", "category": "Accessibility & Usability"},

        # SEO Tools
        {"name": "Titles (H1)", "description": "Analyze title tags for SEO improvements.", "link": "/tools/seo/titles", "icon": "fas fa-heading", "category": "SEO"},
        {"name": "Meta Descriptions", "description": "Optimize meta descriptions for search engines.", "link": "/tools/seo/meta-description", "icon": "fas fa-clipboard", "category": "SEO"},
        {"name": "Headings", "description": "Check proper use of heading tags.", "link": "/tools/seo/headings", "icon": "fas fa-heading", "category": "SEO"},
        {"name": "Canonical Tags", "description": "Ensure canonicalization to prevent duplicates.", "link": "/tools/seo/canonicals", "icon": "fas fa-link", "category": "SEO"},
        {"name": "Robots.txt", "description": "Analyze robots.txt for crawling directives.", "link": "/tools/seo/robots", "icon": "fas fa-robot", "category": "SEO"},
        {"name": "Sitemap", "description": "Check the XML sitemap for search engines.", "link": "/tools/seo/sitemap", "icon": "fas fa-sitemap", "category": "SEO"},

        # Website Security
        {"name": "HTTPS/SSL", "description": "Verify HTTPS and SSL certificate compliance.", "link": "/tools/security/ssl", "icon": "fas fa-lock", "category": "Website Security"},
        {"name": "Server Response", "description": "Analyze server response headers.", "link": "/tools/security/server-response", "icon": "fas fa-server", "category": "Website Security"}
    ]

    return dict(tools=tools)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#@app.before_request
#def check_show_cookies_modal():
#    if not current_user.is_authenticated and 'cookies_accepted' not in session:
#        session['show_cookies_modal'] = True

