#!/usr/bin/python3
"""An index module
"""
from flask import jsonify

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return api status"""
    return jsonify({
        "status": "OK",
        })


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Retrieve the number of each object by type"""
    stats_by_storage = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }
    return jsonify(stats_by_storage)
