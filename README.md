# Checky: An app for checking certificates.

## API Endpoints

### List DNS Records

* Endpoint: /list_dns_records
* Method: GET
* Description: Retrieves a list of all DNS records in the database.
* Response: JSON array of DNS records.

### Add DNS Record

* Endpoint: /add_dns_record
* Method: POST
* Description: Adds a new DNS record to the database.
* Request Body: JSON object containing the DNS record details.
* Response: JSON object with a message confirming the addition of the record.

### Remove DNS Record

* Endpoint: /remove_dns_record/<int:record_id>
* Method: DELETE
* Description: Removes a DNS record from the database based on its ID.
* URL Parameter: record_id - The ID of the DNS record to be removed.
* Response: JSON object with a message confirming the deletion of the record.

## JSON Endpoint

* URL: /metrics_json
* Method: GET
* Description: Retrieves all DNS records with their SSL/TLS certificate information in a JSON format.

### Response Format

The endpoint returns a JSON array of objects, each representing a DNS record. Each object contains the following fields:

* id: The unique identifier of the DNS record.
* name: The name of the DNS record.
* expiry_date: The expiry date of the associated SSL/TLS certificate.
* issued_date: The issue date of the certificate.
* issuer: The issuer of the certificate.
* subject: The subject for which the certificate was issued.
* serial_number: The serial number of the certificate.
* signature_algorithm: The algorithm used for the certificate's signature.
* tls_version: The version of TLS used.
* version: The version of the certificate.

### Example

```json
[
  {
    "expiry_date": "2024-02-24 18:41:52 UTC",
    "id": 1,
    "issued_date": "2023-11-26 18:41:53 UTC",
    "issuer": "Google Trust Services LLC",
    "name": "blog.muffn.io",
    "sans": "",
    "serial_number": "6FC5F9226C70B26B111D003D5A19F169",
    "signature_algorithm": null,
    "subject": "blog.muffn.io",
    "tls_version": "TLSv1.3",
    "version": 3
  }
]

```