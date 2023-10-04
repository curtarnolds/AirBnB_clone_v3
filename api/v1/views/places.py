#!/usr/bin/python3
"""Handle Place API actions"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city_id(city_id):
    """Retrieve list of places of a city"""
    city_obj = storage.get(City, city_id)
    if city_obj:
        places = [place.to_dict() for place in city_obj.places if len(city_obj.places) > 0]
        if
        return jsonify(places)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a place by id"""
    place_obj = storage.get(Place, place_id)
    if place_obj:
        return jsonify(place_obj.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a place object"""
    place_obj = storage.get(Place, place_id)
    if place_obj:
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place in a specified city"""
    city_obj = storage.get(City, city_id)
    if city_obj:
        place = request.get_json()
        if not place:
            abort(400, description='Not a JSON')
        if not place.get('user_id'):
            abort(400, description='Missing user_id')
        if not storage.get(User, place.get('user_id')):
            abort(404)
        if not place.get('name'):
            abort(400, description='Missing name')
        else:
            new_place = Place(name=place['name'], city_id=city_id,
                              user_id=place.get('user_id'))
            storage.new(new_place)
            storage.save()
            return jsonify(new_place.to_dict()), 201
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a place object"""
    place_obj = storage.get(Place, place_id)
    if place_obj:
        place = request.get_json()
        if not place:
            abort(400, description='Not a JSON')
        else:
            keys_to_remove = ['updated_at', 'id', 'user_id', 'city_id',
                              'created_at']
            filtered_place = {key: value for key, value in place.items()
                              if key not in keys_to_remove}
            for key, value in place_obj.to_dict().items():
                if key in keys_to_remove and key != 'updated_at':
                    setattr(filtered_place, key, value)
            storage.new(filtered_place)
            storage.delete(place_obj)
            storage.save()
            return jsonify(filtered_place.to_dict()), 200
            # new_place = Place(**filtered_place)
            # storage.new(new_place)
            # storage.delete(place_obj)
            # storage.save()
            # return jsonify(new_place.to_dict()), 200
    else:
        abort(404)
