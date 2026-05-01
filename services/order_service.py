import datetime
from typing import List, Optional
from models.order import Order, OrderItem
from models.user import User
from services.product_service import ProductService
from services.cart_service import CartService
from services.auth_service import AuthService
from utils.data_manager import DataManager

class OrderService:
    def __init__(self, auth_service: AuthService, product_service: ProductService, cart_service: CartService):
        self.auth_service = auth_service
        self.product_service = product_service
        self.cart_service = cart_service
        self._load_orders()

    def _load_orders(self):
        data = DataManager.load_data("orders.json")
        self.orders = {o_data["order_id"]: Order.from_dict(o_data) for o_data in data}

    def _save_orders(self):
        DataManager.save_data("orders.json", [o.to_dict() for o in self.orders.values()])

    def create_order(self, user: User, payment_method: str = "COD", discount: float = 0.0) -> Optional[Order]:
        if not user.cart:
            return None
            
        subtotal = self.cart_service.calculate_subtotal(user)
        tax = round((subtotal - discount) * 0.05, 2)  # 5% tax
        total = round(subtotal - discount + tax, 2)
        
        items = []
        for pid, qty in user.cart.items():
            product = self.product_service.get_product(pid)
            if product:
                items.append(OrderItem(product.product_id, product.name, qty, product.price))
                self.product_service.update_stock(pid, -qty)
                
        order_id = f"ORD{len(self.orders) + 1:04d}"
        new_order = Order(order_id, user.user_id, items, subtotal, discount, tax, total, payment_method)
        
        self.orders[order_id] = new_order
        self._save_orders()
        self.auth_service.log_activity(user.user_id, f"Placed order {order_id} for ₹{total}")
        self.cart_service.clear_cart(user)
        return new_order

    def get_user_orders(self, user_id: str) -> List[Order]:
        return [o for o in self.orders.values() if o.user_id == user_id]

    def get_all_orders(self) -> List[Order]:
        return list(self.orders.values())

    def cancel_order(self, order_id: str, user_id: str) -> bool:
        order = self.orders.get(order_id)
        if order and order.user_id == user_id and order.status in ["Placed", "Packed"]:
            order.status = "Cancelled"
            # Return stock
            for item in order.items:
                self.product_service.update_stock(item.product_id, item.quantity)
            self._save_orders()
            self.auth_service.log_activity(user_id, f"Cancelled order {order_id}")
            return True
        return False

    def simulate_order_status(self, order: Order) -> str:
        """Simulate order status based on time elapsed since creation."""
        if order.status == "Cancelled":
            return "Cancelled"
        
        try:
            created_at = datetime.datetime.fromisoformat(order.timestamp)
        except ValueError:
            return order.status
            
        delta = datetime.datetime.now() - created_at
        minutes = delta.total_seconds() / 60.0
        
        states = ["Placed", "Packed", "Shipped", "Out for Delivery", "Delivered"]
        
        if minutes > 4: order.status = "Delivered"
        elif minutes > 3: order.status = "Out for Delivery"
        elif minutes > 2: order.status = "Shipped"
        elif minutes > 1: order.status = "Packed"
        
        return order.status

    def process_return(self, order_id: str, user_id: str) -> str:
        order = self.orders.get(order_id)
        if not order or order.user_id != user_id:
            return "Order not found."
            
        self.simulate_order_status(order)
        if order.status != "Delivered":
            return "Only delivered orders can be returned."
            
        order.status = "Returned (Refund in progress)"
        for item in order.items:
            self.product_service.update_stock(item.product_id, item.quantity)
            
        self._save_orders()
        self.auth_service.log_activity(user_id, f"Initiated return for order {order_id}")
        return "Return accepted. Refund will be processed in 3-5 business days."
