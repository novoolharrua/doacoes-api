#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint, jsonify, request, abort, make_response
from models import region
import logging


_logger = logging.getLogger(__name__)

blueprint = Blueprint('regions', __name__)


def endpoints_exception(code, msg):
    abort(make_response(jsonify(message=msg), code))

@blueprint.route('/region', methods=['POST', 'OPTIONS'])
def post_region():
    """
    account post must follow:
    {
      "name": "string",
      "address": "string"
    }
    :return: a region entity
    """
    body = request.json
    result = {}
    name = body['name']
    address = body['address']

    # region_obj = region.create_region(region_name=name, address=address)
    # if region_obj:
    #     result['id_region'] = region_obj.id
    #     result['name'] = region_obj.name
    #     result['address'] = region_obj.address


    result['calendars'] = []

    return jsonify(result), 200


@blueprint.route('/region', methods=['GET', 'OPTIONS'])
def list_regions():
    result = {}
    data = region.get_regions()
    result['data'] = data
    return jsonify(result), 200



@blueprint.route('/region/<region_id>', methods=['GET', 'OPTIONS'])
def get_region(region_id):
    result = {}
    region_obj = region.get_region(region_id)
    if region_obj:
        result['id_region'] = region_obj.id
        result['name'] = region_obj.name
        result['address'] = region_obj.address
    return jsonify(result), 200
