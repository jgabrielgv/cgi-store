#!/usr/bin/python
"""Handles the cart page"""
from utils import constants
from utils.helpers import print_page, get_session_user_id, loadhtml
from data.dao import Connection

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

print_page('', "Mis carrito", constants.DEFAULT_CSS, __build_dynamic_content())
