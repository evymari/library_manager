import pytest


def test_update_book_updated_correctly(mock_books_controller_with_model):
    """
    Given correct update data
    When update book function is called
    Then data is updated correctly
    And status 200 is returned
    """
    # Arrange
    books_controller, mock_books_model = mock_books_controller_with_model
    book_id = 123
    update_data = {
        "stock": 1,
        "title": "Under the Dome",
        "summary": "A thriller about the residents of Chester's Mill, Maine, who are suddenly trapped under an "
                   "impenetrable, invisible dome, leading to chaos and revealing the darker sides of human nature. As "
                   "they struggle to survive and uncover the dome''s origin, tensions and conflicts escalate "
                   "dramatically,",
        "availability": True,
    }
    mock_books_model.update_book.return_value = True
    # Act
    result = books_controller.update_book(book_id, update_data)
    # Assert
    mock_books_model.update_book.assert_called_with(book_id, update_data)
    assert result["status_code"] == 200
    assert result["message"] == "Book updated successfully"


def test_update_book_validation_error(mock_books_controller_with_model):
    """
    Given invalid update data
    When update book function is called
    Then a validation error is raised
    And status 400 is returned
    """
    # Arrange
    books_controller, mock_books_model = mock_books_controller_with_model
    book_id = 123
    update_data = {
        "invalid_field": ""
    }
    # Act
    result = books_controller.update_book(book_id, update_data)
    # Assert
    assert result["status_code"] == 400
    assert "Validation error" in result["message"]
    mock_books_model.update_book.assert_not_called()


def test_update_book_failure(mock_books_controller_with_model):
    """
    Given valid update data
    When update book function is called
    And the update operation fails
    Then a status 500 is returned
    """
    # Arrange
    books_controller, mock_books_model = mock_books_controller_with_model
    book_id = 123
    update_data = {
        "stock": 5,
        "title": "Under the Dome",
        "availability": True,
    }
    mock_books_model.update_book.return_value = False
    # Act
    result = books_controller.update_book(book_id, update_data)
    # Assert
    mock_books_model.update_book.assert_called_once_with(book_id, update_data)
    assert result["status_code"] == 500
    assert result["message"] == "Failed to update book"
