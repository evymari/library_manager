from config.DBConnection import DBConnection
from src.controllers.BooksController import BooksController

book = BooksController()
book_data = {
    "isbn13":"9780141365467",
    "author":"Roald Dahl",
    "title":"Danny the Champion of the World"
    }

register_book = book.add_book(book_data)
print(register_book)

"""myConnection=DBConnection()
print(myConnection.execute_query("SELECT * FROM books"))"""

