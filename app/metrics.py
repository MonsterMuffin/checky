from datetime import datetime
from prometheus_client import Gauge, CollectorRegistry
from .models import DNSRecord

custom_registry = CollectorRegistry()

DNS_RECORD_EXPIRY = Gauge('dns_record_expiry', 'Days until DNS record expires', ['name', 'issuer'], registry=custom_registry)
DNS_RECORD_VERSION = Gauge('dns_record_version', 'Version of the DNS record', ['name'], registry=custom_registry)
DNS_RECORD_SERIAL_NUMBER = Gauge('dns_record_serial_number', 'Serial number of the DNS record', ['name'], registry=custom_registry)
DNS_RECORD_TLS_VERSION = Gauge('dns_record_tls_version', 'TLS version of the DNS record', ['name'], registry=custom_registry)

def update_dns_metrics():
    records = DNSRecord.list_records()
    for record in records:
        try:
            expiry_date = datetime.strptime(record['expiry_date'], "%Y-%m-%d %H:%M:%S UTC")
            days_until_expiry = (expiry_date - datetime.utcnow()).days
        except ValueError:
            days_until_expiry = -1

        DNS_RECORD_EXPIRY.labels(name=record['name'], issuer=record['issuer']).set(days_until_expiry)
        DNS_RECORD_VERSION.labels(name=record['name']).set(record['version'])
        DNS_RECORD_SERIAL_NUMBER.labels(name=record['name']).set(record['serial_number'])
        DNS_RECORD_TLS_VERSION.labels(name=record['name']).set(record['tls_version'])