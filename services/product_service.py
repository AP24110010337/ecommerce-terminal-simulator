from typing import List, Optional
from models.product import Product
from utils.data_manager import DataManager

class ProductService:
    def __init__(self):
        self._load_products()

    def _load_products(self):
        data = DataManager.load_data("products.json")
        self.products = {p_data["product_id"]: Product.from_dict(p_data) for p_data in data}

    def _save_products(self):
        DataManager.save_data("products.json", [p.to_dict() for p in self.products.values()])

    def get_all_products(self) -> List[Product]:
        return list(self.products.values())

    def get_product(self, product_id: str) -> Optional[Product]:
        return self.products.get(product_id)

    def search_products(self, query: str) -> List[Product]:
        query = query.lower()
        return [p for p in self.products.values() if query in p.name.lower() or query in p.description.lower() or query in p.category.lower()]

    def filter_products(self, category: Optional[str] = None, min_price: float = 0, max_price: float = float('inf'), min_rating: float = 0) -> List[Product]:
        result = self.get_all_products()
        if category:
            result = [p for p in result if p.category.lower() == category.lower()]
        result = [p for p in result if min_price <= p.price <= max_price]
        result = [p for p in result if p.rating >= min_rating]
        return result

    def sort_products(self, products: List[Product], by: str = "price", reverse: bool = False) -> List[Product]:
        if by == "price":
            products.sort(key=lambda x: x.price, reverse=reverse)
        elif by == "rating":
            products.sort(key=lambda x: x.rating, reverse=reverse)
        return products

    def update_stock(self, product_id: str, quantity_change: int) -> bool:
        """Decrease stock (pass negative) or increase (pass positive). Return True if successful."""
        product = self.get_product(product_id)
        if product and product.stock + quantity_change >= 0:
            product.stock += quantity_change
            self._save_products()
            return True
        return False

    def add_product(self, product: Product):
        self.products[product.product_id] = product
        self._save_products()

    def remove_product(self, product_id: str):
        if product_id in self.products:
            del self.products[product_id]
            self._save_products()
