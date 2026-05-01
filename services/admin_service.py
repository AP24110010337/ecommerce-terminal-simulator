from typing import Dict, Any, List
from services.order_service import OrderService
from services.product_service import ProductService
from utils.data_manager import DataManager

class AdminService:
    def __init__(self, order_service: OrderService, product_service: ProductService):
        self.order_service = order_service
        self.product_service = product_service

    def get_sales_report(self) -> Dict[str, Any]:
        orders = self.order_service.get_all_orders()
        total_revenue = sum(o.total for o in orders if o.status != "Cancelled" and "Return" not in o.status)
        total_orders = len(orders)
        
        sold_products = {}
        for o in orders:
            if o.status == "Cancelled" or "Return" in o.status: continue
            for item in o.items:
                sold_products[item.name] = sold_products.get(item.name, 0) + item.quantity
                
        most_sold = max(sold_products.items(), key=lambda x: x[1]) if sold_products else ("None", 0)
        
        return {
            "Total Revenue": f"₹{total_revenue:.2f}",
            "Total Orders": total_orders,
            "Most Sold Product": f"{most_sold[0]} ({most_sold[1]} units)"
        }

    def get_activity_logs(self, limit: int = 20) -> List[Dict[str, Any]]:
        logs = DataManager.load_data("activity_logs.json")
        return logs[-limit:] if logs else []

    def set_dynamic_pricing(self, category: str, percentage_change: float):
        """Simulates dynamic pricing by increasing/decreasing prices by a percentage for a category."""
        products = self.product_service.filter_products(category=category)
        for p in products:
            new_price = p.price * (1 + (percentage_change / 100))
            p.price = round(new_price, 2)
            self.product_service._save_products()
        return len(products)
