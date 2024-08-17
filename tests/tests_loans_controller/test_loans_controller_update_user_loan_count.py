import pytest


def test_update_user_loan_count(mock_loans_controller_with_user_model):
    """
         Given an existing user
         When update_user_loans_count function is called
         Then the user id is returned
     """
    loans_controller, mock_user_model = mock_loans_controller_with_user_model
    mock_user_model.update_user_loans_count.return_value = 1
    user_id = 1
    user_data = {"current_loans": 0}
    change = 1
    result = loans_controller.update_user_loans_count(user_id, user_data, change)

    assert result == 1


def test_update_user_data_failure(mock_loans_controller_with_user_model):
    """
        Given an existing user
        When update_user_loans_count function is called
        Then an error is raised
    """
    loans_controller, mock_user_model = mock_loans_controller_with_user_model
    mock_user_model.update_user_loans_count.return_value = None
    user_id = 1
    user_data = {"current_loans": 0}
    change = 1
    with pytest.raises(ValueError) as e:
        loans_controller.update_user_loans_count(user_id, user_data, change)
    assert str(e.value) == "Failed to update user loans count"
