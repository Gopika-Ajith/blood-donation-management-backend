from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

auth_bp = Blueprint('auth_bp', __name__)

# 1️⃣ User login
@auth_bp.route('/login_user', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({"message": "User login successful", "user": user})
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)})

# 2️⃣ Admin login
@auth_bp.route('/login_admin', methods=['POST'])
def login_admin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (username, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin:
            return jsonify({"message": "Admin login successful", "admin": admin})
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)})
