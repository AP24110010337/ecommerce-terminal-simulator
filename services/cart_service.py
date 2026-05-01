from models.user import User
from services.product_service import ProductService
from services.auth_service import AuthService
from typing import Dict, Any

class CartService:
    def __init__(self, auth_service: AuthService, product_service: ProductService):
        self.auth_service = auth_service
        self.product_service = product_service

    def add_item(self, user: User, product_id: str, quantity: int = 1) -> str:
        product = self.product_service.get_product(product_id)
        if not product:
            return "Product not found."
            
        current_qty = user.cart.get(product_id, 0)
        if product.stock < current_qty + quantity:
            return "Insufficient stock."
            
        user.cart[product_id] = current_qty + quantity
        self.auth_service.update_user_data(user)
        return "Added to cart."

    def update_quantity(self, user: User, product_id: str, quantity: int) -> str:
        product = self.product_service.get_product(product_id)
        if not product:
            return "Product not found."
            
        if quantity <= 0:
            return self.remove_item(user, product_id)
            
        if product.stock < quantity:
            return "Insufficient stock."
            
        user.cart[product_id] = quantity
        self.auth_service.update_user_data(user)
        return "Cart updated."

    def remove_item(self, user: User, product_id: str) -> str:
        if product_id in user.cart:
            del user.cart[product_id]
            self.auth_service.update_user_data(user)
            return "Removed from cart."
        return "Item not in cart."

    def calculate_subtotal(self, user: User) -> float:
        subtotal = 0.0
        for pid, qty in user.cart.items():
            product = self.product_service.get_product(pid)
            if product:
                subtotal += product.price * qty
        return round(subtotal, 2)

    def get_cart_details(self, user: User) -> list:
        details = []
        for pid, qty in user.cart.items():
            product = self.product_service.get_product(pid)
            if product:
                details.append({
                    "product_id": product.product_id,
                    "name": product.name,
                    "price": product.price,
                    "quantity": qty,
                    "total": round(product.price * qty, 2)
                })
        return details

    def clear_cart(self, user: User):
        user.cart.clear()
        self.auth_service.update_user_data(user)
