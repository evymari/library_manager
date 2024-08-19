import pytest


def test_update_loans_status_success(mock_loans_controller_with_loan_model):
    """
        Given an existing loan
        When update_loans_status function is called
        Then the loan status is updated
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model
    mock_loan_model.update_loan_status.return_value = 1
    loan_id = 1
    status = "returned"
    result = loans_controller.update_loan_status(loan_id, status)

    assert result == 1


def test_update_loans_status_failure(mock_loans_controller_with_loan_model):
    """
        Given an existing loan
        When update_loans_status function is called
        Then an error is raised
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model
    mock_loan_model.update_loan_status.return_value = None
    loan_id = 1
    status = "returned"
    with pytest.raises(ValueError) as e:
        loans_controller.update_loan_status(loan_id, status)
    assert str(e.value) == "Failed to update loan status"
