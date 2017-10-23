#!/usr/bin/python
"""This script contains the helper functions used across the website"""

import os
from urllib2 import unquote

#import sys, urllib
#query_string = sys.stdin.read()
#multiform = urllib.parse_qs(query_string)

def get_local_path():
    """Returns the local path"""
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def embed_file(path, file_name):
    """Embed content"""
    #includes the signup html code
    f = open(os.path.join(path, file_name), 'r')
    print f.read()
    f.close()

def embed_local_file(file_name):
    """Embed content from local path"""
    __location__ = get_local_path()
    embed_file(__location__, file_name)

class FormParser(object):
    """Form parser class"""

    def __init__(self):
        #validate element
        self.reset_properties()

    def get(self, key, default_value):
        """Gets an element from an array"""
        return self.__elements.get(key, default_value)

    def elements_count(self):
        """Retunrs the elements size"""
        return self.__elements_count

    def parse_values(self, input_value):
        """Parse parameters"""
        self.reset_properties()
        default_return_value = []

        input_values = input_value.split("&")
        if not input_values:
            return default_return_value

        filtered_list = [x for x in input_values if "=" in x]
        if not filtered_list:
            return default_return_value

        params_definition = []
        for value in filtered_list:
            key_value = value.split("=")
            if not key_value or key_value[0] in params_definition:
                continue
            self.__elements[key_value[0]] = unquote(key_value[1]) if len(key_value) > 1 else ""
            self.__elements_count += 1
            params_definition.append(key_value[0])

    def reset_properties(self):
        """Reset the parameters to the default state"""
        self.__elements_count = 0
        self.__elements = {}
