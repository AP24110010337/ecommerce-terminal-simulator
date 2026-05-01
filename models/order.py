from typing import Dict, Any, List
import datetime

class OrderItem:
    def __init__(self, product_id: str, name: str, quantity: int, price: float):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.price = price

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrderItem':
        return cls(
            product_id=data.get("product_id"),
            name=data.get("name"),
            quantity=data.get("quantity"),
            price=data.get("price")
        )

class Order:
    def __init__(self, order_id: str, user_id: str, items: List[OrderItem], 
                 subtotal: float, discount: float, tax: float, total: float, 
                 payment_method: str = "COD", status: str = "Placed"):
        self.order_id = order_id
        self.user_id = user_id
        self.items = items
        self.subtotal = subtotal
        self.discount = discount
        self.tax = tax
        self.total = total
        self.payment_method = payment_method
        self.status = status
        self.timestamp = datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "items": [item.to_dict() for item in self.items],
            "subtotal": self.subtotal,
            "discount": self.discount,
            "tax": self.tax,
            "total": self.total,
            "payment_method": self.payment_method,
            "status": self.status,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Order':
        order = cls(
            order_id=data.get("order_id"),
            user_id=data.get("user_id"),
            items=[OrderItem.from_dict(i) for i in data.get("items", [])],
            subtotal=data.get("subtotal"),
            discount=data.get("discount"),
            tax=data.get("tax"),
            total=data.get("total"),
            payment_method=data.get("payment_method", "COD"),
            status=data.get("status", "Placed")
        )
        if "timestamp" in data:
            order.timestamp = data["timestamp"]
        return order
