#!/usr/bin/env python
# -*- coding: utf-8 -*

"""
A model for the region entity.
"""
from services.database import get_db_instance
import logging
from datetime import datetime


_logger = logging.getLogger(__name__)
table_name = 'institution'


status_enum = {
    "0": 'NEW',
    "1": 'PENDING',
    "2": 'ACTIVE',
    "3": 'DENIED',
}

status_enum_reverse = {
    'NEW': 0,
    'PENDING': 1,
    'ACTIVE': 2,
    'DENIED': 3,
}

class Institution():
    def __init__(self, id, address, name, email, passwd, types, shelter, status, created_at):
        self.id = id
        self.address = address
        self.name = name
        self.email = email
        self.passwd = passwd
        self.types = types
        self.shelter = shelter
        self.status = status
        self.created_at = created_at

    def __repr__(self):
        return "<Institution(id='%s', name=%s)>" % (self.id, self.name)


def create_institution(address, name, email, passwd, types, shelter, status):
    db = get_db_instance()
    institution = None
    try:
        with db.cursor() as cursor:
            # insert record
            sql = "INSERT INTO {} (ADDRESS, NAME, EMAIL, PASSWD, TYPES, SHELTER, STATUS) VALUES " \
                  "('{}', '{}', '{}','{}','{}',{},{})"
            cursor.execute(sql.format(table_name, address, name, email, passwd, types, shelter, status))
            created_id = db.insert_id()
            cursor.execute('commit')
            institution = Institution(id=created_id, address=address, name=name, email=email, passwd=passwd,
                                      types=types, shelter=shelter, status=status,
                                      created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            return institution
    finally:
        db.close()

def get_institutions():
    db = get_db_instance()
    data = []
    try:
        with db.cursor() as cursor:
            # Read all records
            sql = "select * from {} order by STATUS,CREATED_AT"
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
                        'shelter': row[6],
                        'status': status_enum[str(row[7])],
                        'created_at': row[8].strftime('%Y-%m-%d %H:%M:%S')
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
                                          passwd=result[4], types=result[5], shelter=result[6], status=result[7],
                                          created_at=result[8])
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

def update_institution(institution, name, address, email, passwd, types, shelter, status):
    from utils.password_utils import convert_md5
    db = get_db_instance()
    try:
        with db.cursor() as cursor:
            # update a single record
            sql = "update {} set ".format(table_name)
            if name:
                sql += "NAME = '{}', ".format(name)
                institution.name = name
            if address:
                sql += "ADDRESS = '{}', ".format(address)
                institution.address = address
            if email:
                sql += "EMAIL = '{}', ".format(email)
                institution.email = email
            if passwd:
                sql += "PASSWD = '{}', ".format(convert_md5(passwd))
                institution.passwd = convert_md5(passwd)
            if types:
                sql += "TYPES = '{}', ".format(types)
                institution.types = type
            if shelter:
                sql += "SHELTER = {}, ".format(shelter)
                institution.shelter = shelter
            if status:
                sql += "STATUS = {}, ".format(status_enum_reverse[status])
                institution.status = status_enum_reverse[status]
            sql += "UPDATED_AT = '{}', ".format(datetime.now())
            sql = sql[:-2] + " "
            sql += "where ID_INSTITUTION = {}".format(institution.id)

            cursor.execute(sql)
            cursor.execute('commit')
            return institution
    finally:
        db.close()