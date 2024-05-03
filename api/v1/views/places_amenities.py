#!/usr/bin/python3
"""places_amenities.py"""
from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.amenity import Amenity
from models.place import Place
from flasgger.utils import swag_from


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'])
@swag_from('documentation/place_amenity/get_id.yml', methods=['GET'])
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    
    if place is None:
        abort(404)
    
    if storage.__class__.__name__ == "DBStorage":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = []
        for amenity_id in place.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenities.append(amenity.to_dict())

    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'])
@swag_from('documentation/place_amenity/delete.yml', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """ Deletes an Amenity object from a Place """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'])
@swag_from('documentation/place_amenity/post.yml', methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    """ Links an Amenity object to a Place """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
