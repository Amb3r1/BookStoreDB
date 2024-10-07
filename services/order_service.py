from database.insert_data import add_order, add_order_detail
from database.queries import get_order_detail, get_order, get_all_orders


def create_order(customer_email: str):
    """Creates an order for the given customer."""
    try:
        add_order(customer_email)
    except Exception as e:
        print(f"Error creating order for customer: {e}")


def create_order_detail(book_title: str, order_id: int, quantity: int):
    """Creates an order detail for the given book and order."""
    try:
        add_order_detail(book_title, order_id, quantity)
    except Exception as e:
        print(
            f"Error creating order detail for book {book_title}, order ID {order_id}: {e}"
        )


def search_order(order_id: int):
    """Searches and retrieves order details by order ID."""
    get_order(order_id)


def show_all_orders():
    """Displays all orders in the database."""
    get_all_orders()


def search_order_detail(order_id: int):
    """Retrieves details for a specific order by order ID."""
    get_order_detail(order_id)
