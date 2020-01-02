import inspect

from flask import Flask
app = Flask(__name__)


@app.route('/v1/products', methods=['GET'])
def get_products():
    return "Hello World from " + inspect.stack()[0][3]


@app.route('/v1/product', methods=['POST'])
def add_product():
    return "Hello World from " + inspect.stack()[0][3]


@app.route('/v1/product/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def product_by_id(product_id):
    return "Hello World from " + inspect.stack()[0][3]


if __name__ == '__main__':
    app.run()
