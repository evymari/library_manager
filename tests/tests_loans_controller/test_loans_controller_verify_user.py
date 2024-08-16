import pytest


def test_verify_user_data_success(mock_loans_controller_with_user_model):
    """
        Given an existing user
        And the user is active
        And a user that can borrow more books
        When verify_user_data function is called
        Then the user data is returned
    """
    loans_controller, mock_user_model = mock_loans_controller_with_user_model

    mock_user_model.get_user_by_id.return_value = {"name": "John Doe", "id": 1, "status": "active", "current_loans": 0,
                                                   "max_loans": 5}
    mock_user_model.is_user_active.return_value = True
    mock_user_model.has_reached_max_loans.return_value = False
    user_id = 1
    result = loans_controller.verify_user_data(user_id)

    assert result == {"name": "John Doe", "id": 1, "status": "active", "current_loans": 0, "max_loans": 5}


def test_verify_user_data_no_user_found(mock_loans_controller_with_user_model):
    """
        Given a not existing user
        When verify_user_data function is called
        Then a ValueError with the message "User not found" is raised
    """
    loans_controller, mock_user_model = mock_loans_controller_with_user_model
    mock_user_model.get_user_by_id.return_value = None
    user_id = 1
    with pytest.raises(ValueError) as e:
        loans_controller.verify_user_data(user_id)
    assert str(e.value) == "User not found"


def test_verify_user_data_no_active_user(mock_loans_controller_with_user_model):
    """
        Given an existing user
        And the user is not active
        When verify_user_data function is called
        Then a ValueError with the message "User is not active" is raised
    """
    loans_controller, mock_user_model = mock_loans_controller_with_user_model
    mock_user_model.get_user_by_id.return_value = {"name": "John Doe", "id": 1, "status": "inactive",
                                                   "current_loans": 0,
                                                   "max_loans": 5}
    mock_user_model.is_user_active.return_value = False
    user_id = 1
    with pytest.raises(ValueError) as e:
        loans_controller.verify_user_data(user_id)
    assert str(e.value) == "User is not active"


def test_verify_user_data_user_has_reached_max_loans(mock_loans_controller_with_user_model):
    """
        Given an existing user
        And the user has reached maximum loans
        When verify_user_data function is called
        Then a ValueError with the message "User has reached maximum loans" is raised
    """
    loans_controller, mock_user_model = mock_loans_controller_with_user_model
    mock_user_model.get_user_by_id.return_value = {"name": "John Doe", "id": 1, "status": "active",
                                                   "current_loans": 5,
                                                   "max_loans": 5}
    mock_user_model.has_reached_max_loans.return_value = True
    user_id = 1
    with pytest.raises(ValueError) as e:
        loans_controller.verify_user_data(user_id)
    assert str(e.value) == "User has reached maximum loans"
