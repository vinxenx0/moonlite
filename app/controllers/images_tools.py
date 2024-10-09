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

def check_image_size(html_content):
    if not html_content or isinstance(html_content, dict) and 'Error' in html_content:
        return html_content
    
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    
    oversized_images = []
    for img in img_tags:
        src = img.get('src')
        if src:
            try:
                response = requests.head(src)
                size = int(response.headers.get('content-length', 0))
                if size > 150000:  # 150 KB threshold
                    oversized_images.append(src)
            except Exception as e:
                pass
    
    return oversized_images

def check_alt_text(html_content):
    if not html_content or isinstance(html_content, dict) and 'Error' in html_content:
        return html_content
    
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    
    missing_alt_text_images = []
    for img in img_tags:
        alt = img.get('alt')
        if not alt:
            src = img.get('src')
            missing_alt_text_images.append(src)
    
    return missing_alt_text_images

def image_tags_audit(url):
    try:
        html_content = fetch_page_content(url)
        
        oversized_images = check_image_size(html_content)
        missing_alt_text_images = check_alt_text(html_content)
        
        result = {
            'Oversized Images': oversized_images,
            'Missing Alt Text Images': missing_alt_text_images
        }
        
        return result
    except Exception as e:
        return {'Error': str(e)}

# Ejemplo de uso
url_to_audit = 'https://www.example.com'
result = image_tags_audit(url_to_audit)
print(result)
