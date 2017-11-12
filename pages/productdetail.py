#!/usr/bin/python3
"""Shows a product detail"""

import os
import sys

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from data.dao import Connection
from utils.helpers import FormParser, loadhtml, print_page
from utils import constants, helpers

helpers.redirect_if_session_expired()

def __build_dynamic_content():
    parser = FormParser()
    parser.discover_values()
    code = parser.get_value("code", "")

    if not code or not parser.elements_count:
        return ''

    conn = Connection()
    product = conn.fetch_product_by_code(code)
    if not product:
        return ''

    return loadhtml("productdetail.html").format(product.code, product.descr, product.price, \
    product.username, product.entry_date)

__DATA = __build_dynamic_content()

print_page('', "Producto", constants.DEFAULT_CSS, \
__DATA if __DATA else "<p>El producto no existe.</p>", \
 '<script src="../js/product_detail.js"></script>')
