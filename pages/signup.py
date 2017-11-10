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

username = None
password = None
email = None
result = None
htmlerror = ''
creeateAccount = False
conn = None

def validate_properties():
    """Validate the product properties before save it to database"""
    errorMessage = None
    if not username and not password and not email:
        errorMessage = 'all'
    elif not username:
        errorMessage = 'user'
    elif not password:
        errorMessage = 'pass'
    elif not email:
        errorMessage = 'email'
    return errorMessage

query_string = sys.stdin.read() # reads the parameters, username=xxx&password=xxx

if query_string:
    parser = FormParser()
    parser.parse_values(query_string)#query_string.partition('&')
    
    conn = Connection()
    name = parser.get_value("name", "")
    username = parser.get_value("username", "")
    password = parser.get_value("password", "")
    email = parser.get_value("email", "")
    
    if username and password and email:
        user = User(0, username, email, password, '', name)
        creeateAccount = conn.create_account(user)
    else:
        result = validate_properties()

css = '<link rel="stylesheet" type="text/css" href="../css/styles.css">'
body = loadhtml('signup.html')

if result:
    if result == 'all':
        htmlerror = valiadtionMessage.replace('**error**', 'Contrasena es requerida')
        htmlerrorUser = valiadtionMessage.replace('**error**', 'Usuario es requerido')
        htmlerrorEmail = valiadtionMessage.replace('**error**', 'Email es requerido')
        body = body.replace('</password>', htmlerror).replace('errorClassPass', 'form-invalid-data')
        body = body.replace('</username>', htmlerrorUser).replace('errorClassUser', 'form-invalid-data')
        body = body.replace('</email>', htmlerrorEmail).replace('errorClassEmail', 'form-invalid-data')
    if result == 'pass':
        htmlerror = valiadtionMessage.replace('**error**', 'Contrasena es requerida')
        body = body.replace('</password>', htmlerror).replace('errorClassPass', 'form-invalid-data')
    elif result == 'user':
        htmlerror = valiadtionMessage.replace('**error**', 'Usuario es requerido')
        body = body.replace('</username>', htmlerror).replace('errorClassUser', 'form-invalid-data')
    elif result == 'email':
        htmlerror = valiadtionMessage.replace('**error**', 'Email es requerido')
        body = body.replace('</email>', htmlerror).replace('errorClassEmail', 'form-invalid-data')

if creeateAccount:
    #save to session
    print ("Content-type: text/html\n\n")
    print ("Location: signup.py")
else:
    if conn is not None:
        err = str(conn.errors())
        body = body.replace('</error>', err).replace('errorClass', 'form-invalid-data')

print ("Content-type: text/html\n\n")
wholepage = pagetemplate.replace('**title**', 'Sign Up').replace('**css**', css).replace('**body**', body).replace('#action', 'signup.py')
ucgiprint(wholepage)
    