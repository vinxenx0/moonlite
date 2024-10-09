import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_and_check_links(url):
    try:
        # Realizar la solicitud GET a la URL
        response = requests.get(url)
        # Parsear el contenido HTML de la respuesta
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Inicializar listas para almacenar los diferentes tipos de recursos
        urls = []
        internal_links = []
        external_links = []
        mailto_links = []
        tel_links = []
        meta_tags = []
        javascript_links = []
        css_links = []
        image_links = []
        other_links = []
        broken_links = []
        
        # Extraer todos los enlaces de la página
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            # Verificar si es un enlace interno, externo, mailto o tel
            if full_url.startswith(url):
                internal_links.append(full_url)
            elif href.startswith('mailto:'):
                mailto_links.append(full_url)
            elif href.startswith('tel:'):
                tel_links.append(full_url)
            else:
                external_links.append(full_url)
            # Agregar a la lista general de URLs
            urls.append(full_url)
            # Verificar el código de estado HTTP del enlace
            try:
                link_response = requests.head(full_url)
                if link_response.status_code != 200:
                    broken_links.append({'url': full_url, 'status_code': link_response.status_code})
            except Exception as e:
                print(f"Error al verificar el enlace {full_url}: {e}")
        
        # Extraer todas las etiquetas meta de la página
        for meta in soup.find_all('meta'):
            meta_tags.append(meta)
        
        # Extraer todos los enlaces a archivos JavaScript
        for script in soup.find_all('script', src=True):
            javascript_links.append(script['src'])
        
        # Extraer todos los enlaces a archivos CSS
        for css in soup.find_all('link', {'rel': 'stylesheet'}):
            css_links.append(css['href'])
        
        # Extraer todos los enlaces a imágenes
        for img in soup.find_all('img', src=True):
            image_links.append(img['src'])
        
        # Extraer todos los enlaces no comunes
        for link in soup.find_all('a', href=True):
            href = link['href']
            if not href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', '/')):
                other_links.append(urljoin(url, href))
        
        return {
            'urls': urls,
            'internal_links': internal_links,
            'external_links': external_links,
            'mailto_links': mailto_links,
            'tel_links': tel_links,
            'meta_tags': meta_tags,
            'javascript_links': javascript_links,
            'css_links': css_links,
            'image_links': image_links,
            'other_links': other_links,
            'broken_links': broken_links
        }
    
    except Exception as e:
        print(f"Error al extraer y verificar los enlaces: {e}")
        return None

# Ejemplo de uso
url = 'https://4glsp.com'
link_data = extract_and_check_links(url)
if link_data:
    print("URLs encontradas:")
    print(link_data['urls'])
    print("\nEnlaces internos encontrados:")
    print(link_data['internal_links'])
    print("\nEnlaces externos encontrados:")
    print(link_data['external_links'])
    print("\nEnlaces 'mailto:' encontrados:")
    print(link_data['mailto_links'])
    print("\nEnlaces 'tel:' encontrados:")
    print(link_data['tel_links'])
    print("\nMeta etiquetas encontradas:")
    print(link_data['meta_tags'])
    print("\nEnlaces a archivos JavaScript encontrados:")
    print(link_data['javascript_links'])
    print("\nEnlaces a archivos CSS encontrados:")
    print(link_data['css_links'])
    print("\nEnlaces a imágenes encontradas:")
    print(link_data['image_links'])
    print("\nOtros enlaces encontrados:")
    print(link_data['other_links'])
    print("\nEnlaces rotos encontrados:")
    print(link_data['broken_links'])
