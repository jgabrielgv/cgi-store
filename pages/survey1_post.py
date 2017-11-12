#!/usr/bin/python
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

#conn = Connection()
#creeateSuggestion = conn.tt(str('3b1b61eb4d0cdb16fc295a50896cd5bce628df66'))

query_string = sys.stdin.read()
name = None
message = None
reason = None
email = None
result = None
creeateSuggestion = None
user = None
Fordiben = None
def validate_properties():
    """Validate the product properties before save it to database"""
    errorMessage = None
    if not message and not reason:
        errorMessage = 'all'
    elif not message:
        errorMessage = 'message'
    elif not reason:
        errorMessage = 'reason'
    return errorMessage

if query_string:
    parser = FormParser()
    parser.parse_values(query_string)

    conn = Connection()
    reason = parser.get_value("reason", "")
    message = parser.get_value("message", "")

    sess = session.Session(expires=365*24*60*60, cookie_path='/')
    #lastvisit = sess.data.get('lastvisit')
    sess.data['lastvisit'] = repr(time.time())
    user = conn.autorized_session(sess.cookie['sid'].value)
    if user is not None and user is not '403':
        user_id = user.user_id
        name = user.username
        email = user.email
        if message and reason:
            suggestion = Suggestion(user_id, '', reason, message, name, email)
            creeateSuggestion = conn.create_suggestion(suggestion)
        else:
            result = validate_properties()
    else:
        Fordiben = True

__ERRORS = {}
if result:
    if result == 'all':
        __ERRORS['invalid_message'] = 'Mensaje es requerido'
        __ERRORS['invalid_reason'] = 'Razon es requerido'
    elif result == 'message':
        __ERRORS['invalid_message'] = 'Mensaje es requerido'
    elif result == 'reason':
       __ERRORS['invalid_reason'] = 'Tema es requerido'

if Fordiben is not None:
    payload = json.JSONEncoder().encode({'errors': 'user not autorize'})
    print "Status: 403 Forbidden"
    print "Content-Type: application/json"
    print "Content-Length: %d" % (len(payload))
    print ""
    print payload 
elif __ERRORS:
    payload = json.dumps(__ERRORS) 
    print "Status: 400 Bad Request"
    print "Content-Type: application/json"
    print "Content-Length: %d" % (len(payload))
    print ""
    print payload 
else:
    #payload = json.JSONEncoder().encode({'cookie': sess.cookie['sid'].value, 'message': message, 'reason': reason, 'user_id': creeateSuggestion})
    payload = json.JSONEncoder().encode({'response': 'ok'})
    print "Status: 200 OK"
    print "Content-Type: application/json"
    print "Content-Length: %d" % (len(payload))
    print ""
    print payload 
