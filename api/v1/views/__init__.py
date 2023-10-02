#!/usr/bin/python3
"""A simple views package"""
from api.v1.views.index import *  # noqa
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
