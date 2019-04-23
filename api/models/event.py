#!/usr/bin/env python
# -*- coding: utf-8 -*
from models import calendar as calendar_model, institution as institution_model

"""
A model for the event entity.
"""

from services.database import get_db_instance
import logging

_logger = logging.getLogger(__name__)
table_name = 'event'


class Event():
    def __init__(self, id, date, period, type, gcloud_id, calendar, institution):
        self.id = id
        self.date = date
        self.period = period
        self.gcloud_id = gcloud_id
        self.type = type
        self.calendar = calendar
        self.institution = institution

    def __repr__(self):
        return "<Event(id='%d', region_id=%s, type=%s)>" % (self.id, self.region_id, self.type)


def create_event(date, period, type, gcloud_id, calendar, institution):
    db = get_db_instance()
    event = None
    try:
        with db.cursor() as cursor:
            # insert record
            sql = "INSERT INTO {} (DATE, PERIOD, GCLOUD_ID, TYPE, ID_CALENDAR, ID_INSTITUTION)" \
                  " VALUES ('{}', '{}', '{}', '{}', {}, {})"
            cursor.execute(sql.format(table_name, date, period, gcloud_id, type, calendar.id, institution.id))
            created_id = db.insert_id()
            cursor.execute('commit')
            event = Event(id=created_id, date=date, period=period, type=type, gcloud_id=gcloud_id,
                          calendar=calendar, institution=institution)
            return event
    finally:
        db.close()


def get_events_by_calendar_id(calendar_id):
