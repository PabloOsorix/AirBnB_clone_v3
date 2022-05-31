#!/usr/bin/python3
"""
Module that contains the RESTfull API actions
to user object it allow GET, DELETE, POST OR PUT
to the the storage engine (database of file).
"""
from models import storage
from models.amenity import Amenity
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from os import getenv


@app_views.route("/places/<place_id>/amenities",
                 methods=['GET'], strict_slashes=False)
def amenities_by_place(place_id=None):
    """Routes to return a list of Amenities of
    a specific Place with a given id."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    objs = place.amenities

    list_amen = []
    for obj in objs:
        list_amen.append(obj.to_dict())

    return jsonify(list_amen)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def del_amenity(place_id=None, amenity_id=None):
    """Deletes an Amenity from a selected Place
     with a given id."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenenity = storage.get(Amenity, amenity_id)
    if not amenenity:
        abort(404)

    objs = place.amenities

    for obj in objs:
        if obj.id == amenity_id:
            place.amenities.remove(obj)
            flag = 1
            break
        else:
            flag = 0

    if flag == 1:
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['POST'], strict_slashes=False)
def link_amenity(place_id=None, amenity_id=None):
    """Links an Amenity from a selected Place
     with a given id."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenenity = storage.get(Amenity, amenity_id)
    if not amenenity:
        abort(404)

    objs = place.amenities

    for obj in objs:
        if obj.id == amenity_id:
            return make_response(jsonify(obj.to_dict()), 200)

    place.amenities.append(amenenity)

    return make_response(jsonify(amenenity.to_dict()), 201)
