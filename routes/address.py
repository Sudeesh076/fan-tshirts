from flask import Blueprint, request, jsonify

from coredb.address import add_address,get_addresses_by_user_id
from helpers.address import Address

address_api = Blueprint('address', __name__)

@address_api.route('/address', methods=['POST'])
def new_address():
    try:
        data = request.get_json()
        product = Address.from_json(data)
        record = add_address(product)
        return record.to_dict()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@address_api.route('/address/<string:user_id>', methods=['GET'])
def fetch_addresses_by_user_id(user_id):
    try:
        records = get_addresses_by_user_id(user_id)
        print(records)
        products = [record.to_dict() for record in records]
        return products
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
