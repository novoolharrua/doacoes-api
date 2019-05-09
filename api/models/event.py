#!/usr/bin/env python
# -*- coding: utf-8 -*


"""
A model for the event entity.
"""

from services.database import get_db_instance
import logging
from models import calendar as calendar_model
from models import region as region_model
from models import institution as institution_model



_logger = logging.getLogger(__name__)
table_name = 'event'


class Event():
    def __init__(self, id, date, period, type, gcloud_id, calendar, institution, region):
        self.id = id
        self.date = date
        self.period = period
        self.gcloud_id = gcloud_id
        self.type = type
        self.calendar = calendar
        self.institution = institution
        self.region = region
    def __repr__(self):
        return "<Event(id='%d', region__name=%s, institution_name=%s)>" % (self.id, self.region.name, self.institution.name)


def parse_event_obj(db_row):
    id = db_row[0]
    date = db_row[1]
    period = db_row[2]
    gcloud_id = db_row[3]
    type = db_row[4]
    id_region = db_row[5]
    id_calendar = db_row[6]
    id_institution = db_row[7]
    calendar = calendar_model.get_calendar(id_calendar)
    institution = institution_model.get_institution(id_institution)
    region = region_model.get_region(id_region)

    event = Event(id=id, date=date, period=period, type=type, gcloud_id=gcloud_id, calendar=calendar,
                  institution=institution, region=region)
    return event


def create_event(date, period, type, gcloud_id, calendar, institution, region):
    db = get_db_instance()
    event = None
    try:
        with db.cursor() as cursor:
            # insert record
            sql = "INSERT INTO {} (DATE, PERIOD, GCLOUD_ID, TYPE, ID_CALENDAR, ID_INSTITUTION, ID_REGION)" \
                  " VALUES ('{}', '{}', '{}', '{}', {}, {}, {})"
            cursor.execute(sql.format(table_name, date, period, gcloud_id, type, calendar.id, institution.id, region.id))
            created_id = db.insert_id()
            cursor.execute('commit')
            event = Event(id=created_id, date=date, period=period, type=type, gcloud_id=gcloud_id,
                          calendar=calendar, institution=institution, region=region)
            return event
    finally:
        db.close()


def list_events(iid=None, rid=None, type=None, date=None):
    db = get_db_instance()
    data = []
    try:
        with db.cursor() as cursor:
            # Read all records
            sql = "select * from {} where GCLOUD_ID like '%'"
            if iid:
                sql += ' and ID_INSTITUTION = {}'.format(iid)
            if rid:
                sql += ' and ID_REGION = {}'.format(rid)
            if type:
                sql += ' and TYPE = "{}"'.format(type)
            if date:
                sql += ' and DATE >= "{}"'.format(date)
            cursor.execute(sql.format(table_name))
            result = cursor.fetchall()
            if result:
                for row in result:
                    event = parse_event_obj(row)
                    data.append(event)
                return data
            else:
                return None
    finally:
        db.close()


def get_event(event_id):
    db = get_db_instance()
    event = None
    try:
        with db.cursor() as cursor:
            # Read a single record
            sql = "select * from {} where ID_EVENT = {}"
            cursor.execute(sql.format(table_name, event_id, type))
            result = cursor.fetchone()
            if result:
                event = parse_event_obj(result)
            return event
    finally:
        db.close()

def delete_event(id):
    db = get_db_instance()
    try:
        with db.cursor() as cursor:
            # Remove a single record
            sql = "delete from {} where ID_EVENT = {}"
            cursor.execute(sql.format(table_name, id))
            cursor.execute('commit')
            return True
    finally:
        db.close()

def check_free(date, calendar, type):
    db = get_db_instance()
    event = None
    try:
        with db.cursor() as cursor:
            # Read a single record
            sql = "select * from {} where ID_REGION = {} and DATE = '{}' and TYPE = '{}'"
            cursor.execute(sql.format(table_name, calendar.id, date, type))
            result = cursor.fetchone()
            if not result:
                return True
            else:
                return False
    finally:
        db.close()