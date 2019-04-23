#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint, jsonify, request, abort, make_response
from utils.date_utils import format_date_from_period, date_to_string, date_to_google
from models.calendar import get_calendar_by_region_and_type, get_calendars_by_region
from models.region import get_region
from models.institution import get_institution
from models import event as event_model
from services.calendar_api import post_event as create_gcloud_event
import logging


_logger = logging.getLogger(__name__)

blueprint = Blueprint('events', __name__)


def endpoints_exception(code, msg):
    abort(make_response(jsonify(message=msg), code))

def check_free():
    return True

def to_dict(event):
    dict_format = {}
    dict_format['id'] = event.id
    dict_format['gcloud_id'] = event.gcloud_id
    dict_format['date'] = event.date
    dict_format['period'] = event.period
    dict_format['type'] = event.type
    dict_format['calendar_id'] = event.calendar.id
    dict_format['institution'] = event.institution.name

    return dict_format

@blueprint.route('/region/<region_id>/event', methods=['POST', 'OPTIONS'])
def post_event(region_id):
    """
    date, period, type, gcloud_id, calendar, institution
    account post must follow:
    {
      "date": "string",
      "period": "string"
      "type": "string",

    }
    :return: a region entity

    """
    result = {}

    body = request.json
    date = body['date']
    period = body['period']
    donation_type = body['type']

    if not check_free():
        endpoints_exception(409, "EVENT_ALREADY_IN_TIMESLOT")

    institution = get_institution(request.args.get('iid'))
    region = get_region(region_id)

    if donation_type in ['FOOD', 'CLOTHING', 'RELIGION']:
        calendar = get_calendar_by_region_and_type(region_id, donation_type)
    else:
        calendar = get_calendar_by_region_and_type(region_id, 'OTHERS')

    start, stop = format_date_from_period(date, period)
    created_event = create_gcloud_event(region, calendar, institution, donation_type, date_to_google(start), date_to_google(stop))
    event = event_model.create_event(date=date, period=period, type=donation_type, gcloud_id=created_event['id'],
                                     calendar=calendar, institution=institution)

    result = to_dict(event)
    return jsonify(result), 200


@blueprint.route('/region/<region_id>/event', methods=['GET', 'OPTIONS'])
def get_institutions(region_id):
    result = {}
    data = []
    calendars = get_calendars_by_region(region_id)
    for calendar in calendars:
        data.append(event_model.get_events_by_calendar_id(calendar['id']))

    return jsonify(result), 200