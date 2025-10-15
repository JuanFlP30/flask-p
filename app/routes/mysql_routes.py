"""
Rutas para operaciones con MariaDB/MySQL
"""
from flask import Blueprint, jsonify, request
from app.config.database import get_mariadb_connection

mysql_bp = Blueprint('mysql', __name__, url_prefix='/mysql')

@mysql_bp.route('/users', methods=['GET', 'POST'])
def users():
    """Endpoint para gestionar usuarios en MariaDB"""
    conn = get_mariadb_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        data = request.get_json()
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        cursor.execute(query, (data.get('name'), data.get('email')))
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({
            'message': 'Usuario creado en MariaDB',
            'id': user_id
        }), 201
    else:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users), 200

@mysql_bp.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(user_id):
    """Endpoint para operaciones específicas de usuario en MariaDB"""
    conn = get_mariadb_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return jsonify(user), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404

    elif request.method == 'PUT':
        data = request.get_json()
        query = "UPDATE users SET name = %s, email = %s WHERE id = %s"
        cursor.execute(query, (data.get('name'), data.get('email'), user_id))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        if affected:
            return jsonify({'message': 'Usuario actualizado'}), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404

    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        if affected:
            return jsonify({'message': 'Usuario eliminado'}), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
