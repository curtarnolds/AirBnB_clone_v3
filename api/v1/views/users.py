#!/usr/bin/python3
"""Handle User API actions"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET'])
@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrieve all User objects"""
    user_obj = storage.all('User')
    users_list = [val for val in user_obj.values()]
    return jsonify([user.to_dict() for user in users_list])


@app_views.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a given user"""
    user_obj = storage.get(User, user_id)
    if user_obj:
        return jsonify(user_obj.to_dict())
    else:
        abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user object"""
    user_obj = storage.get(User, user_id)
    if user_obj:
        storage.delete(user_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users/', methods=['POST'])
@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a user"""
    user = request.get_json()
    if not user:
        abort(400, description='Not a JSON')
    if not user.get('email'):
        abort(400, description='Missing email')
    if not user.get('password'):
        abort(400, description='Missing password')
    else:
        new_user = User(name=user['email'], password=user['password'])
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a user object"""
    user_obj = storage.get(User, user_id)
    if user_obj:
        user = request.get_json()
        if not user:
            abort(400, description='Not a JSON')
        else:
            keys_to_remove = ['created_at', 'updated_at', 'id', 'email']
            filtered_user = {key: value for key, value in user.items()
                             if key not in keys_to_remove}
            filtered_user['id'] = user_obj['id']
            filtered_user['email'] = user_obj['email']
            filtered_user['created_at'] = user_obj['created_at']
            updated_user = User(**filtered_user)
            storage.new(updated_user)
            storage.delete(user_obj)
            storage.save()
            return jsonify(updated_user.to_dict()), 200
    else:
        abort(404)
