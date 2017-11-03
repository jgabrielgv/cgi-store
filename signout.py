#!/usr/bin/python
"""This script shows the logout an user from his current session"""
import time
import session


sess = session.Session(expires='Thu, 01 Jan 1970 00:00:00 GMT', cookie_path='/')
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
sess.cookie['sid']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
#sess.cookie["sid"] = ''
sess.close()
#sess.cookie.clear()
print "Location: signin.py"
#print 'Set-Cookie:sid=null;'
#print "Content-type: text/html\n\n"
print """\
%s
Content-Type: text/plain\n
sess.cookie = %s
%s
""" % (sess.cookie, sess.cookie, message)

#print "Content-type: text/html\n\n"
