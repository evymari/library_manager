from src.controllers.BooksController import BooksController
from models.GenresModel import GenresModel

book = BooksController()
search_criterio = {"author": "Suzanne Collins"}
print(book.search_books(search_criterio))
