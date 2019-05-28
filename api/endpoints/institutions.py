#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint, jsonify, request, abort, make_response
from models import institution as institution_model
from utils.password_utils import convert_md5
import datetime
import logging


_logger = logging.getLogger(__name__)

blueprint = Blueprint('institutions', __name__)


def endpoints_exception(code, msg):
    abort(make_response(jsonify(message=msg), code))


status_enum = {
    "0": 'NEW',
    "1": 'PENDING',
    "2": 'ACCEPTED',
    "3": 'REFUSED',
}


def to_dict(institution):
    dict_format = {}
    dict_format['id'] = institution.id
    dict_format['address'] = institution.address
    dict_format['name'] = institution.name
    dict_format['email'] = institution.email
    dict_format['passwd'] = institution.passwd
    dict_format['types'] = institution.types.split(',')
    dict_format['shelter'] = institution.shelter
    dict_format['status'] = status_enum[str(institution.status)]
    if isinstance(institution.created_at, datetime.date):
        dict_format['created_at'] = institution.created_at.strftime('%Y-%m-%d %H:%M:%S')
    else:
        dict_format['created_at'] = institution
    return dict_format

@blueprint.route('/institution', methods=['POST', 'OPTIONS'])
def post_institution():
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
                                                       types=types, shelter=shelter, status=0)
    result = to_dict(institution)

    return jsonify(result), 200

@blueprint.route('/institution', methods=['GET', 'OPTIONS'])
def get_institutions():
    result = institution_model.get_institutions()
    return jsonify(result), 200


@blueprint.route('/institution/<institution_id>', methods=['GET', 'OPTIONS'])
def get_institution(institution_id):
    result = {}
    institution = institution_model.get_institution(institution_id)
    if institution:
        result = to_dict(institution)

    return jsonify(result), 200

@blueprint.route('/institution/<institution_id>', methods=['DELETE', 'OPTIONS'])
def delete_institution(institution_id):
    result = {}
    institution = institution_model.get_institution(institution_id)
    if institution:
        institution_model.delete_institution(institution.id)
        result = to_dict(institution)
        return jsonify(result), 200
    else:
        endpoints_exception(404, "REGION_NOT_FOUND")


@blueprint.route('/institution/<institution_id>', methods=['PUT', 'OPTIONS'])
def put_institution(institution_id):
    """
    institutions put must follow:
    {
      "name": "string",
      "address": "string"
      "email" string,
      "passwd": string,
      "types": string,
      "shelter": int
      "status": "string"
    }
    :return: a region entity
    """
    result = {}

    body = request.json
    name = body.get("name", None)
    address = body.get("address", None)
    email = body.get("email", None)
    passwd = body.get("passwd", None)
    types = body.get("types", None)
    shelter = body.get("shelter", None)
    status = body.get("status", None)

    institution = institution_model.get_institution(institution_id)
    if institution:
        institution_model.update_institution(institution, name, address, email, passwd, types, shelter, status)
        result = to_dict(institution)
        return jsonify(result), 200
    else:
        endpoints_exception(404, "REGION_NOT_FOUND")


@blueprint.route('/institution/auth', methods=['GET', 'OPTIONS'])
def auth_institution():
    email = request.args.get('email', None)
    passwd = request.args.get('passwd', None)

    result = {}
    if email:
        institution = institution_model.get_institution_by_email(email)
    else:
        endpoints_exception(400, "EMAIL_PARAM_NOT_FOUND")

    if passwd and convert_md5(passwd) == institution.passwd:
        token = institution_model.generate_token(institution)
        result = {
            "token": token.decode('utf-8'),
            "duration": 3600
        }
    else:
        endpoints_exception(400, "BAD_OR_MISSING_PASSWORD")

    return jsonify(result), 200

@blueprint.route('/institution/validate_token', methods=['GET', 'OPTIONS'])
def validade_jwt():
    token = request.args.get('token', None)

    result = {}
    decoded_payload = None
    if token:
        decoded_payload = institution_model.decode_token(token)
    else:
        endpoints_exception(400, "MISSING_TOKEN")

    if decoded_payload['expiration_date'] < datetime.datetime.now():
        endpoints_exception(401, "TOKEN_EXPIRED")
    else:
        return '', 200
