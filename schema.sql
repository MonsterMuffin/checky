-- schema.sql

CREATE TABLE IF NOT EXISTS dns_records (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    expiry_date TEXT,
    issuer TEXT,
    subject TEXT,
    issued_date TEXT,
    version INTEGER,
    serial_number TEXT,
    signature_algorithm TEXT,
    tls_version TEXT,
    sans TEXT
    tls_version TEXT
);
