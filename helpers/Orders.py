from dataclasses import dataclass
from typing import List
from datetime import datetime
import uuid

@dataclass
class OrderFilters:
    OrderId: str = None
    UserId: str = None

    @classmethod
    def from_json(cls, data):
        OrderId = data.get('orderId', None)
        UserId = data.get('userId', None)
        result = cls(OrderId=OrderId, UserId=UserId)
        return result

@dataclass
class OrderUpdate:
    OrderItemId: str = None
    Status: str = None

    @classmethod
    def from_json(cls, data):
        OrderItemId = data.get('orderItemId', None)
        Status = data.get('status', None)
        result = cls(OrderItemId=OrderItemId, Status=Status)
        return result



@dataclass
class NewOrdersRequest:
    user_id: str
    address_id: str
    product_ids: List[str]

    @classmethod
    def from_json(cls, data):
        required_fields = ['user_id', 'address_id', 'product_ids']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'Missing required field: {field}')
        user_id = data.get('user_id')
        address_id = data.get('address_id')
        product_ids = data.get('product_ids')
        return cls(user_id=user_id, address_id=address_id, product_ids=product_ids)

    @staticmethod
    def to_Order(order_request):
        order_id = str(uuid.uuid4())
        return Order(id=order_id, user_id=order_request.user_id, address_id=order_request.address_id, payment_method="COD")

    @staticmethod
    def to_OrderItems(order_request, order):
        return [OrderItem(id=str(uuid.uuid4()), user_id=order_request.user_id, order_id=order.id, product_id=product_id) for product_id in order_request.product_ids]

    @staticmethod
    def to_OrderTrack(order_items):
        order_tracks = []
        current_datetime = datetime.now()
        current_datetime = current_datetime.strftime('%d/%m/%Y %H:%M')
        for item in order_items:
            order_tracks.append(OrderTrack(id=str(uuid.uuid4()), user_id=item.user_id, order_id=item.order_id, order_item_id=item.id, product_id=item.product_id, status="Order Placed", Time=current_datetime))
        return order_tracks

@dataclass
class Order:
    id : str
    user_id: str
    address_id : str
    payment_method :str

@dataclass
class OrderItem:
    id : str
    order_id: str
    user_id : str
    product_id :str

@dataclass
class OrderTrack:
    id : str
    order_id: str
    order_item_id : str
    product_id : str
    user_id : str
    status : str
    Time :str
# Order Placed,Order Shipped,Order Delivered,Order Refunded
