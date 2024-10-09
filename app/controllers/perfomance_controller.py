import subprocess
import json
import requests

def run_lighthouse(url, output_path="lighthouse_report.json"):
    try:
        command = [
            "lighthouse", url,
            "--output=json",
            f"--output-path={output_path}",
            "--quiet"
        ]
        subprocess.run(command, check=True)
        with open(output_path, "r") as file:
            report = json.load(file)
        return report
    except subprocess.CalledProcessError as e:
        return {'Error': str(e)}
    except json.JSONDecodeError as e:
        return {'Error': 'Failed to parse Lighthouse report: ' + str(e)}

def fetch_web_vitals(url):
    try:
        response = requests.get(f"https://chromeuxreport.googleapis.com/v1/records:query?url={url}&key=YOUR_API_KEY")
        data = response.json()
        return data
    except requests.RequestException as e:
        return {'Error': str(e)}
    except json.JSONDecodeError as e:
        return {'Error': 'Failed to parse Web Vitals data: ' + str(e)}

def extract_lighthouse_metrics(report):
    try:
        metrics = {
            'LCP_lab': report['audits']['largest-contentful-paint']['displayValue'],
            'CLS_lab': report['audits']['cumulative-layout-shift']['displayValue'],
            'FCP_lab': report['audits']['first-contentful-paint']['displayValue'],
            'SpeedIndex': report['audits']['speed-index']['displayValue'],
            'TTI': report['audits']['interactive']['displayValue'],
            'TBT': report['audits']['total-blocking-time']['displayValue']
        }
        return metrics
    except KeyError as e:
        return {'Error': f'Missing expected key in Lighthouse report: {str(e)}'}

def extract_web_vitals_metrics(data):
    try:
        metrics = {
            'LCP_real': data['record']['metrics']['largest_contentful_paint']['percentiles']['p75'],
            'FID_real': data['record']['metrics']['first_input_delay']['percentiles']['p75'],
            'CLS_real': data['record']['metrics']['cumulative_layout_shift']['percentiles']['p75'],
            'FCP_real': data['record']['metrics']['first_contentful_paint']['percentiles']['p75'],
            'INP_real': data['record']['metrics']['interaction_to_next_paint']['percentiles']['p75']
        }
        return metrics
    except KeyError as e:
        return {'Error': f'Missing expected key in Web Vitals data: {str(e)}'}

def performance_audit_url(url):
    try:
        # Run Lighthouse to get lab environment metrics
        lighthouse_report = run_lighthouse(url)
        lighthouse_metrics = extract_lighthouse_metrics(lighthouse_report)

        # Fetch Web Vitals data for real-world metrics
        web_vitals_data = fetch_web_vitals(url)
        web_vitals_metrics = extract_web_vitals_metrics(web_vitals_data)

        # Combine both sets of metrics
        combined_metrics = {**lighthouse_metrics, **web_vitals_metrics}

        return combined_metrics
    except Exception as e:
        return {'Error': str(e)}

# Ejemplo de uso
url_to_audit = 'https://www.example.com'
result = performance_audit_url(url_to_audit)
print(result)
