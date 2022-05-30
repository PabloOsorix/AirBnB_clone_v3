#!/usr/bin/python3
"""Module that initialice a flask web instance
it contain one route.
"""
from os import getenv
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(e):
    """Handler to the error 404 when a url(uri) is not
    found"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close(execute):
    """Instance that close conection with engine"""
    storage.close()


if __name__ == "__main__":
    env_host = getenv("HBNB_API_HOST", default="0.0.0.0")
    env_port = getenv("HBNB_API_PORT", default=5000)
    app.run(host=env_host, port=int(env_port), threaded=True)
