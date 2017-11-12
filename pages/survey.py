#!/usr/bin/python3
"""This script shows the suggerents for no register users"""

import sys, os
from utils.helpers import pagetemplate, valiadtionMessage, ucgiprint, loadhtml, FormParser
import urllib
css = '<link rel="stylesheet" type="text/css" href="css/styles.css">'
body = loadhtml('survey.html')
wholepage = pagetemplate.replace('**title**', 'Sugerencias').replace('**css**', css).replace('**body**', body).replace('**scripts**', '<script src="js/create_suge.js"></script>')
ucgiprint(wholepage)