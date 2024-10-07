import psycopg2
from database.connection import connect_to_db, close_connection
from database.insert_data import add_book, add_author
from database.queries import find_book, get_all_books, find_author, get_all_authors


def create_book(
    title: str,
    price: float,
    quantity: int,
    author_name: str,
    author_surname: str,
    year: int,
):
    """Create a new book and add it to the database."""
    try:
        add_book(title, price, quantity, author_name, author_surname, year)
    except Exception as e:
        print(f"Error creating book: {e}")


def add_book_quantity(quantity: int, book_id: int):
    """Add quantity to an existing book."""
    connection, cursor = connect_to_db()
    try:
        cursor.execute(
            """
        UPDATE Books
        SET Quantity = Quantity + %s
        WHERE BookId = %s
        """,
            (quantity, book_id),
        )
        connection.commit()
    except psycopg2.Error as e:
        print(f"Error while adding book quantity: {e}")
    finally:
        if connection:
            close_connection(connection, cursor)


def create_author(firstname: str, lastname: str):
    """Create a new author and add them to the database."""
    try:
        add_author(firstname, lastname)
    except Exception as e:
        print(f"Error creating author: {e}")


def show_books():
    """Display all books from the database."""
    get_all_books()


def show_authors():
    """Display all authors from the database."""
    get_all_authors()


def search_book(book_name: str):
    """Search for a book by its title."""
    find_book(book_name)


def search_author(firstname: str, lastname: str):
    """Search for an author by their first and last name."""
    find_author(firstname, lastname)
