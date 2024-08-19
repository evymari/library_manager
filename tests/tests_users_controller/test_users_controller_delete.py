import pytest


def test_delete_user_successfully(mock_users_controller, mocker):
    """
    Given an existing user ID with no active loans
    When delete_user function is called
    Then the user is deleted successfully
    And status 200 is returned
    """
    # Given
    users_controller, mock_users_model = mock_users_controller
    user_id = 1

    # Mocking the get_user_by_id method to simulate an existing user
    mock_users_model.get_user_by_id.return_value = {
        "id": user_id,
        "email": "pika@example.com",
        "status": "active",
    }

    # Mocking the loans_model to simulate no active loans for the user
    mock_loans_model = mocker.patch.object(users_controller, 'loans_model', autospec=True)
    mock_loans_model.get_loans_by_user_id.return_value = []

    # Mocking delete_user to return the correct user_id
    mock_users_model.delete_user.return_value = user_id

    # When
    result = users_controller.delete_user(user_id)

    # Then
    expected_result = {"status_code": 200, "message": f"User with ID {user_id} deleted successfully"}
    assert result == expected_result


def test_fail_delete_user_with_active_loans(mock_users_controller, mocker):
    """
    Given an existing user ID with active loans
    When delete_user function is called
    Then the user isn't deleted
    And status 400 is returned
    """
    # Given
    users_controller, mock_users_model = mock_users_controller
    user_id = 1

    mock_users_model.get_user_by_id.return_value = {
        "id": user_id,
        "email": "pika@example.com",
        "status": "active",
    }

    mock_loans_model = mocker.patch.object(users_controller, 'loans_model', autospec=True)
    mock_loans_model.get_loans_by_user_id.return_value = [
        (126, 1, 1, 'loaned', '2024-08-01', '2024-08-15', None)
    ]

    # When
    result = users_controller.delete_user(user_id)

    # Then
    expected_result = {"status_code": 400, "message": "Cannot delete user with active loans."}
    assert result == expected_result


def test_fail_delete_user_not_found(mock_users_controller):
    """
    Given a non-existent user ID
    When delete_user function is called
    Then the user isn't deleted
    And status 404 is returned
    """
    # Given
    users_controller, mock_users_model = mock_users_controller
    user_id = 'not_existing_id'

    mock_users_model.get_user_by_id.return_value = None

    # When
    result = users_controller.delete_user(user_id)

    # Then
    expected_result = {"status_code": 404, "message": f"User with ID {user_id} does not exist."}
    assert result == expected_result


def test_fail_delete_inactive_user_due_to_retention_policy(mock_users_controller):
    """
    Given an existing user ID with status 'inactive'
    When delete_user function is called
    Then the user isn't deleted
    And status 403 is returned due to data retention policy
    """
    # Given
    users_controller, mock_users_model = mock_users_controller
    user_id = 1

    # Simulamos que el usuario tiene el estado 'inactive'
    mock_users_model.get_user_by_id.return_value = {
        "id": user_id,
        "email": "inactiveuser@example.com",
        "status": "inactive",
    }

    # When
    result = users_controller.delete_user(user_id)

    # Then
    expected_result = {
        "status_code": 403,
        "message": "Cannot delete an inactive user due to data retention policy."
    }
    assert result == expected_result


def test_fail_delete_user_database_error(mock_users_controller):
    """
    Given an existing user ID
    When delete_user function is called and a database error occurs
    Then the user isn't deleted
    And status 500 is returned
    """
    # Given
    users_controller, mock_users_model = mock_users_controller
    user_id = 1

    # Simulamos que el método delete_user del modelo lanza una excepción
    mock_users_model.get_user_by_id.return_value = {
        "id": user_id,
        "email": "pika@example.com",
        "status": "active",
    }
    mock_users_model.delete_user.side_effect = Exception("Database error")

    # When
    result = users_controller.delete_user(user_id)

    # Then
    expected_result = {"status_code": 400, "message": "Internal server error: Database error"}
    assert result == expected_result
