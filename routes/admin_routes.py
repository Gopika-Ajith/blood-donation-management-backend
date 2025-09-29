from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

admin_bp = Blueprint('admin_bp', __name__)

# --- Get all donors ---
@admin_bp.route('/admin/donors', methods=['GET'])
def get_all_donors():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM donors")
        donors = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(donors)
    except Exception as e:
        return jsonify({"error": str(e)})

# --- Update donor ---
@admin_bp.route('/admin/update_donor/<int:id>', methods=['PUT'])
def update_donor(id):
    data = request.get_json()
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = """UPDATE donors
                 SET name=%s, age=%s, blood_type=%s, phone=%s, email=%s
                 WHERE id=%s"""
        cursor.execute(sql, (
            data['name'], data['age'], data['blood_type'],
            data['phone'], data['email'], id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Donor updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

# --- Delete donor ---
@admin_bp.route('/admin/delete_donor/<int:id>', methods=['DELETE'])
def delete_donor(id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM donors WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Donor deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

# --- Get all requests ---
@admin_bp.route('/admin/requests', methods=['GET'])
def get_all_requests():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM requests")  # make sure your table is named `requests`
        requests_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(requests_list)
    except Exception as e:
        return jsonify({"error": str(e)})

# --- Approve request ---
@admin_bp.route('/admin/approve_request/<int:id>', methods=['PUT'])
def approve_request(id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("UPDATE requests SET status='Approved' WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Request approved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
