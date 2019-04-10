#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint, jsonify, request, abort, make_response
from utils.date_utils import format_date_from_period, date_to_string, date_to_google
from models.calendar import get_calendar_by_region_and_type
from models.region import get_region
from services.calendar_api import post_event
import logging


_logger = logging.getLogger(__name__)

blueprint = Blueprint('events', __name__)


def endpoints_exception(code, msg):
    abort(make_response(jsonify(message=msg), code))

@blueprint.route('/region/<region_id>/event', methods=['POST', 'OPTIONS'])
def create_event(region_id):
    """
    account post must follow:
    {
      "start": "string",
      "stop": "string"
      "type": "string"
    }
    :return: a region entity

    """

    result = {}

    body = request.json
    date = body['date']
    period = body['period']
    donation_type = body['type']

    region = get_region(region_id)
    calendar = get_calendar_by_region_and_type(region_id, donation_type)

    start, stop = format_date_from_period(date, period)

    created_event = post_event(region, calendar,  date_to_google(start), date_to_google(stop))

    result['start'] = date_to_string(start)
    result['stop'] = date_to_string(stop)

    return jsonify(result), 200
