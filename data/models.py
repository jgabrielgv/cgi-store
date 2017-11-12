#!/usr/bin/python3
"""Defines the entity models"""

import os
import sys
__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

#from utils.helpers import current_date
from datetime import datetime

class User(object):
    """Defines a simple User entity"""
    def __init__(self, user_id=0, username="", email="", password="", salt="", entry_date="", name=""):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.salt = salt
        self.entry_date = entry_date
        self.name = name

class Suggestion(object):
    """Defines a simple User entity"""
    def __init__(self, user_id=0, entry_date="", reason="", message="", name="", email=""):
        self.user_id = user_id
        self.entry_date = entry_date
        self.reason = reason
        self.message = message  
        self.name = name
        self.email = email
              
class Product(object):
    """Defines a simple Product entity"""
    def __init__(self, product_id=0, user_id=0, code="", entry_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), descr="", price=0, image_path=""): 
        self.product_id = product_id 
        self.user_id = user_id 
        self.code = code 
        self.entry_date = entry_date 
        self.descr = descr 
        self.price = price 
        self.image_path = image_path 

class ProductDetail(object): 
    """Defines a simple Product entity""" 
    def __init__(self, product_id=0, username="", code="", entry_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), descr="", price=0, image_path=""): 
        self.product_id = product_id 
        self.username = username 
        self.code = code 
        self.entry_date = entry_date 
        self.descr = descr 
        self.price = price 
        self.image_path = image_path 
 
class ShoppingCart(object): 
    def __init__(self, user_id=0, product_id=0, quantity=0): 
        self.user_id = user_id 
        self.product_id = product_id 
        self.quantity = quantity 
 
class ShoppingCartDetail(object): 
    """def __init__(self, quantity): 
        super(ShoppingCartDetail, self).__init__(quantity) 
        self.quantity = quantity""" 
    def __init__(self, code, descr, price, username, quantity): 
        self.code = code 
        self.descr = descr 
        self.price = price 
        self.username = username 
        self.quantity = quantity 

    def total(self): 
        return self.price * self.quantity 
