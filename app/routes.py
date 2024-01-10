from flask import request, jsonify, Blueprint, Response, Flask
from prometheus_client import generate_latest
from .metrics import custom_registry
from .models import DNSRecord, get_db

bp = Blueprint('checky', __name__)

def init_routes(app):
    app.register_blueprint(bp)

@bp.route('/metrics_json', methods=['GET'])
def metrics_json():
    records = DNSRecord.list_records()
    return jsonify(records)

@bp.route('/metrics')
def metrics():
    return Response(generate_latest(custom_registry), mimetype='text/plain')

@bp.route('/add_dns_record', methods=['POST'])
def add_dns_record():
    data = request.get_json()
    result = DNSRecord.add_record(data['name'])
    if isinstance(result, dict) and "error" in result:
        return jsonify({"error": result["error"]}), 400
    return jsonify({"message": "DNS record added", "id": result}), 201

@bp.route('/remove_dns_record/<int:record_id>', methods=['DELETE'])
def remove_dns_record(record_id):
    DNSRecord.remove_record(record_id)
    return jsonify({"message": "DNS record removed"}), 200

@bp.route('/list_dns_records', methods=['GET'])
def list_dns_records():
    records = DNSRecord.list_records()
    return jsonify(records), 200