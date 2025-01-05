import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, Timeout


def extract_external_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        external_links = []
        for link in soup.find_all("a", href=True):
            href = link.get("href")
            if href and href.startswith("http"):
                anchor_text = link.get_text(strip=True)
                rel = link.get("rel")
                external_links.append({
                    'url': href,
                    'anchor_text': anchor_text,
                    'nofollow': 'nofollow' in (rel or []),
                })

        return external_links
    except RequestException as e:
        return {'Error': str(e)}
    except Exception as e:
        return {'Error': str(e)}


def analyze_external_link(link):
    try:
        response = requests.get(link['url'], timeout=15)
        response.raise_for_status()
        link['status'] = 'Active'
    except Timeout:
        link['status'] = 'Timed out'
    except RequestException:
        link['status'] = 'Error'
    return link


def external_links_audit(url):
    try:
        external_links = extract_external_links(url)
        if isinstance(external_links, dict) and 'Error' in external_links:
            return external_links

        if not external_links:
            return {'External Links Issues': 'No external links found.'}

        issues = []
        for link in external_links:
            if not link['anchor_text']:
                issues.append(f'External link missing anchor: {link["url"]}')
            elif link['anchor_text'].strip() == '':
                issues.append(
                    f'External link with empty anchor: {link["url"]}')
            elif link['anchor_text'].startswith(('http://', 'https://')):
                issues.append(
                    f'External link with naked URL anchor: {link["url"]}')
            elif all(char in '!@#$%^&*()_+=-[]{}|;:",.<>?/`~'
                     for char in link['anchor_text']):
                issues.append(
                    f'External link with anchor containing only symbols: {link["url"]}'
                )

            if link['nofollow']:
                issues.append(f'Nofollow external link: {link["url"]}')

            link_analysis = analyze_external_link(link)
            if link_analysis['status'] == 'Timed out':
                issues.append(f'External link timed out: {link["url"]}')

        return {
            'External Links Issues': issues
        } if issues else {
            'External Links Issues': 'No issues found'
        }
    except Exception as e:
        return {'Error': str(e)}


# Ejemplo de uso
url_to_audit = 'https://www.example.com'
result = external_links_audit(url_to_audit)
print(result)
