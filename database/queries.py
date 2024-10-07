import psycopg2
from database.connection import connect_to_db, close_connection


def get_all_authors():
    connection, cursor = connect_to_db()

    try:
        cursor.execute("SELECT * FROM Authors")
        authors = cursor.fetchall()

        if not authors:
            print("No authors found in database.")
            return

        for author in authors:
            print(
                f"AuthorId: {author[0]}\n"
                f"Name: {author[1]}\n"
                f"Surname: {author[2]}."
            )
            print("-" * 30)
    except psycopg2.Error as e:
        print(f"Error while displaying an author: {e.pgerror}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    finally:
        if connection:
            close_connection(connection, cursor)


def find_author(firstname, lastname):
    connection, cursor = connect_to_db()

    try:
        cursor.execute(
            """SELECT * FROM Authors
         WHERE FirstName = %s AND LastName = %s
         """,
            (firstname, lastname),
        )
        author = cursor.fetchone()

        if not author:
            print(f"Author {firstname} {lastname} not found in the database.")
            return

        cursor.execute(
            """SELECT Title, Year, Price, Quantity
        FROM Books
        WHERE AuthorId = %s
        """,
            (author[0],),
        )
        books = cursor.fetchall()

        if not books:
            print(f"No books available by author {firstname} {lastname}")
        else:
            print(f"Books in stock from author {author[1]} {author[2]}:")
            for book in books:
                print(
                    f"""
                Title: {book[0]}\n
                Publication Year: {book[1]}\n
                Price: {book[2]}\n
                Quantity: {book[3]}."""
                )
                print("-" * 30)

    except psycopg2.Error as e:
        print(f"Error while displaying an author: {e.pgerror}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    finally:
        if connection:
            close_connection(connection, cursor)


def get_all_books():
    connection, cursor = connect_to_db()

    try:
        cursor.execute(
            """
        SELECT B.Title, B.Year, B.Price, B.Quantity, A.FirstName, A.LastName
        FROM Books B
        JOIN Authors A ON B.AuthorId = A.AuthorId"""
        )
        books = cursor.fetchall()

        if not books:
            print("No books found in database.")

        else:
            for book in books:
                print(
                    f"""
                Title: '{book[0]}'
                Publication Year: {book[1]}
                Price: {book[2]}
                Quantity: {book[3]}
                Author Name: {book[4]} {book[5]}"""
                )
                print("-" * 30)

    except psycopg2.Error as e:
        print(f"Error while retrieving books: {e.pgerror}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    finally:
        if connection:
            close_connection(connection, cursor)


def find_book(book_name):
    connection, cursor = connect_to_db()

    try:
        cursor.execute(
            """
        SELECT B.Title, B.Year, B.Price, B.Quantity, A.FirstName, A.LastName
        FROM Books B
        JOIN Authors A ON B.AuthorId = A.AuthorId
        WHERE B.Title ILIKE %s""",
            (f"%{book_name}%",),
        )

        books = cursor.fetchall()

        if not books:
            print("No books found in database.")
            return

        for book in books:
            print(
                f"""
            Title: '{book[0]}'\n
            Publication Year: {book[1]}\n
            Price: {book[2]}\n
            Quantity: {book[3]}\n
            Author Name: {book[4]} {book[5]}"""
            )
            print("-" * 30)

    except psycopg2.Error as e:
        print(f"Error while retrieving books: {e.pgerror}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    finally:
        if connection:
            close_connection(connection, cursor)


def get_all_customers():
    connection, cursor = connect_to_db()

    try:
        cursor.execute(
            """
        SELECT FirstName, LastName, PhoneNumber, Email, Address
        FROM Customers"""
        )

        customers = cursor.fetchall()

        if not customers:
            print("No created customers in database.")

        else:
            for customer in customers:
                print(
                    f"""
                Customer: {customer[0]} {customer[1]}\n
                PhoneNumber: {customer[2]}\n
                Email: {customer[3]}\n
                Address: {customer[4]}\n"""
                )
                print("-" * 30)

    except psycopg2.Error as e:
        print(f"Error while getting customers: {e.pgerror}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    finally:
        if connection:
            close_connection(connection, cursor)


def find_customer(email):
    connection, cursor = connect_to_db()

    try:
        cursor.execute(
            """
            SELECT FirstName, LastName, PhoneNumber, Email, Address
            FROM Customers
            Where Email = %s
            """,
            (email,),
        )
        customer = cursor.fetchone()

        if not customer:
            print(f"No customer found with email: {email}")
        else:
            print(
                f"""\tCustomer Information:\n
Name: {customer[0]} {customer[1]}\n
PhoneNumber: {customer[2]}\n
Email: {customer[3]}\n
Address: {customer[4]}
"""
            )
            print("-" * 30)
    except psycopg2.Error as e:
        print(f"Error while getting customer: {e.pgerror}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    finally:
        if connection:
            close_connection(connection, cursor)


def get_all_orders():
    connection, cursor = connect_to_db()

    try:
        cursor.execute(
            """
        SELECT
        O.OrderDate,
        C.FirstName,
        C.LastName,
        C.PhoneNumber,
        C.Email,
        C.Address,
        O.OrderId
        FROM
            Orders O
        JOIN
            Customers C ON C.CustomerId = O.CustomerId
            """
        )

        orders = cursor.fetchall()

        if not orders:
            print("There are no orders yet.")
            return

        for order in orders:
            print(
                f"""
Order Date: {order[0]}
Customer Name: {order[1]} {order[2]}
Phone Number: {order[3]}
Email: {order[4]}
Address: {order[5]}
Order ID: {order[6]}"""
            )
            print("-" * 30)

    except psycopg2.Error as e:
        print(f"Error while retrieving orders: {e.pgerror}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    finally:
        if connection:
            close_connection(connection, cursor)


def get_order(order_id):
    connection, cursor = connect_to_db()

    try:
        cursor.execute(
            """SELECT
            O.OrderDate,
            C.FirstName,
            C.LastName,
            C.PhoneNumber,
            C.Email,
            C.Address,
            O.OrderId
            FROM
                Orders O
            JOIN
                Customers C ON C.CustomerId = O.CustomerId
            WHERE O.OrderId = %s
            """,
            (order_id,),
        )

        order = cursor.fetchone()

        if not order:
            print(f"No order found with id: {order_id}.")
            return

        print(
            f"""
        OrderDate: {order[0]}
        Customer Name: {order[1]} {order[2]}
        PhoneNumber: {order[3]}
        Email: {order[4]}
        Address: {order[5]}
        OrderId: {order[6]}"""
        )
        print("-" * 30)

    except psycopg2.Error as e:
        print(f"Error while retrieving the order: {e.pgerror}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    finally:
        if connection:
            close_connection(connection, cursor)


def get_order_detail(order_id):
    connection, cursor = connect_to_db()

    try:
        cursor.execute(
            """SELECT
            OD.Quantity,
            OD.UnitPrice,
            OD.TotalPrice,
            B.Title,
            A.FirstName AS AuthorFirstName,
            A.LastName AS AuthorLastName,
            C.FirstName AS CustomerFirstName,
            C.LastName AS CustomerLastName,
            C.Email,
            O.OrderDate
         FROM
            OrderDetails OD
         JOIN
            Books B ON B.BookId = OD.BookId
         JOIN
            Authors A ON B.AuthorId = A.AuthorId
         JOIN
            Orders O ON OD.OrderId = O.OrderId
         JOIN
            Customers C ON C.CustomerId = O.CustomerId
         WHERE
            OD.OrderId = %s
         """,
            (order_id,),
        )

        order_detail = cursor.fetchone()

        if order_detail:
            print(
                f"""
        Quantity: {order_detail[0]}
        Unit Price: {order_detail[1]}
        Total Price: {order_detail[2]}
        Book Title: {order_detail[3]}
        Author: {order_detail[4]} {order_detail[5]}
        Customer: {order_detail[6]} {order_detail[7]}
        Email: {order_detail[8]}
        Date: {order_detail[9]}"""
            )
        else:
            print(f"No order detail found with OrderId: {order_id}")

    except psycopg2.Error as e:
        print(f"Error while retrieving order detail: {e.pgerror}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    finally:
        if connection:
            close_connection(connection, cursor)
