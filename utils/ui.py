import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str = "PYSHOP TERMINAL STORE"):
    clear_screen()
    header_text = Text(title, style="bold bright_cyan", justify="center")
    console.print(Panel(header_text, style="cyan", expand=False))
    console.print()

def simulate_loading(message: str, seconds: float = 1.0):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=f"[cyan]{message}", total=None)
        time.sleep(seconds)

def display_menu(options: dict, title: str = "Menu"):
    table = Table(title=title, show_header=False, box=None)
    table.add_column("Key", style="bold green")
    table.add_column("Action", style="cyan")
    
    for key, action in options.items():
        table.add_row(f"[{key}]", action)
        
    console.print(Align.center(table))
    console.print()

def display_products(products: list, title: str = "Products List"):
    if not products:
        console.print("[yellow]No products found![/yellow]")
        return
        
    table = Table(title=title, style="blue")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Name", style="bright_white")
    table.add_column("Category", style="magenta")
    table.add_column("Price", style="green", justify="right")
    table.add_column("Rating", justify="right")
    table.add_column("Stock", justify="right")
    
    for p in products:
        stock_style = "red" if p.stock < 10 else "green"
        table.add_row(
            p.product_id,
            p.name,
            p.category,
            f"₹{p.price:.2f}",
            f"{'★' * int(p.rating)} {p.rating}",
            f"[{stock_style}]{p.stock}[/{stock_style}]"
        )
        
    console.print(table)
    console.print()

def display_cart(cart_details: list, subtotal: float):
    if not cart_details:
        console.print(Panel("[yellow]Your cart is empty.[/yellow]", title="🛒 Shopping Cart"))
        return
        
    table = Table(title="🛒 Shopping Cart", style="blue")
    table.add_column("Product ID", style="cyan")
    table.add_column("Name", style="bright_white")
    table.add_column("Price", style="green", justify="right")
    table.add_column("Qty", style="yellow", justify="center")
    table.add_column("Total", style="green", justify="right")
    
    for item in cart_details:
        table.add_row(
            item["product_id"],
            item["name"],
            f"₹{item['price']:.2f}",
            str(item["quantity"]),
            f"₹{item['total']:.2f}"
        )
        
    console.print(table)
    console.print(Align.right(f"[bold green]Subtotal: ₹{subtotal:.2f}[/bold green]"))
    console.print()

def get_input(prompt: str, password: bool = False) -> str:
    return console.input(f"[bold yellow]{prompt}[/bold yellow] ", password=password)

def print_success(msg: str):
    console.print(f"[bold green]✔ {msg}[/bold green]")
    
def print_error(msg: str):
    console.print(f"[bold red]✖ {msg}[/bold red]")
