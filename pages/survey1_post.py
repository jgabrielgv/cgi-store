#!/usr/bin/python3
"""This script shows the login page"""
import sys
import json
import os
import session
import time
from utils.helpers import FormParser
from data.dao import Connection
from data.models import Suggestion, User

#conn = Connection()
#conn.fetch_user('mcanales', '1234')
#user = conn.valid_username_cookie_id_user('93fd3bc7d420658343defa4c72a25d17138d6c03')

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
    reason = parser.get_value("reason", "")
    message = parser.get_value("message", "")

    sess = session.Session(expires='Thu, 01 Jan 1970 00:00:00 GMT', cookie_path='/')
    #lastvisit = sess.data.get('lastvisit')
    sess.data['lastvisit'] = repr(time.time())
    user = conn.valid_username_cookie_id(sess.cookie['sid'].value)
    user_id = user.user_id
    name = user.username
    email = user.email
    if name and message and email:
        suggestion = Suggestion(user_id, '', reason, message, name, email)
        creeateSuggestion = conn.create_suggestion(suggestion)
    else:
        result = validate_properties()
error = []
if result:
    if result == 'all':
        error.append('Nombre es requerido')
        error.append('Email es requerido')
        error.append('Mensaje es requerido')
    elif result == 'name':
        error.append('Nombre es requerido')
    elif result == 'message':
        error.append('Mensaje es requerido')
    elif result == 'email':
       error.append('Email es requerido')

if error:
    payload = json.JSONEncoder().encode({'errors': error})
    print "Status: 403 Forbidden"
    print "Content-Type: application/json"
    print "Content-Length: %d" % (len(payload))
    print ""
    print payload 
else:
    payload = json.JSONEncoder().encode({'name': sess.cookie['sid'].value, 'message': message, 'email': email, 'user_id': user_id})
    print "Status: 200 OK"
    print "Content-Type: application/json"
    print "Content-Length: %d" % (len(payload))
    print ""
    print payload 

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
