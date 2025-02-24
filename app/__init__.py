# __init__py
import datetime
import json
import os
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from logging.handlers import RotatingFileHandler
#from mailhog import Mailhog
from itertools import groupby
from operator import itemgetter
from flask_apscheduler import APScheduler



def record_daily_metrics():
    """Función programada para registrar las métricas diarias."""
    from app.controllers import marketing_controller  # Importar dentro de la función para evitar dependencias circulares
    from app.models import MarketingMetrics, db
    from datetime import datetime

    with app.app_context():  # Esto asegura que la función tenga acceso al contexto de Flask
        stats = marketing_controller.calculate_marketing_metrics()

        # Guardar métricas en la base de datos
        metric = MarketingMetrics(
            churn_rate=stats['churn_rate'],
            clv=stats['clv'],
            cac=stats['cac'],
            mrr=stats['mrr'],
            arr=stats['arr'],
            nrr=stats['nrr'],
            expansion_revenue_rate=stats['expansion_revenue_rate'],
            created_at=datetime.utcnow()
        )
        db.session.add(metric)
        db.session.commit()

        print(f"✅ Daily metrics recorded at {datetime.utcnow()}")
    

app = Flask(__name__)
app.config.from_pyfile('../instance/config.py')

app.config['MAIL_SERVER'] = 'smtp.ionos.es'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vicente@ciberpunk.es'
app.config['MAIL_PASSWORD'] = 'rt6K_22MHj'
app.config['SECRET_KEY'] = 'your_secret_key'

app.config['SCHEDULER_API_ENABLED'] = True

app.config['PREFERRED_URL_SCHEME'] = 'https'  # Forzar https

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
csrf = CSRFProtect(app)
#mailhog = Mailhog()


scheduler = APScheduler()

# Inicia y configura el scheduler
scheduler.init_app(app)
scheduler.start()

# Registra la tarea programada
scheduler.add_job(
        id='daily_metrics_job',
        func=record_daily_metrics,
        trigger='cron',
        hour=0,  # Ejecuta a medianoche
        minute=0
)

