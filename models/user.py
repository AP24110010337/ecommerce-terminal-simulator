from typing import Dict, Any, List

class User:
    def __init__(self, user_id: str, username: str, password_hash: str, role: str = "customer"):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.cart: Dict[str, int] = {}  # product_id -> quantity
        self.wishlist: List[str] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role,
            "cart": self.cart,
            "wishlist": self.wishlist
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        user = cls(
            user_id=data.get("user_id"),
            username=data.get("username"),
            password_hash=data.get("password_hash"),
            role=data.get("role", "customer")
        )
        user.cart = data.get("cart", {})
        user.wishlist = data.get("wishlist", [])
        return user
