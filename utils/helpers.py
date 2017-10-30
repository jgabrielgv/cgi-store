#!/usr/bin/python
"""This script contains the helper functions used across the website"""

import os
import sys
from urllib2 import unquote
from datetime import datetime

def current_date():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_session_user_id():
    return 2

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def print_page(html_file, title, css_file='', body=''):
    """Prints a page based on the html and css parameter specifications"""
    print "Content-type: text/html\n\n"
    if not body and html_file:
        body = loadhtml(html_file)
    wholepage = pagetemplate.replace('**title**', title).replace('**css**', css_file).replace('**body**', body)
    ucgiprint(wholepage)

def ucgiprint(inline='', unbuff=False, encoding='UTF-8'):
    """Print to the stdout.
    Includes keywords to define the output encoding
    (UTF-8 default, set to None to switch off encoding)
    and also whether we should flush the output buffer
    after every write (default not).
    """
    line_end = '\r\n'
    if encoding:
        inline = inline.encode(encoding)
        # prob. not necessary as line endings will be the
        # same in most encodings
        line_end = line_end.encode(encoding)
    sys.stdout.write(inline)
    sys.stdout.write(line_end)
    if unbuff:
        sys.stdout.flush()

def loadhtml(filename):
    with open(filename, 'rb') as myfile:
        body = myfile.read().decode("UTF-8").replace('\n', '')
    return body

def replace(instring, indict):
    """
    A convenient way of doing multiple replaces in a
    single string. E.g. for html templates. Takes a
    string and a dictionary of replacements. In the
    dictionary - each key is replaced with it's value.
    We can also accept a list of tuples instead of a
    dictionary (or anything accepted by the dict
    function).
    """
    indict = dict(indict)
    for key in indict:
        instring = instring.replace(key, indict[key])
    return instring

# let's define out html values and templates
pagetemplate = '''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0
    Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml"
            lang="en" xml:lang="en">
            <head>
                    <title>**title**</title>
                    <meta http-equiv="Content-Type"
                            content="text/html;
                            charset=UTF-8" />
                            **css**
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
            </head>
            <body>
                    **body**
                    <script src="js/main.js"></script>
            </body>
    </html>
    '''

class FormParser(object):
    """Form parser class"""

    def __init__(self):
        #validate element
        self.reset_properties()

    def get_value(self, key, default_value):
        """Gets an element from an array"""
        return self.__elements[key] if key in self.__elements else default_value

    def elements_count(self):
        """Retunrs the elements size"""
        return self.__elements_count

    def parse_get_values(self):
        """Parse the QUERY_STRING parameters"""
        self.parse_values(os.environ["QUERY_STRING"])

    def parse_post_values(self):
        """Parse the stdin parameters"""
        self.parse_values(sys.stdin.read())

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
