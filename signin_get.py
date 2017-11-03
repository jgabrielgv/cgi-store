#!/usr/bin/python
"""This script stores the post action when sign in"""

#from os import getenv
import sys
from helpers import FormParser
from dao import Connection

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
