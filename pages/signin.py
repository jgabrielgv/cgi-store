#!/usr/bin/python3
"""This script shows the login page"""

import os
import sys

#PACKAGE_PARENT = 
__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from utils.helpers import pagetemplate, valiadtionMessage, ucgiprint
from utils.helpers import loadhtml, FormParser, create_cookie, check_user_seesion
from data.dao import Connection

user = False
err = False
username = None
password = None
result = None
htmlerror = ''
query_string = sys.stdin.read() # reads the parameters, username=xxx&password=xxx
sys.stdout.flush()
#print "Content-type: text/html\n\n"

def createSession():
    create_cookie(username)
    #print "Location: cookie.py"

def validate_properties():
    """Validate the product properties before save it to database"""
    errorMessage = None
    if not username and not password:
        errorMessage = 'all'
    elif not username:
        errorMessage = 'user'
    elif not password:
        errorMessage = 'pass'
    return errorMessage

if query_string:
    parser = FormParser()
    parser.parse_values(query_string)#query_string.partition('&')
    conn = Connection()
    username = parser.get_value("username", "")
    password = parser.get_value("password", "")
    if username and password:
        user = conn.fetch_user(username, password)
        if user:
            #save to session
            createSession()
            #print "Location: index.py"
            #print session.Data
        else:
            err = True
            htmlerror = valiadtionMessage.replace('**error**', str(conn.errors()))
    else:
        result = validate_properties()

if check_user_seesion():
    print "Location: index.py"
    print "Content-type: text/html\n\n"
else:
    css = '<link rel="stylesheet" type="text/css" href="css/styles.css">'
    body = loadhtml('signin.html')   
    if result:
    if result == 'all':
        htmlerror = valiadtionMessage.replace('**error**', 'Contrasena es requerida')
        htmlerrorUser = valiadtionMessage.replace('**error**', 'Usuario es requerido')
        body = body.replace('</password>', htmlerror).replace('errorClassPass', 'form-invalid-data')
        body = body.replace('</username>', htmlerrorUser).replace('errorClassUser', 'form-invalid-data')
    if result == 'pass':
        htmlerror = valiadtionMessage.replace('**error**', 'Contrasena es requerida')
        body = body.replace('</password>', htmlerror).replace('errorClassPass', 'form-invalid-data')
    elif result == 'user':
        htmlerror = valiadtionMessage.replace('**error**', 'Usuario es requerido')
        body = body.replace('</username>', htmlerror).replace('errorClassUser', 'form-invalid-data')
    if err:
    body = body.replace('</error>', htmlerror).replace('errorClass', 'form-invalid-data')

    wholepage = pagetemplate.replace('**title**', 'Log In').replace('**css**', css).replace('**body**', body).replace('#action', 'signin.py')
    ucgiprint(wholepage)