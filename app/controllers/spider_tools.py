import re
import socket
import subprocess
from urllib.parse import urlparse
#from app import app
import requests
import json
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import aspell

import ssl
import datetime

from app.controllers import mobile_tools



def get_soup(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')
        else:
            return None
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None


def get_header_info(url):
    try:
        response = requests.head(url, allow_redirects=True)
        header_info = {
            'Header Name': [],
            'Header Value': []
        }

        for header_name, header_value in response.headers.items():
            header_info['Header Name'].append(header_name)
            header_info['Header Value'].append(header_value)

        return header_info

    except requests.RequestException as e:
        print(f"Error fetching headers for URL {url}: {e}")
        return None

def ejecutar_pa11y(url):
    command = f"pa11y -T 1 --ignore issue-code-2 --ignore issue-code-1 -r json {url} 2>/dev/null"
    process = subprocess.run(command,
                              shell=True,
                              check=False,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)
    #print(process.stdout)
    return process.stdout


def analizar_ortografia(content, language='es'):
    # Configurar el corrector ortográfico
    speller = aspell.Speller('lang', language)
    
    # Tokenizar el contenido para analizar palabra por palabra
    words = content.split()
    
    # Buscar errores ortográficos y gramaticales
    spelling_errors = []
    grammar_errors = []
    for word in words:
        if not speller.check(word):
            # Si la palabra no está en el diccionario, es un error ortográfico
            spelling_errors.append(word)
            suggestions = speller.suggest(word)
            # Si hay sugerencias disponibles, consideramos que es un error gramatical
            if suggestions:
                grammar_errors.append((word, suggestions))
    
    return spelling_errors, grammar_errors

def audit_image_details(url, soup):
    images = soup.find_all('img')
    image_details = []

    for img in images:
        image_src = img.get('src', '')
        alt_text = img.get('alt', '')
        width = img.get('width', '')
        height = img.get('height', '')

        # Check if alt text is missing
        if not alt_text:
            missing_alt_text = True
        else:
            missing_alt_text = False

        # Check if alt attribute is missing
        if 'alt' not in img.attrs:
            missing_alt_attribute = True
        else:
            missing_alt_attribute = False

        # Check if alt text exceeds 100 characters
        if len(alt_text) > 100:
            alt_text_over_100_characters = True
        else:
            alt_text_over_100_characters = False

        image_details.append({
            'Image_Source': image_src,
            'Alt_Text': alt_text,
            'Width': width,
            'Height': height,
            'Missing_Alt_Text': missing_alt_text,
            'Missing_Alt_Attribute': missing_alt_attribute,
            'Alt_Text_Over_100_Characters': alt_text_over_100_characters
        })

    print(url)
    print(image_details)
    return {
        'URL': url,
        'Images': image_details
    }


def get_canonical_info(soup, url, response):
    canonical_link = soup.find('link', attrs={'rel': 'canonical'})
    canonical_url = canonical_link.get('href') if canonical_link else ''
    canonical_in_head = canonical_link is not None
    canonical_self_referencing = canonical_url == url
    canonicalised = canonical_url != url and canonical_url != ''
    canonical_absolute = bool(urlparse(canonical_url).netloc) if canonical_url else False
    canonical_relative = not canonical_absolute
    canonical_http_header = response.headers.get('Canonical')
    canonical_http_present = canonical_http_header is not None
    canonical_http_absolute = bool(urlparse(canonical_http_header).netloc) if canonical_http_header else False
    canonical_http_relative = not canonical_http_absolute if canonical_http_header else False
    canonical_multiple = bool(soup.find_all('link', attrs={'rel': 'canonical'})) or (canonical_http_header and canonical_http_header != canonical_url)
    canonical_multiple_conflicting = canonical_multiple and len(set(canonical_url for canonical_url in soup.find_all('link', attrs={'rel': 'canonical'}))) > 1
    canonical_non_indexable = False  # Aquí necesitarías implementar la lógica para verificar si el canonical URL es indexable o no.
    canonical_is_relative = canonical_link and not canonical_absolute
    canonical_unlinked = False  # Aquí necesitarías implementar la lógica para verificar si el canonical URL no está enlazado en el sitio web.
    canonical_outside_head = False  # Aquí necesitarías implementar la lógica para verificar si el canonical link está fuera del elemento head.

    return {
        'Contains_Canonical': canonical_link is not None,
        'Self_Referencing': canonical_self_referencing,
        'Canonicalised': canonicalised,
        'Canonical_Absolute': canonical_absolute,
        'Canonical_Relative': canonical_relative,
        'Canonical_HTTP Present': canonical_http_present,
        'Canonical_HTTP Absolute': canonical_http_absolute,
        'Canonical_HTTP Relative': canonical_http_relative,
        'Canonical_Multiple': canonical_multiple,
        'Canonical_Multiple Conflicting': canonical_multiple_conflicting,
        'Canonical_Non-Indexable': canonical_non_indexable,
        'Canonical_Is Relative': canonical_is_relative,
        'Canonical_Unlinked': canonical_unlinked,
        'Canonical_Outside Head': canonical_outside_head
    }

def get_security_info(url, response, soup):
    http_url = url.startswith('http://') if url else False
    https_url = url.startswith('https://') if url else False
    mixed_content = bool(soup.find_all(lambda tag: tag.name in ['img', 'script', 'link'] and tag.get('src') and tag['src'].startswith('http://'))) if soup else False
    form_url_insecure = bool(soup.find('form', attrs={'action': lambda x: x and x.startswith('http://')})) if soup else False
    form_on_http_url = bool(soup.find('form', attrs={'action': lambda x: x and x.startswith('http://')})) if soup else False
    unsafe_cross_origin_links = bool(soup.find_all(lambda tag: tag.name == 'a' and tag.get('target') == '_blank' and ('rel' not in tag.attrs or 'noopener' not in tag.get('rel', [])))) if soup else False
    protocol_relative_resource_links = bool(soup.find_all(lambda tag: tag.name in ['img', 'script', 'link'] and tag.get('src') and tag['src'].startswith('//'))) if soup else False
    missing_hsts_header = 'strict-transport-security' not in response.headers if response else False
    missing_content_security_policy_header = 'content-security-policy' not in response.headers if response else False
    missing_x_content_type_options_header = 'x-content-type-options' not in response.headers or response.headers['x-content-type-options'] != 'nosniff' if response else False
    missing_x_frame_options_header = 'x-frame-options' not in response.headers if response else False
    missing_secure_referrer_policy_header = 'referrer-policy' not in response.headers or response.headers['referrer-policy'] not in ['no-referrer-when-downgrade', 'strict-origin-when-cross-origin', 'no-referrer', 'strict-origin'] if response else False
    bad_content_type = response.headers.get('content-type', '').split(';')[0] != 'text/html' if response else False
    
    return {
        'HTTP_URLs': http_url,
        'HTTPS_URLs': https_url,
        'Mixed_Content': mixed_content,
        'Form_URL_Insecure': form_url_insecure,
        'Form_on_HTTP_URL': form_on_http_url,
        'Unsafe_Cross-Origin_Links': unsafe_cross_origin_links,
        'Protocol-Relative_Resource_Links': protocol_relative_resource_links,
        'Missing_HSTS Header': missing_hsts_header,
        'Missing_Content-Security-Policy_Header': missing_content_security_policy_header,
        'Missing_X-Content-Type-Options_Header': missing_x_content_type_options_header,
        'Missing_X-Frame-Options_Header': missing_x_frame_options_header,
        'Missing_Secure_Referrer-Policy_Header': missing_secure_referrer_policy_header,
        'Bad_Content_Type': bad_content_type
    }

def get_common_url_issues(url):
    non_ascii_characters = any(ord(char) > 127 for char in url) if url else False
    underscores = '_' in url if url else False
    uppercase = any(char.isupper() for char in url) if url else False
    multiple_slashes = '//' in url if url else False
    repetitive_path = any(url.count(part) > 1 for part in url.split('/')) if url else False
    contains_space = ' ' in url if url else False
    internal_search = '/search' in url or '/search?' in url if url else False
    parameters = '?' in url or '&' in url if url else False
    broken_bookmark = '#' in url if url else False
    ga_tracking_parameters = any(param in url for param in ['utm=', '_ga=', '_gl=']) if url else False
    over_115_characters = len(url) > 115 if url else False
    
    return {
        'Non_ASCII_Characters': non_ascii_characters,
        'Underscores': underscores,
        'Uppercase': uppercase,
        'Multiple_Slashes': multiple_slashes,
        'Repetitive_Path': repetitive_path,
        'Contains_A_Space': contains_space,
        'Internal_Search': internal_search,
        'Parameters': parameters,
        'Broken_Bookmark': broken_bookmark,
        'GA_Tracking_Parameters': ga_tracking_parameters,
        'Over_115_characters': over_115_characters
    }

def get_page_title_issues(soup):

    title_missing = not soup.find('title') or not soup.find('title').text.strip() if soup else False
    all_titles = [title.text.strip() for title in soup.find_all('title')] if soup else []
    title_duplicate = len(all_titles) != len(set(all_titles))
    title_over_60_characters = any(len(title.text.strip()) > 60 for title in soup.find_all('title')) if soup else False
    title_below_30_characters = any(len(title.text.strip()) < 30 for title in soup.find_all('title')) if soup else False
    # Over X Pixels
    # Esta lógica requeriría conocer la longitud en píxeles de los títulos en la página, que normalmente se determina mediante CSS o inspección manual de la página.
    # Below X Pixels
    # Similar a "Over X Pixels", necesitaríamos información específica sobre la longitud en píxeles de los títulos en la página.
    title_same_as_h1 = any(title.text.strip() == (soup.find('h1').text.strip() if soup.find('h1') else '') for title in soup.find_all('title')) if soup else False
    title_multiple = len(soup.find_all('title')) > 1 if soup else False
    title_outside_head = any(title.find_parent('head') is None for title in soup.find_all('title')) if soup else False
    title_1 = soup.find('title').text # if soup.find('title') else ''
    title_1_Length = len(soup.find('title').text) # if soup.find('title') else 0
    
    return {
                'Title_1': title_1,
                'Title_1_Length': title_1_Length,
                'Missing': title_missing,
                'Duplicate': title_duplicate,
                'Over_60_characters': title_over_60_characters,
                'Below_30_characters': title_below_30_characters,
                'Same_as_h1': title_same_as_h1,
                'Multiple': title_multiple,
                'Outside_head': title_outside_head,
                

            }

def get_meta_description_issues(soup):
    ########### META DESCRIPTION #########################
    meta_description_missing = not soup.find('meta', attrs={'name': 'description'}) or not soup.find('meta', attrs={'name': 'description'}).get('content').strip() if soup else False
    all_meta_descriptions = [meta.get('content').strip() for meta in soup.find_all('meta', attrs={'name': 'description'})] if soup else []
    meta_description_duplicate = len(all_meta_descriptions) != len(set(all_meta_descriptions))
    meta_description_over_155_characters = any(len(meta.get('content').strip()) > 155 for meta in soup.find_all('meta', attrs={'name': 'description'})) if soup else False
    meta_description_below_70_characters = any(len(meta.get('content').strip()) < 70 for meta in soup.find_all('meta', attrs={'name': 'description'})) if soup else False
    # Over X Pixels
    # Similar to "Over X Pixels" for page title, we would need specific information about the pixel length of meta descriptions on the page.
    # Below X Pixels
    # Similar to "Below X Pixels" for page title, we would need specific information about the pixel length of meta descriptions on the page.
    meta_description_multiple = len(soup.find_all('meta', attrs={'name': 'description'})) > 1 if soup else False
    meta_description_outside_head = any(meta.find_parent('head') is None for meta in soup.find_all('meta', attrs={'name': 'description'})) if soup else False

    return {
                'Missing': meta_description_missing,
                'Duplicate': meta_description_duplicate,
                'Over_155_characters': meta_description_over_155_characters,
                'Below_70_characters': meta_description_below_70_characters,
                'Multiple': meta_description_multiple,
                'Outside_head': meta_description_outside_head
             }

def get_meta_keywords_issues(soup):
    ############# KEYWORDS #######################
    keywords_missing = not soup.find('meta', attrs={'name': 'keywords'}) if soup else True
    all_keywords = [keywords.get('content', '').strip() for keywords in soup.find_all('meta', attrs={'name': 'keywords'})] if soup else []
    keywords_duplicate = len(all_keywords) != len(set(all_keywords))
    keywords_multiple = len(soup.find_all('meta', attrs={'name': 'keywords'})) > 1 if soup else False

    return {
                'Missing': keywords_missing,
                'Duplicate': keywords_duplicate,
                'Multiple': keywords_multiple
           }

def get_h1_issues(soup):
    h1_missing = not soup.find('h1') or not soup.find('h1').text.strip() if soup else False
    all_h1s = [h1.text.strip() for h1 in soup.find_all('h1')] if soup else []
    h1_duplicate = len(all_h1s) != len(set(all_h1s))
    h1_over_70_characters = any(len(h1.text.strip()) > 70 for h1 in soup.find_all('h1')) if soup else False
    h1_multiple = len(soup.find_all('h1')) > 1 if soup else False
    alt_text_in_h1 = bool(soup.find('h1 img[alt]')) if soup else False
    non_sequential_h1 = not soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6']) or soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6'])[0].name != 'h1' if soup else False
    
    return {
        'Missing': h1_missing,
        'Duplicate': h1_duplicate,
        'Over_70_characters': h1_over_70_characters,
        'Multiple': h1_multiple,
        'Alt_Text_in_h1': alt_text_in_h1,
        'Non-sequential': non_sequential_h1
    }

