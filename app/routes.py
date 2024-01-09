from flask import request, jsonify, Blueprint, Response
from .models import DNSRecord, get_db

bp = Blueprint('checky', __name__)

def init_routes(app):
    app.register_blueprint(bp)

@bp.route('/metrics_json', methods=['GET'])
def metrics_json():
    records = DNSRecord.list_records()
    return jsonify(records)

@bp.route('/add_dns_record', methods=['POST'])
def add_dns_record():
    data = request.get_json()
    record_id = DNSRecord.add_record(data['name'])
    return jsonify({"message": "DNS record added", "id": record_id}), 201

@bp.route('/remove_dns_record/<int:record_id>', methods=['DELETE'])
def remove_dns_record(record_id):
    DNSRecord.remove_record(record_id)
    return jsonify({"message": "DNS record removed"}), 200

@bp.route('/list_dns_records', methods=['GET'])
def list_dns_records():
    records = DNSRecord.list_records()
    return jsonify(records), 200