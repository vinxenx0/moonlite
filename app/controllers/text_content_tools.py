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

def analyze_text_content(html_content):
    if not html_content or isinstance(html_content, dict) and 'Error' in html_content:
        return html_content
    
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()
    word_count = len(text_content.split())
    
    h1_tags = soup.find_all('h1')
    h2_tags = soup.find_all('h2')
    
    h1_issues = {
        'missing': len(h1_tags) == 0,
        'empty': any(not tag.get_text().strip() for tag in h1_tags),
        'too_long': any(len(tag.get_text()) > 60 for tag in h1_tags),
        'multiple': len(h1_tags) > 1,
        'duplicate': any(tag.get_text().strip() == h1_tags[0].get_text().strip() for tag in h1_tags[1:]),
        'identical_title': soup.title and any(tag.get_text().strip() == soup.title.get_text().strip() for tag in h1_tags)
    }
    
    h2_issues = {
        'missing': len(h2_tags) == 0,
        'empty': any(not tag.get_text().strip() for tag in h2_tags),
        'too_long': any(len(tag.get_text()) > 60 for tag in h2_tags)
    }
    
    return {
        'low_word_count': word_count < 250,
        'h1_issues': h1_issues,
        'h2_issues': h2_issues
    }

def text_content_audit(url):
    try:
        html_content = fetch_page_content(url)
        analysis = analyze_text_content(html_content)
        
        issues = []
        if analysis.get('Error'):
            return analysis
        
        if analysis['low_word_count']:
            issues.append('Low word count: Less than 250 words')
        
        if analysis['h1_issues']['missing']:
            issues.append('H1 tag missing')
        if analysis['h1_issues']['empty']:
            issues.append('H1 tag empty')
        if analysis['h1_issues']['too_long']:
            issues.append('H1 tag too long')
        if analysis['h1_issues']['multiple']:
            issues.append('Multiple H1 tags')
        if analysis['h1_issues']['duplicate']:
            issues.append('Duplicate H1 tags on different pages')
        if analysis['h1_issues']['identical_title']:
            issues.append('Identical Title and H1 tags')
        
        if analysis['h2_issues']['missing']:
            issues.append('H2 tag missing')
        if analysis['h2_issues']['empty']:
            issues.append('H2 tag empty')
        if analysis['h2_issues']['too_long']:
            issues.append('H2 tag too long')
        
        return {'Text Content Issues': issues} if issues else {'Text Content Issues': 'No issues found'}
    except Exception as e:
        return {'Error': str(e)}

# Ejemplo de uso
url_to_audit = 'https://www.example.com'
result = text_content_audit(url_to_audit)
print(result)
