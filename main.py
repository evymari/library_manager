from src.controllers.UsersController import UsersController

from config.DBConnection import DBConnection
from src.controllers.BooksController import BooksController
from models.GenresModel import GenresModel

book = BooksController()
genres = GenresModel()

"""
update_data = {
    "original_publication_year": "Set in a dystopian future where society is divided into factions based on virtues, Divergent follows Tris Prior as she discovers her identity as a Divergent, a person who does not fit neatly into any one faction. Her journey reveals a conspiracy that threatens the fragile peace of her world.",
}
print(book.update_book(5, update_data))
"""

book_data = {
    "isbn13": "9780062073501",
    "author": "Agatha Christie",
    "title": "Murder on the Orient Express"
}

register_book = book.add_book(book_data)
print(register_book)

"""myConnection=DBConnection()
print(myConnection.execute_query("SELECT * FROM books"))"""
