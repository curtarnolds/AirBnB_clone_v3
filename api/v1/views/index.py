#!/usr/bin/python3
"""An index module"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return api status"""
    return jsonify({
        "status": "OK",
        })