tools = [
    # Domains & Email
    {
        "name": "WHOIS",
        "description": "Check domain ownership details.",
        "link": "/tools/domains/whois",
        "icon": "fas fa-info-circle",
        "category": "Domains & Email",
        "subcategory": "Domain Information",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "Reverse Domain",
        "description": "Explore reverse domain lookups.",
        "link": "/tools/domains/reverse",
        "icon": "fas fa-globe",
        "category": "Domains & Email",
        "subcategory": "Domain Information",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "CNAME Lookup",
        "description": "Check CNAME records.",
        "link": "/tools/domains/cname",
        "icon": "fas fa-cog",
        "category": "Domains & Email",
        "subcategory": "Domain Information",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "IP Lookup",
        "description": "Find the IP address associated with a domain.",
        "link": "/tools/domains/ip",
        "icon": "fas fa-search",
        "category": "Domains & Email",
        "subcategory": "Domain Information",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "AAAA Lookup",
        "description": "Retrieve IPv6 records for a domain.",
        "link": "/tools/domains/aaaa",
        "icon": "fas fa-link",
        "category": "Domains & Email",
        "subcategory": "Domain Information",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Traceroute",
        "description": "Trace the route packets take to a domain.",
        "link": "/tools/domains/traceroute",
        "icon": "fas fa-route",
        "category": "Domains & Email",
        "subcategory": "Domain Information",
        "most_used": True,
        "is_new": True
    },
    {
        "name": "Nmap",
        "description": "Perform a network map scan.",
        "link": "/tools/domains/nmap",
        "icon": "fas fa-network-wired",
        "category": "Domains & Email",
        "subcategory": "Domain Information",
        "most_used": True,
        "is_new": True
    },
    {
        "name": "Blacklist Check",
        "description": "Check if your domain is blacklisted.",
        "link": "/tools/domains/blacklist",
        "icon": "fas fa-ban",
        "category": "Domains & Email",
        "subcategory": "Domain Information",
        "most_used": True,
        "is_new": True
    },

    # Mail Server
    {
        "name": "MX Discover",
        "description": "Identify mail exchange servers for a domain.",
        "link": "/tools/domains/mx",
        "icon": "fas fa-server",
        "category": "Domains & Email",
        "subcategory": "Mail Server",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "DMARC Lookup",
        "description": "Check DMARC records for a domain.",
        "link": "/tools/domains/dmarc",
        "icon": "fas fa-envelope-open",
        "category": "Domains & Email",
        "subcategory": "Mail Server",
        "most_used": True,
        "is_new": True
    },
    {
        "name": "SPF Lookup",
        "description": "Check SPF records to prevent email spoofing.",
        "link": "/tools/domains/spf",
        "icon": "fas fa-shield-alt",
        "category": "Domains & Email",
        "subcategory": "Mail Server",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "DKIM Lookup",
        "description": "Verify DKIM signatures for email authentication.",
        "link": "/tools/domains/dkim",
        "icon": "fas fa-signature",
        "category": "Domains & Email",
        "subcategory": "Mail Server",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "TXT Lookup",
        "description": "Retrieve TXT records for a domain.",
        "link": "/tools/domains/txt",
        "icon": "fas fa-file-alt",
        "category": "Domains & Email",
        "subcategory": "Mail Server",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "DNS Key Lookup",
        "description": "Check DNSSEC key records.",
        "link": "/tools/domains/dnskey",
        "icon": "fas fa-key",
        "category": "Domains & Email",
        "subcategory": "Mail Server",
        "most_used": True,
        "is_new": True
    },
    {
        "name": "LOC Entry",
        "description": "Retrieve LOC records for a domain.",
        "link": "/tools/domains/loc",
        "icon": "fas fa-map-marker-alt",
        "category": "Domains & Email",
        "subcategory": "Mail Server",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "IP Sec Key",
        "description": "Analyze IPSEC Key records.",
        "link": "/tools/domains/ipseckey",
        "icon": "fas fa-shield-alt",
        "category": "Domains & Email",
        "subcategory": "Mail Server",
        "most_used": False,
        "is_new": False
    },

    # DNS Lookup
    {
        "name": "SOA Lookup",
        "description": "Check SOA DNS records.",
        "link": "/tools/domains/soa",
        "icon": "fas fa-info",
        "category": "Domains & Email",
        "subcategory": "DNS Lookup",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "ASN Lookup",
        "description": "Perform an ASN record lookup.",
        "link": "/tools/domains/asn",
        "icon": "fas fa-sitemap",
        "category": "Domains & Email",
        "subcategory": "DNS Lookup",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "ARIN Lookup",
        "description": "Retrieve ARIN information for a domain.",
        "link": "/tools/domains/arin",
        "icon": "fas fa-database",
        "category": "Domains & Email",
        "subcategory": "DNS Lookup",
        "most_used": False,
        "is_new": True
    },
    {
        "name": "RRSIG Lookup",
        "description": "Retrieve RRSIG DNS records.",
        "link": "/tools/domains/rrsig",
        "icon": "fas fa-lock",
        "category": "Domains & Email",
        "subcategory": "DNS Lookup",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "NSEC Lookup",
        "description": "Perform NSEC DNS lookups.",
        "link": "/tools/domains/nsec",
        "icon": "fas fa-lock",
        "category": "Domains & Email",
        "subcategory": "DNS Lookup",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "MTA STS",
        "description": "Check MTA STS compliance.",
        "link": "/tools/domains/mtasts",
        "icon": "fas fa-envelope",
        "category": "Domains & Email",
        "subcategory": "DNS Lookup",
        "most_used": False,
        "is_new": True
    },
    {
        "name": "NSEC3PARAM",
        "description": "Check NSEC3PARAM DNS records.",
        "link": "/tools/domains/nsec3param",
        "icon": "fas fa-key",
        "category": "Domains & Email",
        "subcategory": "DNS Lookup",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "SRV Lookup",
        "description": "Perform SRV record lookup.",
        "link": "/tools/domains/srv",
        "icon": "fas fa-network-wired",
        "category": "Domains & Email",
        "subcategory": "DNS Lookup",
        "most_used": True,
        "is_new": False
    },

    # Accessibility
    {
        "name": "WCAG-AA/AAA",
        "description": "Evaluate website accessibility compliance.",
        "link": "/tools/accesibility/wcag",
        "icon": "fas fa-universal-access",
        "category": "Accessibility & Usability",
        "subcategory": "Accessibility",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Spelling Check",
        "description": "Detect spelling issues on your site.",
        "link": "/tools/accesibility/ortografia",
        "icon": "fas fa-spell-check",
        "category": "Accessibility & Usability",
        "subcategory": "Accessibility",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Velocidad",
        "description": "Analyze website performance metrics.",
        "link": "/tools/accesibility/core-web-vitals",
        "icon": "fas fa-vials",
        "category": "Accessibility & Usability",
        "subcategory": "Accessibility",
        "most_used": True,
        "is_new": True
    },
    {
        "name": "Core Web Vitals",
        "description": "Analyze website performance metrics.",
        "link": "/tools/accesibility/core-web-vitals",
        "icon": "fas fa-vials",
        "category": "Accessibility & Usability",
        "subcategory": "Accessibility",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Responsive Design",
        "description": "Check website responsiveness.",
        "link": "/tools/accesibility/responsive",
        "icon": "fas fa-mobile-alt",
        "category": "Accessibility & Usability",
        "subcategory": "Accessibility",
        "most_used": True,
        "is_new": False
    },
    # Img optimization
    {
        "name": "Images",
        "description": "Validate AMP page compliance.",
        "link": "/tools/accesibility/amp",
        "icon": "fas fa-mobile-alt",
        "category": "Accessibility & Usability",
        "subcategory": "Image Optimization",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "Lazy Loading",
        "description": "Optimize image loading for speed.",
        "link": "/tools/accesibility/lazy-loading",
        "icon": "fas fa-clock",
        "category": "Accessibility & Usability",
        "subcategory": "Image Optimization",
        "most_used": True,
        "is_new": False
    },
    # Mobile optimization
    {
        "name": "AMP Valid Page",
        "description": "Validate AMP page compliance.",
        "link": "/tools/accesibility/amp",
        "icon": "fas fa-mobile-alt",
        "category": "Accessibility & Usability",
        "subcategory": "Mobile Optimization",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "Mobile Audit",
        "description": "Perform a mobile optimization audit.",
        "link": "/tools/accesibility/mobile-audit",
        "icon": "fas fa-mobile-alt",
        "category": "Accessibility & Usability",
        "subcategory": "Mobile Optimization",
        "most_used": False,
        "is_new": True
    },
    # Usability
    {
        "name": "Favicon Missing",
        "description": "Validate AMP page compliance.",
        "link": "/tools/accesibility/amp",
        "icon": "fas fa-mobile-alt",
        "category": "Accessibility & Usability",
        "subcategory": "Usability",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "Flash Used",
        "description": "Perform a mobile optimization audit.",
        "link": "/tools/accesibility/mobile-audit",
        "icon": "fas fa-mobile-alt",
        "category": "Accessibility & Usability",
        "subcategory": "Usability",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "X Card Tag Missing",
        "description": "Validate AMP page compliance.",
        "link": "/tools/accesibility/amp",
        "icon": "fas fa-mobile-alt",
        "category": "Accessibility & Usability",
        "subcategory": "Usability",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "Google Search Display",
        "description": "Perform a mobile optimization audit.",
        "link": "/tools/accesibility/mobile-audit",
        "icon": "fas fa-mobile-alt",
        "category": "Accessibility & Usability",
        "subcategory": "Usability",
        "most_used": False,
        "is_new": True
    },
    {
        "name": "Content Optimization",
        "description": "Validate AMP page compliance.",
        "link": "/tools/accesibility/amp",
        "icon": "fas fa-mobile-alt",
        "category": "Accessibility & Usability",
        "subcategory": "Usability",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "Redirection Manager",
        "description": "Perform a mobile optimization audit.",
        "link": "/tools/accesibility/mobile-audit",
        "icon": "fas fa-mobile-alt",
        "category": "Accessibility & Usability",
        "subcategory": "Usability",
        "most_used": False,
        "is_new": True
    },

    # SEO Tools
    {
        "name": "Titles (H1)",
        "description": "Analyze title tags for SEO improvements.",
        "link": "/tools/seo/titles",
        "icon": "fas fa-heading",
        "category": "SEO",
        "subcategory": "On-Page SEO",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Meta Descriptions",
        "description": "Optimize meta descriptions for search engines.",
        "link": "/tools/seo/meta-description",
        "icon": "fas fa-clipboard",
        "category": "SEO",
        "subcategory": "On-Page SEO",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Meta Keywords",
        "description": "Ensure canonicalization to prevent duplicates.",
        "link": "/tools/seo/canonicals",
        "icon": "fas fa-link",
        "category": "SEO",
        "subcategory": "Crawling & Linking",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Encabezados (Headings)",
        "description": "Analyze title tags for SEO improvements.",
        "link": "/tools/seo/titles",
        "icon": "fas fa-heading",
        "category": "SEO",
        "subcategory": "On-Page SEO",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Imágenes (IMG)",
        "description": "Ensure canonicalization to prevent duplicates.",
        "link": "/tools/seo/canonicals",
        "icon": "fas fa-link",
        "category": "SEO",
        "subcategory": "Crawling & Linking",
        "most_used": True,
        "is_new": True
    },
    {
        "name": "Canonical Tags",
        "description": "Ensure canonicalization to prevent duplicates.",
        "link": "/tools/seo/canonicals",
        "icon": "fas fa-link",
        "category": "SEO",
        "subcategory": "Crawling & Linking",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Directives",
        "description": "Analyze title tags for SEO improvements.",
        "link": "/tools/seo/titles",
        "icon": "fas fa-heading",
        "category": "SEO",
        "subcategory": "On-Page SEO",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Schema.org",
        "description": "Optimize meta descriptions for search engines.",
        "link": "/tools/seo/meta-description",
        "icon": "fas fa-clipboard",
        "category": "SEO",
        "subcategory": "On-Page SEO",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "OpenGraph",
        "description": "Ensure canonicalization to prevent duplicates.",
        "link": "/tools/seo/canonicals",
        "icon": "fas fa-link",
        "category": "SEO",
        "subcategory": "Crawling & Linking",
        "most_used": True,
        "is_new": True
    },
    {
        "name": "Hreflang",
        "description": "Analyze title tags for SEO improvements.",
        "link": "/tools/seo/titles",
        "icon": "fas fa-heading",
        "category": "SEO",
        "subcategory": "On-Page SEO",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "URLs",
        "description": "Optimize meta descriptions for search engines.",
        "link": "/tools/seo/meta-description",
        "icon": "fas fa-clipboard",
        "category": "SEO",
        "subcategory": "On-Page SEO",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Duplicate Content",
        "description": "Ensure canonicalization to prevent duplicates.",
        "link": "/tools/seo/canonicals",
        "icon": "fas fa-link",
        "category": "SEO",
        "subcategory": "Crawling & Linking",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Robots.txt",
        "description": "Analyze robots.txt for crawling directives.",
        "link": "/tools/seo/robots",
        "icon": "fas fa-robot",
        "category": "SEO",
        "subcategory": "Crawling & Linking",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Sitemap",
        "description": "Check the XML sitemap for search engines.",
        "link": "/tools/seo/sitemap",
        "icon": "fas fa-sitemap",
        "category": "SEO",
        "subcategory": "Crawling & Linking",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Broken Links",
        "description": "Identify and fix broken links on your website.",
        "link": "/tools/seo/broken-links",
        "icon": "fas fa-unlink",
        "category": "SEO",
        "subcategory": "Crawling & Linking",
        "most_used": True,
        "is_new": True
    },
    {
        "name": "Backlinks",
        "description": "Analyze backlinks to your website.",
        "link": "/tools/seo/backlinks",
        "icon": "fas fa-link",
        "category": "SEO",
        "subcategory": "Crawling & Linking",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Outlinks",
        "description": "Analyze backlinks to your website.",
        "link": "/tools/seo/backlinks",
        "icon": "fas fa-link",
        "category": "SEO",
        "subcategory": "Crawling & Linking",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "External links",
        "description": "Analyze backlinks to your website.",
        "link": "/tools/seo/backlinks",
        "icon": "fas fa-link",
        "category": "SEO",
        "subcategory": "Crawling & Linking",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Internal Links",
        "description": "Evaluate internal linking structure.",
        "link": "/tools/seo/internal-links",
        "icon": "fas fa-link",
        "category": "SEO",
        "subcategory": "Crawling & Linking",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "CSS Issues",
        "description": "Identify CSS problems affecting performance.",
        "link": "/tools/seo/css-issues",
        "icon": "fas fa-code",
        "category": "SEO",
        "subcategory": "HTML/CSS Compliance",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "Deprecated HTML Tags",
        "description": "Find deprecated HTML tags.",
        "link": "/tools/seo/deprecated-html",
        "icon": "fas fa-exclamation-triangle",
        "category": "SEO",
        "subcategory": "HTML/CSS Compliance",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "Gzip Compression",
        "description": "Check if Gzip compression is enabled.",
        "link": "/tools/seo/gzip",
        "icon": "fas fa-compress",
        "category": "SEO",
        "subcategory": "HTML/CSS Compliance",
        "most_used": False,
        "is_new": True
    },

    # Website Security
    {
        "name": "X-Tags",
        "description": "Verify security tags like X-Frame-Options.",
        "link": "/tools/security/x-tags",
        "icon": "fas fa-tags",
        "category": "Website Security",
        "subcategory": "Website Security",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "Header Info",
        "description": "Analyze response headers for security.",
        "link": "/tools/security/header-info",
        "icon": "fas fa-info-circle",
        "category": "Website Security",
        "subcategory": "Website Security",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "HTTPS/SSL",
        "description": "Verify HTTPS and SSL certificate compliance.",
        "link": "/tools/security/ssl",
        "icon": "fas fa-lock",
        "category": "Website Security",
        "subcategory": "Website Security",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Server Response",
        "description": "Analyze server response headers.",
        "link": "/tools/security/server-response",
        "icon": "fas fa-server",
        "category": "Website Security",
        "subcategory": "Website Security",
        "most_used": True,
        "is_new": False
    },
    {
        "name": "Security Info",
        "description": "Review website security configurations.",
        "link": "/tools/security/info",
        "icon": "fas fa-shield-alt",
        "category": "Website Security",
        "subcategory": "Website Security",
        "most_used": False,
        "is_new": True
    },
    {
        "name": "Canonical HTTPS to HTTP",
        "description": "Check if HTTP is redirected to HTTPS.",
        "link": "/tools/security/canonical-http",
        "icon": "fas fa-exchange-alt",
        "category": "Website Security",
        "subcategory": "Website Security",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "HTTP to HTTPS Redirect",
        "description": "Ensure proper redirection from HTTP to HTTPS.",
        "link": "/tools/security/redirect-http-https",
        "icon": "fas fa-exchange-alt",
        "category": "Website Security",
        "subcategory": "Website Security",
        "most_used": False,
        "is_new": False
    },

    # Localization
    {
        "name": "Invalid hreflang Attribute",
        "description": "Detect invalid hreflang attributes.",
        "link": "/tools/localization/invalid-hreflang",
        "icon": "fas fa-code",
        "category": "SEO",
        "subcategory": "Localization",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "Multiple Language Codes",
        "description": "Check for multiple language codes in hreflang.",
        "link": "/tools/localization/multiple-language-codes",
        "icon": "fas fa-language",
        "category": "SEO",
        "subcategory": "Localization",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "Invalid HTML lang Attribute",
        "description": "Identify invalid lang attributes in HTML.",
        "link": "/tools/localization/invalid-html-lang",
        "icon": "fas fa-code",
        "category": "SEO",
        "subcategory": "Localization",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "Language Duplicate",
        "description": "Detect duplicate language attributes.",
        "link": "/tools/localization/language-duplicate",
        "icon": "fas fa-clone",
        "category": "SEO",
        "subcategory": "Localization",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "HTML Lang Missing",
        "description": "Identify missing lang attributes in HTML.",
        "link": "/tools/localization/missing-html-lang",
        "icon": "fas fa-code",
        "category": "SEO",
        "subcategory": "Localization",
        "most_used": False,
        "is_new": False
    },
    {
        "name": "x-default Attribute Missing",
        "description": "Ensure x-default is included in hreflang.",
        "link": "/tools/localization/x-default-missing",
        "icon": "fas fa-exclamation-triangle",
        "category": "SEO",
        "subcategory": "Localization",
        "most_used": False,
        "is_new": False
    },
]

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configurar el registro
#logging.basicConfig(filename='instance/error.log', level=logging.ERROR)

