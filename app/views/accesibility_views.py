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

        is_results_valid = True  ## temporal

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

        is_results_valid = True  ## temporal

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
