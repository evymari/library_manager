import pytest
from src.controllers.BooksController import BooksController

books_controller = BooksController()

def test_search_books():

    """
    Given User introduces book data
    When add book function is called
    Then a book is added
    And status 200 is returned
    """
