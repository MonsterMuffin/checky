from datetime import datetime
from prometheus_client import Gauge, CollectorRegistry
from .models import DNSRecord
import logging

custom_registry = CollectorRegistry()

DNS_RECORD_EXPIRY = Gauge('dns_record_expiry', 'Days until DNS record expires', ['name', 'issuer'], registry=custom_registry)
DNS_RECORD_VERSION = Gauge('dns_record_version', 'Version of the DNS record', ['name'], registry=custom_registry)
DNS_RECORD_SERIAL_NUMBER = Gauge('dns_record_serial_number', 'Serial number of the DNS record', ['name'], registry=custom_registry)
DNS_RECORD_TLS_VERSION = Gauge('dns_record_tls_version', 'TLS version of the DNS record', ['name'], registry=custom_registry)

import logging

def update_dns_metrics():
    logger = logging.getLogger(__name__)
    records = DNSRecord.list_records()

    logger.debug(f"Updating metrics for {len(records)} records")

    for record in records:
        try:
            expiry_date = datetime.strptime(record['expiry_date'], "%Y-%m-%d %H:%M:%S UTC")
            days_until_expiry = (expiry_date - datetime.utcnow()).days
            DNS_RECORD_EXPIRY.labels(name=record['name'], issuer=record['issuer']).set(days_until_expiry)
            DNS_RECORD_VERSION.labels(name=record['name']).set(record['version'])
            # DNS_RECORD_SERIAL_NUMBER.labels(name=record['name']).set(record['serial_number'])
            DNS_RECORD_TLS_VERSION.labels(name=record['name']).set(record['tls_version'])

            logger.debug(f"Updated metrics for record: {record['name']}")
        except Exception as e:
            logger.error(f"Error updating metrics for record {record['name']}: {e}")

    logger.debug("Metrics update complete")