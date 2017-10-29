#!/usr/bin/python
"""Handles the product creation event"""
import os
import sys
import utils.constants as constants
from utils.helpers import FormParser, current_date, is_float
import utils.globals_values as globals_values
from data.dao import Connection
from data.models import Product

###validate user session

__error_list = []

def __build_error_message():
    """Build the error message for assign it as environment variable"""
    error_message = ""
    if not __error_list:
        return error_message
    for element in __error_list:
        error_message = "%s<p>%s</p>" % (error_message, element)
    return error_message

def __redirect_on_error():
    #print "<p>error</p>"
    #os.environ[constants.ERROR] = build_error_message()
    globals_values.add_variable(constants.ERROR, __build_error_message())
    #print "<p>%s</p>" % (os.environ[constants.ERROR])
    print "Location: index.py"
    print "Content-type: text/html\n\n"

__parser = FormParser()
__parser.parse_values(sys.stdin.read())

__code = __parser.get_value("code","").strip()
__descr = __parser.get_value("descr", "").strip()
__price = __parser.get_value("price", "").strip()

def __validate_properties():
    """Validate the product properties before save it to database"""
    code_length = 25
    descr_length = 100
    if not __code:
        __error_list.append("Codigo es requerido.")
    elif len(__code) > code_length:
        __error_list.append("El codigo no puede exceder los %d caracteres." % (code_length))
    if not __descr:
        __error_list.append("Descripcion es requerida.")
    elif len(__descr) > descr_length:
        __error_list.append("La descripcion no puede exceder los %d caracteres." % (descr_length))
    if not __price or not is_float(__price):
        __error_list.append("Precio es requerido.")
    elif float(__price) < 0:
        __error_list.append("El precio debe ser mayor o igual a cero.")
    return __error_list

if __validate_properties():
    __redirect_on_error()

__user_id = 2 #use session value
__product = Product(0, __user_id, __code, current_date(), __descr, float(__price) if is_float(__price) else 0)

__conn = Connection()
if not __conn.create_product(__product):
    __redirect_on_error()

#print "Location: index.py"
#print "Content-type: text/html\n\n"
#print "</body>"

print "Location: createproduct.py"
print "Content-type: text/html\n\n"

"""
print "Print keys: %s" % (os.environ["CONTENT_TYPE"])
for key in os.environ.keys():
    print "Key: %s, value: %s" % (key, os.environ.get(key))
    print "</br>"
"""
