import ssl
import socket
from datetime import datetime

def get_certificate_details(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()

            issuer = dict(x[0] for x in cert['issuer'])
            subject = dict(x[0] for x in cert['subject'])

            sans = []
            for extension in cert.get('extensions', []):
                if extension[0] == 'subjectAltName':
                    for san in extension[1]:
                        sans.append(san[1])

            return {
                "issued_date": datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z').strftime('%Y-%m-%d %H:%M:%S UTC'),
                "expiry_date": datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').strftime('%Y-%m-%d %H:%M:%S UTC'),
                "issuer": issuer.get('organizationName', 'Unknown'),
                "subject": subject.get('commonName', hostname),
                "version": cert.get('version'),
                "serial_number": cert.get('serialNumber'),
                "signature_algorithm": cert.get('signatureAlgorithm'),
                "sans": sans,
            }

def get_tls_version(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            return ssock.version()