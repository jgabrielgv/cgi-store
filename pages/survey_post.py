#!/usr/bin/python
"""This script shows the login page"""
import sys
import json
from utils.helpers import FormParser
from data.dao import Connection
from data.models import Suggestion

query_string = sys.stdin.read()
name = None
message = None
email = None
result = None
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
    user_id = None
    if name and message and email:
        suggestion = Suggestion(user_id, '', reason, message, name, email)
        creeateSuggestion = conn.create_suggestion(suggestion)
    else:
        result = validate_properties()

__ERRORS = {}
if result:
    if result == 'all':
        __ERRORS['invalid_name'] = 'Nombre es requerido'
        __ERRORS['invalid_email'] = 'Email es requerido'
        __ERRORS['invalid_message'] = 'Mensaje es requerido'
    elif result == 'name':
        __ERRORS['invalid_name'] = 'Nombre es requerido'
    elif result == 'message':
        __ERRORS['invalid_message'] = 'Mensaje es requerido'
    elif result == 'email':
       __ERRORS['invalid_email'] = 'Email es requerido'

if __ERRORS:
    payload = json.dumps(__ERRORS) 
    print "Status: 400 Bad Request"
    print "Content-Type: application/json"
    print "Content-Length: %d" % (len(payload))
    print ""
    print payload 
else:
    payload = json.JSONEncoder().encode({'response': 'ok'})
    print "Status: 200 OK"
    print "Content-Type: application/json"
    print "Content-Length: %d" % (len(payload))
    print ""
    print payload

