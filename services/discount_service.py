from utils.data_manager import DataManager
from typing import Dict, Any, Tuple

class DiscountService:
    def __init__(self):
        self._load_coupons()

    def _load_coupons(self):
        self.coupons = DataManager.load_data("coupons.json")

    def validate_coupon(self, code: str, subtotal: float) -> Tuple[bool, str, float]:
        """Returns (is_valid, message, discount_amount)"""
        code = code.upper()
        if code not in self.coupons:
            return False, "Invalid coupon code.", 0.0
            
        coupon = self.coupons[code]
        if subtotal < coupon.get("min_order", 0):
            return False, f"Minimum order amount of ₹{coupon['min_order']} required.", 0.0
            
        if coupon.get("limit", 0) <= 0:
            return False, "Coupon usage limit expired.", 0.0
            
        discount = 0.0
        if coupon["type"] == "percent":
            discount = subtotal * (coupon["value"] / 100.0)
        elif coupon["type"] == "flat":
            discount = float(coupon["value"])
            
        # Ensure discount doesn't exceed subtotal
        discount = min(discount, subtotal)
        return True, "Coupon applied successfully!", round(discount, 2)

    def apply_coupon(self, code: str) -> bool:
        code = code.upper()
        if code in self.coupons and self.coupons[code].get("limit", 0) > 0:
            self.coupons[code]["limit"] -= 1
            DataManager.save_data("coupons.json", self.coupons)
            return True
        return False
