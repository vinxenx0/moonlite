from bs4 import BeautifulSoup
import requests


def mobile_optimization_audit(url):

    def fetch_page_content(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return {'Error': str(e)}
        except Exception as e:
            return {'Error': str(e)}

    def check_viewport_meta_tag(html_content):
        if not html_content or isinstance(html_content,
                                          dict) and 'Error' in html_content:
            return html_content

        soup = BeautifulSoup(html_content, 'html.parser')
        viewport_meta_tag = soup.find('meta', attrs={'name': 'viewport'})

        if viewport_meta_tag:
            content = viewport_meta_tag.get('content')
            if 'width=device-width' not in content:
                return False
        else:
            return False

        return True

    def check_incompatible_plugins(html_content):
        if not html_content or isinstance(html_content,
                                          dict) and 'Error' in html_content:
            return html_content

        soup = BeautifulSoup(html_content, 'html.parser')
        incompatible_plugins = soup.find_all(
            ['embed', 'object'],
            attrs={
                'type':
                ['application/x-shockwave-flash', 'application/x-silverlight']
            })

        return incompatible_plugins

    def check_text_to_html_ratio(html_content):
        if not html_content or isinstance(html_content,
                                          dict) and 'Error' in html_content:
            return html_content

        soup = BeautifulSoup(html_content, 'html.parser')
        text_length = len(soup.get_text())
        html_length = len(str(soup))

        text_to_html_ratio = (text_length /
                              html_length) * 100 if html_length > 0 else 0

        return text_to_html_ratio

    try:
        html_content = fetch_page_content(url)

        viewport_meta_tag_missing = not check_viewport_meta_tag(html_content)
        incompatible_plugins = check_incompatible_plugins(html_content)
        text_to_html_ratio = check_text_to_html_ratio(html_content)

        result = {
            'Viewport Meta Tag Missing': viewport_meta_tag_missing,
            'Fixed Width Value in Viewport Meta Tag':
            not viewport_meta_tag_missing,
            'Incompatible Plugins': incompatible_plugins,
            'Text to HTML Ratio': text_to_html_ratio
        }

        return result
    except Exception as e:
        return {'Error': str(e)}


# Ejemplo de uso
url_to_audit = 'https://www.example.com'
result = mobile_optimization_audit(url_to_audit)
print(result)
