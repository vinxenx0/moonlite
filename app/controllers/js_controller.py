import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

def extract_js_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        js_links = []
        for script in soup.find_all("script", {"src": True}):
            src = script.get("src")
            if src:
                if not src.startswith("http"):
                    src = requests.compat.urljoin(url, src)
                js_links.append(src)

        return js_links
    except RequestException as e:
        return {'Error': str(e)}
    except Exception as e:
        return {'Error': str(e)}

def analyze_js_file(js_url):
    try:
        response = requests.get(js_url)
        response.raise_for_status()

        js_size = len(response.content)
        is_compressed = 'gzip' in response.headers.get('Content-Encoding', '')

        cache_control = response.headers.get('Cache-Control', '')
        is_cached = 'max-age' in cache_control or 'expires' in response.headers

        js_text = response.text
        is_minified = '\n' not in js_text and '\t' not in js_text and '  ' not in js_text

        return {
            'size': js_size,
            'compressed': is_compressed,
            'cached': is_cached,
            'minified': is_minified
        }
    except RequestException as e:
        return {'Error': str(e)}
    except Exception as e:
        return {'Error': str(e)}

def js_audit_url(url):
    try:
        js_links = extract_js_data(url)
        if isinstance(js_links, dict) and 'Error' in js_links:
            return js_links

        if not js_links:
            return {'JavaScript Issues': 'No JavaScript files found.'}

        issues = []
        total_js_files = len(js_links)
        if total_js_files > 30:
            issues.append(f'Too many JavaScript files: {total_js_files} JavaScript files found.')

        total_js_size = 0
        for js_url in js_links:
            js_analysis = analyze_js_file(js_url)
            if isinstance(js_analysis, dict) and 'Error' in js_analysis:
                issues.append(f'Error analyzing {js_url}: {js_analysis["Error"]}')
                continue

            total_js_size += js_analysis['size']
            if js_analysis['size'] > 2 * 1024 * 1024:
                issues.append(f'JavaScript too big: {js_url} is {js_analysis["size"] / (1024 * 1024):.2f} MB.')
            if not js_analysis['compressed']:
                issues.append(f'JavaScript not compressed: {js_url}')
            if not js_analysis['cached']:
                issues.append(f'JavaScript not cached: {js_url}')
            if not js_analysis['minified']:
                issues.append(f'JavaScript not minified: {js_url}')

        if total_js_size > 2 * 1024 * 1024:
            issues.append(f'Total JavaScript size exceeds 2 MB: {total_js_size / (1024 * 1024):.2f} MB.')

        return {'JavaScript Issues': issues} if issues else {'JavaScript Issues': 'No issues found'}
    except Exception as e:
        return {'Error': str(e)}

# Ejemplo de uso
url_to_audit = 'https://www.example.com'
result = js_audit_url(url_to_audit)
print(result)
