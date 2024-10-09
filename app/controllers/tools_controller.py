# app/controllers/tools_controller.py

import subprocess
import socket
import whois
import dns.resolver
import dns.zone
import subprocess
import socket
import dns.resolver
import ipwhois
import ssl
import dns.zone
import dns.rdatatype
import pyasn
import requests


def dnskey_lookup(domain):
    try:
        dnskey_records = dns.resolver.resolve(domain, 'DNSKEY')
        dnskey_results = [str(record) for record in dnskey_records]
        return dnskey_results
    except Exception as e:
        return str(e)

def ssl_lookup(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return cert
    except Exception as e:
        return str(e)

def loc_lookup(domain):
    try:
        loc_records = dns.resolver.resolve(domain, 'LOC')
        loc_results = [str(record) for record in loc_records]
        return loc_results
    except Exception as e:
        return str(e)

def ipseckey_lookup(domain):
    try:
        ipseckey_records = dns.resolver.resolve(domain, 'IPSECKEY')
        ipseckey_results = [str(record) for record in ipseckey_records]
        return ipseckey_results
    except Exception as e:
        return str(e)

def asn_lookup(ip_address):
    try:
        asndb = pyasn.pyasn('ipasn_20210907.dat')  # Cambiar al archivo de base de datos ASN actualizado
        asn, _ = asndb.lookup(ip_address)
        return asn
    except Exception as e:
        return str(e)

def rrsig_lookup(domain):
    try:
        rrsig_records = dns.resolver.resolve(domain, 'RRSIG')
        rrsig_results = [str(record) for record in rrsig_records]
        return rrsig_results
    except Exception as e:
        return str(e)

def nsec_lookup(domain):
    try:
        nsec_records = dns.resolver.resolve(domain, 'NSEC')
        nsec_results = [str(record) for record in nsec_records]
        return nsec_results
    except Exception as e:
        return str(e)

def arin_lookup(ip_address):
    try:
        whois_query = ipwhois.IPWhois(ip_address)
        result = whois_query.lookup_rdap()
        return result
    except Exception as e:
        return str(e)

def mta_sts_lookup(domain):
    try:
        mta_sts_records = dns.resolver.resolve(f'_mta-sts.{domain}', 'TXT')
        mta_sts_results = [str(record) for record in mta_sts_records]
        return mta_sts_results
    except Exception as e:
        return str(e)

def nsec3param_lookup(domain):
    try:
        nsec3param_records = dns.resolver.resolve(domain, 'NSEC3PARAM')
        nsec3param_results = [str(record) for record in nsec3param_records]
        return nsec3param_results
    except Exception as e:
        return str(e)

def dns_servers_lookup(domain):
    try:
        dns_servers = dns.resolver.resolve(domain, 'NS')
        dns_servers_results = [str(record) for record in dns_servers]
        return dns_servers_results
    except Exception as e:
        return str(e)
    
def mx_lookup(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_results = [str(record.exchange) for record in mx_records]
        return mx_results
    except Exception as e:
        return str(e)

def whois_lookup(domain):
    try:
        domain_info = whois.whois(domain)
        return domain_info
    except Exception as e:
        return str(e)

def dmarc_lookup(domain):
    try:
        dmarc_record = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
        return str(dmarc_record[0])
    except Exception as e:
        return str(e)

def spf_lookup(domain):
    try:
        spf_record = dns.resolver.resolve(domain, 'TXT')
        for record in spf_record:
            if record.to_text().startswith("v=spf"):
                return str(record)
        return "SPF record not found for this domain"
    except Exception as e:
        return str(e)

def dns_lookup(domain):
    try:
        dns_records = dns.resolver.resolve(domain, 'A')
        dns_results = [str(record) for record in dns_records]
        return dns_results
    except Exception as e:
        return str(e)

def reverse_lookup(ip_address):
    try:
        reverse_dns = dns.resolver.resolve_address(ip_address)
        return [str(record) for record in reverse_dns]
    except Exception as e:
        return str(e)

def dkim_lookup(domain):
    try:
        dkim_record = dns.resolver.resolve(f'_domainkey.{domain}', 'TXT')
        return [str(record) for record in dkim_record]
    except Exception as e:
        return str(e)

def aaaa_lookup(domain):
    try:
        aaaa_records = dns.resolver.resolve(domain, 'AAAA')
        aaaa_results = [str(record) for record in aaaa_records]
        return aaaa_results
    except Exception as e:
        return str(e)

def srv_lookup(service, protocol, domain):
    try:
        srv_records = dns.resolver.resolve(f'_{service}._{protocol}.{domain}', 'SRV')
        srv_results = [str(record) for record in srv_records]
        return srv_results
    except Exception as e:
        return str(e)

def cert_lookup(domain):
    try:
        cert_records = dns.resolver.resolve(domain, 'CERT')
        cert_results = [str(record) for record in cert_records]
        return cert_results
    except Exception as e:
        return str(e)

def bimi_lookup(domain):
    try:
        bimi_record = dns.resolver.resolve(f'_bimi.{domain}', 'TXT')
        return [str(record) for record in bimi_record]
    except Exception as e:
        return str(e)

def ip_lookup(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except Exception as e:
        return str(e)

def cname_lookup(domain):
    try:
        cname_records = dns.resolver.resolve(domain, 'CNAME')
        cname_results = [str(record) for record in cname_records]
        return cname_results
    except Exception as e:
        return str(e)

def soa_lookup(domain):
    try:
        soa_record = dns.resolver.resolve(domain, 'SOA')
        return [str(record) for record in soa_record]
    except Exception as e:
        return str(e)

def txt_lookup(domain):
    try:
        txt_records = dns.resolver.resolve(domain, 'TXT')
        txt_results = [str(record) for record in txt_records]
        return txt_results
    except Exception as e:
        return str(e)

def http_lookup(domain):
    try:
        response = requests.get(f'http://{domain}')
        status_code = response.status_code
        headers = dict(response.headers)
        return status_code, headers
    except Exception as e:
        return str(e)

def https_lookup(domain):
    try:
        response = requests.get(f'https://{domain}')
        status_code = response.status_code
        headers = dict(response.headers)
        return status_code, headers
    except Exception as e:
        return str(e)

def ping_lookup(domain):
    try:
        result = subprocess.run(['ping', '-c', '4', domain], capture_output=True, text=True)
        return {'stdout': result.stdout, 'stderr': result.stderr}
    except Exception as e:
        return {'error': str(e)}

def traceroute_lookup(domain):
    try:
       result = subprocess.run(['traceroute', '-m', '12', domain], capture_output=True, text=True)
       return {'stdout': result.stdout, 'stderr': result.stderr}
    except Exception as e:
        return {'error': str(e)}

def nmap_lookup(domain):
    try:
        result = subprocess.run(['nmap', '-F', domain], capture_output=True, text=True)
        return {'stdout': result.stdout, 'stderr': result.stderr}
    except Exception as e:
        return {'error': str(e)}