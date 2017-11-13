#!/usr/bin/python3
"""Page displayed when a resource is not found"""

'''
import os
import sys

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from utils import constants, helpers
'''

print("Content-type: text/html\n\n")
print("<p>El recurso no puede ser accedido. Ir al <a href='index.py'>inicio</a>.</p>")
