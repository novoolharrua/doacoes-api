#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint, jsonify, request, abort, make_response
from models import region
import logging
_logger = logging.getLogger(__name__)

blueprint = Blueprint('regions', __name__)


def endpoints_exception(code, msg):
    abort(make_response(jsonify(message=msg), code))

@blueprint.route('/region', methods=['POST', 'OPTIONS'])
def post_regions():

    body = request.json

    return '', 200


@blueprint.route('/region', methods=['GET', 'OPTIONS'])
def list_regions():

    result = {}

    data = region.get_regions()

    return jsonify(data), 200


@blueprint.route('/region/<account_name>', methods=['GET', 'OPTIONS'])
def get_region(account_name):


    return '', 200