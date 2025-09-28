from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

donor_bp = Blueprint('donor_bp', __name__)

# 1️⃣ Add donor (POST)
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

# 2️⃣ Get all donors (GET)
@donor_bp.route('/donors', methods=['GET'])
def get_donors():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM donors")
        donors = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(donors)
    except Exception as e:
        return jsonify({'error': str(e)})

# 3️⃣ Search donor by blood type (GET)
@donor_bp.route('/search_donor', methods=['GET'])
def search_donor():
    blood_type = request.args.get('blood_type')
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM donors WHERE blood_type=%s", (blood_type,))
        donors = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(donors)
    except Exception as e:
        return jsonify({'error': str(e)})

# 4️⃣ Update donor by ID (PUT)
@donor_bp.route('/update_donor/<int:id>', methods=['PUT'])
def update_donor(id):
    data = request.get_json()
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = "UPDATE donors SET name=%s, age=%s, blood_type=%s, phone=%s, email=%s WHERE id=%s"
        cursor.execute(sql, (data['name'], data['age'], data['blood_type'], data.get('phone'), data.get('email'), id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Donor updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# 5️⃣ Delete donor by ID (DELETE)
@donor_bp.route('/delete_donor/<int:id>', methods=['DELETE'])
def delete_donor(id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM donors WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Donor deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})
