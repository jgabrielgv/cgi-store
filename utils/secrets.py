#!/usr/bin/python3
"""This script contains hash method for encript password in the login form"""
import os
import hashlib
import sys
import uuid

SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
SCRIPT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..'))
if not SCRIPT_DIR in sys.path:
    sys.path.append(SCRIPT_DIR)

def check_password(user, password):
    """
    Checks the OpenLDAP tagged digest against the given password
    """
    hashed_password = hashlib.sha512(password.encode('utf-8') + user.salt.encode('utf-8')).hexdigest()
    return user.password == hashed_password

def make_secret(password):
    #https://stackoverflow.com/a/9595108
    """
    Encodes the given password as a base64 SSHA hash+salt buffer
    """
    salt = uuid.uuid4().hex.encode('utf-8')
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt).hexdigest()
    return {'salt': salt, 'password': hashed_password}
