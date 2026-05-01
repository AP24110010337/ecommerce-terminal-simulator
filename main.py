import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from services.auth_service import AuthService
from services.product_service import ProductService
from services.cart_service import CartService
from services.discount_service import DiscountService
from services.order_service import OrderService
from services.recommendation_service import RecommendationService
from services.admin_service import AdminService

from utils import ui
from models.user import User

console = Console()

class PyShop:
    def __init__(self):
        self.auth = AuthService()
        self.products = ProductService()
        self.cart = CartService(self.auth, self.products)
        self.discount = DiscountService()
        self.orders = OrderService(self.auth, self.products, self.cart)
        self.recommendations = RecommendationService(self.products)
        self.admin = AdminService(self.orders, self.products)
        self.current_user: User = None

    def run(self):
        while True:
            ui.clear_screen()
            ui.print_header()
            if not self.current_user:
                self.guest_menu()
            elif self.current_user.role == "admin":
                self.admin_menu()
            else:
                self.customer_menu()

    def wait_key(self):
        ui.console.input("\n[dim]Press Enter to continue...[/dim]")

    # ================= GUEST MENU =================
    def guest_menu(self):
        ui.console.print(Panel("[bright_magenta]Welcome to PyShop! The premium terminal electronics and lifestyle store.[/bright_magenta]"))
        options = {"1": "Login", "2": "Register", "3": "Exit"}
        ui.display_menu(options)
        choice = ui.get_input("Choose an option:")
        
        if choice == "1":
            self.handle_login()
        elif choice == "2":
            self.handle_register()
        elif choice == "3":
            ui.print_success("Thank you for visiting PyShop!")
            sys.exit(0)

    def handle_login(self):
        ui.print_header("Login")
        u = ui.get_input("Username:")
        p = ui.get_input("Password:", password=True)
        ui.simulate_loading("Authenticating...", 0.5)
        user = self.auth.login(u, p)
        if user:
            self.current_user = user
            ui.print_success(f"Welcome back, {u}!")
        else:
            ui.print_error("Invalid credentials.")
        self.wait_key()

    def handle_register(self):
        ui.print_header("Register")
        u = ui.get_input("Choose Username:")
        p = ui.get_input("Choose Password:", password=True)
        if u and p:
            # Let's keep it simple: no strict validation
            ui.simulate_loading("Creating account...", 0.6)
            if self.auth.register(u, p):
                ui.print_success("Registration successful! You can now log in.")
            else:
                ui.print_error("Username already exists.")
        self.wait_key()

    # ================= CUSTOMER MENU =================
    def customer_menu(self):
        ui.console.print(Panel(f"[cyan]Hello, {self.current_user.username}[/cyan]", border_style="cyan"))
        options = {
            "1": "Browse Catalog",
            "2": "For You (Recommendations)",
            "3": "Cart & Checkout",
            "4": "My Orders & Returns",
            "5": "Wishlist",
            "6": "Logout"
        }
        ui.display_menu(options, title="Main Menu")
        choice = ui.get_input("Select:")

        if choice == "1":
            self.browse_menu()
        elif choice == "2":
            self.recommendation_menu()
        elif choice == "3":
            self.cart_menu()
        elif choice == "4":
            self.orders_menu()
        elif choice == "5":
            self.wishlist_menu()
        elif choice == "6":
            ui.simulate_loading("Logging out...", 0.4)
            self.current_user = None

    def browse_menu(self):
        ui.print_header("Catalog")
        options = {"1": "View All", "2": "Search", "3": "Filter"}
        ui.display_menu(options)
        c = ui.get_input("Select:")
        
        prods = []
        if c == "1":
            prods = self.products.get_all_products()
        elif c == "2":
            q = ui.get_input("Enter search query:")
            prods = self.products.search_products(q)
        elif c == "3":
            cat = ui.get_input("Enter category (leave blank for all):")
            try:
                min_p = float(ui.get_input("Min Price (default 0):") or 0)
                max_p = float(ui.get_input("Max Price (default inf):") or float('inf'))
                min_r = float(ui.get_input("Min Rating (default 0):") or 0)
                prods = self.products.filter_products(cat if cat else None, min_p, max_p, min_r)
            except ValueError:
                ui.print_error("Invalid numbers.")
                self.wait_key()
                return

        if prods:
            ui.display_products(prods)
            action = ui.get_input("Enter Product ID to View Details (or 'b' to go back):")
            if action.upper().startswith("PRD"):
                self.product_detail(action.upper())
        else:
            ui.print_error("No products matched criteria.")
            self.wait_key()

    def product_detail(self, pid: str):
        p = self.products.get_product(pid)
        if not p:
            ui.print_error("Product not found.")
            self.wait_key()
            return
            
        ui.print_header(f"{p.name}")
        info = f"[cyan]Category:[/cyan] {p.category}\n[green]Price:[/green] ₹{p.price:.2f}\n[yellow]Rating:[/yellow] {'★'*int(p.rating)} {p.rating} ({p.reviews_count} reviews)\n[white]Stock:[/white] {p.stock}\n[magenta]Description:[/magenta] {p.description}"
        ui.console.print(Panel(info, title="Product View", border_style="cyan"))
        
        c = ui.get_input("[1] Add to Cart | [2] Add to Wishlist | [b] Back:")
        if c == "1":
            try:
                qty = int(ui.get_input("Quantity:") or 1)
                res = self.cart.add_item(self.current_user, p.product_id, qty)
                if "Added" in res: ui.print_success(res)
                else: ui.print_error(res)
            except ValueError:
                ui.print_error("Invalid quantity.")
            self.wait_key()
        elif c == "2":
            if p.product_id not in self.current_user.wishlist:
                self.current_user.wishlist.append(p.product_id)
                self.auth.update_user_data(self.current_user)
                ui.print_success("Added to wishlist.")
            else:
                ui.print_error("Already in wishlist.")
            self.wait_key()

    def recommendation_menu(self):
        ui.print_header("Recommended For You")
        recs = self.recommendations.get_for_user(self.current_user)
        ui.display_products(recs)
        self.wait_key()

    def cart_menu(self):
        ui.print_header("Your Cart")
        details = self.cart.get_cart_details(self.current_user)
        subtotal = self.cart.calculate_subtotal(self.current_user)
        ui.display_cart(details, subtotal)
        
        if not details:
            self.wait_key()
            return
            
        opts = {"1": "Update Quantity", "2": "Remove Item", "3": "Proceed to Checkout", "4": "Back"}
        ui.display_menu(opts)
        c = ui.get_input("Action:")
        
        if c == "1":
            pid = ui.get_input("Product ID:").upper()
            try:
                q = int(ui.get_input("New Quantity:"))
                ui.print_success(self.cart.update_quantity(self.current_user, pid, q))
            except Exception: ui.print_error("Invalid input.")
            self.wait_key()
        elif c == "2":
            pid = ui.get_input("Product ID:").upper()
            ui.print_success(self.cart.remove_item(self.current_user, pid))
            self.wait_key()
        elif c == "3":
            self.checkout_flow(subtotal)

    def checkout_flow(self, subtotal: float):
        ui.print_header("Checkout")
        code = ui.get_input("Enter Coupon Code (or leave blank):")
        discount = 0.0
        if code:
            valid, msg, discount = self.discount.validate_coupon(code, subtotal)
            if valid: ui.print_success(f"{msg} (-₹{discount:.2f})")
            else: ui.print_error(msg)
            
        tax = (subtotal - discount) * 0.05
        total = subtotal - discount + tax
        
        summary = f"Subtotal: ₹{subtotal:.2f}\nDiscount: -₹{discount:.2f}\nTax (5%): ₹{tax:.2f}\n[bold green]Final Total: ₹{total:.2f}[/bold green]"
        ui.console.print(Panel(summary, title="Bill Summary"))
        
        ui.display_menu({"1": "UPI", "2": "Card", "3": "Cash on Delivery"}, "Payment Method")
        p_c = ui.get_input("Select Payment Method:")
        method_map = {"1": "UPI", "2": "Card", "3": "COD"}
        method = method_map.get(p_c, "COD")
        
        if ui.get_input("\nConfirm Order? (y/n):").lower() == 'y':
            ui.simulate_loading("Processing Payment & Securing Order...", 1.5)
            if code and discount > 0: self.discount.apply_coupon(code)
            order = self.orders.create_order(self.current_user, method, discount)
            ui.print_success(f"Order {order.order_id} placed successfully!")
            ui.console.print(Panel("[bright_cyan]Thank you for shopping at PyShop![/bright_cyan]"))
        else:
            ui.print_error("Checkout cancelled.")
        self.wait_key()

    def orders_menu(self):
        ui.print_header("My Orders")
        orders = self.orders.get_user_orders(self.current_user.user_id)
        if not orders:
            ui.print_error("No orders found.")
            self.wait_key()
            return
            
        table = Table(style="blue")
        table.add_column("Order ID", style="cyan")
        table.add_column("Date", style="white")
        table.add_column("Total", style="green")
        table.add_column("Status", style="yellow")
        
        for o in reversed(orders):
            status = self.orders.simulate_order_status(o)
            s_style = "green" if status == "Delivered" else ("red" if "Cancel" in status else "yellow")
            table.add_row(o.order_id, o.timestamp[:10], f"₹{o.total:.2f}", f"[{s_style}]{status}[/{s_style}]")
            
        ui.console.print(table)
        oid = ui.get_input("Enter Order ID to Cancel/Return (or blank):").upper()
        if oid:
            action = ui.get_input("Type 'cancel' to cancel or 'return' to return:")
            if action.lower() == 'cancel':
                if self.orders.cancel_order(oid, self.current_user.user_id): ui.print_success("Order Cancelled.")
                else: ui.print_error("Cannot cancel this order.")
            elif action.lower() == 'return':
                res = self.orders.process_return(oid, self.current_user.user_id)
                ui.print_success(res) if "accepted" in res else ui.print_error(res)
        self.wait_key()

    def wishlist_menu(self):
        ui.print_header("Wishlist")
        if not self.current_user.wishlist:
            ui.print_error("Wishlist is empty.")
            self.wait_key()
            return
            
        prods = [self.products.get_product(pid) for pid in self.current_user.wishlist if self.products.get_product(pid)]
        ui.display_products(prods)
        pid = ui.get_input("Enter Product ID to move to Cart (or 'del' to remove, blank to exit):").upper()
        if pid in self.current_user.wishlist:
            action = ui.get_input("Type 'cart' or 'del':")
            self.current_user.wishlist.remove(pid)
            if action == 'cart':
                self.cart.add_item(self.current_user, pid, 1)
                ui.print_success("Moved to cart.")
            else:
                ui.print_success("Removed from wishlist.")
            self.auth.update_user_data(self.current_user)
        self.wait_key()

    # ================= ADMIN MENU =================
    def admin_menu(self):
        ui.console.print(Panel(f"[magenta]ADMIN DASHBOARD - {self.current_user.username}[/magenta]"))
        options = {
            "1": "Sales Analytics",
            "2": "Activity Logs",
            "3": "Product Management",
            "4": "Logout"
        }
        ui.display_menu(options)
        c = ui.get_input("Admin Action:")
        
        if c == "1":
            ui.print_header("Sales Analytics")
            rep = self.admin.get_sales_report()
            for k, v in rep.items():
                ui.console.print(f"[cyan]{k}:[/cyan] {v}")
            self.wait_key()
        elif c == "2":
            ui.print_header("Recent Activity (Last 20)")
            logs = self.admin.get_activity_logs()
            for log in logs:
                ui.console.print(f"[dim]{log['timestamp'][:16]}[/dim] [magenta]{log['user_id']}[/magenta] {log['action']}")
            self.wait_key()
        elif c == "3":
            ui.print_header("Products")
            ui.display_products(self.products.get_all_products()[:15], "First 15 Products")
            self.wait_key()
        elif c == "4":
            self.current_user = None

if __name__ == "__main__":
    app = PyShop()
    try:
        app.run()
    except KeyboardInterrupt:
        ui.print_success("\nExiting PyShop.")
        sys.exit(0)
