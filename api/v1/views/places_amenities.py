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


@app_views.route("/places/<place_id>/amenities", methods=['GET'], strict_slashes=False)
def amenities_by_place(place_id=None):
    """Routes to return a list of Amenities of
    a specific Place with a given id."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    
    test = place.amenities

    list_amen = []
    for obj in test:
        list_amen.append(obj.to_dict())
    
    return jsonify(list_amen)


