import pytest
from src.controllers.LoansController import LoansController


def test_create_loan_success(mock_loans_controller_with_loan_model):
    """
    Given correct data
    When create_loan function is called
    Then create a loan
    And return a dictionary with loan_id
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model

    mock_loan_model.create_loan.return_value = 1

    book_id = 1
    user_id = 1
    due_date = "2022-12-31"

    result = loans_controller.create_loan(book_id, user_id, due_date)

    mock_loan_model.create_loan.assert_called_with({
        "book_id": book_id,
        "user_id": user_id,
        "due_date": due_date
    })
    assert result == 1


def test_create_loan_fail_incorrect_value(mock_loans_controller_with_loan_model):
    """
    Given incorrect values
    When create_loan function is called
    Then create a loan
    And return a dictionary with loan_id
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model
    mock_loan_model.create_loan.return_value = None

    book_id = 1
    user_id = 'invalid_input'
    due_date = "2022-12-31"

    with pytest.raises(ValueError) as e:
        loans_controller.create_loan(book_id, user_id, due_date)
    assert str(e.value) == 'Failed to create loan.'


def test_to_create_loan_fail_incorrect_date(mock_loans_controller_with_loan_model):
    """
    Given incorrect date
    When create_loan function is called
    Then create a loan
    And return a dictionary with loan_id
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model
    mock_loan_model.create_loan.return_value = None

    book_id = 1
    user_id = 1
    due_date = "invalid_input"

    with pytest.raises(ValueError) as e:
        loans_controller.create_loan(book_id, user_id, due_date)
    assert str(e.value) == 'Failed to create loan.'
