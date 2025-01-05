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


def check_duplicate_page_titles(html_content):
    if not html_content or isinstance(html_content,
                                      dict) and 'Error' in html_content:
        return html_content

    soup = BeautifulSoup(html_content, 'html.parser')
    title_tags = soup.find_all('title')
    titles = [tag.get_text().strip() for tag in title_tags]

    return len(titles) != len(set(titles))


def check_multiple_title_tags(html_content):
    if not html_content or isinstance(html_content,
                                      dict) and 'Error' in html_content:
        return html_content

    soup = BeautifulSoup(html_content, 'html.parser')
    title_tags = soup.find_all('title')

    return len(title_tags) > 1


def check_title_missing(html_content):
    if not html_content or isinstance(html_content,
                                      dict) and 'Error' in html_content:
        return html_content

    soup = BeautifulSoup(html_content, 'html.parser')
    title_tags = soup.find_all('title')

    return len(title_tags) == 0


def check_title_length(html_content):
    if not html_content or isinstance(html_content,
                                      dict) and 'Error' in html_content:
        return html_content

    soup = BeautifulSoup(html_content, 'html.parser')
    title_tags = soup.find_all('title')

    if len(title_tags) == 0:
        return None

    title_text = title_tags[0].get_text().strip()
    title_length = len(title_text)

    return title_length


def title_tags_audit(url):
    try:
        html_content = fetch_page_content(url)

        duplicate_page_titles = check_duplicate_page_titles(html_content)
        multiple_title_tags = check_multiple_title_tags(html_content)
        title_missing = check_title_missing(html_content)
        title_length = check_title_length(html_content)

        result = {
            'URLs with Duplicate Page Titles': duplicate_page_titles,
            'Multiple Title Tags': multiple_title_tags,
            'Title Tag Missing': title_missing,
            'Title Length': title_length
        }

        return result
    except Exception as e:
        return {'Error': str(e)}


# Ejemplo de uso
url_to_audit = 'https://www.example.com'
result = title_tags_audit(url_to_audit)
print(result)
