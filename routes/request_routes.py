from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

request_bp = Blueprint('request_bp', __name__)

@request_bp.route('/add_request', methods=['POST'])
def add_request():
    data = request.get_json()
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = "INSERT INTO requests (requester_name, blood_type, units, hospital) VALUES (%s, %s, %s, %s)"
        values = (data['requester_name'], data['blood_type'], data['units'], data['hospital'])
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Request submitted successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})
