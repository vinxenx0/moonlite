
from datetime import datetime
from flask_login import current_user
from app.controllers.logs_controller import log_event
from flask import jsonify, request
from app import app
from app.controllers.spider_tools import get_page_info
from app.controllers.tools_controller import *
import time
import subprocess
from flask import render_template
from app import app
from app.forms import PageInfoForm, PingForm
from app.models.usage_model import Activity
from datetime import datetime
import json
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import app, db
from app.controllers.logs_controller import log_event
from app.controllers.spider_tools import get_page_info
from app.forms import ConfigForm, PageInfoForm
from app.models.usage_model import Activity

from app.views.info import tools

# Cargar la base de datos de GeoIP
# geoip_reader = geoip2.database.Reader('GeoLite2-Country.mmdb')

#def get_country_from_ip(ip_address):
#    try:
#        response = geoip_reader.country(ip_address)
#        country = response.country.name
#        return country
#    except Exception as e:
#        print(f"Error getting country from IP: {e}")
#        return None



@app.route('/tools/', methods=['GET', 'POST'])
def index_tools():
    data = None
    validator = None
    spelling_errors = None
    grammar_errors = None
    breadcrumbs = [] #[{'url': '/start', 'text': 'Bienvenido'}]
    _tools = [
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

    return render_template('tools/index.html',
                           data=data,
                           validator=validator,
                           form=form,
                           breadcrumbs=breadcrumbs,
                           tools=tools)

@app.route('/tools/check_domain/<string:domain>') #, methods=['POST'])
def check_domain(domain):
    start_time = time.time() 
    breadcrumbs = [
        {'url': '/tools', 'text': 'Tools'},
        {'url': '/tools/checkdomain', 'text': 'Check Domain'}
    ]
    
    if domain:
        results = {
            'mx_lookup': mx_lookup(domain),
            # 'whois_lookup': whois_lookup(domain),
            'dmarc_lookup': dmarc_lookup(domain),
            'spf_lookup': spf_lookup(domain),
            'dns_lookup': dns_lookup(domain),
            # 'reverse_lookup': reverse_lookup(domain),
            'dkim_lookup': dkim_lookup(domain),
            #'aaaa_lookup': aaaa_lookup(domain),
            'srv_lookup': srv_lookup('_service', '_protocol', domain),
            'cert_lookup': cert_lookup(domain),
            'bimi_lookup': bimi_lookup(domain),
            #'ip_lookup': ip_lookup(domain),
            #'cname_lookup': cname_lookup(domain),
            'soa_lookup': soa_lookup(domain),
            'txt_lookup': txt_lookup(domain),
            'dnskey_lookup': dnskey_lookup(domain),
            'ssl_lookup': ssl_lookup(domain),
            'loc_lookup': loc_lookup(domain),
            'ipseckey_lookup': ipseckey_lookup(domain),
            'asn_lookup': asn_lookup(domain),
            'rrsig_lookup': rrsig_lookup(domain),
            'nsec_lookup': nsec_lookup(domain),
            'arin_lookup': arin_lookup(domain),
            'mta_sts_lookup': mta_sts_lookup(domain),
            'nsec3param_lookup': nsec3param_lookup(domain),
            'dns_servers_lookup': dns_servers_lookup(domain),
            'http_lookup': http_lookup(domain),
            'https_lookup': https_lookup(domain),
            'ping': ping_lookup(domain),
            #'traceroute': traceroute_lookup(domain),
            'nmap': nmap_lookup(domain)
        }

        sorted_results = {key: results[key] for key in sorted(results.keys())}
        
        end_time = time.time()
        duration = end_time - start_time
        
        sorted_results['duration'] = duration 
        log_event('CHECKDOMAIN', 'Herramienta lanzada.')        
        return jsonify(sorted_results)
 
    else:
        log_event('CHECKDOMAIN', 'Error.')
        return jsonify({'error': 'Domain not provided'}), 400



@app.route('/tools/ping', methods=['GET', 'POST'])
def ping():
    breadcrumbs = [
        {'url': '/tools', 'text': 'Tools'},
        {'url': '/tools/ping', 'text': 'Ping'}
    ]
    form = PingForm()
    ping_result = None
    if form.validate_on_submit():
        domain = form.domain.data
        try:
            result = subprocess.run(['ping', '-c', '4', domain], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                log_event('PING', 'Correcto.')
                ping_result = result.stdout
            else:
                ping_result = "No se pudo hacer ping al dominio."
                log_event('PING', 'Fail.')
        except subprocess.TimeoutExpired:
            log_event('PING', 'Timeout.')
            ping_result = "El ping ha superado el tiempo de espera."
    return render_template('tools/ping.html', title='PING', form=form, ping_result=ping_result, breadcrumbs=breadcrumbs)
