#!/usr/bin/python
"""This script shows the login page"""

from utils import constants
from utils.helpers import print_page

print_page('signin.html', "Iniciar sesion", constants.DEFAULT_CSS)
