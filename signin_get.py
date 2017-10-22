#!/usr/bin/python
"""This script stores the post action when sign in"""

#from os import getenv
import sys
from helpers import FormParser

query_string = sys.stdin.read() # reads the parameters, username=xxx&password=xxx
parser = FormParser()
parser.parse_values(query_string)#query_string.partition('&')

#print "Location: signup.py" # redirect to another page when success

print "Content-type:text/html\r\n\r\n"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<p>Parrafo<p>"
print "<h2>username: %s, password: %s, other: %s, len: %s</h2>" % (parser.get_value("username", ""), parser.get_value("password", ""), parser.get_value("other", ""), parser.elements_count())
print "</body>"
print "</html>"
