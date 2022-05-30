#!/usr/bin/python3
"""
Module that contains the route (/states)
it allow GET, DELETE, POST OR PUT an object
to the the storage engine (database of file).
"""
from api.v1.app import page_not_found
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Route that returns a list of all states in
    the storage engine."""
    list_states = []
    for obj in storage.all(State).values():
        list_states.append(obj.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    """Route that returns a state of the
    storage engine with a given id."""
    try:
        object = {}
        object = storage.get(State, state_id)
        if object is not None:
            return jsonify(object.to_dict())
        abort(404)
    except Exception:
        return abort(404)


@app_views.route('/states/<state_id>',
                methods=['DELETE'], strict_slashes=False)
def del_state_id(state_id):
    """Route that delete a state from the
    storage engine with a given id"""
    object = {}
    object = storage.get(State, state_id)
    if object:
        storage.delete(object)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def new_state():
    """Route to add a new object State in a
    storage engine.
    args = Data input of body the
    post request.
    """
    try:
        args = request.get_json()
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if args.get("name") is None or args.get("name") == "":
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_state = State(**args)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Route to update an object with a given
    id in the storage engine"""
    search_object = storage.get(State, state_id)
    if search_object is None:
        abort(404)
    try:
        args = request.get_json()
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in args.items():
        if key != ["updated_at", "created_at", "id"]:
            setattr(search_object, key, value)
    storage.save()
    return make_response(jsonify(search_object.to_dict()), 200)
