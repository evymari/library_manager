import pytest

def test_delete_loan_success(mock_loans_controller_with_loan_model):
    """
    Given existing loan_id
    When delete_loan function is called
    Then loan entry is deleted
    And a dictionary with status code 200 is returned
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model
    loan_id = 1
    mock_loan_model.get_loan_by_id.return_value = 1

    result = loans_controller.delete_loan(loan_id)
    mock_loan_model.delete_loan.assert_called_with(loan_id)

    assert result == {"status_code": 200, "message": "loan deleted successfully"}

def test_delete_loan_fail_loan_not_found(mock_loans_controller_with_loan_model):
    """
    Given invalid loan_id
    When delete_loan function is called
    Then a value error is raised, no loan entry is deleted
    And a dictionary with status code 400 is returned
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model
    loan_id = 999
    mock_loan_model.get_loan_by_id.return_value = None

    result = loans_controller.delete_loan(loan_id)
    mock_loan_model.delete_loan.assert_not_called()

    assert result == {"status_code": 400, "message": "loan not found"}

def test_delete_loan_fail_unexpected_error(mock_loans_controller_with_loan_model):
    """
    Given valid load id but an unexpected error occurred during deletion
    When delete_loan function is called
    Then an exception is raised, no loan entry is deleted,
    And a dictionary with status code 500 is returned
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model
    loan_id = 1
    mock_loan_model.get_loan_by_id.return_value = (1, )
    mock_loan_model.delete_loan.side_effect = Exception("Database error")

    result = loans_controller.delete_loan(loan_id)
    mock_loan_model.delete_loan.assert_called_with(loan_id)

    assert result == {"status_code": 500, "message": "Internal server error"}
