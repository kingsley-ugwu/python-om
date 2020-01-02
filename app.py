# Standard library imports
import sqlite3
import os

# Third party imports
from flask import Flask, json, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db

# Local application imports
from db.connection import create_connection
from db.create_table import create_table_and_seed
from db.crud import insert_products, update_product, delete_product

fileDir = os.path.dirname(os.path.realpath("__file__"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///db\pythonsqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Products(db.Model):
    # explicitiy define tablename to avoid use of the class name
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    price = db.Column(db.Float())

    def __repr__(self):
        return str({
            "id": self.id,
            "name": self.name,
            "price": str(self.price)
        })


@app.before_first_request
def run_once():
    main()


@app.route('/v1/products', methods=['GET'])
def get_products():
    response = app.response_class(
        response=str(db.session.query(Products).all()).replace("'", '"'),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/v1/product/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def product_by_id(product_id):
    result = db.session.query(Products).filter_by(
        id=product_id).all()

    if result == []:
        return app.response_class(
            response="Not Found",
            status=404,
            mimetype='application/json'
        )

    product = result[0]
    response = app.response_class(
        response=str(result[0]).replace("'", '"'),
        status=200,
        mimetype='application/json'
    )

    request_body = request.json

    if request.method == 'PUT':
        conn = get_db_connection()
        updated_product = (request_body['name'] if 'name' in request_body else
                           product['name']), (request_body['price'] if 'price' in request_body else
                                              product['price']), product['id']
        update_product(conn, tuple(updated_product))
    elif request.method == 'DELETE':
        conn = get_db_connection()
        delete_product(conn, product_id)

    return response


@app.route('/v1/product', methods=['POST'])
def add_product():
    product = request.json
    result = validate_body(product)

    if result is not None:
        return result

    conn = get_db_connection()
    insert_products(conn, [tuple(list(product.values()))])
    result = str(db.session.query(Products).filter_by(
        name=product['name']).all()).replace("'", '"')
    return json.loads(result)[0]


def validate_body(product):
    if not 'name' in product or not 'price' in product:
        response = app.response_class(
            response='{"error": "required attributes missing"}',
            status=400,
            mimetype='application/json'
        )
        return response


def main():
    # create a db connection
    conn = get_db_connection()

    if conn is not None:
        sql_create_products_table = """ CREATE TABLE products (id integer PRIMARY KEY, name text NOT NULL, price real); """
        products = [('Lavender heart', 9.25),
                    ('Personalised cufflinks', 45.00), ('Kids T-shirt', 19.95)]

        # create table and seed if a successful connection has been made to the database
        create_table_and_seed(conn, sql_create_products_table, products)
        print("Database connection established")
    else:
        print("Cannot create database connection.")


def get_db_connection():
    database = os.path.join(fileDir, "db", "pythonsqlite.db")
    return create_connection(database)


if __name__ == '__main__':
    main()
