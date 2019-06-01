#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint, jsonify
from services.database import get_db_instance

blueprint = Blueprint('status', __name__)

@blueprint.route('/status', methods=['GET', 'OPTIONS'])
def get_status_request():
    return '', 200


@blueprint.route('/ready', methods=['GET', 'OPTIONS'])
def get_readiness_request():
    """Test all used services and return readiness."""
    result = {
        "API": "OK"
    }
    try:
        db = get_db_instance()
        if db:
            result['database'] = 'OK'
            db.close()
    except:
        result['database'] = 'ERROR'


    #TODO: google api ready

    code = 200

    for key in result.keys():
        if result[key] is not 'OK':
            code = 503

    return jsonify(result), code