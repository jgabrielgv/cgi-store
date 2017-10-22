#!/usr/bin/python
"""This script shows the login page"""

print "Content-type: text/html\n\n"

from helpers import embed_local_file

embed_local_file('signin.html')