def get_h2_issues(soup):
    h2_missing = not soup.find('h2') or not soup.find('h2').text.strip() if soup else False
    all_h2s = [h2.text.strip() for h2 in soup.find_all('h2')] if soup else []
    h2_duplicate = len(all_h2s) != len(set(all_h2s))
    h2_over_70_characters = any(len(h2.text.strip()) > 70 for h2 in soup.find_all('h2')) if soup else False
    h2_multiple = len(soup.find_all('h2')) > 1 if soup else False
    non_sequential_h2 = False
    h1_exists = soup.find('h1')
    if h1_exists:
        h1_position = soup.find_all(['h1', 'h2']).index(soup.find('h1'))
        h2s_after_h1 = soup.find_all(['h1', 'h2'])[h1_position + 1:]
        non_sequential_h2 = any(tag.name == 'h2' for tag in h2s_after_h1)
    
    return {
        'Missing': h2_missing,
        'Duplicate': h2_duplicate,
        'Over_70_characters': h2_over_70_characters,
        'Multiple': h2_multiple,
        'Non-sequential': non_sequential_h2
    }

def get_directive_issues(soup, response):
    # Get meta robots tag content
    meta_robots_tag = soup.find('meta', attrs={'name': 'robots'})
    meta_robots_content = meta_robots_tag.get('content') if meta_robots_tag else ''
    
    # Get X-Robots-Tag from HTTP header
    x_robots_tag = response.headers.get('X-Robots-Tag', '')

    # Extract individual directives
    directives = {
        'Index': 'index' in meta_robots_content.lower() or 'index' in x_robots_tag.lower(),
        'Noindex': 'noindex' in meta_robots_content.lower() or 'noindex' in x_robots_tag.lower(),
        'Follow': 'follow' in meta_robots_content.lower() or 'follow' in x_robots_tag.lower(),
        'Nofollow': 'nofollow' in meta_robots_content.lower() or 'nofollow' in x_robots_tag.lower(),
        'None': 'none' in meta_robots_content.lower() or 'none' in x_robots_tag.lower(),
        'NoArchive': 'noarchive' in meta_robots_content.lower() or 'noarchive' in x_robots_tag.lower(),
        'NoSnippet': 'nosnippet' in meta_robots_content.lower() or 'nosnippet' in x_robots_tag.lower(),
        'Max-Snippet': 'max-snippet' in meta_robots_content.lower() or 'max-snippet' in x_robots_tag.lower(),
        'Max-Image-Preview': 'max-image-preview' in meta_robots_content.lower() or 'max-image-preview' in x_robots_tag.lower(),
        'Max-Video-Preview': 'max-video-preview' in meta_robots_content.lower() or 'max-video-preview' in x_robots_tag.lower(),
        'NoODP': 'noodp' in meta_robots_content.lower() or 'noodp' in x_robots_tag.lower(),
        'NoYDIR': 'noydir' in meta_robots_content.lower() or 'noydir' in x_robots_tag.lower(),
        'NoImageIndex': 'noimageindex' in meta_robots_content.lower() or 'noimageindex' in x_robots_tag.lower(),
        'NoTranslate': 'notranslate' in meta_robots_content.lower() or 'notranslate' in x_robots_tag.lower(),
        'Unavailable_After': 'unavailable_after' in meta_robots_content.lower() or 'unavailable_after' in x_robots_tag.lower(),
        'Refresh': soup.find('meta', attrs={'http-equiv': 'refresh'}) is not None,
        'Outside_<head>': meta_robots_tag and not meta_robots_tag.find_parent('head')
    }

    return directives

