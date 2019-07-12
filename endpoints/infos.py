#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint, jsonify, request, abort, make_response
from models import info as info_model
import logging

_logger = logging.getLogger(__name__)

blueprint = Blueprint('infos', __name__)


def endpoints_exception(code, msg):
    abort(make_response(jsonify(message=msg), code))


def to_dict(info):
    dict_format = {}
    dict_format['id'] = info.id
    dict_format['name'] = info.name
    dict_format['phone'] = info.phone
    dict_format['link'] = info.link
    dict_format['image'] = info.image
    dict_format['description'] = info.description
    return dict_format

@blueprint.route('/info', methods=['POST'])
def post_information():
    """
    information post must follow:
    {
      "name": "string",
      "phone": "string"
      "link" string,
      "image": string,
      "description": string,
    }
    :return: a info entity
    """
    result = {}

    body = request.json
    name = body.get('name', None)
    phone = body.get('phone', None)
    link = body.get('link', None)
    image = body.get('image', None)
    description = body.get('description', None)

    info = info_model.create_information(name=name, phone=phone, link=link, description=description, image=image)

    result = to_dict(info)

    return jsonify(result), 200


@blueprint.route('/info', methods=['GET', 'OPTIONS'])
def get_infos():
    result = info_model.get_infos()
    return jsonify(result), 200


@blueprint.route('/info/<info_id>', methods=['GET', 'OPTIONS'])
def get_info(info_id):
    result = {}
    info = info_model.get_info(info_id)
    if info:
        result = to_dict(info)

    return jsonify(result), 200


@blueprint.route('/info/<info_id>', methods=['DELETE', 'OPTIONS'])
def delete_info(info_id):
    result = {}
    info = info_model.get_info(info_id)
    if info:
        info_model.delete_info(info_id)
        result = to_dict(info)
        return jsonify(result), 200
    else:
        endpoints_exception(404, "INFO_NOT_FOUND")