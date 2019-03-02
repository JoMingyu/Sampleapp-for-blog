from flask import jsonify

from schematics.exceptions import BaseError
from werkzeug.exceptions import HTTPException


def schematics_baseerror_handler(e: BaseError):
    return jsonify({
        'msg': e.to_primitive()
    }), 400


def http_exception_handler(e: HTTPException):
    return '', e.code


def broad_exception_handler(e: Exception):
    return '', 500
