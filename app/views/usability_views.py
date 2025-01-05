import time
from app.controllers.usability_tools import check_favicon, check_flash_usage, check_x_card_tag, fetch_page_content
from flask import render_template
import requests
from app.controllers.spider_tools import get_soup
from flask_login import current_user
from flask import render_template, request
from app import app, db
from app.controllers.logs_controller import log_event
from app.controllers.spider_tools import *
from app.forms import SeoToolsForm
from datetime import datetime
from app.models.usage_model import Activity

from app.models.user_model import Users
from app.utils.logger import log_user_event
from app.views.info import tool_info

##########
###
###
###
#######


@app.route("/tools/usability/<string:tool>", methods=["GET", "POST"])
def tools_usability(tool):

    start_time = time.time()
    definition = ""
    slogan = ""
    keywords = ""
    info_popup = ""
    soup = None
    response = None

    # Inicializar los contadores
    total_entries = 0
    true_count = 0
    false_count = 0
    none_or_empty_count = 0
    breadcrumbs = [
        {
            "url": "/tools",
            "text": "Tools"
        },
        {
            "url": "/tools/usability/",
            "text": "USABILITY"
        },
        {
            "url": "/tools/usability/" + tool,
            "text": tool
        },
    ]
    form = SeoToolsForm()
    results = None
    is_results_valid = False

    # Comprobar que existe la herramienta primero
    if tool in tool_info:
        definition = tool_info[tool]['definition']
        slogan = tool_info[tool]['slogan']
        keywords = tool_info[tool]['keywords']
        info_popup = tool_info[tool]['info_popup']
    else:
        print("no existe la herramienta")
        #return render_template("tools/usability/notfound.html")

    if form.validate_on_submit():

        page = form.domain.data

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

        soup = get_soup(url)
        response = requests.get(url)
        html_content = fetch_page_content(url)

        if soup:
            try:
                # Ejecutar la función correspondiente
                if tool == 'missing-favicon':
                    results = check_favicon(html_content)

                elif tool == 'flash-used':
                    results = check_flash_usage(html_content)

                elif tool == 'x-card-missing':
                    results = check_x_card_tag(html_content)

                print(results)

            except Exception as e:
                print(f"Error processing page info: {e}")
                log_event(tool, 'Fail:' + e)
                results = {'error': e}

            is_results_valid = True

            if results is not None:
                log_event(tool, page)
                is_results_valid = True
                user = Users.query.get(current_user.id)
                log_user_event(user, f"Analisis Usabilidad en {url}", tool,
                               'info')

                # Recorrer el diccionario y contar los valores según las condiciones dadas
                #for key, value in results.items():
                #    total_entries += 1
                #    if value is True:
                #        true_count += 1
                #    elif value is False:
                #        false_count += 1
                #    elif value is None or value == '':
                #        none_or_empty_count += 1

            else:
                log_event(tool, 'Fail:' + page)
                results = {'error': 'Fail None results'}

        else:
            log_event(tool, 'Fail:' + page)
            results = {'error': 'Unable to parse HTML'}

    # añadir la info extra
    # contar los true, false, y none
    # añadir ayuda

    # Calcular el porcentaje de valores False con respecto al total
    if total_entries > 0:
        false_percentage = (false_count / total_entries) * 100
    else:
        false_percentage = 0

    end_time = time.time()
    duration = end_time - start_time

    return render_template(
        "tools/usability/usability_results.html",
        # "tools/seo/" + tool + ".html",
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
        total_checks=total_entries,
        success_count=true_count,
        empty_checks=none_or_empty_count,
        danger_count=false_count,
        danger_percentage=false_percentage)
