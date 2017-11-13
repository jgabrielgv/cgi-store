#!/usr/bin/python3
"""This script shows the login page"""
import os
import sys
import json

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from utils.helpers import FormParser
from utils.CaptchasDotNet import CaptchasDotNet
from data.dao import Connection
from data.models import Suggestion

captchas = CaptchasDotNet (client   = 'demo',  secret   = 'secret')#, #alphabet = 'abcdefghkmnopqrstuvwxyz', #letters  = 6)
query_string = sys.stdin.read()
name = None
message = None
email = None
result = None
__ERRORS = {}

def validate_captcha(captcha, random):
    result = True
    if not captchas.validate(random):
        __ERRORS['invalid_captcha'] =  ('Every CAPTCHA can only be used once. The current '
                + 'CAPTCHA has already been used. Try again.')
        result = False

    # Check, that the right CAPTCHA password has been entered and
    # return an error message otherwise.
    if not captchas.verify(captcha):
        __ERRORS['invalid_captcha'] = 'El captcha ingresado no es valido'
        result = False
    return result

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
    random = parser.get_value("random", "")
    captcha = parser.get_value("captcha", "")

    user_id = None
    if name and message and email:
        valid_captcha = validate_captcha(captcha, random)
        if valid_captcha:
        suggestion = Suggestion(user_id, '', reason, message, name, email)
        creeateSuggestion = conn.create_suggestion(suggestion)
    else:
        result = validate_properties()


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
    print("Status: 400 Bad Request")
    print("Content-Type: application/json")
    print("Content-Length: %d" % (len(payload)))
    print("")
    print(payload)
else:
    payload = json.JSONEncoder().encode({'response': 'suveyOk'})
    print("Status: 200 OK")
    print("Content-Type: application/json")
    print("Content-Length: %d" % (len(payload)))
    print("")
    print(payload)
