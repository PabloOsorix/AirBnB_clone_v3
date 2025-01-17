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
from models.state import State
from models.amenity import Amenity
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


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """ retrieves all Place objects depending
    of the JSON in the body of the request
    """
    info = request.get_json()
    if info is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    len_total = 0
    if "states" in info.keys():
        list_states = info["states"]
        len_total += len(list_states)
    if "cities" in info.keys():
        list_cities = info["cities"]
        len_total += len(list_cities)
    if "amenities" in info.keys():
        list_amenities = info["amenities"]
        len_total += len(list_amenities)

    if len(info.keys()) == 0 or len_total == 0:
        list_places = []
        for obj in storage.all(Place).values():
            list_places.append(obj.to_dict())
        return jsonify(list_places)

    list_places = []

    if "states" in info.keys():
        for state_id in list_states:
            state = storage.get(State, state_id)
            for city in storage.all(City).values():
                if city.state_id == state.id:
                    for place in storage.all(Place).values():
                        if place.city_id == city.id:
                            list_places.append(place)

    if "cities" in info.keys():
        for city_id in list_cities:
            city = storage.get(City, city_id)
            if "states" in info.keys():
                if city.state_id not in list_states:
                    for place in storage.all(Place).values():
                        if place.city_id == city.id:
                            list_places.append(place)
            else:
                for place in storage.all(Place).values():
                    if place.city_id == city.id:
                        list_places.append(place)

    to_print = []
    if len(list_places) == 0 and len(info.keys()) > 0:
        for obj in storage.all(Place).values():
            list_places.append(obj)

    if "amenities" in info.keys():
        for place in list_places:
            count = 0
            for amenity_id in list_amenities:
                amenity = storage.get(Amenity, amenity_id)
                if amenity in place.amenities:
                    count += 1
            if count == len(list_amenities):
                to_print.append(place)
    else:
        to_print = list_places

    new_dict = []

    for place in to_print:
        new_dict.append(place.to_dict())

    for i in new_dict:
        if "amenities" in i.keys():
            del i["amenities"]

    return jsonify(new_dict)
