#!/usr/bin/python3
"""Handles the payment"""

import json
import os
import sys

#PACKAGE_PARENT = 
__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from utils import constants, helpers
from  data.dao import Connection

__ERRORS = {}

def __validate_properties(address):
    helpers.validate_string_input('address', address, 100, 'Dirección', __ERRORS)
    return __ERRORS

def __place_order():
    parser = helpers.FormParser()
    parser.discover_values()
    address = parser.get_value('address', '')
    if __validate_properties(address):
        return False

    conn = Connection()
    user_id = helpers.get_session_user_id()
    if not conn.place_order(user_id, address):
        __ERRORS[constants.VALIDATION_ERROR] = conn.errors()
        return False
    return True

__RESULT = __place_order()
helpers.print_status_code(__RESULT, {}, __ERRORS)
