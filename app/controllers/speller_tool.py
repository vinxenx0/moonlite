import hashlib
import re
import textstat
#from gingerit.gingerit import GingerIt
from bs4 import BeautifulSoup

def analyze_content(url, html_content, language='en'):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Word Count
        body_text = soup.find('body').get_text() if soup.find('body') else ''
        word_count = len(re.findall(r'\w+', body_text))

        # Average Words Per Sentence
        sentences = textstat.sentences(body_text)
        total_words = sum(len(re.findall(r'\w+', sentence)) for sentence in sentences)
        average_words_per_sentence = total_words / len(sentences) if len(sentences) > 0 else 0

        # Flesch Reading Ease Score
        flesch_reading_ease_score = textstat.flesch_reading_ease(body_text)

        # Readability
        if flesch_reading_ease_score >= 90:
            readability = "Very Easy"
        elif flesch_reading_ease_score >= 80:
            readability = "Easy"
        elif flesch_reading_ease_score >= 70:
            readability = "Fairly Easy"
        elif flesch_reading_ease_score >= 60:
            readability = "Standard"
        elif flesch_reading_ease_score >= 50:
            readability = "Fairly Difficult"
        elif flesch_reading_ease_score >= 30:
            readability = "Difficult"
        else:
            readability = "Very Confusing"

        # Grammar and Spelling Check
        ginger_parser = GingerIt()
        ginger_results = ginger_parser.parse(body_text)
        total_language_errors = ginger_results['corrections'] if 'corrections' in ginger_results else 0
        spelling_errors = sum(1 for error in ginger_results['corrections'] if error['correct'] != error['text']) if 'corrections' in ginger_results else 0
        grammar_errors = sum(1 for error in ginger_results['corrections'] if error['correct'] == error['text']) if 'corrections' in ginger_results else 0

        # Hash
        page_hash = hashlib.md5(html_content.encode()).hexdigest()

        # Indexability
        indexable = True
        indexability_status = ''

        # Constructing JSON output
        content_analysis = {
            'Address': url,
            'Word Count': word_count,
            'Average Words Per Sentence': average_words_per_sentence,
            'Flesch Reading Ease Score': flesch_reading_ease_score,
            'Readability': readability,
            'Total Language Errors': total_language_errors,
            'Spelling Errors': spelling_errors,
            'Grammar Errors': grammar_errors,
            'Language': language,
            'Hash': page_hash,
            'Indexability': indexable,
            'Indexability Status': indexability_status
        }

        return content_analysis

    except Exception as e:
        return {'error': str(e)}