def get_hreflang_issues(soup):
    hreflang_elements = soup.find_all('link', attrs={'rel': 'alternate', 'hreflang': True})
    
    contains_hreflang = bool(hreflang_elements)
    
    non_200_hreflang_urls = []
    unlinked_hreflang_urls = []
    missing_return_links = []
    inconsistent_language_region_return_links = []
    non_canonical_return_links = []
    noindex_return_links = []
    incorrect_language_region_codes = []
    multiple_entries = []
    missing_self_reference = []
    not_using_canonical = []
    missing_x_default = []
    missing = []
    outside_head = []
    
    for hreflang_element in hreflang_elements:
        hreflang_url = hreflang_element.get('href')
        hreflang_status_code = requests.head(hreflang_url).status_code if hreflang_url else None
        
        if hreflang_status_code and hreflang_status_code != 200:
            non_200_hreflang_urls.append(hreflang_url)
        
        if not soup.find('a', href=hreflang_url):
            unlinked_hreflang_urls.append(hreflang_url)
        
        return_hreflang_url = soup.find('link', attrs={'rel': 'alternate', 'href': hreflang_url})
        if return_hreflang_url and not return_hreflang_url.get('hreflang'):
            missing_return_links.append(hreflang_url)
        elif return_hreflang_url and return_hreflang_url.get('hreflang') != hreflang_element.get('hreflang'):
            inconsistent_language_region_return_links.append(hreflang_url)
        
        canonical_href = soup.find('link', rel='canonical').get('href') if soup.find('link', rel='canonical') else None
        if canonical_href and canonical_href != hreflang_url:
            non_canonical_return_links.append(hreflang_url)
        
        if soup.find('meta', attrs={'name': 'robots', 'content': 'noindex'}):
            noindex_return_links.append(hreflang_url)
        
        hreflang_value = hreflang_element.get('hreflang')
        if not hreflang_value or not re.match(r'^[a-z]{2}(-[A-Z]{2})?$', hreflang_value):
            incorrect_language_region_codes.append(hreflang_url)
        
        hreflang_entries = soup.find_all('link', attrs={'rel': 'alternate', 'hreflang': hreflang_value})
        if len(hreflang_entries) > 1:
            multiple_entries.append(hreflang_url)
        
        if not return_hreflang_url:
            missing_self_reference.append(hreflang_url)
        
        if canonical_href and canonical_href != hreflang_element.get('href'):
            not_using_canonical.append(hreflang_url)
        
        if not hreflang_element.find_parent('head'):
            outside_head.append(hreflang_url)
    
    return {
        'Contains_Hreflang': contains_hreflang,
        'Non-200_Hreflang_URLs': non_200_hreflang_urls,
        'Unlinked_Hreflang_URLs': unlinked_hreflang_urls,
        'Missing_Return_Links': missing_return_links,
        'Inconsistent_Language_&_Region_Return_Links': inconsistent_language_region_return_links,
        'Non-Canonical_Return_Links': non_canonical_return_links,
        'Noindex_Return_Links': noindex_return_links,
        'Incorrect_Language_&_Region_Codes': incorrect_language_region_codes,
        'Multiple_Entries': multiple_entries,
        'Missing_Self_Reference': missing_self_reference,
        'Not_Using_Canonical': not_using_canonical,
        'Missing_X-Default': missing_x_default,
        'Missing': missing,
        'Outside_<head>': outside_head
    }

