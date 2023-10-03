#!/usr/bin/python3
"""Handle State API actions"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.state import State


# @app_views.errorhandler(400)
# def not_json(exception):
#     make_response('')


@app_views.route('/states', methods=['GET'])
@app_views.route('/states/', methods=['GET'])
def get_states():
    """Retrieve all States objects"""
    state_obj = storage.all('State')
    states_list = [val for val in state_obj.values()]
    return jsonify([state.to_dict() for state in states_list])


@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieve a given state"""
    state_obj = storage.get(State, state_id)
    if state_obj:
        return jsonify(state_obj.to_dict())
    else:
        abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete a State object"""
    state_obj = storage.get(State, state_id)
    if state_obj:
        storage.delete(state_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'])
@app_views.route('/states/', methods=['POST'])
def create_state():
    """Creates a State"""
    state = request.get_json()
    if not state:
        abort(400, description='Not a JSON')
    elif not state.get('name'):
        abort(400, description='Missing name')
    else:
        new_state = State(name=state['name'])
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a state object"""
    state_obj = storage.get(State, state_id)
    if state_obj:
        state = request.get_json()
        if not state:
            abort(400, description='Not a JSON')
        else:
            keys_to_remove = ['updated_at']
            filtered_state = {key: value for key, value in state_obj.to_dict()
                              .items()
                              if key not in keys_to_remove}
            filtered_state['name'] = state['name']
            new_state = State(**filtered_state)
            storage.new(new_state)
            storage.delete(state_obj)
            storage.save()
            return jsonify(new_state.to_dict()), 200
    else:
        abort(404)
