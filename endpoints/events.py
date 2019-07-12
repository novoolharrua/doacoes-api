#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint, jsonify, request, abort, make_response
from utils.date_utils import format_date_from_period, date_to_string, date_to_google
from models.calendar import get_calendar_by_region_and_type, get_calendars_by_region
from models.region import get_region
from models.institution import get_institution
from models import event as event_model
from services.calendar_api import post_event as create_gcloud_event
from services.calendar_api import delete_event as delete_gcloud_event
import datetime
import logging


_logger = logging.getLogger(__name__)

blueprint = Blueprint('events', __name__)


def endpoints_exception(code, msg):
    abort(make_response(jsonify(message=msg), code))


def find_calendar_based_on_type(donation_type, region_id):
    if donation_type in ['FOOD', 'CLOTHING', 'RELIGION']:
        return get_calendar_by_region_and_type(region_id, donation_type)
    else:
        return get_calendar_by_region_and_type(region_id, 'OTHERS')


def to_dict(event):
    dict_format = {}
    dict_format['id'] = event.id
    dict_format['gcloud_id'] = event.gcloud_id
    if isinstance(event.date, datetime.date):
        dict_format['date'] = '{}-{}-{}'.format(event.date.year, event.date.month, event.date.day)
    else:
        dict_format['date'] = event.date
    dict_format['period'] = event.period
    dict_format['type'] = event.type
    dict_format['region'] = {
        'region_id': event.region.id,
        'region_address': event.region.address,
        'region_name': event.region.name
    }
    dict_format['institution'] = {
        'institution_id': event.institution.id,
        'institution_name': event.institution.name,
        'institution_email': event.institution.email
    }

    return dict_format

@blueprint.route('/event', methods=['POST'])
def post_event():
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

    institution = get_institution(request.args.get('iid'))
    region = get_region(request.args.get('rid'))
    calendar = find_calendar_based_on_type(donation_type, region.id)

    if not event_model.check_free(date, calendar, donation_type):
        endpoints_exception(409, "EVENT_CONFLICT_IN_TIMESLOT")

    start, stop = format_date_from_period(date, period)
    created_event = create_gcloud_event(region, calendar, institution, donation_type, date_to_google(start), date_to_google(stop))
    event = event_model.create_event(date=date, period=period, type=donation_type, gcloud_id=created_event['id'],
                                     calendar=calendar, institution=institution, region=region)

    result = to_dict(event)
    return jsonify(result), 200


@blueprint.route('/event', methods=['GET', 'OPTIONS'])
def get_events():
    result = {}
    result['data'] =[]
    iid = request.args.get('iid')
    rid = request.args.get('rid')
    type = request.args.get('type')
    date = request.args.get('date')
    events = event_model.list_events(iid=iid, rid=rid, type=type, date=date)
    if events:
        for event in events:
            result['data'].append(to_dict(event))

    return jsonify(result), 200


@blueprint.route('/event/<event_id>', methods=['GET', 'OPTIONS'])
def get_event(event_id):
    result = {}
    event = event_model.get_event(event_id)
    if event:
        result = to_dict(event)
    else:
        endpoints_exception(404, "EVENT_NOT_FOUND")

    return jsonify(result), 200



@blueprint.route('/event/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    result = {}
    event = event_model.get_event(event_id)
    if event:
        delete_gcloud_event(event.calendar.gcloud_id, event.gcloud_id)
        event_model.delete_event(event.id)
        result = to_dict(event)
        return jsonify(result), 200
    else:
        endpoints_exception(404, "EVENT_NOT_FOUND")

