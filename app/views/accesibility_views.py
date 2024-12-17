import json
import time

import requests
from app.controllers.spider_tools import analizar_ortografia, ejecutar_pa11y, get_page_info
from flask import render_template
from flask_login import current_user
from flask import render_template, request
from app import app, db
from app.controllers.logs_controller import log_event
from app.controllers.tools_controller import *
from app.forms import DomainToolsForm, PageInfoForm
from datetime import datetime
from app.models.usage_model import Activity

from app.views.info import tool_info


@app.route('/tools/accesibility/', methods=['GET', 'POST'])
def index_accesiblity():
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

    return render_template('tools/accesibility/index.html',
                           data=data,
                           validator=validator,
                           form=form,
                           breadcrumbs=breadcrumbs,
                           spelling_errors=spelling_errors,
                           grammar_errors=grammar_errors)

@app.route("/tools/accesibility/wcag", methods=["GET", "POST"])
def wcag():
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
            "text": "Accesibilidad"
        },
        {
            "url": "/tools/accesiblity/wcag",
            "text": "WCAG"
        },
    ]
    form = DomainToolsForm()
    results = None
    is_results_valid = False
    if form.validate_on_submit():
        domain = form.domain.data

        results = json.loads(ejecutar_pa11y(domain))
        print(results)
        
        if results is not None:
            is_results_valid = True
        else:
            is_results_valid = False

        is_results_valid = True ## temporal

    end_time = time.time()
    duration = end_time - start_time
    return render_template(
        "tools/accesibility/wcag.html",
        title="WCAG",
        is_results_valid=is_results_valid,
        duration=duration,
        form=form,
        results=results,
        breadcrumbs=breadcrumbs,
        definition=definition,
        slogan=slogan,
        info_popup=info_popup,
        keywords=keywords,
    )


# spelling_errors, grammar_errors = analizar_ortografia(response.text)

@app.route("/tools/accesibility/ortografia", methods=["GET", "POST"])
def ortografia():
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
            "text": "Accesibilidad"
        },
        {
            "url": "/tools/accesiblity/ortografia",
            "text": "Ortografia"
        },
    ]
    form = DomainToolsForm()
    results = None
    is_results_valid = False
    if form.validate_on_submit():
        domain = form.domain.data
        response = requests.get(domain)
        spelling_errors, results = analizar_ortografia(response.text)

        #print(spelling_errors)
        print("----")
        print(results)
        print("----")
        
        if results is not None:
            is_results_valid = True
        else:
            is_results_valid = False

        is_results_valid = True ## temporal

    end_time = time.time()
    duration = end_time - start_time
    return render_template(
        "tools/accesibility/spelling.html",
        title="SPELLING",
        is_results_valid=is_results_valid,
        duration=duration,
        form=form,
        results=results,
        breadcrumbs=breadcrumbs,
        definition=definition,
        slogan=slogan,
        info_popup=info_popup,
        keywords=keywords,
    )