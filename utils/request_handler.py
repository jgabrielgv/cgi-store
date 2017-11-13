#!/usr/bin/python3

import os
import sys
import json

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from utils import constants, helpers
from data.dao import Connection

def fetch_authorized_user_session():
    sess = helpers.build_session_entity()
    conn = Connection()
    return conn.autorized_session(sess.cookie['sid'].value)

def is_user_authorized(user):
    return user and not user == '403'

def process_request(funct, errors):
    auth_user = fetch_authorized_user_session()
    if not is_user_authorized(auth_user):
        helpers.print_request(constants.FORBIDDEN, json.JSONEncoder()\
        .encode({'validation_error': constants.RELOAD_PAGE_MESSAGE}))
    elif not funct(auth_user):
        helpers.print_request(constants.BAD_REQUEST, json.dumps(errors))
    else:
        helpers.print_request(constants.SUCCESS, json.JSONEncoder().encode({'response': 'ok'}))
