#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
A model for the account entity.
CREATE TABLE `tb_calendars` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_region` int(11) DEFAULT NULL,
  `id_calendar` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  #KEY `fk_tb_calendars_tb_region_idx` (`id_region`),
  CONSTRAINT `fk_tb_calendars_tb_regions` FOREIGN KEY (`id_region`) REFERENCES `tb_regions` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""

from services.database import get_db_instance



import logging
_logger = logging.getLogger(__name__)
table_name = 'tb_regions'

class Region():
    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address

    def __repr__(self):
        return "<Region(name='%s', adress=%s)>" % (self.name, self.name)


def get_regions():
    db = get_db_instance()
    data=[]
    try:
        with db.cursor() as cursor:
            # Read a single record
            sql = "select * from {}"
            cursor.execute(sql.format(table_name))
            result = cursor.fetchall()
            for row in result:
                data.append({
                    'name': row[1],
                    'address': row[2]
                })
            return  data
    finally:
        db.close()