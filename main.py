from config.DBConnection import DBConnection
from src.controllers.BooksController import BooksController
from models.GenresModel import GenresModel
book = BooksController()
genres = GenresModel()


update_data = {
    "summary": "A science fiction novel about a parasitic alien species that takes over human bodies. The story follows Wanderer, an alien soul, who struggles with her host's strong will and memories, ultimately forming an alliance to seek the remaining free humans.",
    "best_seller": False
}
print(book.update_book(25, update_data))

# falta - check other data to update, test with invalid data or types

"""
book_data = {
    "isbn13": "9780141365467",
    "author": "Roald Dahl",
    "title": "Danny the Champion of the World"
}

register_book = book.add_book(book_data)
print(register_book)"""

"""myConnection=DBConnection()
print(myConnection.execute_query("SELECT * FROM books"))"""
