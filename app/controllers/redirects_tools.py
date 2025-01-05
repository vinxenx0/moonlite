import requests


def get_redirect_chain(url):
    try:
        response = requests.get(url, allow_redirects=True)
        chain = response.history
        final_url = response.url
        status_code = response.status_code

        redirect_chain = []
        for resp in chain:
            redirect_chain.append({
                'url': resp.url,
                'status_code': resp.status_code
            })

        redirect_chain.append({'url': final_url, 'status_code': status_code})

        return redirect_chain
    except requests.RequestException as e:
        return {'Error': str(e)}
    except Exception as e:
        return {'Error': str(e)}


def analyze_redirects(redirect_chain):
    if not redirect_chain or isinstance(redirect_chain,
                                        dict) and 'Error' in redirect_chain:
        return redirect_chain

    redirect_issues = {
        'redirect_chain': [],
        'redirect_loop': False,
        'redirect_to_4xx_or_5xx': [],
        'meta_refresh_redirect': [],
        'temporary_redirects': []
    }

    urls = set()
    for i, redirect in enumerate(redirect_chain):
        url = redirect['url']
        status_code = redirect['status_code']

        if url in urls:
            redirect_issues['redirect_loop'] = True
        urls.add(url)

        if i > 0 and i < len(redirect_chain) - 1:
            redirect_issues['redirect_chain'].append(url)

        if status_code >= 400:
            redirect_issues['redirect_to_4xx_or_5xx'].append(url)

        if status_code in [302, 303, 307]:
            redirect_issues['temporary_redirects'].append(url)

        if '<meta http-equiv="refresh"' in requests.get(url).text.lower():
            redirect_issues['meta_refresh_redirect'].append(url)

    return redirect_issues


def redirects_audit(url):
    try:
        redirect_chain = get_redirect_chain(url)
        analysis = analyze_redirects(redirect_chain)

        issues = []
        if analysis.get('Error'):
            return analysis

        if analysis['redirect_chain']:
            issues.append(f'Redirect chain: {analysis["redirect_chain"]}')
        if analysis['redirect_loop']:
            issues.append('Redirect loop detected')
        if analysis['redirect_to_4xx_or_5xx']:
            issues.append(
                f'Redirect to 4xx or 5xx: {analysis["redirect_to_4xx_or_5xx"]}'
            )
        if analysis['meta_refresh_redirect']:
            issues.append(
                f'Meta refresh redirect: {analysis["meta_refresh_redirect"]}')
        if analysis['temporary_redirects']:
            issues.append(
                f'Temporary redirects (302, 303, 307): {analysis["temporary_redirects"]}'
            )

        return {
            'Redirect Issues': issues
        } if issues else {
            'Redirect Issues': 'No issues found'
        }
    except Exception as e:
        return {'Error': str(e)}


# Ejemplo de uso
url_to_audit = 'https://www.example.com'
result = redirects_audit(url_to_audit)
print(result)
