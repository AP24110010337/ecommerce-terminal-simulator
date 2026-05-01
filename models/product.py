from typing import Dict, Any, List

class Product:
    def __init__(self, product_id: str, name: str, category: str, price: float, 
                 stock: int, rating: float = 0.0, reviews_count: int = 0, description: str = ""):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.rating = rating
        self.reviews_count = reviews_count
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "rating": self.rating,
            "reviews_count": self.reviews_count,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        return cls(
            product_id=data.get("product_id"),
            name=data.get("name"),
            category=data.get("category"),
            price=data.get("price"),
            stock=data.get("stock"),
            rating=data.get("rating", 0.0),
            reviews_count=data.get("reviews_count", 0),
            description=data.get("description", "")
        )