# Creamos archivo de log
log_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'app.log')
if not os.path.exists(log_path):
    open(log_path, 'w').close()

# Configuración de registros
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = RotatingFileHandler('instance/app.log',
                                   maxBytes=102400,
                                   backupCount=10)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

#@app.errorhandler(Exception)
#def handle_exception(error):
#    app.logger.error('Unhandled Exception: %s', error)
#    return 'Internal Server Error', 500

# Importar modelos y vistas

from app.controllers import main_controller, user_controller, tools_controller, admin_controller, logs_controller, spider_tools, mobile_tools, image_tools, speller_tool, marketing_controller
from app.controllers.logs_controller import log_event
from app.views import user_views, tools_views, logs_views, new_domain_views, new_seo_views, accesibility_views, usability_views  #seo_views #domain_tools
from app.models.user_model import Users
from app.models.marketing_model import MarketingMetrics  

#from app.forms import LoginForm, ConfigForm

# Comprobamos si la base de datos SQLite existe, y si no, la creamos
database_path = os.path.join(os.path.dirname(__file__), '..', 'instance',
                             'database.db')
if not os.path.exists(database_path):
    open(database_path, 'w').close()

# Crear la primera instancia de usuario si no existe
with app.app_context():
    db.create_all()
    if not Users.query.first():
        new_user = Users(username='user',
                         email='user@user.com',
                         role='usuario',
                         active=True,
                         config={
                             "color_primary": "#ffffff",
                             "color_secondary": "#000000",
                             "color_tertiary": "#0066cc",
                             "web_name": "WHITE",
                             "logo_url": "https://web.com/asdfadsf.png"
                         })
        new_user.set_password('user')

        new_admin = Users(username='admin',
                          email='admin@admin.com',
                          role='admin',
                          active=True,
                          config={
                              "color_primary": "#ffffff",
                              "color_secondary": "#000000",
                              "color_tertiary": "#0066cc",
                              "web_name": "WHITE",
                              "logo_url": "https://web.com/asdfadsf.png"
                          })
        new_admin.set_password('admin')
        db.session.add(new_admin)
        db.session.add(new_user)
        db.session.commit()

        # Insertar datos de marketing si no existen
    if not MarketingMetrics.query.first():
        marketing_data = MarketingMetrics(
            churn_rate=5.0,  # Ejemplo de tasa de cancelación
            clv=1500.0,  # Ejemplo de Customer Lifetime Value
            cac=100.0,  # Ejemplo de Costo de Adquisición de Clientes
            mrr=25000.0,  # Ejemplo de Monthly Recurring Revenue
            arr=300000.0,  # Ejemplo de Annual Recurring Revenue
            nrr=120.0,  # Ejemplo de Net Revenue Retention
            expansion_revenue_rate=10.0,  # Ejemplo de Expansion Revenue Rate
            #created_at=datetime.datetime.utcnow,
            #updated_at=datetime.datetime.utcnow
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        db.session.add(marketing_data)
        db.session.commit()

#@login_manager.user_loader
#def load_user(user_id):
#    return User.query.get(int(user_id))


@app.context_processor
def inject_sidebar_info():
    return dict(is_admin=current_user.is_authenticated
                and current_user.role == 'admin')


@app.context_processor
def inject_breadcrumb():
    breadcrumbs = [{
        'url': '/',
        'text': 'Inicio'
    }, {
        'url': '/profile',
        'text': 'Opcion 1'
    }, {
        'url': '/profile/edit',
        'text': 'Sub opcion 1'
    }]
    return {'breadcrumbs': breadcrumbs}


@app.context_processor
def inject_grouped_tools():
    # Agrupar herramientas por categoría y subcategoría
    grouped_tools = {}
    for category, tools_in_category in groupby(sorted(
            tools, key=itemgetter('category')),
                                               key=itemgetter('category')):
        subcategories = {}
        for subcategory, tools_in_subcategory in groupby(
                sorted(tools_in_category, key=itemgetter('subcategory')),
                key=itemgetter('subcategory')):
            subcategories[subcategory] = list(tools_in_subcategory)
        grouped_tools[category] = subcategories
    return dict(grouped_tools=grouped_tools)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


#@app.before_request
#def check_show_cookies_modal():
#    if not current_user.is_authenticated and 'cookies_accepted' not in session:
#        session['show_cookies_modal'] = True


# Manejar error 400 (Bad Request)
@app.errorhandler(400)
def bad_request(error):
    return render_template('error_pages/400.html', error=error), 400


# Manejar otros errores comunes
@app.errorhandler(403)
def forbidden(error):
    return render_template('error_pages/403.html', error=error), 403


@app.errorhandler(404)
def not_found(error):
    return render_template('error_pages/404.html', error=error), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error_pages/500.html', error=error), 500

