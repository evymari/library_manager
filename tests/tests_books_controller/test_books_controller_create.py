'''import pytest
from src.controllers.BooksController import BooksController

books_controller = BooksController()

def test_add_book():

    """
    Given User introduces book data
    When add book function is called
    Then a book is added
    And status 200 is returned
    """
    book_data = {"stock": None, "isbn13":"9780000222", 'author': "Jim Carrey", "original_publication_year": 1987, "title": "Who Are You", "summary": None, "genre_id": None, "availability": None, "best_seller": None}

    result = books_controller.add_book(book_data)
    expected_result = {"status_code": 200, "message": "Book added successfully"}
    assert result["status_code"] == expected_result["status_code"]'''
