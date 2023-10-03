#!/usr/bin/python3
"""Handle City API actions"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state_id(state_id):
    """Retrieve list of cities of a State"""
    state_obj = storage.get(State, state_id)
    if state_obj:
        cities = [city.to_dict() for city in state_obj.cities]
        return jsonify(cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a city by id"""
    city_obj = storage.get(City, city_id)
    if city_obj:
        return jsonify(city_obj.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a City object"""
    city_obj = storage.get(City, city_id)
    if city_obj:
        storage.delete(city_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    """Creates a City"""
    state_obj = storage.get(State, state_id)
    if state_obj and state_obj.id == state_id:
        city = request.get_json()
        if not city:
            abort(400, description='Not a JSON')
        elif not city.get('name'):
            abort(400, description='Missing name')
        else:
            new_city = City(name=city['name'], state_id=state_id)
            storage.new(new_city)
            storage.save()
            return jsonify(new_city.to_dict()), 201
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a city object"""
    city_obj = storage.get(City, city_id)
    if city_obj:
        city = request.get_json()
        if not city:
            abort(400, description='Not a JSON')
        else:
            keys_to_remove = ['updated_at']
            filtered_city = {key: value for key, value in city_obj.to_dict()
                             .items()
                             if key not in keys_to_remove}
            filtered_city['name'] = city['name']
            new_city = City(**filtered_city)
            storage.new(new_city)
            storage.delete(city_obj)
            storage.save()
            return jsonify(new_city.to_dict()), 200
    else:
        abort(404)
