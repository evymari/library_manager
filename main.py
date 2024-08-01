from config.DBConnection import DBConnection
from src.controllers.BooksController import BooksController
from models.GenresModel import GenresModel
book = BooksController()
genres = GenresModel()


update_data = {
    "summary": "The Hunger Games by Suzanne Collins is a dystopian novel where 16-year-old Katniss Everdeen volunteers to take her sister's place in a televised death match. She must navigate the brutal competition while facing complex political and social challenges in a totalitarian society.",
    "best_seller": False
}
print(book.books_model.update_book(update_data, "isbn13", "9780439023480"))


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
