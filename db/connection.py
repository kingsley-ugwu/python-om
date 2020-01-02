import inspect
import sqlite3

from sqlite3 import Error


def create_connection(full_db_path):
    try:
        # return connection object to SQLite db if successful
        return sqlite3.connect(full_db_path)
    except Error as e:
        message = str(e) + " from method " + inspect.stack()[0][3]
        print(message)

        # return none if connection to db was not successful
        return None
