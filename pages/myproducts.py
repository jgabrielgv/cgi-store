#!/usr/bin/python3
# coding=iso-8859-1
"""This script shows the myproducts page"""

import os
import sys

#PACKAGE_PARENT = 
__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from data.dao import Connection
from utils.helpers import loadhtml, print_page, get_session_user_id, check_user_seesion
from utils import constants, helpers, request_handler

helpers.redirect_if_session_expired()

def __details_html():
    return """<tr>
                <td><a href="productdetail.py?code={0}">{0}</a></td>
                <td>{1}</td>
                <td>{2}</td>
                <td>{3}</td>
            </tr>"""

def __build_detail_list_html(product_list):
    detail_list = []
    if not product_list:
        return ""
    for product in product_list:
         detail_list.append(__details_html().format(product.code, product.descr, product.price, product.entry_date))
    return ''.join([x for x in detail_list])

def __build_dynamic_content():
    conn = Connection()
    product_list = conn.fetch_products_by_user_id(request_handler.fetch_authorized_user_session().user_id)
    return loadhtml("myproducts.html").replace("**details**", __build_detail_list_html(product_list))

print_page('', "Mis productos", constants.DEFAULT_CSS, __build_dynamic_content(), '', True)
