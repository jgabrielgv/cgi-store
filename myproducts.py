#!/usr/bin/python
"""This script shows the myproducts page"""

from data.dao import Connection
from utils.helpers import loadhtml, print_page
from utils import constants

#check session status
#print "Content-type: text/html\n\n"

def __details_html():
    return """<tr>
                <td><a href="productdetail.py?code={0}">{0}</a></td>
                <td>{1}</td>
                <td>{2}</td>
                <td>{3}</td>
            </tr>"""

def __build_detail_list_html():
    user_id = 2
    conn = Connection()
    product_list = conn.fetch_products_by_user_id(user_id)
    detail_list = []
    if not product_list:
        return ""
    for product in product_list:
         detail_list.append(__details_html().format(product.code, product.descr, product.price, product.entry_date))
    return ''.join([x for x in detail_list])

def __build_dynamic_content():
    return loadhtml("myproducts.html").replace("**details**", __build_detail_list_html())

#print __build_detail_list_html()
print_page('', "Mis productos", constants.DEFAULT_CSS, __build_dynamic_content())
