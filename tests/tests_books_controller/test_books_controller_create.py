import pytest


def test_add_book_added_correctly(mock_books_controller_with_model):
    """
    Given User introduces book data
    When add book function is called
    Then a book is added
    And status 200 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    book_data = {
        "stock": 1,
        "isbn13": "9781501156786",
        "author": "Stephen King",
        "original_publication_year": "01011987",
        "title": "Under the Dome",
        "summary": "Under the Dome by Stephen King is a thriller about the residents of Chester's Mill, Maine, "
                   "who are suddenly trapped under an impenetrable, invisible dome, leading to chaos and revealing "
                   "the darker sides of human nature. As they struggle to survive and uncover the dome''s origin, "
                   "tensions and conflicts escalate dramatically,",
        "genre_id": 4,
        "availability": True,
        "best_seller": False}
    mock_books_model.get_book_by_isbn.return_value = []
    mock_books_model.create_book.return_value = 123
    # When
    result = books_controller.add_book(book_data)
    # Then
    mock_books_model.get_book_by_isbn.assert_called_with("9781501156786")
    mock_books_model.create_book.assert_called_with(book_data)
    assert result["status_code"] == 200
    assert result["message"] == "Book added successfully"


def test_add_book_stock_updated_correctly(mock_books_controller_with_model):
    """
    Given book data of book to add
    When add book function is called, regardless of whether book is already in stock,
    Then stock is updated by 1
    And status 200 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    mock_books_model.get_book_by_isbn.return_value = [{"stock": 5, "isbn13": 9781501156786}]
    book_data = {
        "isbn13": "9781501156786",
        "author": "Stephen King",
        "title": "Under the Dome",
    }
    # When
    result = books_controller.add_book(book_data)
    # Then
    mock_books_model.get_book_by_isbn.assert_called_with("9781501156786")
    mock_books_model.update_stock_by_isbn13.assert_called_with("9781501156786")
    assert result["status_code"] == 200
    assert result["message"] == "Book stock updated successfully"


def test_add_book_fail_missing_required_field(mock_books_controller_with_model):
    """
    Given missing required book data
    When add book function is called,
    Then a ValueError is raised
    And the book is not added
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    book_data = {
        "author": "Stephen King",
        "title": "Under the Dome",
    }
    # When
    result = books_controller.add_book(book_data)
    # Then
    assert result["status_code"] == 400
    assert result["message"] == "Validation error: Required fields missing or empty: isbn13"
    mock_books_model.create_book.assert_not_called()


def test_add_book_fail_invalid_data_type(mock_books_controller_with_model):
    """
    Given invalid data type
    When add book function is called,
    Then a TypeError is raised
    And the book is not added
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    book_data = {
        "isbn13": 9781501156786,
        "author": "Stephen King",
        "title": "Under the Dome",
    }
    # When
    result = books_controller.add_book(book_data)
    # Then
    assert result["status_code"] == 400
    assert result["message"] == "Validation error: Invalid type for isbn13. Expected str, got int."
    mock_books_model.create_book.assert_not_called()


def test_add_book_fail_invalid_data_key(mock_books_controller_with_model):
    """
    Given invalid data key
    When add book function is called,
    Then a KeyError is raised
    And the book is not added
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    book_data = {
        "isbn13": 9781501156786,
        "author": "Stephen King",
        "tittle": "Under the Dome",
    }
    # When
    result = books_controller.add_book(book_data)
    # Then
    assert result["status_code"] == 400
    assert result["message"] == "Validation error: 'Unexpected keys found: tittle'"
    mock_books_model.create_book.assert_not_called()


def test_add_book_fail_unable_to_retrieve_new_book_id(mock_books_controller_with_model):
    """
    Given valid book data
    When add book function is called but no new book_id is returned
    Then status code 500 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    book_data = {
        "isbn13": "9781501156786",
        "author": "Stephen King",
        "title": "Under the Dome",
    }
    mock_books_model.get_book_by_isbn.return_value = []
    mock_books_model.create_book.return_value = None
    # When
    result = books_controller.add_book(book_data)
    # Then
    assert result["status_code"] == 500
    assert result["message"] == "Failed to add book."


def test_add_book_fail_general_exception(mock_books_controller_with_model):
    """
    Given valid book data
    When add book function is called but an unexpected error occurs
    Then an exception is raised and status code 500 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    book_data = {
        "isbn13": "9781501156786",
        "author": "Stephen King",
        "title": "Under the Dome",
    }
    mock_books_model.get_book_by_isbn.side_effect = Exception("Unexpected database error")
    # When
    result = books_controller.add_book(book_data)
    # Then
    assert result["status_code"] == 500
    assert result["message"] == "Error adding book: Unexpected database error"
