import pytest


def test_update_return_date_success(mock_loans_controller_with_loan_model):
    """
    Given a valid loan ID
    And the loan exists in the system
    And the return date is updated
    When the update_return_date function is called
    Then the return date should be updated
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model

    loan_id = 1

    mock_loan_model.update_return_date.return_value = loan_id

    result = loans_controller.update_return_date(loan_id)

    mock_loan_model.update_return_date.assert_called_with(loan_id)

    assert result == loan_id


def test_update_return_date_failure(mock_loans_controller_with_loan_model):
    """
    Given an invalid loan ID
    When the update_return_date function is called
    Then a ValueError with the message "Loan not found" should be raised
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model

    loan_id = "invalid_id"

    mock_loan_model.update_return_date.return_value = None

    with pytest.raises(ValueError) as e:
        loans_controller.update_return_date(loan_id)
        assert str(e.value) == "Failed to update return date"
