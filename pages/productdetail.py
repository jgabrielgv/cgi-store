#!/usr/bin/python3
"""Shows a product detail"""

import os
import sys

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from data.dao import Connection
from utils.helpers import FormParser, loadhtml, print_page
from utils import constants, helpers

def __form_add_qty_content():
    return """
            <form name="frmIncreaseCartQty" method="post" onSubmit="javaScript:increase_cart_qty('frmIncreaseCartQty', event)">
                        <input type="hidden" name="code" value="{0}">
                        <fieldset>
                            <legend>Agregar al carrito</legend>
                            <table>
                                <tr>
                                    <td>Cantidad</td>
                                    <td>
                                        <div id="invalid_quantity">
                                            <input type="number" name="quantity" value="1">
                                            <div class="hide-content">
                                                <span class="form-invalid-data-sign">
                                                    <i class="fa fa-close"></i>
                                                </span>
                                                <span id="invalid_quantity_msg" class="form-invalid-data-info"></span>
                                            </div>
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="2">
                                        <div id="validation_error">
                                            <div class="hide-content">
                                                <span id="validation_error_msg" class="form-invalid-data-info"></span>
                                            </div>
                                        </div>
                                        <input type="submit" value="Agregar">
                                    </td>
                                </tr>
                            </table>
                        </fieldset>
                    </form>
           """

def __build_dynamic_content():
    parser = FormParser()
    parser.discover_values()
    code = parser.get_value("code", "")

    if not code or not parser.elements_count:
        return ''

    conn = Connection()
    product = conn.fetch_product_by_code(code)
    if not product:
        return ''

    return loadhtml("productdetail.html").format(product.code, product.descr, product.price, \
    product.username, product.entry_date).replace("**add_qty**", __form_add_qty_content().format(product.code) if helpers.check_user_session() else '')

__DATA = __build_dynamic_content()

print_page('', "Producto", constants.DEFAULT_CSS, \
__DATA if __DATA else "<p>El producto no existe.</p>", \
 '<script src="../js/product_detail.js"></script>')
