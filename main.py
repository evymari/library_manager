from config.DBConnection import DBConnection
from src.controllers.BooksController import BooksController
from models.GenresModel import GenresModel

Book = BooksController()
search_criteria= {
    "author":"Markus Zusak",
    "title":"The Messenger",
    "genre_id":None
}

print(Book.search_books(search_criteria))


"""myConnection=DBConnection()
print(myConnection.execute_query("SELECT * FROM books"))"""
