#!/usr/bin/python
"""This script shows the myproducts page"""

from data.dao import Connection
from utils.helpers import print_page
from utils import constants

#check session status

def __list_products_html():
    return """<table>
                <thead>
                    <th>Codigo</th>
                    <th>Descripcion</th>
                    <th>Precio</th>
                </thead>
                <tbody>
                    **details**
                </tbody>
              </table>"""

def __details_html():
    return """<tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>"""

def __build_detail_list_html():
    user_id = 2
    conn = Connection()
    product_list = conn.fetch_products(user_id)
    #print len(product_list)
    detail_list = []
    if not product_list:
        return ""
    for product in product_list:
         detail_list.append(__details_html() % (product.code, product.descr, product.entry_date))
    return ''.join([x for x in detail_list])

def __build_dynamic_content():
    return __list_products_html().replace("**details**", __build_detail_list_html())

print_page('', "Mis productos", constants.DEFAULT_CSS, __build_dynamic_content())
