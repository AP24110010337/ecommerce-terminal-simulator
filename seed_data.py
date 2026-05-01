import random
from utils.data_manager import DataManager
from models.product import Product

categories = {
    "Electronics": ["Smartphone", "Laptop", "Wireless Earbuds", "Smartwatch", "Tablet", "Monitor", "Keyboard", "Mouse"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Hoodie", "Shorts", "Sweater"],
    "Books": ["Python Crash Course", "Clean Code", "The Pragmatic Programmer", "Design Patterns", "Atomic Habits", "Dune"]
}

adjectives = ["Pro", "Max", "Ultra", "Lite", "Plus", "Premium", "Essential", "Elite"]
brands = ["TechCorp", "GigaByte", "StyleSync", "ReadRight", "Alpha", "Omega"]

def generate_products(count=50):
    products = []
    for i in range(1, count + 1):
        cat = random.choice(list(categories.keys()))
        base_name = random.choice(categories[cat])
        brand = random.choice(brands)
        adj = random.choice(adjectives)
        
        name = f"{brand} {base_name} {adj}"
        prod_id = f"PRD{i:04d}"
        
        if cat == "Electronics":
            price = round(random.uniform(99.0, 1999.0), 2)
        elif cat == "Clothing":
            price = round(random.uniform(15.0, 150.0), 2)
        else:
            price = round(random.uniform(9.99, 59.99), 2)
            
        stock = random.randint(0, 150)
        rating = round(random.uniform(2.5, 5.0), 1)
        reviews_count = random.randint(0, 500)
        
        desc = f"High quality {name} from {brand}. Perfect for your daily needs."
        
        p = Product(prod_id, name, cat, price, stock, rating, reviews_count, desc)
        products.append(p.to_dict())
    return products

if __name__ == "__main__":
    print("Seeding initial data...")
    # Seed Products
    prods = generate_products(50)
    DataManager.save_data("products.json", prods)
    
    # Seed Coupons
    coupons = {
        "WELCOME10": {"type": "percent", "value": 10, "min_order": 0, "limit": 100},
        "FLAT50": {"type": "flat", "value": 50, "min_order": 100, "limit": 50},
        "SAVE20": {"type": "percent", "value": 20, "min_order": 500, "limit": 20}
    }
    DataManager.save_data("coupons.json", coupons)
    
    # Ensure other files exist
    DataManager.ensure_file_exists("users.json", [])
    DataManager.ensure_file_exists("orders.json", [])
    DataManager.ensure_file_exists("activity_logs.json", [])
    
    print("Data seeding complete.")
