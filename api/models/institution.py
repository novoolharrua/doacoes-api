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


def main():
    result = create_institution('endereco', 'nome', 'email', 'passwd','food,religion,shelter', 0)
    print(result)

if __name__ == "__main__":
    main()
