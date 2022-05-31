#!/usr/bin/python3
"""
Module that contains all default RESTful API
actions for the Amenity objects
"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def all_amenities(amenity_id=None):
    """Route that return all Amenity objects
    from the storage engine of just one with a
    given id.
    (objects of class Amenity) amenities = list
                               of all amenities"""
    if amenity_id is None:
        amenities = []
        for obj in storage.all(Amenity).values():
            amenities.append(obj.to_dict())
        return jsonify(amenities)
    else:
        wanted_amenity = storage.get(Amenity, amenity_id)
        if not wanted_amenity:
            abort(404)
        return jsonify(wanted_amenity.to_dict())

@app_views.route("amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id=None):
    """Route that DELETE an Amenity object
    with a given amenity_id.
    (Object class Amenity) del_amenity =
    object to delete by a given id"""
    del_amenity = storage.get(Amenity, amenity_id)
    if not del_amenity:
        abort(404)
    storage.delete(del_amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def add_amenity():
    """Route that adds a new amenity in the
    storage engine.
    (dict) inf_amenity = input information with which
    we create the new amenity"""
    inf_amenity = request.get_json()
    if not inf_amenity:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in inf_amenity:
        return make_response(jsonify({"error": "Missing name"}))

    new_amenity = Amenity(**inf_amenity)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)

@app_views.route("amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """Route that updates an Amenity with a
    given id.
    (dict) inf_amenity = input information with which
    we update the intended amenity.
    (Object class Amenity) amenity_to_upd =
    amenity to update."""
    amenity_to_upd = storage.get(Amenity, amenity_id)
    if not amenity_to_upd:
        abort(404)

    inf_amenity = request.get_json()
    if not inf_amenity:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in inf_amenity.items():
        if key not in ["updated_at", "created_at", "id"]:
            setattr(amenity_to_upd, key, value)
    storage.save()
    return make_response(jsonify(amenity_to_upd.to_dict()), 200)
