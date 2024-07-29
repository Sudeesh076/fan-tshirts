from flask import Blueprint, request, jsonify

from coredb.product import add_product, fetch_products
from helpers.Products import Product, ProductFilters

product_api = Blueprint('product', __name__)

@product_api.route('/product', methods=['POST'])
def new_product():
    try:
        data = request.get_json()
        product = Product.from_json(data)
        record = add_product(product)
        return record.to_dict()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_api.route('/product', methods=['POST'])
def get_user():
    try:
        data = request.get_json()
        productFilters = ProductFilters.from_json(data)
        return fetch_products(productFilters)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
