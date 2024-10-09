import requests

def website_speed_audit(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        content_size = len(response.content) / 1024  # Convert bytes to kilobytes
        html_size_too_big = content_size > 3072  # 3 MB in kilobytes
        
        loading_speed_slow = response.elapsed.total_seconds() > 3  # 3 seconds
        
        uncompressed_content = 'Content-Encoding' not in response.headers
        
        result = {
            'HTML Size Too Big': html_size_too_big,
            'Slow Page Loading Speed': loading_speed_slow,
            'Uncompressed Content': uncompressed_content
        }
        
        return result
    except requests.RequestException as e:
        return {'Error': str(e)}
    except Exception as e:
        return {'Error': str(e)}

# Ejemplo de uso
url_to_audit = 'https://www.example.com'
result = website_speed_audit(url_to_audit)
print(result)
