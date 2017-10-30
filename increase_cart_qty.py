#!/usr/bin/python

from data.dao import Connection
from data.models import ShoppingCart
from utils.helpers import FormParser, get_session_user_id, is_float

__error_list = []

def __validate_properties(user_id, product_id, quantity):
    if not user_id or not is_float(user_id):
        __error_list.append("Usuario es requerido.")
    if not product_id or not is_float(product_id):
        __error_list.append("Producto es requerido.")
    if not quantity or not is_float(quantity):
        __error_list.append("Cantidad es requerida.")

def __process_update_cart_qty():
    parser = FormParser()
    #validate session
    user_id = get_session_user_id()
    product_id = parser.get_value("product_id", "")
    quantity = parser.get_value("quantity", "")
    if not __validate_properties(user_id, product_id, quantity):
        print "Location: index.py"
    conn = Connection()
    if not conn.increase_cart_qty(ShoppingCart(user_id, product_id, quantity)):
        #print errors
        a = 1

__process_update_cart_qty()
print "Location: cart.py"
print "Content-type: text/html\n\n"
