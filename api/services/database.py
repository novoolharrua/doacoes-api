#!/usr/bin/env python
# -*- coding: utf-8 -*

import pymysql
import os


def get_db_instance():

    host = os.environ['SQL_HOST']
    user = os.environ['SQL_USER']
    passwd = os.environ['SQL_PASS']
    database = os.environ['SQL_DB']

    db = pymysql.connect(host, user, passwd, database)

    return db