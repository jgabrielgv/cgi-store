#!/usr/bin/python3
"""Handles the connection between Python and MariaDB"""

import os
import sys
import binascii

__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

from utils.helpers import current_date
from utils.secrets import check_password, make_secret
import mysql.connector as mariadb
from data.models import Product, ProductDetail, User, ShoppingCartDetail
#from getpass import getpass

class Connection(object):
    """Handles the connection between Python and MariaDB"""

    __default_sql_error = "Un error ha ocurrido en el sistema. Favor intente de nuevo."

    def __init__(self):
        self.__db = None
        self.__error_dict = ''

    def __close_connection(self, cursor=None):
        """Close the existing connection"""
        if cursor:
            cursor.close()
        self.__db.close()

    def __open_connection(self):
        """Open the existing connection"""
        self.__db = mariadb.connect(host="localhost", user='cgistore', password='M2rI.DB_C', database='store_lab')

    def __log(self, message, exception=None):
        """Logs an error in error entity"""
        self.__error_dict = message
        #print "<p>Error: %s</p>" % (message)
        #if exception:
        #    print "<p>Exception: %s</p>" % (exception)
        #logging.warn("%d", affected_count)
        #logging.info("inserted values %d, %s", id, filename)
        #logging.warn("%d", affected_count)
            #logging.info("inserted values %d, %s", id, filename)
        #except mariadb.IntegrityError as e:

    def create_account(self, user):
        """Creates an account based on the user information"""
        self.__open_connection()
        cursor = self.__db.cursor()
        result = False
        try:
            if not self.valid_user_to_create(user,  cursor):
                return result
            sql_query = """insert into user (name, username, email, password, salt, entry_date) values (%s, %s, %s, %s, %s, %s)"""
            hashed_password = make_secret(user.password)
            cursor.execute(sql_query, ('Juanchito', user.username, user.email, hashed_password['password'], hashed_password['salt'], current_date(),))
            if not cursor.rowcount:
                self.__log("No se ha podido crear la cuenta. Favor intente de nuevo.")
                return result
            self.__db.commit()
        except mariadb.Error as error:
            self.__log(self.__default_sql_error, error)
            return result
        finally:
            self.__close_connection(cursor)
        return True

    def create_product(self, product):
        """Creates an article into the database"""
        self.__open_connection()
        cursor = self.__db.cursor()
        result = False
        try:
            if not self.valid_product_to_create(product, cursor):
                return result
            sql_query = """insert into product (user_id, code, entry_date, descr, price, image_path) values (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql_query, (product.user_id, product.code, product.entry_date, product.descr, product.price, product.image_path,))
            #print "<p>rowcount1: %d</p>" % (cursor.rowcount)
            if not cursor.rowcount:
                self.__log("No se ha podido crear el producto. Favor intente de nuevo.")
                return result
            self.__db.commit()
        except mariadb.Error as error:
            self.__log(self.__default_sql_error, error)
            return result
        finally:
            self.__close_connection(cursor)
        return True

    def create_suggestion(self, suggestion):
        """Creates a suggestion for a register or not register user"""
        self.__open_connection()
        cursor = self.__db.cursor()
        result = False
        try:
            sql_query = """insert into suggestion (user_id, entry_date, reason, message, name, email) values (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql_query, (suggestion.user_id, current_date(), suggestion.reason, suggestion.message, suggestion.name, suggestion.email,))
            if not cursor.rowcount:
                self.__log("No se ha podido crear la sugerencia. Favor intente de nuevo.")
                return result
            self.__db.commit()
        except mariadb.Error as error:
            self.__log(self.__default_sql_error, error)
            return result
        finally:
            self.__close_connection(cursor)
        return True

    def errors(self):
        """Returns the error list"""
        return self.__error_dict

    def fetch_cart_products_by_user_id(self, user_id): 
        """Fetch the cart products from a specific user""" 
        self.__open_connection() 
        cursor = self.__db.cursor() 
        result = [] 
        try: 
            sql_query = """select p.code, p.descr, p.price, u.username, sc.quantity/*, price * quantity as total*/ from product p inner join shopping_cart sc on p.product_id = sc.product_id inner join user u on sc.user_id = u.user_id and sc.user_id = %s;""" 
            cursor.execute(sql_query, (user_id,)) 
            query = cursor.fetchall() 
            for code, descr, price, username, quantity in query: 
                result.append(ShoppingCartDetail(code, descr, price, username, quantity)) 
        except mariadb.Error as error: 
            self.__log(self.__default_sql_error, error) 
        finally: 
            self.__close_connection(cursor) 
        return result 

    def fetch_user(self, user_name, passwd):
        """Fetch an specific user by username"""
        self.__open_connection()
        cursor = self.__db.cursor()
        result = {}
        try:
            error_message = "Usuario y contras&eacute;a no coinciden."
            sql_query = """select user_id, username, email, password, salt, entry_date from user where username = %s"""
            cursor.execute(sql_query, (user_name,))
            dataset = cursor.fetchall()
            if not dataset:
                self.__log(error_message)
                return result
            for user_id, user_name, email, password, salt, entry_date in dataset:
                user = User(user_id, user_name, email, password, salt, entry_date)
            #print ("Content-type: text/plain\n")
            if not check_password(user, passwd):
                self.__log(error_message)
                user = result
            return user
        except mariadb.Error as error:
            self.__log(self.__default_sql_error, error)
        finally:
            self.__close_connection(cursor)
        return result

    def fetch_product_by_code(self, code): 
        """Fetch all products""" 
        self.__open_connection() 
        cursor = self.__db.cursor() 
        result = None 
        try: 
            sql_query = """select p.code, p.descr, p.price, p.entry_date, u.username from product p inner join user u on p.user_id = u.user_id and p.code = %s""" 
            cursor.execute(sql_query, (code,)) 
            query = cursor.fetchall() 
            for code, descr, price, entry_date, username in query: 
                result = ProductDetail(0, username, code, entry_date, descr, price) 
        except mariadb.Error as error: 
            self.__log(self.__default_sql_error, error) 
        finally: 
            self.__close_connection(cursor) 
        return result 

    def fetch_products_by_user_id(self, user_id):
        """Fetch all products from a specic user"""
        self.__open_connection()
        cursor = self.__db.cursor()
        result = []
        try:
            sql_query = """select code,descr,price,entry_date,image_path from product where user_id = %s""" 
            cursor.execute(sql_query, (user_id,)) 
            query = cursor.fetchall() 
            for code, descr, price, entry_date, image_path in query: 
                result.append(Product(0, 0, code, entry_date, descr, float(price), image_path)) 
        except mariadb.Error as error: 
            self.__log(self.__default_sql_error, error) 
        finally: 
            self.__close_connection(cursor) 
        return result

    #.get_value("search-keyboards", '')

    def fetch_products(self):
        """Fetch all products"""
        self.__open_connection()
        cursor = self.__db.cursor()
        result = []
        try:
            sql_query = """select p.code, p.descr, p.price, p.entry_date, u.username from product p inner join user u on p.user_id = u.user_id"""
            cursor.execute(sql_query)
            query = cursor.fetchall()
            for code, descr, price, entry_date, username in query:
                result.append(ProductDetail(0, username, code, entry_date, descr, price))
        except mariadb.Error as error:
            self.__log(self.__default_sql_error, error)
        finally:
            self.__close_connection(cursor)
        return result

    def fetch_products_by_keywords(self, keywords=''):
        result = []
        if not keywords:
            return result
        """Fetch all products by keyboard"""
        self.__open_connection()
        cursor = self.__db.cursor()
        try:
            sql_query = """select p.code, p.descr, p.price, p.entry_date, u.username from product p inner join user u on p.user_id = u.user_id where p.code like concat('%', %(keywords)s, '%') or p.descr like concat('%', %(keywords)s, '%')"""
            cursor.execute(sql_query, {"keywords": keywords})
            query = cursor.fetchall()
            for code, descr, price, entry_date, username in query:
                result.append(ProductDetail(0, username, code, entry_date, descr, price))
        except mariadb.Error as error:
            self.__log(self.__default_sql_error, error)
        finally:
            self.__close_connection(cursor)
        return result
    
    def increase_cart_qty(self, cart): 
        """Creates an article into the database""" 
        self.__open_connection() 
        cursor = self.__db.cursor() 
        result = False 
        try: 
            sql_query = """insert into shopping_cart (user_id, product_id, quantity) values  
            (%(user_id)s, %(product_id)s %(quantity)s) on duplicate key update quantity = quantity + %(quantity)s;""" 
            cursor.execute(sql_query, { "user_id": cart.user_id, "product_id": cart.product_id, "quantity": cart.quantity }) 
            if not cursor.rowcount: 
                self.__log("No se ha podido realizar la transaccion. Favor intente de nuevo.") 
                return result 
            self.__db.commit() 
        except mariadb.Error as error: 
            self.__log(self.__default_sql_error, error) 
            return result 
        finally: 
            self.__close_connection(cursor) 
        return True 
 
    def place_order(self, user_id): 
        """Checkout the current""" 
        self.__open_connection() 
        cursor = self.__db.cursor() 
        result = False 
        try: 
            sql_query = """select quantity from shopping_cart where user_id = %s limit 1;""" 
            cursor.execute(sql_query, (user_id,)) 
            query = cursor.fetchone() 
            if not query: 
                self.__log("No hay productos para pagar.") 
                return result 
 
            sql_query = """insert into invoice_header (user_id, descr, subtotal, taxes, total)  
            select u.user_id, 'Invoice' as descr, sum(p.price * sc.quantity) as subtotal, 0 as taxes,  
            sum(p.price * sc.quantity) as total from product p  
            inner join shopping_cart sc on p.product_id = sc.product_id  
            inner join user u on sc.user_id = u.user_id and sc.user_id = %s;""" 
            cursor.execute(sql_query, (user_id,)) 
 
            sql_query = """insert into invoice_detail(invoice_no, product_id, descr, quantity, price, discount)  
            select %s as invoice_no, p.product_id, p.descr, sc.quantity, p.price, 0 as discount from product p  
            inner join shopping_cart sc on p.product_id = sc.product_id  
            inner join user u on sc.user_id = u.user_id and sc.user_id = %s;""" 
            cursor.execute(sql_query, (cursor.lastrowid, user_id,)) 
 
            sql_query = """delete from shopping_cart where user_id = %s""" 
            cursor.execute(sql_query, (user_id,)) 
 
            self.__db.commit() 
        except mariadb.Error as error: 
            self.__db.rollback() 
            self.__log(self.__default_sql_error, error) 
            return result 
        finally: 
            self.__close_connection(cursor) 
        return True 

    def valid_product_to_create(self, product, cursor):
        """Validate product properties bofore save, for example, that the code_id does not exists yet"""
        result = False
        try:
            sql_query_user = """select product_id from product where code= %s limit 1"""
            #print "<p>Query: %s</p>" % (sql_query_user % (product.code))
            cursor.execute(sql_query_user, (product.code,))
            #print "<p>row count validate: %d</p>" % (cursor.rowcount)
            if cursor.fetchall():
                self.__log("El código digitado ya se encuentra registrado en el sistema.")
                return result
        except mariadb.Error as error:
            self.__log(self.__default_sql_error, error)
            return result
        return True

    def valid_user_to_create(self, user, cursor):
        """Validate product properties bofore save, for example, that the code_id does not exists yet"""
        result = False
        try:
            sql_query_user = """select user_id, username, email, password, entry_date from user where username = %s or email = %s limit 1"""
            cursor.execute(sql_query_user, (user.username, user.email,))
            if cursor.fetchall():
                self.__log("El usuario ya se encuentra registrado.")
                return result
        except mariadb.Error as error:
            self.__log(self.__default_sql_error, error)
            return result
        return True        
