#!/usr/bin/python3
"""
Module that contains the route (/states)
it allow GET, DELETE, POST OR PUT an object
to the the storage engine (database of file).
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def all_states(state_id=None):
    """Route that returns a list of all states in
    the storage engine. or return a State with a
    given id"""
    if state_id is None:
        list_states = []
        for obj in storage.all(State).values():
            list_states.append(obj.to_dict())
        return jsonify(list_states)
    else:
        object = {}
        object = storage.get(State, state_id)
        if not object:
            abort(404)
        return jsonify(object.to_dict())


@app_views.route('/states/<state_id>',
                methods=['DELETE'], strict_slashes=False)
def del_state_id(state_id=None):
    """Route that delete a state from the
    storage engine with a given id"""
    object = {}
    object = storage.get(State, state_id)
    if not object:
        abort(404)
    storage.delete(object)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def new_state():
    """Route to add a new object State in a
    storage engine.
    args = Data input of body the
    post request.
    """
    args = request.get_json()

    if args is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in args:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_state = State(**args)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """Route to update an object with a given
    id in the storage engine"""
    search_object = storage.get(State, state_id)
    if not search_object:
        abort(404)
    args = request.get_json()
    if args is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in args.items():
        if key not in ["updated_at", "created_at", "id"]:
            setattr(search_object, key, value)
    storage.save()
    return make_response(jsonify(search_object.to_dict()), 200)
