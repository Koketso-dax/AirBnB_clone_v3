#!/usr/bin/python3
"""Return OK if api is running with no issue."""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns status OK"""
    return jsonify({"status": "OK"})
