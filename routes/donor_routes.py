from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

donor_bp = Blueprint('donor_bp', __name__)

@donor_bp.route('/add_donor', methods=['POST'])
def add_donor():
    data = request.get_json()
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = "INSERT INTO donors (name, age, blood_type, phone, email) VALUES (%s, %s, %s, %s, %s)"
        values = (data['name'], data['age'], data['blood_type'], data.get('phone'), data.get('email'))
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Donor added successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})
