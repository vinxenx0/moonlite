from app.controllers.logs_controller import log_event
from flask import jsonify
from app import app
from app.controllers.tools_controller import *
import time
import subprocess
from flask import render_template
from app import app
from app.forms import PingForm
from flask import render_template, redirect, url_for
from app import app
from app.controllers.logs_controller import log_event

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


@app.route('/tools', methods=['GET'])
def index_tools_redirect():
    return redirect(url_for('index_tools_with_trailing_slash'))


@app.route('/tools/', methods=['GET'])
def index_tools_with_trailing_slash():
    breadcrumbs = [{'url': '/tools', 'text': 'Todas las herramientas'}]

    return render_template('tools/index.html',
                           breadcrumbs=breadcrumbs,
                           tools=tools)


@app.route('/tools/domains/', methods=['GET', 'POST'])
def index_domains():

    breadcrumbs = [{
        'url': '/tools',
        'text': 'Tools'
    }, {
        'url': '/tools/domains',
        'text': 'Dominios'
    }]

    return render_template('tools/domains/index.html',
                           breadcrumbs=breadcrumbs,
                           tools=tools)


@app.route('/tools/seo/', methods=['GET', 'POST'])
def index_seo():

    breadcrumbs = [{
        'url': '/tools',
        'text': 'Tools'
    }, {
        'url': '/tools/seo',
        'text': 'SEO'
    }]
    return render_template('tools/seo/index.html',
                           breadcrumbs=breadcrumbs,
                           tools=tools)


@app.route('/tools/accesibility/', methods=['GET', 'POST'])
def index_accesiblity():

    breadcrumbs = [{
        'url': '/',
        'text': 'Inicio'
    }, {
        'url': '/tools',
        'text': 'Tools'
    }, {
        'url': '/tools/domains',
        'text': 'Accesibilidad'
    }]

    return render_template('tools/accesibility/index.html',
                           breadcrumbs=breadcrumbs,
                           tools=tools)


@app.route('/tools/check_domain/<string:domain>')  #, methods=['POST'])
def check_domain(domain):
    start_time = time.time()
    breadcrumbs = [{
        'url': '/tools',
        'text': 'Tools'
    }, {
        'url': '/tools/checkdomain',
        'text': 'Check Domain'
    }]

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


@app.route('/tools/ping/', methods=['GET', 'POST'])
def ping():
    breadcrumbs = [{
        'url': '/tools',
        'text': 'Tools'
    }, {
        'url': '/tools/ping',
        'text': 'Ping'
    }]
    form = PingForm()
    ping_result = None
    if form.validate_on_submit():
        domain = form.domain.data
        try:
            result = subprocess.run(['ping', '-c', '4', domain],
                                    capture_output=True,
                                    text=True,
                                    timeout=10)
            if result.returncode == 0:
                log_event('PING', 'Correcto.')
                ping_result = result.stdout
            else:
                ping_result = "No se pudo hacer ping al dominio."
                log_event('PING', 'Fail.')
        except subprocess.TimeoutExpired:
            log_event('PING', 'Timeout.')
            ping_result = "El ping ha superado el tiempo de espera."
    return render_template('tools/ping.html',
                           title='PING',
                           form=form,
                           ping_result=ping_result,
                           breadcrumbs=breadcrumbs)
