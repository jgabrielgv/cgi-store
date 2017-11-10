#!/usr/bin/python3
"""Shows a product detail"""

import os
import sys

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

#print ("Content-type: text/html\n\n")

from data.dao import Connection
from utils.helpers import FormParser, loadhtml, print_page
from utils import constants

def __build_dynamic_content():
    return loadhtml("productdetail.html").format(__product.code, __product.descr, __product.price, \
    __product.username, __product.entry_date)

__parser = FormParser()
__parser.parse_get_values()
__code = __parser.get_value("code", "")
__flag = True

if not __code or not __parser.elements_count:
    __flag = False

__conn = Connection()
__product = __conn.fetch_product_by_code(__code)

if not __product:
    __flag = False

print_page('', "Producto", constants.DEFAULT_CSS, \
__build_dynamic_content() if __flag else "<p>El producto no existe.</p>")

'''
for key in os.environ.keys():
    print "Key: %s, value: %s" % (key, os.environ.get(key))
    print "</br>"
'''
