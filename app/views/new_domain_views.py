import time
from flask import render_template
from flask_login import current_user
from flask import render_template, request
from app import app, db
from app.controllers.logs_controller import log_event
from app.controllers.spider_tools import get_page_info
from app.controllers.tools_controller import *
from app.forms import DomainToolsForm, PageInfoForm
from datetime import datetime
from app.models.usage_model import Activity

from app.views.info import tool_info

##########
###
###
###
#######


@app.route("/tools/domains/<string:tool>", methods=["GET", "POST"])
def tools_domains_new(tool):

    total_entries = 0
    true_count = 0
    false_count = 0
    none_or_empty_count = 0
    
    definition = ""
    slogan = ""
    keywords = ""
    info_popup = ""
    start_time = time.time()
    breadcrumbs = [
        {
            "url": "/tools",
            "text": "Tools"
        },
        {
            "url": "/tools/domains/",
            "text": "Dominios"
        },
        {
            "url": "/tools/domains/" + tool,
            "text": tool
        },
    ]
    form = DomainToolsForm()
    results = None
    is_results_valid = False

    # Comprobar que existe la herramienta primero
    if tool in tool_info:
        definition = tool_info[tool]['definition']
        slogan = tool_info[tool]['slogan']
        keywords = tool_info[tool]['keywords']
        info_popup = tool_info[tool]['info_popup']
    else:
        return render_template("tools/domains/notfound.html")

    if form.validate_on_submit():
        domain = form.domain.data

        # Obtener información del usuario
        username = 'Anonymous'
        email = ''
        if current_user.is_authenticated:
            username = current_user.username
            email = current_user.email

        url = form.domain.data
        ip_address = request.remote_addr
        user_agent = request.user_agent.string
        country = 'Spain'  # get_country_from_ip(ip_address)
        language = request.accept_languages.best

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

        _results = {
            #'mx_lookup': mx_lookup(domain),
            # 'whois_lookup': whois_lookup(domain),
            #'dmarc_lookup': dmarc_lookup(domain),
            #'spf_lookup': spf_lookup(domain),
            #'dns_lookup': dns_lookup(domain),
            # 'reverse_lookup': reverse_lookup(domain),
            #'dkim_lookup': dkim_lookup(domain),
            #'aaaa_lookup': aaaa_lookup(domain),
            #'srv_lookup': srv_lookup('_service', '_protocol', domain),
            #'cert_lookup': cert_lookup(domain),
            #'bimi_lookup': bimi_lookup(domain),
            #'ip_lookup': ip_lookup(domain),
            #'cname_lookup': cname_lookup(domain),
            #'soa_lookup': soa_lookup(domain),
            #'txt_lookup': txt_lookup(domain),
            #'dnskey_lookup': dnskey_lookup(domain),
            #'ssl_lookup': ssl_lookup(domain),
            #'loc_lookup': loc_lookup(domain),
            #'ipseckey_lookup': ipseckey_lookup(domain),
            #'asn_lookup': asn_lookup(domain),
            #'rrsig_lookup': rrsig_lookup(domain),
            #'nsec_lookup': nsec_lookup(domain),
            #'arin_lookup': arin_lookup(domain),
            #'mta_sts_lookup': mta_sts_lookup(domain),
            #'nsec3param_lookup': nsec3param_lookup(domain),
            #'dns_servers_lookup': dns_servers_lookup(domain),
            #'http_lookup': http_lookup(domain),
            #'https_lookup': https_lookup(domain),
            'ping': ping_lookup(domain),
            #'traceroute': traceroute_lookup(domain),
            #'nmap': nmap_lookup(domain)
        }


        # Ejecutar la función correspondiente
        if tool == 'nmap':
            results = {'nmap': nmap_lookup(domain)}
        elif tool == 'traceroute':
            results = {'traceroute_lookup': traceroute_lookup(domain)}
        elif tool == 'aaaa':
            results = {'aaaa_lookup': aaaa_lookup(domain)}
        elif tool == 'ip':
            results = {'ip_lookup': ip_lookup(domain)}
        elif tool == 'cname':
            results = {'cname_lookup': cname_lookup(domain)}
        elif tool == 'reverse':
            results = {'reverse_lookup': reverse_lookup(domain)}
        elif tool == 'whois':
            results = {"whois_lookup": whois_lookup(domain)}
        
        elif tool == 'nsec3param':
            results = {'nsec3param_lookup': nsec3param_lookup(domain)}

        elif tool == 'mtasts':
            results = { 'mta_sts_lookup': mta_sts_lookup(domain)}

        elif tool == 'arin':
            results = { 'arin_lookup': arin_lookup(domain)}
        
        elif tool == 'nsec':
            results = { 'nsec_lookup': nsec_lookup(domain)}

        elif tool == 'rrsig':
            results = {  'rrsig_lookup': rrsig_lookup(domain)}

        elif tool == 'asn':
            results = {'asn_lookup': asn_lookup(domain)}
        
        elif tool == 'ipseckey':
            results = {'ipseckey_lookup': ipseckey_lookup(domain)}

        elif tool == 'loc':
            results = { 'loc_lookup': loc_lookup(domain)}

        elif tool == 'ssl':
            results = {'ssl_lookup': ssl_lookup(domain),}

        elif tool == 'soa':
            results = {'soa_lookup': soa_lookup(domain)}

        elif tool == 'txt':
            results = { 'txt_lookup': txt_lookup(domain)}

        elif tool == 'bimi':
            results = {'bimi_lookup': bimi_lookup(domain)}

        elif tool == 'dns_server':
            results = {'dns_servers_lookup': dns_servers_lookup(domain)}

        elif tool == 'http':
            results = {'http_lookup': http_lookup(domain)}

        elif tool == 'https':
            results = {'https_lookup': https_lookup(domain),}

        elif tool == 'dnskey':
            results = {'dnskey_lookup': dnskey_lookup(domain)}

        elif tool == 'cert':
            results = {'cert_lookup': cert_lookup(domain)}

        elif tool == 'srv':
            results = {'srv_lookup': srv_lookup('_service', '_protocol', domain)}
        elif tool == 'dkim':
            results = {'dkim_lookup': dkim_lookup(domain)}
        elif tool == 'dns':
            results = {'dns_lookup': dns_lookup(domain)}
        elif tool == 'spf':
            results = {'spf_lookup': spf_lookup(domain)}
        elif tool == 'dmarc':
            results = {'dmarc_lookup': dmarc_lookup(domain)}
        elif tool == 'mx':
            results = {'mx_lookup': mx_lookup(domain)}





        if results is not None:
            log_event(tool, domain)
            is_results_valid = True
        else:
            log_event(tool, 'Fail:' + domain)

        
        # Recorrer el diccionario y contar los valores según las condiciones dadas
        for key, value in results.items():
            total_entries += 1
            if value is True:
                true_count += 1
            elif value is False:
                false_count += 1
            elif value is None or value == '':
                none_or_empty_count += 1

    # Calcular el porcentaje de valores False con respecto al total
    if total_entries > 0:
        false_percentage = (false_count / total_entries) * 100
    else:
        false_percentage = 0

    end_time = time.time()
    duration = end_time - start_time
    
    return render_template(
        "tools/domains/results_domains.html",
        # "tools/domains/" + tool + ".html",
        title=tool,
        is_results_valid=is_results_valid,
        duration=duration,
        form=form,
        results=results,
        breadcrumbs=breadcrumbs,
        definition=definition,
        slogan=slogan,
        info_popup=info_popup,
        keywords=keywords,
        total_checks =  total_entries,
        success_count = true_count,
        empty_checks = none_or_empty_count,
        danger_count=false_count,
        danger_percentage=false_percentage
    )
