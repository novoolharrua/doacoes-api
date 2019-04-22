#!/usr/bin/env python
# -*- coding: utf-8 -*

"""
A model for the region entity.
"""
from services.database import get_db_instance
import logging

_logger = logging.getLogger(__name__)
table_name = 'institution'


class Institution():
    def __init__(self, id, address, name, email, passwd, types, shelter):
        self.id = id
        self.address = address
        self.name = name
        self.email = email
        self.passwd = passwd
        self.types = types
        self.shelter = shelter

    def __repr__(self):
        return "<Institution(id='%s', name=%s)>" % (self.id, self.name)


def create_institution(address, name, email, passwd, types, shelter):
    db = get_db_instance()
    institution = None
    try:
        with db.cursor() as cursor:
            # insert record
            sql = "INSERT INTO {} (ADDRESS, NAME, EMAIL, PASSWD, TYPES, SHELTER) VALUES ('{}', '{}', '{}','{}','{}',{})"
            cursor.execute(sql.format(table_name, address, name, email, passwd, types, shelter))
            created_id = db.insert_id()
            cursor.execute('commit')
            institution = Institution(id=created_id, address=address, name=name, email=email, passwd=passwd, types=types, shelter=shelter)
            return institution
    finally:
        db.close()


def get_institutions():
    db = get_db_instance()
    data = []
    try:
        with db.cursor() as cursor:
            # Read all records
            sql = "select * from {}"
            cursor.execute(sql.format(table_name))
            result = cursor.fetchall()
            for row in result:
                data.append({
                    'id_institution': row[0],
                    'address': row[1],
                    'name': row[2],
                    'email': row[3],
                    'password': row[4],
                    'types': row[5].split(','),
                    'shelter': row[6]
                })
            return data
    finally:
        db.close()