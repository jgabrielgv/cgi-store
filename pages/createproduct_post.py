#!/usr/bin/python3
"""Handles the product creation event"""

import os
import sys
import json
import requests

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from utils.helpers import FormParser, current_date, is_float
from utils import constants, helpers
from data.dao import Connection
from data.models import Product

__ERRORS = {}

__PARSER = FormParser()
__PARSER.parse_post_values()

__CODE = __PARSER.get_value("code", "").strip()
__DESCR = __PARSER.get_value("descr", "").strip()
__PRICE = __PARSER.get_value("price", "").strip()

def __validate_properties():
    """Validate the product properties before save it to database"""
    code_length = 25
    descr_length = 100
    if not __CODE:
        __ERRORS['invalid_code'] = "Codigo es requerido."
    elif len(__CODE) > code_length:
        __ERRORS['invalid_code'] = "El codigo no puede exceder los %d caracteres." % (code_length)
    if not __DESCR:
        __ERRORS['invalid_descr'] = "Descripcion es requerida."
    elif len(__DESCR) > descr_length:
        __ERRORS['invalid_descr'] = "La descripcion no puede exceder los %d caracteres." % (descr_length)
    if not __PRICE:
        __ERRORS['invalid_price'] = "Precio es requerido."
    elif not is_float(__PRICE):
        __ERRORS['invalid_price'] = "Precio debe ser un valor numérico."
    elif float(__PRICE) < 0:
        __ERRORS['invalid_price'] = "El precio debe ser mayor o igual a cero."
    return __ERRORS

__RESULT = True

if __validate_properties():
    __RESULT = False
else:
    __PRODUCT = Product(0, helpers.get_session_user_id(), __CODE, current_date(), \
    __DESCR, float(__PRICE) if is_float(__PRICE) else 0)

    __CONN = Connection()
    if not __CONN.create_product(__PRODUCT):
        __RESULT = False
        __ERRORS['validation_error'] = __CONN.errors()

if __RESULT:
    print('Content-Type: text/json')
    print('Status: 200 success')
    print()
else:
    print('Content-Type: text/json')
    print('Status: 400 Bad Request')
    print()
    print(json.dumps(__ERRORS))
