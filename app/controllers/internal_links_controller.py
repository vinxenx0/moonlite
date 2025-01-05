import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


def extract_internal_links(url, domain):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        internal_links = []
        for link in soup.find_all("a", href=True):
            href = link.get("href")
            if href and domain in href:
                anchor_text = link.get_text(strip=True)
                rel = link.get("rel")
                internal_links.append({
                    'url': href,
                    'anchor_text': anchor_text,
                    'nofollow': 'nofollow' in (rel or []),
                })

        return internal_links
    except RequestException as e:
        return {'Error': str(e)}
    except Exception as e:
        return {'Error': str(e)}


def analyze_internal_links(links):
    no_anchor = []
    nofollow_links = []
    one_inbound_links = {}
    page_links_count = {}

    for link in links:
        if not link['anchor_text']:
            no_anchor.append(link['url'])
        elif link['anchor_text'].strip() == '':
            no_anchor.append(link['url'])
        elif link['anchor_text'].startswith(('http://', 'https://')):
            no_anchor.append(link['url'])
        elif all(char in '!@#$%^&*()_+=-[]{}|;:",.<>?/`~'
                 for char in link['anchor_text']):
            no_anchor.append(link['url'])

        if link['nofollow']:
            nofollow_links.append(link['url'])

        if link['url'] in page_links_count:
            page_links_count[link['url']] += 1
        else:
            page_links_count[link['url']] = 1

    one_inbound_links = [
        url for url, count in page_links_count.items() if count == 1
    ]
    too_many_links = [
        url for url, count in page_links_count.items() if count > 400
    ]

    return {
        'no_anchor': no_anchor,
        'nofollow_links': nofollow_links,
        'one_inbound_links': one_inbound_links,
        'too_many_links': too_many_links
    }


def inbound_links_audit(url):
    try:
        domain = url.split("//")[-1].split("/")[0]
        internal_links = extract_internal_links(url, domain)
        if isinstance(internal_links, dict) and 'Error' in internal_links:
            return internal_links

        if not internal_links:
            return {'Inbound Links Issues': 'No internal links found.'}

        analysis = analyze_internal_links(internal_links)
        issues = []
        if analysis['no_anchor']:
            issues.append(
                f'Internal links missing anchor: {analysis["no_anchor"]}')
        if analysis['nofollow_links']:
            issues.append(
                f'Nofollow internal links: {analysis["nofollow_links"]}')
        if analysis['one_inbound_links']:
            issues.append(
                f'One inbound internal link: {analysis["one_inbound_links"]}')
        if analysis['too_many_links']:
            issues.append(f'Too many links: {analysis["too_many_links"]}')

        return {
            'Inbound Links Issues': issues
        } if issues else {
            'Inbound Links Issues': 'No issues found'
        }
    except Exception as e:
        return {'Error': str(e)}


# Ejemplo de uso
url_to_audit = 'https://www.example.com'
result = inbound_links_audit(url_to_audit)
print(result)
