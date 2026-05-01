<div align="center">

# 🛒 PyShop 

**A Premium Terminal E-Commerce Simulation**

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Terminal](https://img.shields.io/badge/Terminal-4D4D4D?style=for-the-badge&logo=windows-terminal&logoColor=white)
![Rich](https://img.shields.io/badge/Rich-Text_Formatting-blueviolet?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

</div>

Welcome to **PyShop**, a feature-rich, terminal-based premium electronics and lifestyle store simulation written in Python! Experience a complete e-commerce lifecycle right from your command line, complete with a beautiful and dynamic text-based user interface powered by the `rich` library.

---

## ✨ Key Features

### 👤 Customer Experience
*   **Authentication System**: Secure user registration and login.
*   **Dynamic Product Catalog**: Browse, search, and precisely filter products by category, price range, and minimum rating.
*   **Smart Recommendations**: "For You" personalized product suggestions.
*   **Robust Shopping Cart**: Add items, adjust quantities, remove items, and view dynamic subtotals.
*   **Checkout & Billing**: Apply discount coupons, auto-calculate taxes, and simulate seamless payments (UPI, Card, Cash on Delivery).
*   **Order Management**: Track order history, simulate delivery statuses, and handle cancellations or returns easily.
*   **Wishlist**: Save favorite items to purchase later and seamlessly move them to the cart.

### 🛡️ Admin Dashboard
*   **Sales Analytics**: View comprehensive sales reports and revenue metrics.
*   **Activity Logs**: Monitor recent system and user activities in real-time.
*   **Product Management**: Oversee the entire product catalog directly from the terminal.

---

## 🏗️ Project Architecture

PyShop follows a clean, modular architecture, separating data, business logic, and UI:

```text
pyshop/
├── main.py                # Main application entry point & orchestration
├── add_admin.py           # Script to create an admin user
├── seed_data.py           # Script to populate initial products/data
├── models/                # Data structures
│   ├── user.py            # User object definition
│   ├── product.py         # Product object definition
│   └── order.py           # Order object definition
├── services/              # Core business logic modules
│   ├── auth_service.py    # Login/Register handling
│   ├── cart_service.py    # Cart operations
│   ├── product_service.py # Catalog and searching
│   ├── order_service.py   # Checkout and returns
│   ├── discount_service.py# Coupon validation
│   ├── recommendation...  # Smart suggestions
│   └── admin_service.py   # Admin analytics
├── utils/                 # Helpers and utilities
│   ├── ui.py              # Terminal rendering with Rich
│   └── data_manager.py    # File I/O and JSON storage
└── data/                  # Persistent data storage (auto-generated)
```

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

*   **Python 3.7** or higher
*   **pip** (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AP24110010337/ecommerce-terminal-simulator.git
    cd ecommerce-terminal-simulator
    ```

2.  **Install dependencies:**
    The only external requirement is the `rich` library for the gorgeous UI.
    ```bash
    pip install rich
    ```

3.  **Initialize Database (Recommended):**
    Populate the store with some initial electronic and lifestyle products.
    ```bash
    python seed_data.py
    ```

4.  **Create an Admin Account (Optional):**
    If you want to explore the admin dashboard, create an admin user.
    ```bash
    python add_admin.py
    ```

5.  **Run the Application:**
    Start your PyShop experience!
    ```bash
    python main.py
    ```

---

## 🛠️ Usage Guide

1.  **Launch the App**: Run `python main.py` to see the welcome screen.
2.  **Login/Register**: Choose option `1` to login or `2` to create a new account.
3.  **Explore Options**: Once logged in, use the numbered menus to navigate through the catalog, view your cart, or check your orders.
4.  **Admin Access**: Log in with an admin account (created via `add_admin.py`) to automatically be routed to the Admin Dashboard.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/AP24110010337/ecommerce-terminal-simulator/issues) if you want to contribute.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open-source and available under the [MIT License](https://choosealicense.com/licenses/mit/).

---
<div align="center">
Made with ❤️ using Python
</div>
