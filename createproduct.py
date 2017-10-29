#!/usr/bin/python
"""Shows the page for create new products"""
import os
import utils.constants as constants
from utils.helpers import print_page
from utils.helpers import loadhtml, ucgiprint
import utils.globals_values
from utils.globals_values import constains_key, pop_value
#from __main__ import *

print "Content-type: text/html\n\n"

print '''
    <!--<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0
    Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml"
            lang="en" xml:lang="en">-->
            <head>
                    <title>Titulo</title>
                    <meta http-equiv="Content-Type"
                            content="text/html;
                            charset=UTF-8" />
                            <link rel="stylesheet" type="text/css" href="css/styles.css">
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
            </head>
            <body>
            '''
ucgiprint(loadhtml("createproduct.html"))
print "Contains: %s" % (constains_key(constants.ERROR))
print "Error: %s" % (utils.globals_values.error)
if constains_key(constants.ERROR):
    print "<b>%s</b>" % (pop_value(constants.ERROR))
else:
    print "<b>mierda</b>"
#                    **body**
print '''                    <script src="js/main.js"></script>
            </body>
    
    '''

#print_page("createproduct.html", "Crear producto")