def get_structured_data_issues(soup):
    structured_data = soup.find_all('script', type='application/ld+json')
    
    contains_structured_data = bool(structured_data)
    missing_structured_data = not contains_structured_data
    
    validation_errors = []
    validation_warnings = []
    parse_errors = []
    microdata_urls = []
    json_ld_urls = []
    rdfa_urls = []
    
    for script in structured_data:
        data = script.string.strip()
        
        try:
            structured_data_json = json.loads(data)
        except json.JSONDecodeError:
            parse_errors.append(data)  # Almacenamos el contenido del script en lugar del objeto Tag
            continue
        
        if '@type' in structured_data_json:
            type_value = structured_data_json.get('@type')
            if type_value == 'BreadcrumbList':
                continue  # Ignoramos el tipo de datos estructurados de migas de pan para la validación
                
            if type_value:
                if 'error' in type_value:
                    validation_errors.append(data)  # Almacenamos el contenido del script
                else:
                    validation_warnings.append(data)  # Almacenamos el contenido del script
        
        if 'Microdata' in data:
            microdata_urls.append(data)  # Almacenamos el contenido del script
        elif 'application/ld+json' in script.get('type'):
            json_ld_urls.append(data)  # Almacenamos el contenido del script
        elif 'RDFa' in data:
            rdfa_urls.append(data)  # Almacenamos el contenido del script
    
    return {
        'Contains_Structured_Data': contains_structured_data,
        'Missing_Structured_Data': missing_structured_data,
        'Validation_Errors': validation_errors,
        'Validation_Warnings': validation_warnings,
        'Parse_Errors': parse_errors,
        'Microdata_URLs': microdata_urls,
        'JSON-LD_URLs': json_ld_urls,
        'RDFa_URLs': rdfa_urls
    }

def get_url_details(url, soup):
    status_code = None
    status = None
    content_type = None
    size = None
    
    inlinks = len(soup.find_all('a', href=url))
    outlinks = len(soup.find_all('a'))
    
    try:
        response = requests.head(url)
        status_code = response.status_code
        status = response.reason
        content_type = response.headers.get('Content-Type')
        size = int(response.headers.get('Content-Length', 0))
    except Exception as e:
        pass
    
    return {
        'URL': url,
        'Status_Code': status_code,
        'Status': status,
        'Content': content_type,
        'Size': size,
        'Inlinks': inlinks,
        'Outlinks': outlinks
    }

def validate_html(html_content):
    if isinstance(html_content, bytes):
        html_content = html_content.decode('utf-8')

    soup = BeautifulSoup(html_content, 'html.parser')

    invalid_head_elements = len(soup.find_all(lambda tag: tag.name == 'head' and tag.parent.name != 'html'))
    body_preceding_html = len(soup.find_all(lambda tag: tag.name == 'body' and tag.parent.name != 'html'))
    head_not_first = len(soup.find_all(lambda tag: tag.name == 'head' and tag.parent.contents[0].name != 'html'))
    missing_head_tag = 1 if not soup.find('head') else 0
    multiple_head_tags = len(soup.find_all('head')) - 1 if len(soup.find_all('head')) > 1 else 0
    missing_body_tag = 1 if not soup.find('body') else 0
    multiple_body_tags = len(soup.find_all('body')) - 1 if len(soup.find_all('body')) > 1 else 0

    html_size = len(html_content.encode('utf-8'))
    html_size_mb = html_size / (1024 * 1024)  # Convert bytes to megabytes

    html_over_15mb = 1 if html_size_mb > 15 else 0

    return {
        'Invalid_HTML_Elements_In_<head>': invalid_head_elements,
        'Body_Element_Preceding_<html>': body_preceding_html,
        'Head_Not_First_In_<html>_Element': head_not_first,
        'Missing_<head>_Tag': missing_head_tag,
        'Multiple_<head>_Tags': multiple_head_tags,
        'Missing_<body>_Tag': missing_body_tag,
        'Multiple_<body>_Tags': multiple_body_tags,
        'HTML_Document_Over_15MB': html_over_15mb
    }

# Checks TAD

def check_redirects(url):
    try:
        response = requests.get(url)
        redirects = response.history
        redirect_chain = [resp.url for resp in redirects]
        redirect_chain.append(response.url)
        return redirect_chain
    except requests.RequestException as e:
        return f"Error: {e}"

def check_gzip(url):
    try:
        response = requests.get(url)
        return 'Content-Encoding' in response.headers and ('gzip' in response.headers['Content-Encoding'] or 'br' in response.headers['Content-Encoding'])
    except requests.RequestException as e:
        return f"Error: {e}"

def check_page_size(url):
    try:
        response = requests.get(url)
        return len(response.content)
    except requests.RequestException as e:
        return f"Error: {e}"

def check_deprecated_tags(soup):
    deprecated_tags = ['acronym', 'applet', 'basefont', 'big', 'blink', 'center', 'dir', 'font', 'frame', 'frameset', 'isindex', 'keygen', 'listing', 'marquee', 'menuitem', 'multicol', 'nextid', 'nobr', 'noembed', 'noframes', 'plaintext', 'rb', 'rtc', 'spacer', 'strike', 'tt', 'xmp']
    found_tags = []
    for tag in deprecated_tags:
        if soup.find(tag):
            found_tags.append(tag)
    return found_tags

def check_friendly_url(url):
    return ' ' not in url and url.islower() and '-' in url and '=' not in url

def check_favicon(soup):
    icon_link = soup.find("link", rel="icon")
    if icon_link and icon_link.get('href'):
        return True
    return False

def check_www_redirect(url):
    try:
        response = requests.get(url, allow_redirects=False)
        www_url = url.replace('://', '://www.')
        if response.status_code == 301 or response.status_code == 302:
            return response.headers['Location'] == www_url
        else:
            response_www = requests.get(www_url, allow_redirects=False)
            return response.status_code == 200 and response_www.status_code == 200
    except requests.RequestException as e:
        return f"Error: {e}"



def check_lazy_loading(soup):
    lazy_images = soup.find_all('img', loading='lazy')
    return len(lazy_images) > 0

def check_google_search_display(soup):
    title = soup.title.string if soup.title else ''
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    description = meta_desc['content'] if meta_desc else ''
    return {
        'Title': title,
        'Title Length': len(title),
        'Description': description,
        'Description Length': len(description)
    }

def check_responsive_images(soup):
    images = soup.find_all('img')
    large_images = [img['src'] for img in images if 'width' in img.attrs and int(img['width']) > 1000]
    return large_images

def check_http_to_https_redirect(url):
    if url.startswith('http://'):
        https_url = url.replace('http://', 'https://')
        try:
            response = requests.get(url, allow_redirects=True)
            return response.url.startswith(https_url)
        except requests.RequestException as e:
            return f"Error: {e}"
    return False

##########
############# SECURITY RANK ##############
##########

