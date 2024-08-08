import pytest
from src.controllers.LoansController import LoansController


def test_create_loan_success(mock_loans_controller):
    """
    Given correct data
    When create_loan function is called
    Then create a loan
    And return a dictionary with loan_id
    """
    loans_controller, mock_loan_model = mock_loans_controller

    mock_loan_model.create_loan.return_value = 1
    loan_data = {
        "book_id": 4,
        "user_id": 1,
        "due_date": "2022-12-31"
    }

    result = loans_controller.create_loan(loan_data)

    mock_loan_model.create_loan.assert_called_with(loan_data)
    assert result == {
        "status_code": 201,
        "message": "Loan created successfully",
        "data": {"loan_id": 1}
    }


def test_create_loan_fail_incorrect_value(mock_loans_controller):
    """
    Given incorrect values
    When create_loan function is called
    Then create a loan
    And return a dictionary with loan_id
    """
    loans_controller, mock_loan_model = mock_loans_controller
    mock_loan_model.create_loan.return_value = None
    loan_data = {
        "book_id": 'incorrect_value',
        "user_id": 1,
        "due_date": "2022-12-31"
    }

    result = loans_controller.create_loan(loan_data)

    mock_loan_model.create_loan.assert_called_with(loan_data)
    assert result == {
        "status_code": 400,
        "message": 'Failed to create loan.'
    }


def test_create_loan_fail_incorrect_key(mock_loans_controller):
    """
    Given incorrect key
    When create_loan function is called
    Then a loan is not created
    And return a dictionary with status code 400

    """
    loans_controller, mock_loan_model = mock_loans_controller
    mock_loan_model.create_loan.return_value = None
    loan_data = {
        "invalid-key": 3,
        "user_id": 1,
        "due_date": "2022-12-31"
    }

    result = loans_controller.create_loan(loan_data)

    mock_loan_model.create_loan.assert_called_with(loan_data)
    assert result == {
        "status_code": 400,
        "message": 'Failed to create loan.'
    }
    assert result["status_code"] == 400
