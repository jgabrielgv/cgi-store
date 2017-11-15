#!/usr/bin/python3
"""Handles the current session"""

import os
import sys
from http import cookies
import shelve
import time
import hashlib

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from utils import config

sys.path.append(config.SESSION_FILES_ROOT_PATH)

SESSION = None
class Session(object):
    
    def __init__(self, expires=None, cookie_path=None):
        string_cookie = os.environ.get('HTTP_COOKIE', '')
        self.cookie = cookies.SimpleCookie()
        self.cookie.load(string_cookie)
        
        #if S_ID in self.cookie:
        #        sid = self.cookie[S_ID].value
        #global Data
        if self.cookie.get('sid'):
            sid = self.cookie['sid'].value
            # Clear session cookie from other cookies
            self.cookie.clear()

        else:
            self.cookie.clear()
            sid = hashlib.sha256(repr(time.time()).encode()).hexdigest()

        self.cookie['sid'] = sid

        if cookie_path:
            self.cookie['sid']['path'] = cookie_path
        
        session_dir = config.SESSION_FILES_FOLDER_PATH
       
        '''
        if not os.path.exists(session_dir):
            try:
                os.mkdir(session_dir, 0o2770)
                # If the apache user can't create it do it manualy
            except OSError as e:
                errmsg =  """
                    %s when trying to create the session directory.
                    Create it as '%s'
                """ % (e.strerror, os.path.abspath(session_dir))
                raise OSError       
        ''' 
        '''
        self.data = shelve.open (
            '%s/sess_%s' % (session_dir, sid), 
            writeback=True
        )
        nsid = sid# + '.db'
        os.chmod('%s/sess_%s' % (session_dir, nsid), 0o660)
        '''
        # Initializes the expires data
        #if not self.data.get('cookie'):
        #    self.data['cookie'] = {'expires':''}

        self.set_expires(expires)
        #Data = self.data

    def set_expires(self, expires=None):
        if expires == '':
            self.cookie['sid']['expires'] = ''
        elif isinstance(expires, int):
            self.cookie['sid']['expires'] = expires
