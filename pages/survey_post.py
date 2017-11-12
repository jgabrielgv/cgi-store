#!/usr/bin/python3
"""This script shows the login page"""
import os
import sys
import json

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from utils import constants, helpers
from data.dao import Connection
from data.models import Suggestion

__ERRORS = {}

def __validate_properties(user, name, email, reason, message):
    if not user:
        helpers.validate_string_input('name', name, 50, 'Nombre', __ERRORS)
        helpers.validate_string_input('email', email, 50, 'Correo', __ERRORS)
    helpers.validate_string_input('reason', reason, 100, 'Asunto', __ERRORS, False)
    helpers.validate_string_input('message', message, 300, 'Mensaje', __ERRORS, False)
    return __ERRORS

def __process_survey():
    parser = helpers.FormParser()
    parser.discover_values()
    name = parser.get_value("name", "")
    reason = parser.get_value("reason", "")
    message = parser.get_value("message", "")
    email = parser.get_value("email", "")
    user_id = helpers.get_session_user_id()

    user = None
    conn = Connection()
    if helpers.is_float(user_id) and float(user_id) > 0:
        user = conn.fetch_user_by_user_id(float(user_id))
        if not user:
            __ERRORS[constants.VALIDATION_ERROR] = 'Usuario no existente.'
            return False
        else:
            email = user.email
            name = user.name
    if __validate_properties(user, name, email, reason, message):
        return False

    suggestion = Suggestion(user_id, name, email, reason, message)
    return conn.create_suggestion(suggestion)

__RESULT = __process_survey()
helpers.print_status_code(__RESULT, {}, __ERRORS)
