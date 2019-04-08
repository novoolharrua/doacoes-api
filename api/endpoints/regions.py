#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint, jsonify, request, abort, make_response
from models import region, calendar
from services import calendar_api
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
    region_name = body['name']
    region_address = body['address']

    _logger.info('Creating Region {}'.format(region_name))

    region_obj = region.create_region(region_name=region_name, address=region_address)
    if region_obj:
        result['id_region'] = region_obj.id
        result['name'] = region_obj.name
        result['address'] = region_obj.address

    _logger.info('Region {} created with id {}.'.format(region_name,region_obj.id))


    result['calendars'] = []

    for type in ['Clothing', 'Food', 'Others']:
        _logger.info('Creating {} calendar for region {}'.format(type, region_name))
        created_calendar_id = calendar_api.create_calendar(region_name, type)
        calendar_obj = calendar.create_calendar(region_obj.id,created_calendar_id, type.upper())
        calendar_dto = {
            'id': calendar_obj.id,
            'type': calendar_obj.type,
            'region_id': calendar_obj.region_id,
            'gcloud_url': calendar_obj.gcloud_id
        }
        result['calendars'].append(calendar_dto)
        _logger.info('{} calendar for region {} created with id {}'.format(type, region_name, calendar_obj.id))

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
        result['calendars'] = calendar.get_calendars_by_region(region_obj.id)
    return jsonify(result), 200

@blueprint.route('/region/<region_id>', methods=['DELETE', 'OPTIONS'])
def delete_region(region_id):
    result = {}
    region_obj = region.get_region(region_id)
    calendars = calendar.get_calendars_by_region(region_id)
    if region_obj:
        for calendar_obj in calendars:
            calendar_api.delete_calendar(calendar_obj['gcloud_id'])
        region.delete_region(region_obj.id)
        result['id_region'] = region_obj.id
        result['name'] = region_obj.name
        result['address'] = region_obj.address
        result['calendars'] = calendars
        return jsonify(result), 200
    else:
        endpoints_exception(404, "REGION_NOT_FOUND")

