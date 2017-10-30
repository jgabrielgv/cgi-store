#!/usr/bin/python
"""Shows the page for create new products"""
import utils.constants as constants
from utils.helpers import print_page
#import utils.globals_values
#from utils.globals_values import constains_key, pop_value

print_page("createproduct.html", "Crear nuevo producto", constants.DEFAULT_CSS)

#print "Contains: %s" % (constains_key(constants.ERROR))
#print "Error: %s" % (utils.globals_values.error)
#if constains_key(constants.ERROR):
#    print "<b>%s</b>" % (pop_value(constants.ERROR))
#else:
#    print "<b>mierda</b>"