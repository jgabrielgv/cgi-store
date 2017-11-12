#!/usr/bin/python3
"""This script shows the myproducts page"""

import os
import sys

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

import string
from data.dao import Connection
from utils import helpers
from utils.helpers import print_page, loadhtml, check_user_seesion, FormParser, is_request
from utils import constants, helpers
#from utils.email_handler import SmtpClient

helpers.redirect_if_session_expired()

"""
client = SmtpClient("jgmezvargas@gmail.com", ["lm.sanchezvargas@gmail.com", "jgabriel.gv@hotmail.com"])
client.build_registration_template()
client.send_email()
"""

__PARSER = helpers.FormParser()
__PARSER.discover_values()

def __content_html():
    return """
    <table>
            <thead>
                <th>Codigo</th>
                <th>Descripcion</th>
                <th>Precio</th>
                <th>Vendedor</th>
                <th>Fecha de ingreso</th>
            </thead>
            <tbody>
                **details**
            </tbody>
        </table>
    """

def __details_html():
    return """<tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>"""

def __field_keywords():
    return helpers.lstrip_string(__PARSER.get_value("field-keywords", '', False))

def __build_detail_list_html():
    conn = Connection()
    product_list = conn.fetch_products_by_keywords(__field_keywords())
    detail_list = []
    if not product_list:
        return ""
    for product in product_list:
        detail_list.append(__details_html() % (product.code, product.descr, product.price, product.username, product.entry_date))
    return ''.join([x for x in detail_list])

def __build_dynamic_content():
    if helpers.is_request():
        __PARSER.discover_values()
    html = loadhtml("index.html").replace("**keywords**", __field_keywords())
    if not __field_keywords():
        return html.replace("**content**", "<p>No se ha aplicado ningun criterio de busqueda.</p>")
    detail_list = __build_detail_list_html()
    if not detail_list:
        return html.replace("**content**", "<p>No se ha encontrado coincidencias.</p>")
    return html.replace("**content**", __content_html()).replace("**details**", detail_list)

helpers.print_page('', "Inicio", constants.DEFAULT_CSS, __build_dynamic_content(), '', True)
