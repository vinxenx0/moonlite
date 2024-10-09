from bs4 import BeautifulSoup
import requests

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return {'Error': str(e)}
    except Exception as e:
        return {'Error': str(e)}

def extract_amp_links(html_content):
    if not html_content or isinstance(html_content, dict) and 'Error' in html_content:
        return html_content
    
    soup = BeautifulSoup(html_content, 'html.parser')
    amp_links = [link['href'] for link in soup.find_all('link', rel='amphtml')]
    
    return amp_links if amp_links else None

def check_amp_page(amp_url):
    try:
        response = requests.get(amp_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example checks: You can expand these checks based on specific AMP requirements
        is_amp = bool(soup.find('html', amp=True) or soup.find('html', **{'⚡': True}))
        return is_amp
    except requests.RequestException as e:
        return {'Error': str(e)}
    except Exception as e:
        return {'Error': str(e)}

def amp_pages_audit(url):
    try:
        html_content = fetch_page_content(url)
        amp_links = extract_amp_links(html_content)
        
        if not amp_links:
            return {'AMP Pages': 'No AMP pages used'}
        
        amp_results = []
        for amp_url in amp_links:
            result = check_amp_page(amp_url)
            if isinstance(result, dict) and 'Error' in result:
                amp_results.append({'URL': amp_url, 'Error': result['Error']})
            else:
                amp_results.append({'URL': amp_url, 'Valid AMP': result})
        
        return {'AMP Pages': amp_results}
    except Exception as e:
        return {'Error': str(e)}

# Ejemplo de uso
url_to_audit = 'https://www.example.com'
result = amp_pages_audit(url_to_audit)
print(result)
