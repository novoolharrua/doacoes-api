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
            if result:
                for row in result:
                    data.append({
                        'id': row[0],
                        'address': row[1],
                        'name': row[2],
                        'email': row[3],
                        'password': row[4],
                        'types': row[5].split(','),
                        'shelter': row[6]
                    })
                return data
            else:
                return None
    finally:
        db.close()

def get_institution(iid):
    db = get_db_instance()
    institution = None
    try:
        with db.cursor() as cursor:
            # Read a single record
            sql = "select * from {} where ID_INSTITUTION = {}"
            cursor.execute(sql.format(table_name, iid))
            result = cursor.fetchone()
            if result:
                institution = Institution(id=result[0], address=result[1], name=result[2], email=result[3],
                                          passwd=result[4], types=result[5], shelter=result[6])
                return institution
            else:
                return None
    finally:
        db.close()

def delete_institution(iid):
    db = get_db_instance()
    try:
        with db.cursor() as cursor:
            # Remove a single record
            sql = "delete from {} where ID_INSTITUTION = {}"
            cursor.execute(sql.format(table_name, iid))
            cursor.execute('commit')
            return True
    finally:
        db.close()