#!/usr/bin/python
"""This script shows the login page"""
import time
import session


sess = session.Session(expires=365*24*60*60, cookie_path='/')
# expires can be reset at any moment:
#sess.set_expires('')
# or changed:
#sess.set_expires(30*24*60*60)
#data = session.Data
# Session data is a dictionary like object
lastvisit = sess.data.get('lastvisit')
if lastvisit:
    message = 'Welcome back. Your last visit was at ' + \
        time.asctime(time.gmtime(float(lastvisit)))
else:
    message = 'New session'
# Save the current time in the session
sess.data['lastvisit'] = repr(time.time())
print "Location: index.py"
print """\
%s
Content-Type: text/plain\n
sess.cookie = %s
sess.data = %s
%s
""" % (sess.cookie, sess.cookie, sess.data, message)

#print "Content-type: text/html\n\n"
