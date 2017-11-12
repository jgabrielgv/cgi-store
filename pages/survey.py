#!/usr/bin/python3
"""This script shows the suggerents for no register users"""

import sys, os

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from utils import constants
from utils.helpers import pagetemplate, valiadtionMessage, ucgiprint, loadhtml, FormParser
import urllib

body = loadhtml('survey.html')
wholepage = pagetemplate.replace('**title**', 'Sugerencias').replace('**css**', constants.DEFAULT_CSS).replace('**body**', body).replace('**scripts**', '<script src="../js/create_suge.js"></script>') \
.replace('**menu**', '')
print("Content-type: text/html\n\n")
ucgiprint(wholepage)
