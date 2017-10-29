#!/usr/bin/python
"""This script shows the signup screen"""
import sys
from utils.helpers import FormParser
from data.dao import Connection
from data.models import User

query_string = sys.stdin.read() # reads the parameters, username=xxx&password=xxx
parser = FormParser()
parser.parse_values(query_string)#query_string.partition('&')

"""
conn = Connection()
name = parser.get_value("name", "")
username = parser.get_value("username", "")
password = parser.get_value("password", "")
email = parser.get_value("email", "")
user = User(0, username, email, password, '')
result = conn.create_account(user)
if result:
    #save to session
    print "Location: signin.py"
else:
    print "Location: index.py"
"""

print "Content-type: text/html\n\n"
