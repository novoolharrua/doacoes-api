#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint, jsonify, request, abort, make_response
from  models import institution as institution_model
from utils.password_utils import convert_md5
import logging


_logger = logging.getLogger(__name__)

blueprint = Blueprint('institutions', __name__)


def endpoints_exception(code, msg):
    abort(make_response(jsonify(message=msg), code))


def to_dict(institution):
    dict_format = {}
    dict_format['id'] = institution.id
    dict_format['address'] = institution.address
    dict_format['name'] = institution.name
    dict_format['email'] = institution.email
    dict_format['passwd'] = institution.passwd
    dict_format['types'] = institution.types.split(',')
    dict_format['shelter'] = institution.shelter
    return dict_format

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
    passwd = convert_md5(body['passwd'])
    types = body['types']
    shelter = int(body['shelter'])

    institution = institution_model.create_institution(name=name, address=address, email=email, passwd=passwd,
                                                       types=types, shelter=shelter)
    result = to_dict(institution)

    return jsonify(result), 200

@blueprint.route('/institution', methods=['GET', 'OPTIONS'])
def get_regions():
    result = institution_model.get_institutions()
    return jsonify(result), 200


@blueprint.route('/institution/<institution_id>', methods=['GET', 'OPTIONS'])
def get_region(institution_id):
    result = {}
    institution = institution_model.get_institution(institution_id)
    if institution:
        result = to_dict(institution)

    return jsonify(result), 200

@blueprint.route('/institution/<institution_id>', methods=['DELETE', 'OPTIONS'])
def delete_region(institution_id):
    result = {}
    institution = institution_model.get_institution(institution_id)
    if institution:
        institution_model.delete_institution(institution.id)
        result = to_dict(institution)
        return jsonify(result), 200
    else:
        endpoints_exception(404, "REGION_NOT_FOUND")