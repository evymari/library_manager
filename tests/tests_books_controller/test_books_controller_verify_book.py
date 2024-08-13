import pytest
from src.controllers.BooksController import BooksController

books_controller = BooksController()

def test_pass_get_book_by_isbn_book_exists():
    """
        Given book isbn
        When book exists using get_book_by_isbn function
        Then return existing book id
    """
    isbn = "9781501156786"
    result = books_controller.books_model.get_book_by_isbn(isbn)[0][0]
    expected_result = 235
    assert result == expected_result

def test_get_book_by_isbn_book_does_not_exist():
    """
        Given book isbn
        When book does not exist using get_book_by_isbn function
        Then return empty list
    """
    isbn = "978150111515"
    result = books_controller.books_model.get_book_by_isbn(isbn)
    expected_result = []
    assert result == expected_result

def test_update_stock_correctly():
    """
    Given book isbn
    when update_stock function is called
    then stock should be incremented by 1
    """
    isbn = "9780142412084"
    initial_stock = books_controller.books_model.get_book_by_isbn(isbn)[0][1]
    books_controller.books_model.update_stock(isbn)
    updated_stock = books_controller.books_model.get_book_by_isbn(isbn)[0][1]
    expected_stock = initial_stock + 1
    assert updated_stock == expected_stock

def test_pass_book_data_validator():
    """
    Given correct book data
    When data validator function is called
    Then return True
    """
    book_data = {
        "stock": 1,
        "isbn13": "9780142412084",
        "author": "Roald Dahl",
        "original_publication_year": "13101981",
        "title": "George's Marvelous Medicine",
        "summary": "George's Marvelous Medicine by Roald Dahl is a children's book about a boy named George who concocts a magical potion to cure his grandmother's nastiness, leading to unexpected and humorous results.",
        "genre_id": 16,
        "availability": True,
        "best_seller": False
    }

    result = books_controller.books_model.book_data_validator(book_data)
    expected_result = True
    assert result == expected_result

def test_fail_book_data_validator_incorrect_key():
    """
    Given incorrect book data key
    When data validator function is called
    Then key error is raised
    """
    book_data = {
        "isbn13": "9780142412084",
        "author": "Roald Dahl",
        "titulo": "George's Marvelous Medicine",
    }

    with pytest.raises(KeyError):
        books_controller.books_model.book_data_validator(book_data)

def test_fail_book_data_validator_incorrect_value():
    """
    Given incorrect book data value
    When data validator function is called
    Then type error is raised
    """
    book_data = {
        "isbn13": 9780142412084,
        "author": "Roald Dahl",
        "title": "George's Marvelous Medicine",
    }

    with pytest.raises(TypeError):
        books_controller.books_model.book_data_validator(book_data)
