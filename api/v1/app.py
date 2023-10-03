#!/usr/bin/python3
"""A sample flask app
"""
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Custom 404
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def close_db(exception):
    """Close the database
    """
    storage.close()


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', 5000)), threaded=True)
