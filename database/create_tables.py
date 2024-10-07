# import psycopg2
#
# from database.connection import connect_to_db, close_connection
#
#
# def create_tables():
#     """Creating tables for the book store database."""
#     connection = None
#     cursor = None
#
#     try:
#         connection, cursor = connect_to_db()
#
#         cursor.execute("""CREATE TABLE IF NOT EXISTS Authors(
#             AuthorId SERIAL PRIMARY KEY,
#             FirstName VARCHAR(50),
#             LastName VARCHAR(50)
#             )""")
#
#         cursor.execute("""CREATE TABLE IF NOT EXISTS Books(
#         BookId SERIAL PRIMARY KEY,
#         Title VARCHAR(100),
#         AuthorId INTEGER REFERENCES Authors(AuthorId),
#         Year INTEGER,
#         Price DECIMAL(10, 2),
#         Quantity INTEGER
#         )""")
#
#         cursor.execute("""CREATE TABLE IF NOT EXISTS Customers(
#             CustomerId SERIAL PRIMARY KEY,
#             FirstName VARCHAR(50),
#             LastName VARCHAR(50),
#             PhoneNumber VARCHAR(14),
#             Email VARCHAR(100),
#             Address VARCHAR(255)
#             )""")
#
#         cursor.execute("""CREATE TABLE IF NOT EXISTS Orders(
#                 OrderId SERIAL PRIMARY KEY,
#                 CustomerId INTEGER REFERENCES Customers(CustomerId),
#                 OrderDate DATE
#                 )""")
#
#         cursor.execute("""CREATE TABLE IF NOT EXISTS OrderDetails(
#                 OrderDetailId SERIAL PRIMARY KEY,
#                 OrderId INTEGER REFERENCES Orders(OrderId),
#                 BookId INTEGER REFERENCES Books(BookId),
#                 Quantity INTEGER,
#                 UnitPrice DECIMAL(10, 2),
#                 TotalPrice DECIMAL(10, 2)
#                 )""")
#
#         connection.commit()
#
#     except psycopg2.Error as e:
#         print(f'Error: {e}')
#     finally:
#         if connection:
#             close_connection(connection, cursor)
#
# create_tables()
