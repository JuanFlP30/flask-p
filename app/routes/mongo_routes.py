"""
Rutas para operaciones con MongoDB
"""
from flask import Blueprint, jsonify, request
from app.config.database import get_mongodb

mongo_bp = Blueprint('mongo', __name__, url_prefix='/mongo')

@mongo_bp.route('/users', methods=['GET', 'POST'])
def users():
    """Endpoint para gestionar usuarios en MongoDB"""
    mongo = get_mongodb()

    if request.method == 'POST':
        data = request.get_json()
        result = mongo.db.users.insert_one(data)
        return jsonify({
            'message': 'Usuario creado en MongoDB',
            'id': str(result.inserted_id)
        }), 201
    else:
        users = list(mongo.db.users.find())
        for user in users:
            user['_id'] = str(user['_id'])
        return jsonify(users), 200

@mongo_bp.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(user_id):
    """Endpoint para operaciones específicas de usuario en MongoDB"""
    mongo = get_mongodb()
    from bson.objectid import ObjectId

    if request.method == 'GET':
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
            return jsonify(user), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404

    elif request.method == 'PUT':
        data = request.get_json()
        result = mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': data}
        )
        if result.matched_count:
            return jsonify({'message': 'Usuario actualizado'}), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404

    elif request.method == 'DELETE':
        result = mongo.db.users.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count:
            return jsonify({'message': 'Usuario eliminado'}), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
