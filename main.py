import sys
from services.book_service import (
    show_books,
    create_book,
    create_author,
    search_book,
    show_authors,
    search_author,
)
from services.customer_service import (
    create_customer,
    show_customers,
    search_customer,
    delete_customer,
)
from services.order_service import (
    search_order,
    search_order_detail,
    show_all_orders,
    create_order,
    create_order_detail,
)


def show_menu():
    """Displays the main menu for user interaction."""
    print(
        """
        1. Add a new book
        2. Show all books
        3. Search for a book
        4. Add a new author
        5. Show all authors
        6. Search for an author
        7. Add a new customer
        8. Show all customers
        9. Search for a customer
        10. Delete a customer
        11. Create an order
        12. Create order details
        13. Show all orders
        14. Search for an order
        15. Search order details
        0. Exit
        """
    )


def main():
    """Main function to handle user input and call appropriate services."""
    while True:
        show_menu()
        choice = input("Choose an action (0-15): ").strip()

        if choice == "1":
            title = input("Enter book title: ").capitalize().strip()
            while True:
                try:
                    price = float(input("Enter book price: ").strip())
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid price.")
            while True:
                try:
                    quantity = int(input("Enter book quantity: ").strip())
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid quantity.")
            author_name = input("Enter author's first name: ").capitalize().strip()
            author_surname = input("Enter author's last name: ").capitalize().strip()
            while True:
                try:
                    year = int(input("Enter book publication year: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid year.")
            create_book(title, price, quantity, author_name, author_surname, year)

        elif choice == "2":
            show_books()

        elif choice == "3":
            title = input("Enter book title: ").capitalize().strip()
            search_book(title)

        elif choice == "4":
            first_name = input("Enter Author's first name: ").capitalize().strip()
            last_name = input("Enter Author's last name: ").capitalize().strip()
            create_author(first_name, last_name)

        elif choice == "5":
            show_authors()

        elif choice == "6":
            first_name = input("Enter Author's first name: ").capitalize().strip()
            last_name = input("Enter Author's last name: ").capitalize().strip()
            search_author(first_name, last_name)

        elif choice == "7":
            first_name = input("Enter Customer's first name: ").capitalize().strip()
            last_name = input("Enter Customer's last name: ").capitalize().strip()
            phone_number = input("Enter Customer's phone number: ").strip()
            email = input("Enter Customer's email: ").strip()
            address = input("Enter Customer's address: ").strip()
            create_customer(first_name, last_name, phone_number, email, address)

        elif choice == "8":
            show_customers()

        elif choice == "9":
            email = input("Enter Customer's Email: ")
            search_customer(email)

        elif choice == "10":
            email = input("Enter Customer's email: ")
            delete_customer(email)

        elif choice == "11":
            email = input("Enter Customer's Email: ")
            create_order(email)

        elif choice == "12":
            title = input("Enter book title: ")
            while True:
                try:
                    order_id = int(input("Enter Order Id: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid Order Id.")
            while True:
                try:
                    quantity = int(input("Enter quantity for order: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid quantity.")
            create_order_detail(title, order_id, quantity)

        elif choice == "13":
            show_all_orders()

        elif choice == "14":
            while True:
                try:
                    order_id = int(input("Enter Order Id: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid Order Id.")
            search_order(order_id)

        elif choice == "15":
            while True:
                try:
                    order_id = int(input("Enter Order Id: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid Order Id.")
            search_order_detail(order_id)

        elif choice == "0":
            print("Exiting the program...")
            sys.exit()

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
