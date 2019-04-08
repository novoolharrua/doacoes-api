#!/usr/bin/env python
# -*- coding: utf-8 -*

"""
A model for the region entity.
"""

from services.database import get_db_instance
import logging

_logger = logging.getLogger(__name__)
table_name = 'calender'

class Calendar():
    def __init__(self, id, region_id, gcloud_calendar_id, type):
        self.id = id
        self.region_id = region_id
        self.gcloud_calendar_id = gcloud_calendar_id
        self.type = type

    def __repr__(self):
        return "<Region(name='%s', adress=%s)>" % (self.name, self.name)


def create_calendar(region_id, gcloud_calendar_id, type):
    db = get_db_instance()
    region = None
    try:
        with db.cursor() as cursor:
            # insert record
            sql = "INSERT INTO {} (ID_REGION, GCLOUD_URL, TYPE) VALUES ('{}', '{}', '{}')"
            print(sql.format(table_name, region_id, gcloud_calendar_id, type))
            cursor.execute(sql.format(sql.format(table_name, region_id, gcloud_calendar_id, type)))
            created_id = db.insert_id()
            cursor.execute('commit')
            calendar = Calendar(id=created_id, region_id=region_id, gcloud_calendar_id=gcloud_calendar_id, type=type)
            return calendar
    finally:
        db.close()


def get_calendars_by_region(region_id):
    db = get_db_instance()
    region = None
    try:
        with db.cursor() as cursor:
            # Read a single record
            sql = "select * from {} where ID_REGION = {}"
            cursor.execute(sql.format(table_name, id))
            result = cursor.fetchall()[0]
            region = Calendar(id=result[0], address=result[1], name=result[2])
            return region
    finally:
        db.close()


