#!/usr/bin/python3
"""places_amenities.py"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from flasgger.utils import swag_from


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'])
@app_views.route('/places/<place_id>/amenities/', methods=['GET'])
@swag_from('documentation/place_amenity/get_id.yml', methods=['GET'])
def list_amenities_of_place(place_id):
        ''' Retrieves a list of all Amenity objects of a Place '''
        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)
        list_amenities = []
        for obj in all_places:
            if obj.id == place_id:
                for amenity in obj.amenities:
                    list_amenities.append(amenity.to_dict())
        return jsonify(list_amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'])
@swag_from('documentation/place_amenity/delete.yml', methods=['DELETE'])
def delete_amenity(place_id, amenity_id):
    """ delete amenity from place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'])
@swag_from('documentation/place_amenity/post.yml', methods=['POST'])
def create_place_amenity(place_id, amenity_id):
        '''Creates a Amenity'''
        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)

        all_amenities = storage.all("Amenity").values()
        amenity_obj = [obj.to_dict() for obj in all_amenities
                       if obj.id == amenity_id]
        if amenity_obj == []:
            abort(404)

        amenities = []
        for place in all_places:
            if place.id == place_id:
                for amenity in all_amenities:
                    if amenity.id == amenity_id:
                        place.amenities.append(amenity)
                        storage.save()
                        amenities.append(amenity.to_dict())
                        return jsonify(amenities[0]), 200
        return jsonify(amenities[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_place_amenity(amenity_id):
    '''Retrieves a Amenity object '''
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    return jsonify(amenity_obj[0])
