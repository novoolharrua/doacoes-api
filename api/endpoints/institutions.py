#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint, jsonify, request, abort, make_response
from  models import institution as institution_model
import logging


_logger = logging.getLogger(__name__)

blueprint = Blueprint('institutions', __name__)


def endpoints_exception(code, msg):
    abort(make_response(jsonify(message=msg), code))

@blueprint.route('/institution', methods=['POST', 'OPTIONS'])
def post_region():
    """
    institutions post must follow:
    {
      "name": "string",
      "address": "string"
      "email" string,
      "passwd": string,
      "types": string,
      "shelter": int
    }
    :return: a region entity
    """
    result = {}

    body = request.json
    name = body['name']
    address = body['address']
    email = body['email']
    passwd = body['passwd']
    types = body['types']
    shelter = int(body['shelter'])

    institution = institution_model.create_institution(name=name, address=address, email=email, passwd=passwd,
                                                       types=types, shelter=shelter)
    result['id'] = institution.id
    result['address'] = institution.address
    result['name'] = institution.name
    result['email'] = institution.email
    result['passwd'] = institution.passwd
    result['types'] = institution.types.split(',')
    result['shelter'] = institution.shelter

    return jsonify(result), 200

@blueprint.route('/institution', methods=['GET', 'OPTIONS'])
def get_regions():
    result = institution_model.get_institutions()
    return jsonify(result), 200