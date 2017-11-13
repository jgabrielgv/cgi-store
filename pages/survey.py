#!/usr/bin/python3
"""This script shows the suggerents for no register users"""

import sys, os

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from utils import constants, helpers
from utils.helpers import pagetemplate, valiadtionMessage, ucgiprint, loadhtml, FormParser
from utils.CaptchasDotNet import CaptchasDotNet
import urllib

if helpers.check_user_session():
    print("Location: survey1.py")
    print("Content-type: text/html\n\n")
    
captchas = CaptchasDotNet (client   = 'demo', secret   = 'secret')#, #alphabet = 'abcdefghkmnopqrstuvwxyz', #letters  = 6, #width    = 240, #height   = 80)

body = loadhtml('survey.html')
body = body.replace('%s', captchas.random()).replace('**captcha**',captchas.image ())
wholepage = pagetemplate.replace('**title**', 'Sugerencias').replace('**css**', constants.DEFAULT_CSS).replace('**body**', body).replace('**scripts**', '<script src="../js/create_suge.js"></script>') \
.replace('**menu**', helpers.header_menu_non_registered())
print("Content-type: text/html\n\n")
ucgiprint(wholepage)
