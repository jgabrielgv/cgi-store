#!/usr/bin/python3
"""This script stores the post action when sign in"""

import os
import sys

#PACKAGE_PARENT = 
__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

#from os import getenv
from utils.helpers import FormParser
from data.dao import Connection

query_string = sys.stdin.read() # reads the parameters, username=xxx&password=xxx
parser = FormParser()
parser.parse_values(query_string)#query_string.partition('&')


conn = Connection()
user_id = parser.get_value("username", "")
password = parser.get_value("password", "")
user = conn.fetch_user(user_id, password)


if user:
    #save to session
    print "Location: index.py"
else:
    #print "HTTP/1.1 303 See Other\r\n\r\n"
    print "Location: signin.py"

print "Content-type: text/html\r\n\r\n"
