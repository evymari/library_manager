import pytest


def test_search_books_by_title(mock_books_controller_with_model):
    """
    Given existing book title as search criteria,
    When search_books function is called
    Then books with matching title are found
    And status 200 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    # Mocked search criteria
    search_criteria = {"title": "Under the Dome"}
    expected_books = [
        {"book_id": 123, "title": "Under the Dome", "author": "Stephen King"},
        {"book_id": 456, "title": "Under the Dome", "author": "Another Author"}
    ]
    mock_books_model.search_books.return_value = expected_books
    # When
    result = books_controller.search_books(search_criteria)
    mock_books_model.search_books.assert_called_with(None, "Under the Dome", None, None, None, None, None, None)
    # Then
    assert result["status_code"] == 200
    assert result["books"] == expected_books


def test_search_books_by_author(mock_books_controller_with_model):
    """
    Given existing author as search criteria,
    When search_books function is called
    Then books with matching author are found
    And status 200 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    # Mocked search criteria
    search_criteria = {"author": "Suzanne Collins"}
    expected_books = [
        {"book_id": 123, "title": "The Hunger Games", "author": "Suzanne Collins"},
        {"book_id": 456, "title": "The Hunger Games2", "author": "Another Author"}
    ]
    mock_books_model.search_books.return_value = expected_books
    # When
    result = books_controller.search_books(search_criteria)
    mock_books_model.search_books.assert_called_with("Suzanne Collins", None, None, None, None, None, None, None)
    # Then
    assert result["status_code"] == 200
    assert result["books"] == expected_books

def test_search_books_by_isbn13(mock_books_controller_with_model):
    """
    Given existing isbn as search criteria,
    When search_books function is called
    Then books with matching isbn are found
    And status 200 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    # Mocked search criteria
    search_criteria = {"isbn13": "9780439023500"}
    expected_books = [
        {"book_id": 123, "title": "The Hunger Games", "author": "Suzanne Collins"},
        {"book_id": 456, "title": "The Hunger Games2", "author": "Another Author"}
    ]
    mock_books_model.search_books.return_value = expected_books
    # When
    result = books_controller.search_books(search_criteria)
    mock_books_model.search_books.assert_called_with(None, None, None, "9780439023500", None, None, None, None)
    # Then
    assert result["status_code"] == 200
    assert result["books"] == expected_books


def test_search_books_fail_missing_by_title(mock_books_controller_with_model):
    """
    Given search criteria of  title not in database,
    When search_books function is called,
    Then no books are found, an error message is raised
    And status 404 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    search_criteria = {"title": "Non-existent Book"}
    expected_books = []
    mock_books_model.search_books.return_value = expected_books
    # When
    result = books_controller.search_books(search_criteria)
    mock_books_model.search_books.assert_called_with(None, "Non-existent Book", None, None, None, None, None, None)
    # Then
    assert result["status_code"] == 404
    assert "No books found" in result["message"]


def test_search_books_by_author_error(mock_books_controller_with_model):
    """
    Given invalid author as search criteria,
    When search_books function is called,
    Then no books are not found, an error message is raised
    And status 404 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    search_criteria = {"author": "unknown_author"}
    expected_books = []
    mock_books_model.search_books.return_value = expected_books
    # When
    result = books_controller.search_books(search_criteria)
    mock_books_model.search_books.assert_called_with("unknown_author", None, None, None, None, None, None, None)
    # Then
    assert result["status_code"] == 404
    assert "No books found" in result["message"]

def test_search_books_validation_error_invalid_key(mock_books_controller_with_model):
    """
    Given invalid key as search criteria,
    When search_books function is called,
    Then a validation error is raised
    And status 400 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    search_criteria = {"invalid_key": "Suzanne Collins"}
    # When
    result = books_controller.search_books(search_criteria)
    # Then
    assert result["status_code"] == 400
    assert "Validation Error" in result["message"]

def test_search_books_validation_error_invalid_type(mock_books_controller_with_model):
    """
    Given invalid data type as search criteria,
    When search_books function is called,
    Then a validation error is raised
    And status 400 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    search_criteria = {"isbn13": 123434}
    # When
    result = books_controller.search_books(search_criteria)
    # Then
    assert result["status_code"] == 400
    assert "Validation Error" in result["message"]


def test_search_book_fail_general_exception(mock_books_controller_with_model):
    """
    Given valid data as search criteria,
    When search_books function is called but an unexpected error occurs
    Then an exception is raised and  status code 500 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    search_criteria = {"isbn13": "9780439023500"}
    mock_books_model.search_books.side_effect = Exception("Unexpected database error")
    # When
    result = books_controller.search_books(search_criteria)
    # Then
    assert result["status_code"] == 500
    assert result["message"] == "Error searching book: Unexpected database error"
