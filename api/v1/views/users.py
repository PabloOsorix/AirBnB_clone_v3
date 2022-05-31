#!/usr/bin/python3
"""
Module that contains the RESTfull API actions
to user object it allow GET, DELETE, POST OR PUT
to the the storage engine (database of file).
"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort


@app_views.route("/users", methods=['GET'], strict_slashes=False)
@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def users_or_user(user_id=None):
    """Routes to return a list of Users or
    a specific User with a given id."""
    if user_id is None:
        list_users = []
        for obj in storage.all(User).values():
            list_users.append(obj.to_dict())
        return jsonify(list_users)
    else:
        """Return a User with a given id"""
        user = {}
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id=None):
    """Route that delete an user with a given
    id.
    (Object Class User) del_user = user to
                        delete."""
    del_user = {}
    del_user = storage.get(User, user_id)
    if not del_user:
        abort(404)
    storage.delete(del_user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def new_user():
    """Route to create a new User in the storage
    engine.
    (dict) inf_user = information from body request
    that we need to create a new object (register)
    User."""
    inf_user = request.get_json
    if not inf_user:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in inf_user:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in inf_user:
        return make_response(jsonify({"error": "Missing password"}), 400)
    new_user = User(**inf_user)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    """Route to update an User with a given id
    (Object Class User)user_to_upd = User to
    update.
    (dict) inf_user = information from body request
    that we need to update the User (register).
    """
    user_to_upd = storage.get(User, user_id)
    if not user_to_upd:
        abort(404)
    inf_user = request.get_json()
    if not inf_user:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in inf_user.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user_to_upd, key, value)
    storage.save()
    return make_response(jsonify(user_to_upd.to_dict()), 200)
