import pytest

def test_delete_loan_success(mock_loans_controller_with_loan_model):
    """
    Given existing loan_id
    When delete_loan function is called
    Then delete loan
    And return a dictionary with status code 200
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model

    loan_id = 1

    mock_loan_model.get_loan_by_id.return_value = 1

    result = loans_controller.delete_loan(loan_id)

    mock_loan_model.delete_loan.assert_called_with(loan_id)

    assert result == {"status_code": 200, "message": "loan deleted successfully"}
