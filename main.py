from config.DBConnection import DBConnection
from src.controllers.BooksController import BooksController
from models.GenresModel import GenresModel
book = BooksController()
genres = GenresModel()


update_data = {
    "summary": "Young Harry Potter discovers that he is a wizard on his eleventh birthday. He attends Hogwarts School of Witchcraft and Wizardry, where he makes friends, uncovers secrets, and faces the dark wizard Voldemort.",
    "author": ""
}
print(book.update_book(2, update_data))

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
