#!/usr/bin/python3
"""Handle City API actions"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews/', methods=['GET'])
@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place_id(place_id):
    """Retrieve list of reviews of a place"""
    place_obj = storage.get(Place, place_id)
    if place_obj:
        reviews = [review.to_dict() for review in place_obj.reviews]
        return jsonify(reviews)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Retrieves a review by id"""
    review_obj = storage.get(Review, review_id)
    if review_obj:
        return jsonify(review_obj.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a review object"""
    review_obj = storage.get(Review, review_id)
    if review_obj:
        storage.delete(review_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
@app_views.route('/places/<place_id>/reviews/', methods=['POST'])
def create_review(place_id):
    """Creates a review"""
    place_obj = storage.get(Place, place_id)
    if place_obj and place_obj.id == place_id:
        review = request.get_json()
        if not review:
            abort(400, description='Not a JSON')
        if not review.get('user_id'):
            abort(400, description='Missing user_id')
        elif not storage.get(User, review.get('user_id')):
            abort(404)
        if not review.get('text'):
            abort(400, description='Missing text')
        else:
            # new_review = Review(text=review['text'], place_id=place_id,
            #                     user_id=review['user_id'])
            new_review = Review(**review)
            storage.new(new_review)
            storage.save()
            return jsonify(new_review.to_dict()), 201
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a review object"""
    review_obj = storage.get(Review, review_id)
    if review_obj:
        review = request.get_json()
        if not review:
            abort(400, description='Not a JSON')
        else:
            keys_to_remove = ['id', 'user_id', 'place_id', 'created_at',
                              'updated_at']
            filtered_review = {key: value for key, value in review.items()
                               if key not in keys_to_remove}
            for name, value in filtered_review.items():
                setattr(review_obj, name, value)
            # updated_review = Review(**filtered_review)
            # updated_review.save()
            # storage.new(updated_review)
            # storage.delete(review_obj)
            # storage.save()
            return jsonify(review_obj.to_dict()), 200
    else:
        abort(404)
