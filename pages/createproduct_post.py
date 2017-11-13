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
from utils import constants, helpers, request_handler
from data.dao import Connection
from data.models import Product

__ERRORS = {}

def __validate_properties(code, descr, price):
    """Validate the product properties before save it to database"""
    helpers.validate_string_input('code', code, constants.PRODUCT_CODE_LENGTH, 'Codigo', __ERRORS)
    helpers.validate_string_input('descr', descr, constants.PRODUCT_DESCR_LENGTH, 'Descripcion', __ERRORS)
    if not price:
        __ERRORS['invalid_price'] = "Campo Precio es requerido."
    elif not is_float(price):
        __ERRORS['invalid_price'] = "Campo Precio debe ser un valor numérico."
    elif float(price) < 0:
        __ERRORS['invalid_price'] = "Campo Precio debe ser mayor o igual a cero."
    return __ERRORS

__RESULT = True

def __process_request(user):
    parser = FormParser()
    parser.discover_values()
    code = parser.get_value("code", "")
    descr = parser.get_value("descr", "")
    price = parser.get_value("price", "")
    if __validate_properties(code, descr, price):
        return False
    else:
        product = Product(0, user.user_id, code, current_date(), \
        descr, float(price) if is_float(price) else 0)

        conn = Connection()
        if not conn.create_product(product):
            __ERRORS[constants.VALIDATION_ERROR] = conn.errors()
            return False
    return True

request_handler.process_request(__process_request, __ERRORS)