def check_ssl_expiry(url):
    try:
        hostname = url.split("//")[-1].split("/")[0]
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
        conn.connect((hostname, 443))
        ssl_info = conn.getpeercert()
        expiry_date = datetime.datetime.strptime(ssl_info['notAfter'], '%b %d %H:%M:%S %Y %Z')
        days_to_expire = (expiry_date - datetime.datetime.utcnow()).days
        return days_to_expire
    except Exception as e:
        return f"Error: {e}"

def check_outdated_ssl_tls(response):
    try:
        if response.raw.version == 10:  # HTTP/1.0
            return True
        return False
    except requests.RequestException as e:
        return f"Error: {e}"

def check_certificate_name(url):
    try:
        hostname = url.split("//")[-1].split("/")[0]
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
        conn.connect((hostname, 443))
        ssl_info = conn.getpeercert()
        common_name = dict(x[0] for x in ssl_info['subject'])['commonName']
        return common_name == hostname
    except Exception as e:
        return f"Error: {e}"

def check_deprecated_encryption(url):
    try:
        context = ssl.create_default_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=url)
        conn.connect((url, 443))
        ssl_info = conn.cipher()
        return 'SHA1' in ssl_info or 'MD5' in ssl_info
    except Exception as e:
        return f"Error: {e}"

def check_http_in_sitemap(sitemap_url,soup):
    try:
        urls = soup.find_all('loc')
        http_urls = [url.text for url in urls if url.text.startswith('http://')]
        return http_urls
    except requests.RequestException as e:
        return f"Error: {e}"

def check_canonical_https_to_http(url, soup):
    try:
        canonical = soup.find('link', rel='canonical')
        if canonical and canonical['href'].startswith('http://'):
            return True
        return False
    except requests.RequestException as e:
        return f"Error: {e}"

def check_https_to_http_redirect(url):
    if url.startswith('https://'):
        http_url = url.replace('https://', 'http://')
        try:
            response = requests.get(url, allow_redirects=False)
            return response.headers.get('Location') == http_url
        except requests.RequestException as e:
            return f"Error: {e}"
    return False

def check_mixed_content(response):
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        mixed_content_elements = [tag['src'] for tag in soup.find_all(['img', 'script', 'link']) if 'src' in tag.attrs and tag['src'].startswith('http://')]
        return mixed_content_elements
    except requests.RequestException as e:
        return f"Error: {e}"


##########
####### CRAWLING AUDIT
##########

