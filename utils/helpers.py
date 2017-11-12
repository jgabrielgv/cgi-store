#!/usr/bin/python3
"""This script contains the helper functions used across the website"""

import json
import sys
import os
from http import cookies

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))

if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

import time
from utils import constants, session
from os import environ
from urllib import parse
from datetime import datetime
import string

def check_user_seesion():
    try:
        if not "HTTP_COOKIE" in os.environ:
            return False
        cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
        sess = session.Session(expires='Thu, 01 Jan 1970 00:00:00 GMT', cookie_path='/')
        #lastvisit = sess.data.get('lastvisit')
        sess.data['lastvisit'] = repr(time.time())
        #print print_page('index.html', "Inicio")
        #print cookie["sid"].value
        if cookie["sid"].value != sess.cookie["sid"].value:
            return False
        else:
            return True

    except cookies.CookieError as error:
        return False
        #print "Content-type: text/plain\n"
#print "El usuario no esta Logueado"

def check_user_session():
    return check_user_seesion()

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

def print_page(html_file, title, css_file='', body='', scripts=''):
    """Prints a page based on the html and css parameter specifications"""
    print("Content-type: text/html\n\n")
    if not body and html_file:
        body = loadhtml(html_file)
    wholepage = pagetemplate.replace('**title**', title).replace('**css**', css_file) \
    .replace('**body**', body).replace('**scripts**', scripts)
    ucgiprint(wholepage)

def ucgiprint(inline='', unbuff=False, encoding='UTF-8'):
    """Print to the stdout.
    Includes keywords to define the output encoding
    (UTF-8 default, set to None to switch off encoding)
    and also whether we should flush the output buffer
    after every write (default not).
    """
    line_end = '\r\n'
    #if encoding:
        #inline = inline.encode('iso-8859-1')
        # prob. not necessary as line endings will be the
        # same in most encodings
        #line_end = line_end.encode('iso-8859-1')
    #sys.stdout.buffer.write(inline)
    #sys.stdout.buffer.write(line_end)
    #print ("Content-type: text/html\n\n")
    #print ("Number of lines: %s" % str(inline.encode('latin1')).splitlines())
    #for line in str(inline.encode('latin1')).splitlines():
    #    sys.stdout.write(line)

    for line in inline.splitlines(True):
        sys.stdout.write(line.encode('ascii', 'replace').decode('utf-8'))
        #sys.stdout.buffer.write(line.encode('utf-8'))
    #sys.stdout.write(str(inline.encode('latin1')))
    sys.stdout.write(line_end.encode('utf-8').decode('utf-8'))
    
    if unbuff:
        sys.stdout.flush()
    #print (inline.encode('iso-8859-1'))
    #print (line_end.encode('iso-8859-1'))

def loadhtml(filename):
    dir = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    path = os.path.normpath(os.path.join(dir, '../html'))

    filename = "%s/%s" % (path, filename)
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
valiadtionMessage = '''
<span class="form-valid-data-sign"><i class="fa fa-check"></i></span>

                <span class="form-invalid-data-sign"><i class="fa fa-close"></i></span>
                <span class="form-invalid-data-info">**error**</span>
'''
# let's define out html values and templates
pagetemplate = '''
    <!DOCTYPE html>
    <html lang="es">
            <head>
                    <title>**title**</title>
                    <meta http-equiv="Content-Type"
                            content="text/html;
                            charset=UTF-8" />
                            **css**
                            <link rel="stylesheet" href="../css/font-awesome.min.css">
                    
            </head>
            <body>
                    **body**
                    **scripts**
                    <script src="../js/main.js"></script>
            </body>
    </html>
    '''

def is_request():
    return 'REQUEST_METHOD' in environ

def get_uri_param(param_name):
    if not "REQUEST_URI" in environ:
        return ''
    parsed = parse.urlparse(environ["REQUEST_URI"])
    values = parse.urlparse.parse_qs(parsed.query)
    return values[param_name] if param_name in values else ''

def print_status_code(result, success_content={}, error_content={}, \
 success_code='Status: 200 success', error_code='Status: 400 Bad Request'):
    """Print the status code in page, be it succesfull or failed request"""
    if result:
        print('Content-Type: text/json')
        print(success_code)
        print()
        if success_content:
            print(json.dumps(success_content))
    else:
        print('Content-Type: text/json')
        print(error_code)
        print()
        print(json.dumps(error_content))

def lstrip_string(value):
    return value.lstrip() if value else value

class FormParser(object):
    """Form parser class"""

    def __init__(self):
        #validate element
        self.reset_properties()

    def get_value(self, key, default_value, strip_value=True):
        """Gets an element from an array"""
        val = self.__elements[key] if key in self.__elements else default_value
        if val and strip_value:
            val.strip()
        return val

    def elements_count(self):
        """Retunrs the elements size"""
        return self.__elements_count

    def parse_get_values(self): 
        """Parse the QUERY_STRING parameters""" 
        self.parse_values(os.environ["QUERY_STRING"]) 
 
    def parse_post_values(self): 
        """Parse the stdin parameters""" 
        self.parse_values(sys.stdin.read()) 

    def discover_values(self):
        if 'REQUEST_METHOD' in environ:
            if environ['REQUEST_METHOD'] == 'GET':
                self.parse_get_values()
            elif environ["REQUEST_METHOD"] == 'POST':
                self.parse_post_values()
        else:
            self.parse_values('')

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
            self.__elements[key_value[0]] = parse.unquote_plus(key_value[1]) if len(key_value) > 1 else ""
            self.__elements_count += 1
            params_definition.append(key_value[0])

    def reset_properties(self):
        """Reset the parameters to the default state"""
        self.__elements_count = 0
        self.__elements = {}

def validate_string_input(field_name, field_value, max_length, caption, error_dict, required=True):
    if required:
        if not field_value:
            error_dict['invalid_%s' % field_name] = constants.REQUIRED_VALUE_FORMAT % (caption)
        elif len(field_value) > max_length:
            error_dict['invalid_%s' % field_name] = \
             constants.INVALID_LENGTH_FORMAT % (caption, max_length)
    elif field_value and len(field_value) > max_length:
        error_dict['invalid_%s' % field_name] = \
         constants.INVALID_LENGTH_FORMAT % (caption, max_length)

def redirect_if_session_expired():
    if not check_user_session():
        print("Location: signin.py")
        print("Content-type: text/html\n\n")
