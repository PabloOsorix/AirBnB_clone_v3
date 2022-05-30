#!/usr/bin/python3
"""Module with a Blueprint object that have one
route with /status lie an end point"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """Return JSON with the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Route that return the number of each object
    by type"""
    number_of_objects = {
        "amenities": len(storage.all("Amenity")),
        "cities": len(storage.all("City")),
        "places": len(storage.all("Place")),
        "reviews": len(storage.all("Review")),
        "states": len(storage.all("State")),
        "users": len(storage.all("User"))
        }
    return jsonify(number_of_objects)
