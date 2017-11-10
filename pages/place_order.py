#!/usr/bin/python3
"""Handles the payment"""

import os
import sys

#PACKAGE_PARENT = 
__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from utils.helpers import get_session_user_id
from  data.dao import Connection
#print "Content-type: text/html\n\n"
#print "Funciona"

def __place_order():
    conn = Connection()
    conn.place_order(get_session_user_id())
    if conn.errors():
        print conn.errors()["message"]

print ("Content-type: text/html\n\n")
#__place_order()
