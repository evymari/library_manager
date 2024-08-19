import pytest
from unittest.mock import Mock


def test_return_book_success(mock_loans_controller_with_user_and_book_mode_and_loan_model):
    """
    Given a valid loan ID
    And the loan exists in the system
    And the book has not been returned yet
    And the book is returned on time
    When the return_book function is called
    Then the loan status should be updated to "returned"
    And the return date should be updated
    And the user's loan count should be decremented
    And the book stock should be incremented
    And a status code 200 with the message "Book returned successfully" should be returned
    """
    loans_controller, mock_loan_model, mock_user_model, mock_book_model = mock_loans_controller_with_user_and_book_mode_and_loan_model

    loan_id = 1
    user_id = 1
    book_id = 1
    loan_data = {
        "loan_id": loan_id,
        "user_id": user_id,
        "book_id": book_id,
        "status": "loaned",
        "start_loan_date": "2023-01-01",
        "due_date": "2023-12-31",
        "return_date": None
    }
    user_data = {"id": user_id, "name": "John Doe", "current_loans": 2, "status": "active"}

    # Mocking the necessary methods
    mock_loan_model.get_loan_by_id.return_value = loan_data
    mock_loan_model.is_return_late.return_value = False
    mock_user_model.get_user_by_id.return_value = user_data
    loans_controller.update_user_loans_count = Mock()
    loans_controller.update_book_stock = Mock()

    result = loans_controller.return_book(loan_id)

    mock_loan_model.get_loan_by_id.assert_called_with(loan_id)
    mock_loan_model.update_loan_status.assert_called_with(loan_id, "returned")
    mock_loan_model.update_return_date.assert_called_with(loan_id)
    mock_loan_model.is_return_late.assert_called_with(loan_id)
    mock_user_model.suspend_user.assert_not_called()
    loans_controller.update_user_loans_count.assert_called_with(user_id, user_data, -1)
    loans_controller.update_book_stock.assert_called_with(book_id, 1)

    assert result == {
        "status_code": 200,
        "message": "Book returned successfully"
    }


def test_return_book_loan_not_found(mock_loans_controller_with_loan_model):
    """
    Given an invalid loan ID
    When the return_book function is called
    Then a status code 400 with the message "Loan not found" should be returned
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model

    loan_id = 999

    mock_loan_model.get_loan_by_id.return_value = None

    result = loans_controller.return_book(loan_id)

    mock_loan_model.get_loan_by_id.assert_called_with(loan_id)
    mock_loan_model.update_loan_status.assert_not_called()
    mock_loan_model.update_return_date.assert_not_called()

    assert result == {
        "status_code": 400,
        "message": "Loan not found"
    }


def test_return_book_already_returned(mock_loans_controller_with_loan_model):
    """
    Given a loan ID for a book that has already been returned
    When the return_book function is called
    Then a status code 400 with the message "Book already returned" should be returned
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model

    loan_id = 1
    loan_data = {
        "loan_id": loan_id,
        "user_id": 1,
        "book_id": 1,
        "status": "returned",
        "start_loan_date": "2023-01-01",
        "due_date": "2023-12-31",
        "return_date": "2023-12-31"
    }

    mock_loan_model.get_loan_by_id.return_value = loan_data

    result = loans_controller.return_book(loan_id)

    mock_loan_model.get_loan_by_id.assert_called_with(loan_id)
    mock_loan_model.update_loan_status.assert_not_called()
    mock_loan_model.update_return_date.assert_not_called()

    assert result == {
        "status_code": 400,
        "message": "Book already returned"
    }


def test_return_book_late_return(mock_loans_controller_with_user_and_book_mode_and_loan_model):
    """
    Given a loan ID for a book that is returned late
    When the return_book function is called
    Then the user's status should be updated to "suspended"
    And the loan status should be updated to "returned"
    And the return date should be updated
    And the user's loan count should be decremented
    And the book stock should be incremented
    And a status code 200 with the message "Book returned successfully" should be returned
    """
    loans_controller, mock_loan_model, mock_user_model, mock_book_model = mock_loans_controller_with_user_and_book_mode_and_loan_model

    loan_id = 1
    user_id = 1
    book_id = 1
    loan_data = {
        "loan_id": loan_id,
        "user_id": user_id,
        "book_id": book_id,
        "status": "loaned",
        "due_date": "2023-12-31"
    }
    user_data = {"id": user_id, "name": "John Doe", "current_loans": 2, "status": "active"}

    mock_loan_model.get_loan_by_id.return_value = loan_data
    mock_loan_model.is_return_late.return_value = True
    mock_user_model.get_user_by_id.return_value = user_data

    loans_controller.update_user_loans_count = Mock()
    loans_controller.update_book_stock = Mock()

    result = loans_controller.return_book(loan_id)

    mock_loan_model.get_loan_by_id.assert_called_with(loan_id)
    mock_loan_model.update_loan_status.assert_called_with(loan_id, "returned")
    mock_loan_model.update_return_date.assert_called_with(loan_id)
    mock_loan_model.is_return_late.assert_called_with(loan_id)
    mock_user_model.suspend_user.assert_called_with(user_id)
    loans_controller.update_user_loans_count.assert_called_with(user_id, user_data, -1)
    loans_controller.update_book_stock.assert_called_with(book_id, 1)

    assert result == {
        "status_code": 200,
        "message": "Book returned successfully"
    }
