#!/usr/bin/python
"""Defines the entity models"""
from utils.helpers import current_date

class User(object):
    """Defines a simple User entity"""
    def __init__(self, user_id=0, username="", email="", password="", entry_date=current_date()):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.entry_date = entry_date

class Product(object):
    """Defines a simple Product entity"""
    def __init__(self, product_id=0, user_id=0, code="", entry_date=current_date(), descr="", price=0, image_path=""):
        self.product_id = product_id
        self.user_id = user_id
        self.code = code
        self.entry_date = entry_date
        self.descr = descr
        self.price = price
        self.image_path = image_path