import requests
from bs4 import BeautifulSoup
import cssutils
from requests.exceptions import RequestException

def extract_css_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        css_links = []
        for link in soup.find_all("link", {"rel": "stylesheet"}):
            href = link.get("href")
            if href:
                if not href.startswith("http"):
                    href = requests.compat.urljoin(url, href)
                css_links.append(href)

        return css_links
    except RequestException as e:
        return {'Error': str(e)}
    except Exception as e:
        return {'Error': str(e)}

def analyze_css_file(css_url):
    try:
        response = requests.get(css_url)
        response.raise_for_status()

        css_size = len(response.content)
        is_compressed = 'gzip' in response.headers.get('Content-Encoding', '')

        cache_control = response.headers.get('Cache-Control', '')
        is_cached = 'max-age' in cache_control or 'expires' in response.headers

        css_text = response.text
        is_minified = '\n' not in css_text and '\t' not in css_text and '  ' not in css_text

        return {
            'size': css_size,
            'compressed': is_compressed,
            'cached': is_cached,
            'minified': is_minified
        }
    except RequestException as e:
        return {'Error': str(e)}
    except Exception as e:
        return {'Error': str(e)}

def css_audit_url(url):
    try:
        css_links = extract_css_data(url)
        if isinstance(css_links, dict) and 'Error' in css_links:
            return css_links

        if not css_links:
            return {'CSS Issues': 'No CSS files found.'}

        issues = []
        total_css_files = len(css_links)
        if total_css_files > 50:
            issues.append(f'Too many CSS files: {total_css_files} CSS files found.')

        for css_url in css_links:
            css_analysis = analyze_css_file(css_url)
            if isinstance(css_analysis, dict) and 'Error' in css_analysis:
                issues.append(f'Error analyzing {css_url}: {css_analysis["Error"]}')
                continue

            if css_analysis['size'] > 150 * 1024:
                issues.append(f'CSS too big: {css_url} is {css_analysis["size"] / 1024:.2f} KB.')
            if not css_analysis['compressed']:
                issues.append(f'CSS not compressed: {css_url}')
            if not css_analysis['cached']:
                issues.append(f'CSS not cached: {css_url}')
            if not css_analysis['minified']:
                issues.append(f'CSS not minified: {css_url}')

        return {'CSS Issues': issues} if issues else {'CSS Issues': 'No issues found'}
    except Exception as e:
        return {'Error': str(e)}

# Ejemplo de uso
url_to_audit = 'https://www.example.com'
result = css_audit_url(url_to_audit)
print(result)
