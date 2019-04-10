#!/usr/bin/env python
# -*- coding: utf-8 -*

"""
A model for the region entity.
"""

from services.database import get_db_instance
import logging

_logger = logging.getLogger(__name__)
table_name = 'calendar'

class Calendar():
    def __init__(self, id, region_id, gcloud_id, type):
        self.id = id
        self.region_id = region_id
        self.gcloud_id = gcloud_id
        self.type = type

    def __repr__(self):
        return "<Calendar(id='%s', region_id=%s, type=%s)>" % (self.id, self.region_id, self.type)


def create_calendar(region_id, gcloud_id, type):
    db = get_db_instance()
    calendar = None
    try:
        with db.cursor() as cursor:
            # insert record
            sql = "INSERT INTO {} (ID_REGION, GCLOUD_ID, TYPE) VALUES ({}, '{}', '{}')"
            cursor.execute(sql.format(table_name, region_id, gcloud_id, type))
            created_id = db.insert_id()
            cursor.execute('commit')
            calendar = Calendar(id=created_id, region_id=region_id, gcloud_id=gcloud_id, type=type)
            return calendar
    finally:
        db.close()


def get_calendars_by_region(region_id):
    db = get_db_instance()
    data = []
    try:
        with db.cursor() as cursor:
            # Read a single record
            sql = "select * from {} where ID_REGION = {}"
            cursor.execute(sql.format(table_name, region_id))
            result = cursor.fetchall()
            for row in result:
                data.append({
                    'calendar_id': row[0],
                    'type': row[1],
                    'gcloud_id': row[2]
                })
            return data
    finally:
        db.close()


def get_calendar_by_region_and_type(region_id, type):
    db = get_db_instance()
    calendar = None
    try:
        with db.cursor() as cursor:
            # Read a single record
            sql = "select * from {} where ID_REGION = {} and TYPE like '{}'"
            cursor.execute(sql.format(table_name, region_id, type))
            result = cursor.fetchone()
            calendar = Calendar(id=result[0], region_id=result[3], gcloud_id=result[2], type=result[1])
            return calendar
    finally:
        db.close()