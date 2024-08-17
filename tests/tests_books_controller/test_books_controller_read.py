import pytest

def test_search_books_by_title(mock_books_controller_with_model):
    """
    Given search criteria title,
     When search_books function is called
    Then matching books are found
     And status 200 is returned if books are found
     """
    books_controller, mock_books_model = mock_books_controller_with_model
    # Mocked search criteria
    search_criteria = {"title": "Under the Dome"}

    expected_books = [
        {"book_id": 123, "title": "Under the Dome", "author": "Stephen King"},
        {"book_id": 456, "title": "Under the Dome", "author": "Another Author"}
    ]

    mock_books_model.search_books.return_value = expected_books
    result = books_controller.search_books(search_criteria)
    mock_books_model.search_books.assert_called_with(None, "Under the Dome", None, None ,None, None, None, None)

    assert result["status_code"] == 200
    assert result["books"] == expected_books


def test_search_books_by_author(mock_books_controller_with_model):

    """
       Given search criteria author,
      When search_books function is called
     Then books with matching author are returned
      And status 200 is returned if books are found
      """
    books_controller, mock_books_model = mock_books_controller_with_model
    # Mocked search criteria
    search_criteria = {"author": "Suzanne Collins"}

    expected_books = [
        {"book_id": 123, "title": "The Hunger Games", "author": "Suzanne Collins"},
        {"book_id": 456, "title": "The Hunger Games2", "author": "Another Author"}
    ]

    mock_books_model.search_books.return_value = expected_books
    result = books_controller.search_books(search_criteria)
    mock_books_model.search_books.assert_called_with("Suzanne Collins", None, None, None ,None, None, None, None)

    assert result["status_code"] == 200
    assert result["books"] == expected_books

def test_search_books_by_isbn13(mock_books_controller_with_model):
    """
           Given search criteria isbn13,
          When search_books function is called
          Then books with matching isbn13 are returned
          And status 200 is returned if books are found
          """
    books_controller, mock_books_model = mock_books_controller_with_model
    # Mocked search criteria
    search_criteria = {"isbn13": "9780439023500"}

    expected_books = [
        {"book_id": 123, "title": "The Hunger Games", "author": "Suzanne Collins"},
        {"book_id": 456, "title": "The Hunger Games2", "author": "Another Author"}
    ]

    mock_books_model.search_books.return_value = expected_books
    result = books_controller.search_books(search_criteria)
    mock_books_model.search_books.assert_called_with(None, None, None, "9780439023500", None, None, None, None)

    assert result["status_code"] == 200
    assert result["books"] == expected_books



