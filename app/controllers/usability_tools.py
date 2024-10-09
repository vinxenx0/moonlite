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

def check_favicon(html_content):
    if not html_content or isinstance(html_content, dict) and 'Error' in html_content:
        return html_content

    soup = BeautifulSoup(html_content, 'html.parser')
    favicon_tag = soup.find('link', rel='icon')

    return favicon_tag is None

def check_flash_usage(html_content):
    if not html_content or isinstance(html_content, dict) and 'Error' in html_content:
        return html_content

    soup = BeautifulSoup(html_content, 'html.parser')
    flash_tags = soup.find_all('object')

    return len(flash_tags) > 0

def check_x_card_tag(html_content):
    if not html_content or isinstance(html_content, dict) and 'Error' in html_content:
        return html_content

    soup = BeautifulSoup(html_content, 'html.parser')
    x_card_tag = soup.find('meta', attrs={'name': 'twitter:card'})

    return x_card_tag is None

def usability_audit(url):
    try:
        html_content = fetch_page_content(url)

        favicon_missing = check_favicon(html_content)
        flash_used = check_flash_usage(html_content)
        x_card_tag_missing = check_x_card_tag(html_content)

        result = {
            'Favicon Missing': favicon_missing,
            'Flash Used': flash_used,
            'X Card Tag Missing': x_card_tag_missing
        }

        return result
    except Exception as e:
        return {'Error': str(e)}

    # Ejemplo de uso
    #url_to_audit = 'https://www.example.com'
    #result = usability_audit(url_to_audit)
    #print(result)
