from config.DBConnection import DBConnection
from src.controllers.BooksController import BooksController
from models.GenresModel import GenresModel
book = BooksController()
genres = GenresModel()


update_data = {
    "summary": "A young farm boy discovers a mysterious dragon egg that hatches, thrusting him into a world of magic and ancient conflict. As Eragon embarks on a journey to become a Dragon Rider, he must confront dark forces threatening his homeland.",
    "best_seller": False
}
print(book.update_book(20, update_data))

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
