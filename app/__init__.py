from flask import Flask, current_app
from .models import init_db, DNSRecord
from .utils import get_certificate_details, get_tls_version
from .metrics import update_dns_metrics
from flask_cors import CORS
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG)

def checky():
    app = Flask('checky')

    with app.app_context():
        init_db(app)
        update_dns_metrics()

    from .routes import init_routes
    init_routes(app)

    CORS(app)

    updater_thread = threading.Thread(target=start_updater, args=(app,), daemon=True)
    updater_thread.start()

    return app

def start_updater(app):
    with app.app_context():
        while True:
            update_dns_records()
            update_dns_metrics()
            time.sleep(0.1) # CHANGE THIS BEFORE DEPLOY

def update_dns_records():
    records = DNSRecord.list_records()
    for record in records:
        updated_details = get_certificate_details(record['name'])
        updated_tls_version = get_tls_version(record['name'])
        if 'error' in updated_details or 'error' in updated_tls_version:
            continue
        needs_update = any(
            record[field] != updated_details[field]
            for field in ['expiry_date', 'issuer', 'subject', 'issued_date', 'version', 'serial_number', 'signature_algorithm', 'sans']
        ) or record['tls_version'] != updated_tls_version
        if needs_update:
            DNSRecord.update_record(record['id'], updated_details, updated_tls_version)