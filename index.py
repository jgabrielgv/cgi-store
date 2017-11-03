#!/usr/bin/python
"""This script shows the myproducts page"""

from utils.helpers import print_page
from data.dao import Connection
from utils.helpers import loadhtml, check_user_seesion
from utils import constants
#from utils.email_handler import SmtpClient


"""
client = SmtpClient("jgmezvargas@gmail.com", ["lm.sanchezvargas@gmail.com", "jgabriel.gv@hotmail.com"])
client.build_registration_template()
client.send_email()
"""

#check session status
#print "Content-type: text/html\n\n"

#field-keywords
def __details_html():
    return """<tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>"""

def __build_detail_list_html():
    conn = Connection()
    product_list = conn.fetch_products()
    detail_list = []
    if not product_list:
        return ""
    for product in product_list:
        detail_list.append(__details_html() % (product.code, product.descr, product.price, product.username, product.entry_date))
    return ''.join([x for x in detail_list])

def __build_dynamic_content():
    return loadhtml("index.html").replace("**details**", __build_detail_list_html())

#print __build_detail_list_html()
if check_user_seesion():
    print_page('', "Inicio", constants.DEFAULT_CSS, __build_dynamic_content())
else:
    print "Location: signin.py"
    print "Content-type: text/plain\n"
    #print "El usuario no esta Logueado"
