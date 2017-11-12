#!/usr/bin/python
"""This script shows the suggerents for no register users"""

import sys, os
from utils.helpers import pagetemplate, valiadtionMessage, ucgiprint, loadhtml, FormParser, check_user_seesion
import urllib
css = '<link rel="stylesheet" type="text/css" href="css/styles.css">'
body = loadhtml('survey1.html')
wholepage = pagetemplate.replace('**title**', 'Sugerencias').replace('**css**', css).replace('**body**', body).replace('#action', 'signin.py').replace('**scripts**', '<script src="js/create_suge.js"></script>')
if check_user_seesion():
    ucgiprint(wholepage)
else:
    print "Location: signin.py"
    print "Content-type: text/plain\n"
#sURL = os.path.realpath('.')
#print sURL
#url = os.environ["REQUEST_URI"] 
#final_url= "http://127.0.0.1/\x7Emcanales/cgi-bin/survey.py"
#print final_url
#final_url= urllib.urlencode("http://127.0.0.1/~mcanales/cgi-bin/survey.py")
#print final_url