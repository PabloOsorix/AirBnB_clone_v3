#!/usr/bin/python3
"""
Initialice instance of Blueprint in app_views
variable."""
from api.v1.views.states import *
from api.v1.views.index import *
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
