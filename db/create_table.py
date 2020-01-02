import inspect

from sqlite3 import Error

from .crud import insert_products


def create_table_and_seed(conn, create_table_sql, products):
    try:
        result = create_table(conn, create_table_sql)

        if result is not None:
            # seed the table with data if table was created
            insert_products(conn, products)

    except Error as e:
        message = str(e) + " from method " + inspect.stack()[0][3]
        print(message)


def create_table(conn, create_table_sql):
    try:
        return conn.cursor().execute(create_table_sql)

    except Error as e:
        message = str(e) + " from method " + inspect.stack()[0][3]
        print(message)
        return None
