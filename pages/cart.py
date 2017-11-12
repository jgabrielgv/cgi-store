#!/usr/bin/python3
"""Handles the cart page"""
import os
import sys

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from utils import constants, helpers
from utils.helpers import print_page, get_session_user_id, loadhtml, check_user_seesion
from data.dao import Connection

helpers.redirect_if_session_expired()

def __details_html():
    return """<tr>
                <td><a href="productdetail.py?code={0}">{1}</a></td>
                <td>{2}</td>
                <td>{3}</td>
            </tr>"""

def __build_detail_list_html(results):
    detail_list = []
    if not results:
        return "<p>Su carrito se encuentra vacio.</p>"
    for item in results:
        detail_list.append(__details_html().format(item.code, \
         item.descr, item.price, item.quantity))
    return ''.join([x for x in detail_list])

def __build_dynamic_content():
    conn = Connection()
    results = conn.fetch_cart_products_by_user_id(get_session_user_id())
    subtotal = sum(c.total() for c in results)
    return loadhtml("cart.html").replace("**details**", __build_detail_list_html(results)) \
    .replace("**subtotal**", str(subtotal))

print_page('', "Mis carrito", constants.DEFAULT_CSS, __build_dynamic_content(), '', True)
