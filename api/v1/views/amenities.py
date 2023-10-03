#!/usr/bin/python3
"""Handle Amenity API actions"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """Retrieve list of all amenities"""
    amenity_obj = storage.all('Amenity')
    amenities_list = [amenity.to_dict() for amenity in amenity_obj.values()]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """Retrieves an amenity by id"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj:
        return jsonify(amenity_obj.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_by_id(amenity_id):
    """Delete a amenity object"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj:
        storage.delete(amenity_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'])
@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """Creates an amenity"""
    amenity = request.get_json()
    if not amenity:
        abort(400, description='Not a JSON')
    elif not amenity.get('name'):
        abort(400, description='Missing name')
    else:
        new_amenity = Amenity(name=amenity['name'])
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity_by_id(amenity_id):
    """Updates a amenity object"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj:
        amenity = request.get_json()
        if not amenity:
            abort(400, description='Not a JSON')
        else:
            keys_to_remove = ['updated_at']
            filtered_amenity = {key: value for key, value in amenity_obj
                                .to_dict()
                                .items()
                                if key not in keys_to_remove}
            filtered_amenity['name'] = amenity['name']
            new_amenity = amenity(**filtered_amenity)
            storage.new(new_amenity)
            storage.delete(amenity_obj)
            storage.save()
            return jsonify(new_amenity.to_dict()), 200
    else:
        abort(404)
