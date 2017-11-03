#!/usr/bin/python
"""Handles the connection between Python and MariaDB"""

import mysql.connector as mariadb


class Connection(object):
    """Handles the connection between Python and MariaDB"""

    def __init__(self):
        self.db = None

    def close_connection(self):
        """Close the existing connection"""
        self.db.close()

    def open_connection(self):
        """Open the existing connection"""
        self.db = mariadb.connect(user='cgistore', password='M2rI.DB_C', database='store_lab')

    def select_animals(self):
        """Select the animals from the database"""
        return self.select_command("select identifier,name,family from animals")

    def select_command(self, command):
        """Generic select command"""
        self.open_connection()
        cur = self.db.cursor()
        cur.execute(command)
        query = cur.fetchall()
        self.close_connection()
        return query

"""for identifier, name, family in query:
    print("<p> ID: {}, Name: {}, Family: {}</p>\n").format(identifier, name, family)"""