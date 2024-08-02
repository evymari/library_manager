import pytest
from src.controllers.LoansController import LoansController

controller = LoansController()


def test_create_loan_success():
    """
    Given correct data
    When create_loan function is called
    Then create a loan
    And return a dictionary with loan_id
    """

    loan_data = {
        "book_id": 4,
        "user_id": 1,
        "due_date": "2022-12-31"
    }

    result = controller.create_loan(loan_data)

    assert result["status_code"] == 201
    assert result["message"] == "Loan created successfully"
    assert "loan_id" in result["data"]
    assert isinstance(result["data"]["loan_id"], int)


def test_create_loan_fail_incorrect_value():
    """
    Given incorrect values
    When create_loan function is called
    Then create a loan
    And return a dictionary with loan_id
    """

    loan_data = {
        "book_id": 'incorrect value',
        "user_id": 1,
        "due_date": "2022-12-31"
    }

    result = controller.create_loan(loan_data)
    assert result["status_code"] == 400


def test_create_loan_fail_incorrect_key():
    """
    Given incorrect key
    When create_loan function is called
    Then a loan is not created
    And return a dictionary with status code 400

    """
    loan_data = {
        "incorrect_key": 1,
        "user_id": 1,
        "due_date": "2022-12-31"
    }

    result = controller.create_loan(loan_data)
    assert result["status_code"] == 400
