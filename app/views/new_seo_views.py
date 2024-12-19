import time
from flask import render_template, request
import requests
from app import app, db
from flask_login import current_user
from datetime import datetime
from app.forms import PageInfoForm, SeoToolsForm
from app.models.usage_model import Activity
from app.controllers.logs_controller import log_event
from app.controllers.spider_tools import (
    check_css_status, check_deprecated_tags, check_gzip, get_canonical_info, 
    get_common_url_issues, get_directive_issues, get_h1_issues, get_h2_issues, 
    get_hreflang_issues, get_meta_description_issues, get_meta_keywords_issues, get_page_info, 
    get_page_title_issues, get_soup, get_structured_data_issues
)
from app.views.info import tool_info


def process_tool(tool, soup, url, response):
    if tool == 'titles':
        return get_page_title_issues(soup)
    elif tool == 'meta-description':
        return get_meta_description_issues(soup)
    elif tool == 'meta-keywords':
        return get_meta_keywords_issues(soup)
    elif tool == 'headings':
        return get_h1_issues(soup)
    elif tool == 'canonicals':
        return get_canonical_info(soup, url, response)
    elif tool == 'directives':
        return get_directive_issues(soup, response)
    elif tool == 'shema-org':
        return get_structured_data_issues(soup)
    elif tool == 'opengraph':
        return {"sin hacer aun"}
    elif tool == 'hreflang':
        return get_hreflang_issues(soup)
    elif tool == 'urls':
        return get_common_url_issues(url)
    elif tool == 'gzip':
        return check_gzip(url)
    elif tool == 'deprecated-html':
        return check_deprecated_tags(soup)
    elif tool == 'css':
        return check_css_status(response)
    return None

def count_results(results):
    total_entries = len(results)
    true_count = sum(1 for v in results.values() if v is True)
    false_count = sum(1 for v in results.values() if v is False)
    none_or_empty_count = sum(1 for v in results.values() if v is None or v == '')
    false_percentage = (false_count / total_entries * 100) if total_entries > 0 else 0
    return total_entries, true_count, false_count, none_or_empty_count, false_percentage

@app.route("/tools/seo/<string:tool>", methods=["GET", "POST"])
def tools_seo(tool):
    
    
    print("tool_seo new")
    start_time = time.time()
    definition, slogan, keywords, info_popup = "", "", "", ""
    soup, response, results = None, None, None
    is_results_valid = False

    breadcrumbs = [
        {"url": "/tools", "text": "Tools"},
        {"url": "/tools/seo/", "text": "SEO"},
        {"url": "/tools/seo/" + tool, "text": tool}
    ]

    form = SeoToolsForm()
    
    # Comprobar que existe la herramienta primero
    if tool in tool_info:
        definition = tool_info[tool]['definition']
        slogan = tool_info[tool]['slogan']
        keywords = tool_info[tool]['keywords']
        info_popup = tool_info[tool]['info_popup']
    else:
        return render_template("tools/seo/notfound.html")

    if form.validate_on_submit():
        url = form.domain.data

        # Obtener información del usuario
        username = current_user.username if current_user.is_authenticated else 'Anonymous'
        email = current_user.email if current_user.is_authenticated else ''
        ip_address = request.remote_addr
        user_agent = request.user_agent.string
        country = 'Spain'  # get_country_from_ip(ip_address)
        language = request.accept_languages.best
        timestamp = datetime.utcnow()
        page_url = request.url

        # Guardar la información del usuario en la base de datos
        user_usage = Activity(
            username=username, email=email, target=url, ip_address=ip_address,
            user_agent=user_agent, country=country, language=language,
            timestamp=timestamp, page_url=page_url
        )
        db.session.add(user_usage)
        db.session.commit()

        try:
            soup = get_soup(url)
            response = requests.get(url)
            if soup:
                results = process_tool(tool, soup, url, response)
                if results is not None:
                    is_results_valid = True
                    log_event(tool, url)
                else:
                    log_event(tool, 'Fail: No results returned')
            else:
                log_event(tool, 'Fail: Unable to parse HTML')
        except Exception as e:
            log_event(tool, f'Fail: {e}')
            results = {'error': str(e)}

    if results:
        total_entries, true_count, false_count, none_or_empty_count, false_percentage = count_results(results)
    else:
        total_entries, true_count, false_count, none_or_empty_count, false_percentage = 0, 0, 0, 0, 0

    duration = time.time() - start_time
    return render_template(
        "tools/seo/results_seo.html",
        title=tool, is_results_valid=is_results_valid, duration=duration, form=form,
        results=results, breadcrumbs=breadcrumbs, definition=definition,
        slogan=slogan, info_popup=info_popup, keywords=keywords,
        total_checks=total_entries, success_count=true_count,
        empty_checks=none_or_empty_count, danger_count=false_count,
        danger_percentage=false_percentage
    )
