#!/usr/bin/env python
# -*- coding: utf-8 -*

"""
A model for the region entity.
"""

from services.database import get_db_instance
import logging

_logger = logging.getLogger(__name__)
table_name = 'region'


class Region():
    def __init__(self, id, name, address, population):
        self.id = id
        self.name = name
        self.address = address
        self.population = population

    def __repr__(self):
        return "<Region(name='%s', adress='%s')>" % (self.name, self.address)


def create_region(region_name, address, population):
    db = get_db_instance()
    region = None
    try:
        with db.cursor() as cursor:
            # insert record
            sql = "INSERT INTO {} (NAME, ADDRESS, POPULATION) VALUES ('{}', '{}', {})"
            cursor.execute(sql.format(table_name, region_name, address, population))
            created_id = db.insert_id()
            cursor.execute('commit')
            region = Region(id=created_id, address=address, name=region_name, population=population)
            return region
    finally:
        db.close()

def get_regions():
    db = get_db_instance()
    data = []
    try:
        with db.cursor() as cursor:
            # Read all records
            sql = "select * from {}"
            cursor.execute(sql.format(table_name))
            result = cursor.fetchall()
            if result:
                for row in result:
                    data.append({
                        'id_region': row[0],
                        'name': row[1],
                        'address': row[2],
                        'population': row[3]
                    })
                return data
            else:
                return None
    finally:
        db.close()

def get_region(id):
    db = get_db_instance()
    region = None
    try:
        with db.cursor() as cursor:
            # Read a single record
            sql = "select * from {} where ID_REGION = {}"
            cursor.execute(sql.format(table_name, id))
            result = cursor.fetchall()[0]
            if result:
                region = Region(id=result[0], address=result[1], name=result[2], population=result[3])
                return region
            else:
                return None
    finally:
        db.close()

def delete_region(id):
    db = get_db_instance()
    try:
        with db.cursor() as cursor:
            # Remove a single record
            sql = "delete from {} where ID_REGION = {}"
            cursor.execute(sql.format(table_name, id))
            cursor.execute('commit')
            return True
    finally:
        db.close()


