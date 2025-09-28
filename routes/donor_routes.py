from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

# 1️⃣ Create blueprint
donor_bp = Blueprint('donor_bp', __name__)

# 2️⃣ Test route: add donor via browser (GET)
@donor_bp.route('/add_test_donor')
def add_test_donor():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = "INSERT INTO donors (name, age, blood_type, phone, email) VALUES (%s, %s, %s, %s, %s)"
        values = ("Test Donor", 25, "O+", "1234567890", "test@example.com")
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return "Test donor added!"
    except Exception as e:
        return str(e)

# 3️⃣ Get all donors
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

# 4️⃣ Search donors by blood type
@donor_bp.route('/search_donor', methods=['GET'])
def search_donor():
    blood_type = request.args.get('blood_type')
    if not blood_type:
        return jsonify({'error': 'Please provide blood_type as query parameter'}), 400
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM donors WHERE blood_type = %s", (blood_type,))
        donors = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(donors)
    except Exception as e:
        return jsonify({'error': str(e)})

# 5️⃣ Proper POST route to add donor via JSON
@donor_bp.route('/add_donor', methods=['POST'])
def add_donor():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON body provided'}), 400

    required_fields = ['name', 'age', 'blood_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = "INSERT INTO donors (name, age, blood_type, phone, email) VALUES (%s, %s, %s, %s, %s)"
        values = (
            data['name'],
            data['age'],
            data['blood_type'],
            data.get('phone'),
            data.get('email')
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Donor added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
