#!/usr/bin/env python
# -*- coding: utf-8 -*

"""
A model for the information entity.
"""
from services.database import get_db_instance
import logging


_logger = logging.getLogger(__name__)
table_name = 'info'

class Info():
    def __init__(self, id, name, phone, link, description, image):
        self.id = id
        self.name = name
        self.phone = phone
        self.link = link
        self.image = image
        self.description = description

    def __repr__(self):
        return "<Information(id='%s', name=%s)>" % (self.id, self.name)


def create_information(name, phone, link, description, image):
    db = get_db_instance()
    info = None
    try:
        with db.cursor() as cursor:
            # insert record
            sql = "INSERT INTO {} (name, phone, link, description, image) VALUES " \
                  "('{}', '{}', '{}','{}', '{}')"
            cursor.execute(sql.format(table_name, name, phone, link, description, image))
            created_id = db.insert_id()
            cursor.execute('commit')
            info = Info(id=created_id, name=name, phone=phone, link=link, description=description, image=image)
            return info
    finally:
        db.close()


def get_infos():
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
                        'name': row[1],
                        'phone': row[2],
                        'link': row[3],
                        'image': row[4],
                        'description': row[5],

                    })
                return data
            else:
                return {}
    finally:
        db.close()


def get_info(info_id):
    db = get_db_instance()
    info = None
    try:
        with db.cursor() as cursor:
            # Read a single record
            sql = "select * from {} where ID_INFO = {}"
            cursor.execute(sql.format(table_name, info_id))
            result = cursor.fetchone()
            if result:
                info = Info(id=result[0], name=result[1], phone=result[2], link=result[3], image=result[4],
                            description=result[5])
                return info
            else:
                return None
    finally:
        db.close()


def delete_info(info_id):
    db = get_db_instance()
    try:
        with db.cursor() as cursor:
            # Remove a single record
            sql = "delete from {} where ID_INFO = {}"
            cursor.execute(sql.format(table_name, info_id))
            cursor.execute('commit')
            return True
    finally:
        db.close()
