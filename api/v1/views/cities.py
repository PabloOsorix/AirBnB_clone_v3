#!/usr/bin/python3
"""
Module that contains all default RESTful API
actions for the City objects
"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort


@app_views.route("states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def cities_by_state(state_id=None):
    """Route that returns all cities associated
    to a (given) state_id."""
    state = storage.get(State, state_id)
    if not state or not state_id:
        abort(404)
    list_cities = []
    for key in storage.all(City).values():
        if key.state_id == state.id:
            list_cities.append(key.to_dict())
    return jsonify(list_cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city_by_id(city_id=None):
    """Route that return a city with a given id
    (object class City) wanted_city = searched
                        city"""
    wanted_city = {}
    wanted_city = storage.get(City, city_id)
    if not wanted_city:
        abort(404)
    return jsonify(wanted_city.to_dict())


@app_views.route("cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Route that delete a city from the storage
    engine with a given id.
    (Object of class City) city_to_del = city to
                           delete"""
    city_to_del = storage.get(City, city_id)
    if not city_to_del:
        abort(404)
    storage.delete(city_to_del)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def new_city(state_id):
    """Route to add a new city in a State by a
    given state id.
    (json) inf_city = input information to create
           new City object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    inf_city = request.get_json()
    if not inf_city:
        return make_response(jsonify({"errorr": "Not a JSON"}), 400)
    if "name" not in inf_city:
        return make_response(jsonify({"error": "Missing name"}), 400)

    inf_city["state_id"] = state_id
    new_city = City(**inf_city)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id=None):
    """Route that updates city information
    through a given id.
        (obj class City) city_to_upd = city
        to update.
        (json) inf_city = input information to update
        selected city (city_to_upd)"""
    city_to_upd = storage.get(City, city_id)
    if not city_to_upd:
        abort(404)

    inf_city = request.get_json()
    if not inf_city:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in inf_city.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city_to_upd, key, value)
    storage.save()
    return make_response(jsonify(city_to_upd.to_dict()), 200)
