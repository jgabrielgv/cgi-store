#!/usr/bin/python
"""Handles the global values"""

error = "Nada aun"

global_values = {}

def add_variable(key, value):
    global_values[key] = value
    error = value

def constains_key(key):
    return global_values.has_key(key)

def pop_value(key):
    return error
    """
    if not constains_key(key):
        return None
    value = global_values.get(key)
    delattr(global_values, key)
    return value
    """
