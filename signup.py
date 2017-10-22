#!/usr/bin/python
"""This script shows the signup screen"""

print "Content-type: text/html\n\n"

from helpers import embed_local_file

embed_local_file('signup.html')
