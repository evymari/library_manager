import pytest


def test_delete_book_success(mock_books_controller_with_model):
    """
    Given user wants to delete a book that exists in the database
    When the delete_book function is called with the book's ISBN
    Then the book is deleted successfully
    And status 200 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    book_isbn13 = "9781501156786"

    mock_books_model.delete_book.return_value = True

    # When
    result = books_controller.delete_book(book_isbn13)
    # Then
    mock_books_model.delete_book.assert_called_with(book_isbn13)

    assert result["status_code"] == 200
    assert result["message"] == "Book deleted successfully"


def test_delete_book_not_found(mock_books_controller_with_model):
    """
    Given user wants to delete a book that does not exist  in the database
    When the delete_book function is called
    Then an error is raised
    And status 404 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    book_isbn13 = "1234567"

    mock_books_model.get_book_by_isbn.return_value = None

    # When
    result = books_controller.delete_book(book_isbn13)
    # Then
    mock_books_model.get_book_by_isbn.assert_called_with(book_isbn13)
    mock_books_model.delete_book.assert_not_called()

    assert result["status_code"] == 404
    assert result["message"] == "Book not found"

def test_delete_book_unexpected_error_(mock_books_controller_with_model):
    """
    Given an unexpected error occurs during the deletion process
    When the delete_book function is called
    Then an error is raised
    And status 500 is returned
    """
    # Given
    books_controller, mock_books_model = mock_books_controller_with_model
    book_isbn13 = "9780439023500"

    mock_books_model.get_book_by_isbn.side_effect = Exception("Database connection error")

    # When
    result = books_controller.delete_book(book_isbn13)
    # Then
    mock_books_model.get_book_by_isbn.assert_called_with(book_isbn13)
    mock_books_model.delete_book.assert_not_called()

    assert result["status_code"] == 500
    assert result["message"] == "Error deleting book: Database connection error"
