import sqlite3
from flask import g
from .utils import get_certificate_details, get_tls_version

DATABASE = 'instance/checky.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db(app):
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

class DNSRecord:
    def __init__(self, id, name, expiry_date, issuer, subject, issued_date, version, serial_number, signature_algorithm, sans, tls_version):
        self.id = id
        self.name = name
        self.expiry_date = expiry_date
        self.issuer = issuer
        self.subject = subject
        self.issued_date = issued_date
        self.version = version
        self.serial_number = serial_number
        self.signature_algorithm = signature_algorithm
        self.sans = ', '.join(sans)  # Store SANs as a comma-separated string
        self.tls_version = tls_version

    @staticmethod
    def add_record(name):
        details = get_certificate_details(name)
        tls_version = get_tls_version(name)
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO dns_records (name, expiry_date, issuer, subject, issued_date, version, serial_number, signature_algorithm, sans, tls_version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, details['expiry_date'], details['issuer'], details['subject'], details['issued_date'], details['version'], details['serial_number'], details['signature_algorithm'], ', '.join(details['sans']), tls_version))
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def remove_record(record_id):
        db = get_db()
        db.execute("DELETE FROM dns_records WHERE id = ?", (record_id,))
        db.commit()

    @staticmethod
    def list_records():
        db = get_db()
        cursor = db.execute("SELECT * FROM dns_records")
        records = cursor.fetchall()
        return [dict(record) for record in records]