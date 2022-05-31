#!/usr/bin/python3
"""
Module that contains all default RESTful API
actions for the Review objects
"""
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort


@app_views.route("places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews_by_place(place_id=None):
    """Route that returns all reviews associated
    to a (given) place_id."""
    place = storage.get(Place, place_id)
    if not place or not place_id:
        abort(404)
    list_reviews = []
    for key in storage.all(Review).values():
        if key.place_id == place.id:
            list_reviews.append(key.to_dict())
    return jsonify(list_reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def review_by_id(review_id=None):
    """Route that return a review with a given id
    (object class Review) wanted_review = searched
                        review"""
    wanted_review = {}
    wanted_review = storage.get(Review, review_id)
    if not wanted_review:
        abort(404)
    return jsonify(wanted_review.to_dict())


route = "reviews/<review_id>"
@app_views.route(route, methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """Route that delete a review from the storage
    engine with a given id.
    (Object of class Review) review_to_del = review to
                           delete"""
    review_to_del = storage.get(Review, review_id)
    if not review_to_del:
        abort(404)
    storage.delete(review_to_del)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def new_review(place_id):
    """Route to add a new review in a Place by a
    given place id.
    (json) inf_review = input information to create
           new review object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    inf_review = request.get_json()
    if not inf_review:
        return make_response(jsonify({"errorr": "Not a JSON"}), 400)

    if "user_id" not in inf_review:
        return make_response(jsonify({"errorr": "Missing user_id"}), 400)
    user = storage.get(User, inf_review.get("user_id"))
    if not user:
        abort(404)

    if "text" not in inf_review:
        return make_response(jsonify({"error": "Missing text"}), 400)

    inf_review["place_id"] = place_id
    new_review = Review(**inf_review)
    storage.new(new_review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id=None):
    """Route that updates review information
    through a given id.
        (obj class Review) review_to_upd = review
        to update.
        (json) inf_review = input information to update
        selected review (review_to_upd)"""
    review_to_upd = storage.get(Review, review_id)
    if not review_to_upd:
        abort(404)

    inf_review = request.get_json()
    if not inf_review:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in inf_review.items():
        attrs = ["id", "user_id", "created_at", "updated_at", "place_id"]
        if key not in attrs:
            setattr(review_to_upd, key, value)
    storage.save()
    return make_response(jsonify(review_to_upd.to_dict()), 200)
