import psycopg2
from database.connection import connect_to_db, close_connection


def add_author(firstname: str, lastname: str) -> None:
    """Add a new author to the Authors table."""
    connection = None
    cursor = None
    try:
        connection, cursor = connect_to_db()

        cursor.execute(
            """
            SELECT AuthorId
            FROM Authors
            WHERE FirstName = %s AND LastName = %s""",
            (firstname, lastname),
        )
        author_existing = cursor.fetchone()
        if author_existing:
            print(f"Author {firstname} {lastname} is already existing in the database.")
        else:
            cursor.execute(
                "INSERT INTO Authors(FirstName, LastName) VALUES (%s, %s)",
                (firstname, lastname),
            )
            connection.commit()
            print(f"Author {firstname} {lastname} added successfully.")

    except psycopg2.Error as e:
        print(f"Error while adding author: {e}")
    finally:
        if connection:
            close_connection(connection, cursor)


def add_book(
    title: str,
    price: float,
    quantity: int,
    author_name: str,
    author_surname: str,
    year: int,
) -> None:
    """Add a new book to the Books table."""
    connection = None
    cursor = None
    try:
        connection, cursor = connect_to_db()
        cursor.execute(
            """
            SELECT AuthorId
            FROM Authors
            WHERE FirstName = %s AND LastName = %s""",
            (author_name, author_surname),
        )
        author_existing = cursor.fetchone()

        if not author_existing:
            cursor.execute(
                "INSERT INTO Authors(FirstName, LastName) VALUES (%s, %s)",
                (author_name, author_surname),
            )
            connection.commit()

            cursor.execute(
                """
                SELECT AuthorId
                FROM Authors
                WHERE FirstName = %s AND LastName = %s""",
                (author_name, author_surname),
            )
            author_existing = cursor.fetchone()

        cursor.execute("SELECT BookId FROM Books WHERE Title = %s", (title,))
        book_existing = cursor.fetchone()

        if book_existing:
            print(f"Book {title} is already existing in the database.")
            cursor.execute(
                """
            UPDATE Books
            SET Quantity = Quantity + %s
            WHERE BookId = %s
            RETURNING BookId""",
                (quantity, book_existing[0]),
            )
            connection.commit()
        else:
            cursor.execute(
                """
                INSERT INTO Books(Title, AuthorId, Year, Price, Quantity)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (title, author_existing, year, price, quantity),
            )
            connection.commit()
            print(f"Book {title} added successfully.")

    except psycopg2.Error as e:
        print(f"Error while adding book: {e}")
    finally:
        if connection:
            close_connection(connection, cursor)


def add_customer(
    first_name: str, last_name: str, phone_number: str, email: str, address: str
) -> None:
    """Add a new customer to the Customers table."""
    connection = None
    cursor = None
    try:
        connection, cursor = connect_to_db()

        cursor.execute(
            "SELECT CustomerId FROM Customers WHERE LastName = %s AND Email = %s",
            (last_name, email),
        )
        customer_existing = cursor.fetchone()

        if customer_existing:
            print(f"Customer {first_name} {last_name} is already existing.")
        else:
            cursor.execute(
                """
                INSERT INTO Customers(
                FirstName,
                LastName,
                PhoneNumber,
                Email,
                Address)
                VALUES (%s, %s, %s, %s, %s)""",
                (first_name, last_name, phone_number, email, address),
            )
            connection.commit()
            print(f"Customer {first_name} {last_name} added to database.")

    except psycopg2.Error as e:
        print(f"Error while adding customer: {e}")
    finally:
        if connection:
            close_connection(connection, cursor)


def add_order(customer_email: str) -> None:
    connection = None
    cursor = None

    try:
        connection, cursor = connect_to_db()

        cursor.execute(
            """
            SELECT CustomerId
            FROM Customers
            WHERE Email = %s
            """,
            (customer_email,),
        )
        customer = cursor.fetchone()

        if not customer:
            print(f"Customer with email {customer_email} not found")
            return

        customer_id = customer[0]

        cursor.execute(
            """INSERT INTO Orders (
            CustomerId,
            OrderDate)
            VALUES (%s, NOW())
            RETURNING OrderId""",
            (customer_id,),
        )
        order_id = cursor.fetchone()[0]
        connection.commit()
        print(f"Order {order_id} added successfully for customer {customer_email}")

    except psycopg2.Error as e:
        print(f"Error while adding order: {e}")
    finally:
        if connection:
            close_connection(connection, cursor)


def add_order_detail(book_title: str, order_id: int, quantity: int) -> None:
    connection = None
    cursor = None

    try:
        connection, cursor = connect_to_db()

        cursor.execute(
            "SELECT BookId, Price, Quantity FROM Books WHERE Title = %s", (book_title,)
        )

        book = cursor.fetchone()

        if book is None:
            print(f"Book {book_title} is not existing in database.")
            return

        book_id = book[0]
        book_price = book[1]
        available_quantity = book[2]

        if available_quantity < quantity:
            print(f"Not enough in stock, books left in stock : {available_quantity}")
            return

        total_price = book_price * quantity

        cursor.execute(
            "INSERT INTO OrderDetails(OrderId, BookId, Quantity, UnitPrice, TotalPrice) VALUES (%s, %s, %s, %s, %s)",
            (order_id, book_id, quantity, book_price, total_price),
        )

        cursor.execute(
            "UPDATE Books SET Quantity = Quantity - %s WHERE BookId = %s RETURNING Quantity",
            (quantity, book_id),
        )

        updated_quantity = cursor.fetchone()[0]

        connection.commit()

        print(
            f"""Details for order {order_id} added successfully for book "{book_title}" with quantity {quantity}.
         Remaining books in stock: {updated_quantity}."""
        )

    except psycopg2.Error as e:
        print(f"Error while adding order detail: {e}")
    finally:
        if connection:
            close_connection(connection, cursor)
