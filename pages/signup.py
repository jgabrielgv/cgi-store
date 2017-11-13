#!/usr/bin/python3
"""This script shows the signup screen"""

import os
import sys

#PACKAGE_PARENT = 
__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from data.dao import Connection
from data.models import User
from utils.helpers import FormParser, pagetemplate, valiadtionMessage, ucgiprint, loadhtml
from utils import constants, helpers

if helpers.request_method() == 'GET' and helpers.check_user_session():
    helpers.redirect('index.py')

__CONN = Connection()
__ERRORS = {}
__BODY = {}

def __validate_properties(name, username, password, email):
    """Validate the product properties before save it to database"""
    helpers.validate_string_input('name', name, 50, 'Nombre', __ERRORS, False)
    helpers.validate_string_input('username', username, 50, 'Usuario', __ERRORS)
    helpers.validate_string_input('email', email, 50, 'Correo', __ERRORS)
    helpers.validate_string_input('password', password, None, 'Contraseña', __ERRORS)
    return __ERRORS

def __validate_custom_functions(username, email):
    if 'invalid_username' in __ERRORS and 'invalid_email' in __ERRORS:
        return __ERRORS

    if 'email' not in __ERRORS and not helpers.valid_email_address(email):
        __ERRORS['invalid_email'] = 'Correo es tiene formato incorrecto.'
    validation_result = __CONN.username_email_exists(username, email)
    if 'username' in validation_result:
        __ERRORS['invalid_username'] = 'Usuario ya existe.'
    if 'invalid_email' not in __ERRORS and 'email' in validation_result:
        __ERRORS['invalid_email'] = "Correo ya existe."
    return __ERRORS

def __process_request():
    if not helpers.request_method() == 'POST':
        return False
    parser = helpers.FormParser()
    parser.discover_values()
    name = parser.get_value("name", "")
    username = parser.get_value("username", "")
    password = parser.get_value("password", "", False)
    email = parser.get_value("email", "")
    if __validate_properties(name, username, password, email) or \
     __validate_custom_functions(username, email):
        return False
    else:
        user = User(0, username, email, password, '', name)
        return __CONN.create_account(user)
    return True

if helpers.request_method() == 'POST' and __process_request():
    helpers.redirect('signin.py')

def __replace_body_error(validation_name, tag_name, div_name):
    if validation_name not in __ERRORS:
        return
    html_error = valiadtionMessage.replace('**error**', __ERRORS[validation_name])
    __BODY['content'] = __BODY['content'].replace(tag_name, html_error)\
    .replace(div_name, 'form-invalid-data')

__BODY['content'] = loadhtml('signup.html')
if __CONN.errors():
    __ERRORS['validation_error'] = str(__CONN.errors())
    __replace_body_error('validation_error', '</error>', 'errorClass')

if __ERRORS:
    __replace_body_error('invalid_name', '</name>', 'errorClassName')
    __replace_body_error('invalid_username', '</username>', 'errorClassUser')
    __replace_body_error('invalid_email', "</email>", 'errorClassEmail')
    __replace_body_error('invalid_password', '</password>', 'errorClassPass')

print ("Content-type: text/html\n\n")
wholepage = pagetemplate.replace('**title**', 'Sign Up').replace('**css**', constants.DEFAULT_CSS).replace('**body**', __BODY['content']).replace('**scripts**', '').replace('#action', 'signup.py') \
.replace('**menu**', helpers.header_menu_non_registered())
ucgiprint(wholepage)
