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

from utils import constants, helpers, request_handler
from  data.dao import Connection

__ERRORS = {}

def __validate_properties(address):
    helpers.validate_string_input('address', address, 10, 'Dirección', __ERRORS)
    return __ERRORS

def __place_order(user):
    parser = helpers.FormParser()
    parser.discover_values()
    address = parser.get_value('address', '')
    if __validate_properties(address):
        return False

    conn = Connection()
    if not conn.place_order(user.user_id, address):
        __ERRORS[constants.VALIDATION_ERROR] = conn.errors()
        return False
    return True

request_handler.process_request(__place_order, __ERRORS)
