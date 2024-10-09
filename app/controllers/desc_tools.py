from bs4 import BeautifulSoup
import requests

def description_tags_audit(url):
    def fetch_page_content(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return {'Error': str(e)}
        except Exception as e:
            return {'Error': str(e)}

    def check_description_missing(html_content):
        if not html_content or isinstance(html_content, dict) and 'Error' in html_content:
            return html_content

        soup = BeautifulSoup(html_content, 'html.parser')
        description_tag = soup.find('meta', attrs={'name': 'description'})

        return description_tag is None

    def check_duplicate_description(html_content):
        if not html_content or isinstance(html_content, dict) and 'Error' in html_content:
            return html_content

        soup = BeautifulSoup(html_content, 'html.parser')
        description_tags = soup.find_all('meta', attrs={'name': 'description'})

        return len(description_tags) > 1

    def check_description_too_long(html_content):
        if not html_content or isinstance(html_content, dict) and 'Error' in html_content:
            return html_content

        soup = BeautifulSoup(html_content, 'html.parser')
        description_tag = soup.find('meta', attrs={'name': 'description'})

        if description_tag:
            content = description_tag.get('content')
            return len(content) > 160  # Maximum recommended length for description tags

        return False

    try:
        html_content = fetch_page_content(url)

        description_missing = check_description_missing(html_content)
        duplicate_description = check_duplicate_description(html_content)
        description_too_long = check_description_too_long(html_content)

        result = {
            'Description Missing': description_missing,
            'Duplicate Description': duplicate_description,
            'Description Too Long': description_too_long
        }

        return result
    except Exception as e:
        return {'Error': str(e)}

# Ejemplo de uso
url_to_audit = 'https://www.example.com'
result = description_tags_audit(url_to_audit)
print(result)
