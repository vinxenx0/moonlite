import requests
from bs4 import BeautifulSoup


def extract_hreflang_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        hreflang_links = []
        for link in soup.find_all("link", {"rel": "alternate"}):
            hreflang = link.get("hreflang")
            href = link.get("href")
            if hreflang and href:
                hreflang_links.append((hreflang, href))

        html_lang = soup.find("html").get("lang")

        return hreflang_links, html_lang
    except requests.RequestException as e:
        return {'Error': str(e)}, None
    except Exception as e:
        return {'Error': str(e)}, None


def validate_hreflang(hreflang_links, html_lang):
    issues = []

    if not hreflang_links:
        issues.append('No hreflang attributes found.')
        return issues

    # Check for invalid language codes in hreflang attributes
    valid_langs = set([
        'en', 'es', 'de', 'fr', 'it', 'nl', 'ja', 'pt', 'ru', 'zh', 'ar', 'ko',
        'x-default'
    ])  # Simplified example
    for hreflang, href in hreflang_links:
        if hreflang not in valid_langs:
            issues.append(
                f'Invalid language code in hreflang attribute: {hreflang}')

    # Check if hreflang page links out to itself
    for hreflang, href in hreflang_links:
        if not any(
            (hl == hreflang and hr == href) for hl, hr in hreflang_links):
            issues.append(f'Hreflang page {href} does not link out to itself.')

    # Check if hreflang points to non-canonical
    # This example assumes that the canonical URL is the same as the href (for simplicity)
    for hreflang, href in hreflang_links:
        if not href.endswith('/canonical'):  # Simplified check
            issues.append(
                f'Hreflang {href} points to a non-canonical version.')

    # Check if hreflang and HTML lang do not match
    for hreflang, href in hreflang_links:
        if hreflang != html_lang:
            issues.append(
                f'Hreflang and HTML lang do not match: hreflang={hreflang}, html lang={html_lang}'
            )

    # Check for confirmation (return) links missing on hreflang pages
    for hreflang, href in hreflang_links:
        if not any(
            (hl == html_lang and hr == url) for hl, hr in hreflang_links):
            issues.append(
                f'Confirmation link missing for hreflang={hreflang} on page {href}'
            )

    # Check for multiple language codes for one page
    lang_codes = [hreflang for hreflang, href in hreflang_links]
    if len(lang_codes) != len(set(lang_codes)):
        issues.append('Multiple language codes specified for a single URL.')

    # Check for invalid HTML lang
    if html_lang not in valid_langs:
        issues.append(f'Invalid HTML lang attribute: {html_lang}')

    # Check for language duplicates in hreflang
    hreflang_dict = {}
    for hreflang, href in hreflang_links:
        if hreflang in hreflang_dict:
            issues.append(
                f'Language duplicate in hreflang attribute: {hreflang}')
        hreflang_dict[hreflang] = href

    # Check for missing HTML lang
    if not html_lang:
        issues.append('HTML lang attribute is missing.')

    # Check for missing x-default hreflang attribute
    if 'x-default' not in lang_codes:
        issues.append('x-default hreflang attribute is missing.')

    return issues


def localization_audit_url(url):
    try:
        hreflang_links, html_lang = extract_hreflang_data(url)
        if isinstance(hreflang_links, dict) and 'Error' in hreflang_links:
            return hreflang_links

        issues = validate_hreflang(hreflang_links, html_lang)
        return {
            'Localization Issues': issues
        } if issues else {
            'Localization Issues': 'No issues found'
        }
    except Exception as e:
        return {'Error': str(e)}


# Ejemplo de uso
url_to_audit = 'https://www.example.com'
result = localization_audit_url(url_to_audit)
print(result)
