from datetime import datetime
from prometheus_client import Gauge, CollectorRegistry
from .models import DNSRecord
import logging

custom_registry = CollectorRegistry()

DNS_RECORD = Gauge('dns_record', 'Information about DNS records',
                   ['name', 'issuer', 'serial_number', 'tls_version', 'subject', 'version'],
                   registry=custom_registry)

def update_dns_metrics():
    logger = logging.getLogger(__name__)
    records = DNSRecord.list_records()

    logger.debug(f"Updating metrics for {len(records)} records")

    for record in records:
        try:
            expiry_date = datetime.strptime(record['expiry_date'], "%Y-%m-%d %H:%M:%S UTC")
            days_until_expiry = (expiry_date - datetime.utcnow()).days

            DNS_RECORD.labels(name=record['name'], issuer=record['issuer'],
                              serial_number=record['serial_number'], tls_version=record['tls_version'],
                              subject=record['subject'], version=str(record['version'])).set(days_until_expiry)

            logger.debug(f"Updated metrics for record: {record['name']}")
        except Exception as e:
            logger.error(f"Error updating metrics for record {record['name']}: {e}")

    logger.debug("Metrics update complete")
