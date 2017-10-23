#!/usr/bin/python
"""Defines the entity models"""

class User(object):
    """Defines a simple User entity"""
    def __init__(self, user_id=0, username=""):
        self.user_id = user_id
        self.username = username

class Product(object):
    """Defines a simple Product entity"""
    def __init__(self, product_id=0, user_id=0, code="", entry_date=None, descr="", price=0, image=""):
        self.product_id = product_id
        self.user_id = user_id
        self.code = code
        self.entry_date = entry_date
        self.descr = descr
        self.price = price
        self.image = image
