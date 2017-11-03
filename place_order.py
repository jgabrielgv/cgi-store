#!/usr/bin/python
"""Handles the payment"""

from utils.helpers import get_session_user_id
from  data.dao import Connection
#print "Content-type: text/html\n\n"
#print "Funciona"

def __place_order():
    conn = Connection()
    conn.place_order(get_session_user_id())
    if conn.errors():
        print conn.errors()["message"]

print "Content-type: text/html\n\n"
#__place_order()
