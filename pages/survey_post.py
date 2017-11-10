#!/usr/bin/python3
"""This script shows the login page"""
import os
import sys
import json
import requests

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from utils.helpers import FormParser
from data.dao import Connection
from data.models import Suggestion

query_string = sys.stdin.read()
name = None
message = None
email = None
def validate_properties():
    """Validate the product properties before save it to database"""
    errorMessage = None
    if not name and not message and not email:
        errorMessage = 'all'
    elif not name:
        errorMessage = 'name'
    elif not message:
        errorMessage = 'message'
    elif not email:
        errorMessage = 'email'
    return errorMessage

if query_string:
    parser = FormParser()
    parser.parse_values(query_string)

    conn = Connection()
    name = parser.get_value("name", "")
    reason = parser.get_value("reason", "")
    message = parser.get_value("message", "")
    email = parser.get_value("email", "")
    user_id = -1
    if name and message and email:
        suggestion = Suggestion(user_id, '', reason, message, name, email)
        creeateSuggestion = conn.create_suggestion(suggestion)
    else:
        result = validate_properties()

#name = 'queso'
payload = json.JSONEncoder().encode({'name': name, 'message': message, 'email': email})

print("Status: 200 OK")
print("Content-Type: application/json")
print("Content-Length: %d" % (len(payload)))
print("")
print(payload)
#print "HTTP/1.1 302 Found"
#print "Location: survey.py\r\n"
#print "Content-type: text/html\n\n"
#final_url= "http://127.0.0.1/\x7Emcanales/cgi-bin/survey.py"
#payload = {'number': 2, 'value': 1}
#response = requests.post(final_url, data=payload)
#
#
##print(str(response.text).encode('utf-8')) #TEXT/HTML
#print(str(response.status_code).encode('utf-8'), str(response.reason).encode('utf-8')) #HTTP
