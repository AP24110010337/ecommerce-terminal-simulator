from typing import List
from models.product import Product
from models.user import User
from services.product_service import ProductService
import random

class RecommendationService:
    def __init__(self, product_service: ProductService):
        self.product_service = product_service

    def get_popular(self, n: int = 5) -> List[Product]:
        products = self.product_service.get_all_products()
        # Sort by rating and reviews_count combined heuristic
        return sorted(products, key=lambda p: (p.rating * 10) + p.reviews_count, reverse=True)[:n]

    def get_similar(self, product_id: str, n: int = 5) -> List[Product]:
        product = self.product_service.get_product(product_id)
        if not product:
            return []
            
        same_cat = [p for p in self.product_service.get_all_products() if p.category == product.category and p.product_id != product_id]
        random.shuffle(same_cat)
        return same_cat[:n]

    def get_for_user(self, user: User, n: int = 5) -> List[Product]:
        if not user.wishlist and not user.cart:
            return self.get_popular(n)
            
        cats = set()
        for pid in user.wishlist + list(user.cart.keys()):
            p = self.product_service.get_product(pid)
            if p: cats.add(p.category)
            
        recommended = []
        for p in self.product_service.get_all_products():
            if p.category in cats and p.product_id not in user.wishlist and p.product_id not in user.cart:
                recommended.append(p)
                
        random.shuffle(recommended)
        if not recommended:
            return self.get_popular(n)
        return recommended[:n]
