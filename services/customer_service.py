import psycopg2
from database.connection import connect_to_db, close_connection
from database.queries import find_customer, get_all_customers
from database.insert_data import add_customer


def create_customer(
    first_name: str, last_name: str, phone_number: str, email: str, address: str
):
    """Creates a new customer in the database."""
    try:
        add_customer(first_name, last_name, phone_number, email, address)
    except Exception as e:
        print(f"Error creating customer: {e}")


def delete_customer(email: str):
    """Deletes a customer from the database using their email."""
    connection, cursor = connect_to_db()

    try:
        cursor.execute(
            """
        DELETE FROM Customers
        WHERE Email = %s
        """,
            (email,),
        )
        connection.commit()

        if cursor.rowcount > 0:
            print(f"Customer with email {email} has been deleted successfully.")
        else:
            print(f"No customer found with email: {email}.")
    except psycopg2.Error as e:
        print(f"Error while deleting customer: {e.pgerror}")
    except Exception as e:
        print(f"Error while deleting customer: {e}")
    finally:
        if connection:
            close_connection(connection, cursor)


def search_customer(email: str):
    """Searches for a customer by their email."""
    find_customer(email)


def show_customers():
    """Displays all customers in the database."""
    get_all_customers()
