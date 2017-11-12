#!/usr/bin/python
"""This script shows the logout an user from his current session"""
import time
import session
import os
from data.dao import Connection


sess = session.Session(expires='Thu, 01 Jan 1970 00:00:00 GMT', cookie_path='/')
lastvisit = sess.data.get('lastvisit')
if lastvisit:
    message = 'Welcome back. Your last visit was at ' + \
        time.asctime(time.gmtime(float(lastvisit)))
else:
    message = 'New session'
# Save the current time in the session
sess.data['lastvisit'] = repr(time.time())
cookie_file = '/Users/mcanales/Sites' + '/session/sess_' + sess.cookie['sid'].value + '.db'
os.remove(cookie_file)
sess.cookie['sid']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'

conn = Connection()
delete_cookie = conn.delete_user_history(sess.cookie['sid'].value)

for cookie in sess.cookie:
    sess.cookie[cookie]['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
#sess.cookie["sid"] = ''
sess.close()
#sess.cookie.clear()
print "Location: signin.py"
print """\
%s
Content-Type: text/plain\n
sess.cookie = %s
%s
""" % (sess.cookie, sess.cookie, message)
sess.cookie.clear()
#print "Content-type: text/html\n\n"
