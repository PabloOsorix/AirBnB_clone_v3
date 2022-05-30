#!/usr/bin/python3
"""Module that initialice a flask web instance
it contain one route 
"""
from concurrent.futures import thread
from os import getenv
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(execute):
    """Instance that close conection with engine"""
    storage.close()


if __name__ == "__main__":
    env_host = getenv("HBNB_API_HOST", default="0.0.0.0")
    env_port = getenv("HBNB_API_PORT", default=5000)
    app.run(host=env_host, port=int(env_port), threaded=True)
