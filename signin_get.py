#!/usr/bin/python
"""This script stores the post action when sign in"""

#from os import getenv
import sys
from utils.helpers import FormParser
from data.dao import Connection

parser = FormParser()
parser.parse_values(sys.stdin.read())#query_string.partition('&')

conn = Connection()
user_id = parser.get_value("username", "")
password = parser.get_value("password", "")
user = conn.fetch_user(user_id, password)

if user:
    #no errors 
    print "Location: index.py"
else:
    #incorrect user or password
    print "Location: signin.py?error=true"

print "Content-type: text/html\n\n"
