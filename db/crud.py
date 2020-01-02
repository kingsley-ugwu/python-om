import inspect

from sqlite3 import Error


# create
def insert_products(conn, insert_sql):
    try:
        sql = 'INSERT INTO products(name, price) VALUES(?, ?)'
        conn.cursor().executemany(sql, insert_sql)
        conn.commit()
    except Error as e:
        message = str(e) + " from method " + inspect.stack()[0][3]
        print(message)


# update
def update_product(conn, product):
    try:
        sql = 'UPDATE products SET name = ?, price = ? WHERE id = ?'
        conn.cursor().execute(sql, product)
        conn.commit()
    except Error as e:
        message = str(e) + " from method " + inspect.stack()[0][3]
        print(message)


# delete
def delete_product(conn, id):
    try:
        sql = 'DELETE FROM products WHERE id=?'
        conn.cursor().execute(sql, (id,))
        conn.commit()
    except Error as e:
        message = str(e) + " from method " + inspect.stack()[0][3]
        print(message)
