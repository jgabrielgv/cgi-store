#!/usr/bin/python
"""Handles the connection between Python and MariaDB"""

import MySQLdb
from models import Product

class Connection(object):
    """Handles the connection between Python and MariaDB"""

    def __init__(self):
        self.__db = None

    def __close_connection(self):
        """Close the existing connection"""
        self.__db.close()

    def __open_connection(self):
        """Open the existing connection"""
        self.__db = MySQLdb.connect(host="localhost", user="cgistore", passwd="M2rI.DB_C", db="store_lab")

    def create_account(self, user):
        """Creates an account based on the user information"""
        self.__open_connection()
        cursor = self.__db.cursor()
        result = True
        try:
            sql_query = """insert into user (username, email, password) values (%s, %s, %s)"""
            affected_count = cursor.execute(sql_query, (user.username, user.email, user.password,))
            self.__db.commit()
            if not affected_count:
                result = False
            #logging.warn("%d", affected_count)
            #logging.info("inserted values %d, %s", id, filename)
        except MySQLdb.IntegrityError:
            #logging.warn("failed to insert values %d, %s", id, filename)
            result = False
        finally:
            cursor.close()
        return result

    def fetch_articles(self, user_id):
        """Fetch all articles from a specic user"""
        self.__open_connection()
        cursor = self.__db.cursor()
        result = []
        try:
            sql_query = """select product_id,user_id,code,entry_date,descr,price,image_path from product where user_id = %d"""
            cursor.execute(sql_query, (user_id,))
            query = cursor.fetchall()
            for product_id, user_id, code, entry_date, descr, price, image_path in query:
                result.append(Product(product_id, user_id, code, entry_date, descr, price, image_path))
            #logging.warn("%d", affected_count)
            #logging.info("inserted values %d, %s", id, filename)
        except MySQLdb.IntegrityError:
            #logging.warn("failed to insert values %d, %s", id, filename)
        finally:
            cursor.close()
        return result

    #def __select_command(self, command):
    #    """Generic select command"""
    #    self.open_connection()
    #    cur = self.__db.cursor()
    #    cur.execute(command)
    #    
    #    self.close_connection()
    #    return query

"""for identifier, name, family in query:
    print("<p> ID: {}, Name: {}, Family: {}</p>\n").format(identifier, name, family)"""