def check_large_xml_sitemap(sitemap_url_response):
    try:
        response = sitemap_url_response
        if response.headers.get('Content-Length') and int(response.headers['Content-Length']) > 52428800:
            return True
        tree = ET.ElementTree(ET.fromstring(response.content))
        url_count = len(tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'))
        return url_count > 50000
    except requests.RequestException as e:
        return f"Error: {e}"

def check_non_canonical_pages_in_sitemap(sitemap_url_response):
    try:
        response = sitemap_url_response
        tree = ET.ElementTree(ET.fromstring(response.content))
        urls = [elem.text for elem in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        non_canonical = []
        for url in urls:
            page_response = requests.get(url)
            soup = BeautifulSoup(page_response.content, 'html.parser')
            canonical = soup.find('link', rel='canonical')
            if canonical and canonical['href'] != url:
                non_canonical.append(url)
        return non_canonical
    except requests.RequestException as e:
        return f"Error: {e}"

def check_noindex_pages_in_sitemap(sitemap_url):
    try:
        response = requests.get(sitemap_url)
        tree = ET.ElementTree(ET.fromstring(response.content))
        urls = [elem.text for elem in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        noindex_pages = []
        for url in urls:
            page_response = requests.get(url)
            soup = BeautifulSoup(page_response.content, 'html.parser')
            meta_robots = soup.find('meta', attrs={'name': 'robots'})
            if meta_robots and 'noindex' in meta_robots['content']:
                noindex_pages.append(url)
        return noindex_pages
    except requests.RequestException as e:
        return f"Error: {e}"

def check_missing_xml_sitemap(sitemap_url):
    try:
        response = requests.head(sitemap_url)
        return response.status_code != 200
    except requests.RequestException as e:
        return f"Error: {e}"

def check_sitemap_in_robots_txt(robots_url, sitemap_url):
    try:
        response = requests.get(robots_url)
        return f'Sitemap: {sitemap_url}' in response.text
    except requests.RequestException as e:
        return f"Error: {e}"

def check_robots_txt_exists(robots_url):
    try:
        response = requests.head(robots_url)
        return response.status_code == 200
    except requests.RequestException as e:
        return f"Error: {e}"

def check_frame_tag(response):
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        return bool(soup.find('frame'))
    except requests.RequestException as e:
        return f"Error: {e}"

def check_long_url(url):
    return len(url) > 75

def check_noindex_in_html_and_http(response):
    try:

        soup = BeautifulSoup(response.content, 'html.parser')
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        header_robots = response.headers.get('X-Robots-Tag')
        if meta_robots and 'noindex' in meta_robots['content'] and header_robots and 'noindex' in header_robots:
            return True
        return False
    except requests.RequestException as e:
        return f"Error: {e}"

def check_nofollow_in_html_and_http(response):
    try:

        soup = BeautifulSoup(response.content, 'html.parser')
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        header_robots = response.headers.get('X-Robots-Tag')
        if meta_robots and 'nofollow' in meta_robots['content'] and header_robots and 'nofollow' in header_robots:
            return True
        return False
    except requests.RequestException as e:
        return f"Error: {e}"

def check_canonical_chain(url, response):
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        canonical = soup.find('link', rel='canonical')
        if canonical and canonical['href'] != url:
            next_url = canonical['href']
            next_response = requests.get(next_url)
            next_soup = BeautifulSoup(next_response.content, 'html.parser')
            next_canonical = next_soup.find('link', rel='canonical')
            if next_canonical and next_canonical['href'] != next_url:
                return True
        return False
    except requests.RequestException as e:
        return f"Error: {e}"

def check_blocked_by_robots_txt(url):
    try:
        #response = requests.get(url)
        robots_url = f"{url.split('//')[0]}//{url.split('//')[1].split('/')[0]}/robots.txt"
        robots_response = requests.get(robots_url)
        if 'Disallow' in robots_response.text:
            disallow_paths = [line.split(' ')[1] for line in robots_response.text.split('\n') if line.startswith('Disallow')]
            for path in disallow_paths:
                if path in url:
                    return True
        return False
    except requests.RequestException as e:
        return f"Error: {e}"

def check_blocked_by_noindex(response):
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        return meta_robots and 'noindex' in meta_robots['content']
    except requests.RequestException as e:
        return f"Error: {e}"

def check_blocked_by_nofollow(response):
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        return meta_robots and 'nofollow' in meta_robots['content']
    except requests.RequestException as e:
        return f"Error: {e}"

def check_blocked_by_x_robots_tag(response):
    try:

        header_robots = response.headers.get('X-Robots-Tag')
        return header_robots and ('noindex' in header_robots or 'nofollow' in header_robots)
    except requests.RequestException as e:
        return f"Error: {e}"

def check_canonical_http_to_https(url, response):
    try:
       
        soup = BeautifulSoup(response.content, 'html.parser')
        canonical = soup.find('link', rel='canonical')
        return canonical and canonical['href'].startswith('https://') and url.startswith('http://')
    except requests.RequestException as e:
        return f"Error: {e}"

def check_timed_out(url):
    try:
        response = requests.get(url, timeout=15)
        return False
    except requests.Timeout:
        return True
    except requests.RequestException as e:
        return f"Error: {e}"



#########
###### DUPLICATE CONTENT
############

def check_no_www_redirect(url):
    try:
        response_with_www = requests.get(url.replace('://', '://www.'))
        response_without_www = requests.get(url.replace('://www.', '://'))
        return response_with_www.url == response_without_www.url
    except requests.RequestException as e:
        return f"Error: {e}"

def check_multiple_canonical(response):
    try:

        soup = BeautifulSoup(response.content, 'html.parser')
        canonicals = soup.find_all('link', rel='canonical')
        return len(canonicals) > 1 and len(set([canonical['href'] for canonical in canonicals])) > 1
    except requests.RequestException as e:
        return f"Error: {e}"

def check_duplicate_content(response):
    try:

        soup = BeautifulSoup(response.content, 'html.parser')
        page_content = soup.get_text()
        # Placeholder for checking duplicate content against other pages
        return False
    except requests.RequestException as e:
        return f"Error: {e}"

def check_double_slash(response):
    try:

        return '//' in response.url.replace('://', '').replace('www.', '')
    except requests.RequestException as e:
        return f"Error: {e}"

def check_trailing_slash(url):
    try:
        response_with_slash = requests.get(url if url.endswith('/') else url + '/')
        response_without_slash = requests.get(url.rstrip('/'))
        return response_with_slash.url != response_without_slash.url
    except requests.RequestException as e:
        return f"Error: {e}"


#########
## HTTP STATUS CODE
#######

def check_status_code(url):
    try:
        response = requests.get(url)
        return response.status_code
    except requests.RequestException as e:
        return f"Error: {e}"

def check_xml_sitemap_status(sitemap_url_response):
    try:
        response = sitemap_url_response
        soup = BeautifulSoup(response.content, 'xml')
        urls = [loc.text for loc in soup.find_all('loc')]
        status_codes = {url: check_status_code(url) for url in urls}
        issues = {
            '4XX': [url for url, code in status_codes.items() if str(code).startswith('4')],
            '3XX': [url for url, code in status_codes.items() if str(code).startswith('3')],
            '5XX': [url for url, code in status_codes.items() if str(code).startswith('5')]
        }
        return issues
    except requests.RequestException as e:
        return f"Error: {e}"

def check_internal_links_status(response):
    try:
        #response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        status_codes = {link: check_status_code(link) for link in links}
        issues = {
            '3XX': [link for link, code in status_codes.items() if str(code).startswith('3')],
            '4XX': [link for link, code in status_codes.items() if str(code).startswith('4')],
            '5XX': [link for link, code in status_codes.items() if str(code).startswith('5')]
        }
        return issues
    except requests.RequestException as e:
        return f"Error: {e}"

def check_external_links_status(url, response):
    try:
        #response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True) if url not in a['href']]
        status_codes = {link: check_status_code(link) for link in links}
        issues = {
            '3XX': [link for link, code in status_codes.items() if str(code).startswith('3')],
            '4XX': [link for link, code in status_codes.items() if str(code).startswith('4')],
            '5XX': [link for link, code in status_codes.items() if str(code).startswith('5')]
        }
        return issues
    except requests.RequestException as e:
        return f"Error: {e}"

def check_hreflang_status(response):
    try:
        #response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        hreflangs = [link['href'] for link in soup.find_all('link', rel='alternate')]
        status_codes = {hreflang: check_status_code(hreflang) for hreflang in hreflangs}
        issues = {
            '3XX': [hreflang for hreflang, code in status_codes.items() if str(code).startswith('3')],
            '4XX': [hreflang for hreflang, code in status_codes.items() if str(code).startswith('4')],
            '5XX': [hreflang for hreflang, code in status_codes.items() if str(code).startswith('5')]
        }
        return issues
    except requests.RequestException as e:
        return f"Error: {e}"

def check_images_status(response):
    try:
        #response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        images = [img['src'] for img in soup.find_all('img', src=True)]
        status_codes = {img: check_status_code(img) for img in images}
        issues = {
            '3XX': [img for img, code in status_codes.items() if str(code).startswith('3')],
            '4XX': [img for img, code in status_codes.items() if str(code).startswith('4')],
            '5XX': [img for img, code in status_codes.items() if str(code).startswith('5')]
        }
        return issues
    except requests.RequestException as e:
        return f"Error: {e}"

def check_javascript_status(response):
    try:
        #response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        scripts = [script['src'] for script in soup.find_all('script', src=True)]
        status_codes = {script: check_status_code(script) for script in scripts}
        issues = {
            '3XX': [script for script, code in status_codes.items() if str(code).startswith('3')],
            '4XX': [script for script, code in status_codes.items() if str(code).startswith('4')],
            '5XX': [script for script, code in status_codes.items() if str(code).startswith('5')]
        }
        return issues
    except requests.RequestException as e:
        return f"Error: {e}"

def check_css_status(response):
    try:
        #response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        stylesheets = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
        status_codes = {stylesheet: check_status_code(stylesheet) for stylesheet in stylesheets}
        issues = {
            '3XX': [stylesheet for stylesheet, code in status_codes.items() if str(code).startswith('3')],
            '4XX': [stylesheet for stylesheet, code in status_codes.items() if str(code).startswith('4')],
            '5XX': [stylesheet for stylesheet, code in status_codes.items() if str(code).startswith('5')]
        }
        return issues
    except requests.RequestException as e:
        return f"Error: {e}"



## no se usa
def __get_url_details(url_info):

    url_info = {
                #'Address': url,
                #'Content': response.headers.get('Content-Type', ''),
                #'Status Code': response.status_code,
                #'Status': response.reason,
                #'Size': len(response.content)
            }
    url_details = {
        'Address': url_info.get('url'),
        'Content': url_info.get('Content', ''),
        'Status_Code': url_info.get('Status Code', ''),
        'Status': url_info.get('Status', ''),
        'Indexability': url_info.get('Indexability', ''),
        'Indexability_Status': url_info.get('Indexability Status', ''),
        'Title_1': url_info.get('Title 1', ''),
        'Title_1_Length': url_info.get('Title 1 Length', 0),
        'Title_1_Pixel_Width': url_info.get('Title 1 Pixel Width', 0),
        'Meta Description_1': url_info.get('Meta Description 1', ''),
        'Meta Description_Length_1': url_info.get('Meta Description Length 1', 0),
        'Meta Description_Pixel_Width': url_info.get('Meta Description Pixel Width', 0),
        'Meta Keyword_1': url_info.get('Meta Keyword 1', ''),
        'Meta Keywords_Length': url_info.get('Meta Keywords Length', 0),
        'h1_-_1': url_info.get('h1 - 1', ''),
        'h1_-_Len-1': url_info.get('h1 - Len-1', 0),
        'h2_-_1': url_info.get('h2 - 1', ''),
        'h2_-_Len-1': url_info.get('h2 - Len-1', 0),
        'Meta_Robots_1': url_info.get('Meta Robots 1', ''),
        'X-Robots-Tag_1': url_info.get('X-Robots-Tag 1', ''),
        'Meta_Refresh_1': url_info.get('Meta Refresh 1', ''),
        'Canonical_Link_Element': url_info.get('Canonical Link Element', ''),
        'rel="next"_1': url_info.get('rel="next" 1', ''),
        'rel="prev"_1': url_info.get('rel="prev" 1', ''),
        'HTTP_rel="next"_1': url_info.get('HTTP rel="next" 1', ''),
        'HTTP_rel="prev"_1': url_info.get('HTTP rel="prev" 1', ''),
        'Size': url_info.get('Size', 0),
        'Transferred': url_info.get('Transferred', 0),
        'Word_Count': url_info.get('Word Count', 0),
        'Text_Ratio': url_info.get('Text Ratio', 0),
        'Crawl_Depth': url_info.get('Crawl Depth', 0),
        'Folder_Depth': url_info.get('Folder Depth', 0),
        'Link_Score': url_info.get('Link Score', 0),
        'Inlinks': url_info.get('Inlinks', 0),
        'Unique_Inlinks': url_info.get('Unique Inlinks', 0),
        'Unique_JS_Inlinks': url_info.get('Unique JS Inlinks', 0),
        '%_of_Total': url_info.get('% of Total', 0),
        'Outlinks': url_info.get('Outlinks', 0),
        'Unique_Outlinks': url_info.get('Unique Outlinks', 0),
        'Unique_JS_Outlinks': url_info.get('Unique JS Outlinks', 0),
        'External_Outlinks': url_info.get('External Outlinks', 0),
        'Unique_External_Outlinks': url_info.get('Unique External Outlinks', 0),
        'Unique_External_JS_Outlinks': url_info.get('Unique External JS Outlinks', 0),
        'Closest_Similarity_Match': url_info.get('Closest Similarity Match', ''),
        'No._Near_Duplicates': url_info.get('No. Near Duplicates', 0),
        'Spelling_Errors': url_info.get('Spelling Errors', 0),
        'Grammar_Errors': url_info.get('Grammar Errors', 0),
        'Language': url_info.get('Language', ''),
        'Hash': url_info.get('Hash', ''),
        'Response Time': url_info.get('Response Time', ''),
        'Last-Modified': url_info.get('Last-Modified', ''),
        'Redirect_URI': url_info.get('Redirect URI', ''),
        'Redirect_Type': url_info.get('Redirect Type', ''),
        'HTTP_Version': url_info.get('HTTP Version', ''),
        'URL_Encoded Address': url_info.get('URL Encoded Address', ''),
        'Title_2': url_info.get('Title 2', ''),
        'Meta_Description 2': url_info.get('Meta Description 2', ''),
        'h1-2': url_info.get('h1-2', ''),
        'h2-2': url_info.get('h2-2', '')
    }

    return url_details

#
def get_page_info(url):
    
    soup = get_soup(url)
    if soup:
        try:
            response = requests.get(url) 
            page_info = {
                
                'Canonical_Info': get_canonical_info(soup, url, response),
                'Security_Info': get_security_info(url, response, soup),
                'Common_URL_Issues': get_common_url_issues(url),
                'Page_Title_Issues': get_page_title_issues(soup),
                'Meta_Description_Issues': get_meta_description_issues(soup),
                'Meta_Keywords_Issues': get_meta_keywords_issues(soup),
                'H1_Issues': get_h1_issues(soup),
                'H2_Issues': get_h2_issues(soup),
                'Directives_Issues': get_directive_issues(soup,response),
                'HFLang_Ref_Issues' : get_hreflang_issues(soup),
                'Schema_ORG_Issues' : get_structured_data_issues(soup),
                'Header_info' : get_header_info(url),
                'Validation_Issues': validate_html(response.content),
                'Mobile_audit_Results' : mobile_tools.audit_mobile_usability(url, soup),
                
                # probar velocidad con buscar en diccionario # temporal
                'Internal_Details' : #get_url_details(url_info),  # Corregido aquí 
                    {
                        'Header_Name': response.headers.get('Name', ''),
                        'Header_Value': response.headers.get('Value', ''),
                        'URL': url,
                        'Status_Code': response.status_code,
                        'Status': response.reason,
                        'Content': response.headers.get('Content-Type', ''),
                        'Size': len(response.content),
                        'Transferred': response.headers.get('Content-Length', ''),
                        'Title_1': soup.find('title').text if soup.find('title') else '', ##
                        'Title_1_Length': len(soup.find('title').text) if soup.find('title') else 0, ##
                        'h1_-_1': soup.find('h1').text if soup.find('h1') else '',
                        'h1_-_Len-1': len(soup.find('h1').text) if soup.find('h1') else 0,
                        'h2_-_1': soup.find('h2').text if soup.find('h2') else '',
                        'h2_-_Len-1': len(soup.find('h2').text) if soup.find('h2') else 0,
                        'Meta_Description_1': soup.find('meta', attrs={'name': 'description'}).get('content', '') if soup.find('meta', attrs={'name': 'description'}) else '',
                        'Meta_Description_Length_1': len(soup.find('meta', attrs={'name': 'description'}).get('content', '')) if soup.find('meta', attrs={'name': 'description'}) else 0,
                        'Meta_Description_Pixel_Width': 0,  # Aquí necesitarías calcular la anchura en píxeles
                        'Meta_Keyword_1': soup.find('meta', attrs={'name': 'keywords'}).get('content', '') if soup.find('meta', attrs={'name': 'keywords'}) else '',
                        'Meta_Keywords_Length': len(soup.find('meta', attrs={'name': 'keywords'}).get('content', '')) if soup.find('meta', attrs={'name': 'keywords'}) else 0,
                        'Meta_Robots_1': soup.find('meta', attrs={'name': 'robots'}).get('content', '') if soup.find('meta', attrs={'name': 'robots'}) else '',
                        'X-Robots-Tag_1': response.headers.get('X-Robots-Tag', ''),
                        'Meta_Refresh_1': soup.find('meta', attrs={'http-equiv': 'refresh'}).get('content', '') if soup.find('meta', attrs={'http-equiv': 'refresh'}) else '',
                        'Canonical_Link_Element': soup.find('link', attrs={'rel': 'canonical'}).get('href', '') if soup.find('link', attrs={'rel': 'canonical'}) else '',
                        'rel="next"_1': soup.find('link', attrs={'rel': 'next'}).get('href', '') if soup.find('link', attrs={'rel': 'next'}) else '',
                        'rel="prev"_1': soup.find('link', attrs={'rel': 'prev'}).get('href', '') if soup.find('link', attrs={'rel': 'prev'}) else '',
                        'HTTP_rel="next"_1': response.headers.get('Link', '').split(';')[0].strip('<>') if response.headers.get('Link') else '',
                        'HTTP_rel="prev"_1': response.headers.get('Link', '').split(';')[0].strip('<>') if response.headers.get('Link') else '',
                        'Word_Count': len(soup.text.split()),
                        'Response_Time': response.elapsed.total_seconds() if response.elapsed else 0,
                        'h2_Occurrences': len(soup.find_all('h2')),
                        'h2-1': soup.find('h2').text if soup.find('h2') else '',
                        'h2-1_length': len(soup.find('h2').text) if soup.find('h2') else 0,
                        'h1_Occurrences': len(soup.find_all('h1')),
                        'h1-1': soup.find('h1').text if soup.find('h1') else '',
                        'h1-1_length': len(soup.find('h1').text) if soup.find('h1') else 0,
                        'meat_keywords_Occurrences': len(soup.find_all('meta', attrs={'name': 'keywords'})),
                        'Meta_Keyword_2': soup.find_all('meta', attrs={'name': 'keywords'})[1].get('content', '') if len(soup.find_all('meta', attrs={'name': 'keywords'})) > 1 else '',
                        'Meta_Keyword_2_length': len(soup.find_all('meta', attrs={'name': 'keywords'})) > 1 and len(soup.find_all('meta', attrs={'name': 'keywords'}))[1].get('content', '') or 0,
                        'Description_Occurrences': len(soup.find_all('meta', attrs={'name': 'description'})),
                        'Meta_Description_2': soup.find_all('meta', attrs={'name': 'description'})[1].get('content', '') if len(soup.find_all('meta', attrs={'name': 'description'})) > 1 else '',
                        'Meta_Description_2_length': len(soup.find_all('meta', attrs={'name': 'description'}))[1].get('content', '') if len(soup.find_all('meta', attrs={'name': 'description'})) > 1 else 0,
                        'title_Occurrences': len(soup.find_all('title')),
                        'Title_2': soup.find_all('title')[1].text if len(soup.find_all('title')) > 1 else '',
                        'Title_2_length': len(soup.find_all('title')[1].text) if len(soup.find_all('title')) > 1 else 0,
                        'URL_Length': len(url),
                        'Last-Modified': response.headers.get('Last-Modified', ''),
                        'Address': url,
                    },
                    
                # modulos con pestaña en menu
                'Images_Issues' : audit_image_details(url,soup),

                # ultimos checks añadidos
                'Redirect Chain': check_redirects(url),
                'Gzip Compression': check_gzip(url),
                'Page Size': check_page_size(url),
                'Deprecated HTML Tags': check_deprecated_tags(soup),
                'Friendly URL': check_friendly_url(url),
                'Favicon Implemented':  check_favicon(soup),
                'WWW Redirect': check_www_redirect(url),
                'Lazy Loading Images': check_lazy_loading(soup),
                'Google Search Display': check_google_search_display(soup),
                #'Responsive Images': check_responsive_images(soup),
                'HTTP to HTTPS Redirect': check_http_to_https_redirect(url),
            

                # security rank
                'Days to SSL Expiry': check_ssl_expiry(url),
                'Outdated SSL/TLS': check_outdated_ssl_tls(response),
                'Certificate Name Match':  check_certificate_name(url),
                'Deprecated Encryption Algorithm': check_deprecated_encryption(url),
                #'HTTP URLs in Sitemap': check_http_in_sitemap(sitemap_url,soup) if sitemap_url else None,
                'Canonical HTTPS to HTTP': check_canonical_https_to_http(url,soup),
                'HTTPS to HTTP Redirect': check_https_to_http_redirect(url),
                'Mixed Content': check_mixed_content(response),

                # crawling
                #'Large Sitemap': check_large_xml_sitemap(sitemap_url_response) if sitemap_url else None,
                #'Non-Canonical Pages in Sitemap': check_non_canonical_pages_in_sitemap(sitemap_url) if sitemap_url else None,
                #'Noindex Pages in Sitemap': check_noindex_pages_in_sitemap(sitemap_url) if sitemap_url else None,
                #'Missing Sitemap': check_missing_xml_sitemap(sitemap_url) if sitemap_url else None,
                #'Sitemap in Robots.txt': check_sitemap_in_robots_txt(robots_url, sitemap_url) if robots_url and sitemap_url else None,
                #'Robots.txt Exists': check_robots_txt_exists(robots_url) if robots_url else None,
                'Frame Tag': check_frame_tag(response),
                'Long URL': check_long_url(url),
                'Noindex in HTML and HTTP': check_noindex_in_html_and_http(response),
                'Nofollow in HTML and HTTP': check_nofollow_in_html_and_http(response),
                'Canonical Chain': check_canonical_chain(url,response),
                'Blocked by Robots.txt': check_blocked_by_robots_txt(url),
                'Blocked by Noindex': check_blocked_by_noindex(response),
                'Blocked by Nofollow': check_blocked_by_nofollow(response),
                'Blocked by X-Robots-Tag': check_blocked_by_x_robots_tag(response),
                'Canonical HTTP to HTTPS': check_canonical_http_to_https(url, response),
                'Timed Out': check_timed_out(url),


                #### DUPLICATE CONTENT
                'No WWW Redirect': check_no_www_redirect(url),
                'Multiple Canonical Tags': check_multiple_canonical(response),
                'Duplicate Content':check_duplicate_content(response),
                'URLs with Double Slash':  check_double_slash(response),
                'No Trailing Slash':check_trailing_slash(url),
        
                #### HTTP STATUS ISSUES
      
                #'Sitemap Issues':  check_xml_sitemap_status(sitemap_url_response),
                #'Internal Links Issues': check_internal_links_status(response),
                #'External Links Issues': check_external_links_status(url, response),
                #'Hreflang Issues': check_hreflang_status(response),
                #'Images Issues': check_images_status(response),
                #'JavaScript Issues': check_javascript_status(response),
                'CSS Issues': check_css_status(response)

            }

            
            spelling_errors, grammar_errors = analizar_ortografia(response.text)

            
            validator = json.loads(ejecutar_pa11y(url))

            
            #print(json.dumps(page_info))
            return page_info, validator, spelling_errors, grammar_errors
        
        except Exception as e:
            print(f"Error processing page info: {e}")
            return {'error': str(e)}
    else:
        return {'error': 'Unable to parse HTML'}




