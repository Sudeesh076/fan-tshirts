from flask import Blueprint, request, jsonify

from coredb.Orders import add_order, add_order_item, add_order_track,get_orders,add_old_order_track
from helpers.Orders import NewOrdersRequest,OrderFilters,OrderUpdate

orders_api = Blueprint('orders', __name__)


@orders_api.route('/orders', methods=['POST'])
def new_orders():
    try:
        data = request.get_json()
        new_orders_request = NewOrdersRequest.from_json(data)
        order = new_orders_request.to_Order(new_orders_request)
        order_items = new_orders_request.to_OrderItems(new_orders_request, order)
        order_tracks = new_orders_request.to_OrderTrack(order_items)
        add_order(order)
        add_order_item(order_items)
        add_order_track(order_tracks)
        return jsonify({"Message": "your order is successfully placed"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@orders_api.route('/orders', methods=['PUT'])
def update_orders():
    try:
        data = request.get_json()
        orderUpdate = OrderUpdate.from_json(data)
        message = add_old_order_track(orderUpdate.OrderItemId,orderUpdate.Status)
        return jsonify({"Message": message}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@orders_api.route('/orders/get', methods=['POST'])
def get_user():
    try:
        data = request.get_json()
        orderFilters = OrderFilters.from_json(data)
        orders = get_orders(orderFilters.UserId,orderFilters.OrderId)
        return jsonify(orders),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
