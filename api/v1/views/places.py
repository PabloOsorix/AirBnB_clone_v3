#!/usr/bin/python3
"""
Module that contains the RESTfull API actions
to user object it allow GET, DELETE, POST OR PUT
to the the storage engine (database of file).
"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_by_city(city_id=None):
    """Route that returns all places associated
    to a (given) city_id."""
    city = storage.get(City, city_id)
    if not city or not city_id:
        abort(404)
    list_places = []
    for key in storage.all(Place).values():
        if key.city_id == city_id:
            list_places.append(key.to_dict())
    return jsonify(list_places)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def place_by_id(place_id=None):
    """Return a User with a given id"""
    wanted_place = {}
    wanted_place = storage.get(Place, place_id)
    if not wanted_place:
        abort(404)
    return jsonify(wanted_place.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id=None):
    """Route that delete a place with a given
    id.
    (Object Class Place) del_place = place to
                        delete."""
    del_place = {}
    del_place = storage.get(Place, place_id)
    if not del_place:
        abort(404)
    storage.delete(del_place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def new_place(city_id=None):
    """Route to add a new place in a City by a
    given city id.
    (json) inf_place = input information to create
           new Place object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    inf_place = request.get_json()
    if not inf_place:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in inf_place:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, inf_place.get("user_id"))
    if not user:
        abort(404)
    if "name" not in inf_place:
        return make_response(jsonify({"error": "Missing name"}), 400)

    inf_place["city_id"] = city_id
    new_place = Place(**inf_place)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id=None):
    """Route to update a Place with a given id
    (Object Class Place)place_to_upd = Place to
    update.
    (dict) inf_place = information from body request
    that we need to update the Place (register).
    """
    place_to_upd = storage.get(Place, place_id)
    if not place_to_upd:
        abort(404)
    inf_place = request.get_json()
    if inf_place is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in inf_place.items():
        if key not in ["id", "user_id", "created_at", "updated_at", "city_id"]:
            setattr(place_to_upd, key, value)
    storage.save()
    return make_response(jsonify(place_to_upd.to_dict()), 200)
