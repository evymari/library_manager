from unittest.mock import Mock

import pytest


def test_update_user_successfully(mock_users_controller):
    """
    Given an existing user ID and new user data
    When update_user function is called
    Then the user is updated successfully
    And status 200 is returned
    """
    # Given
    users_controller, mock_users_model = mock_users_controller
    user_id = 1
    user_data = {
        'email': 'pika@example.com',
    }

    mock_users_model.get_user_by_id.return_value = {
        "id": user_id,
        "email": "oldemail@example.com",
    }

    mock_users_model.update_user.return_value = [
        (1, '23067947W', 'Robert', 'Holloway', 'pika@example.com', '927561438',
         '008 Boone Court\nAnthonyfort, AK 10711', 'suspended', 3, 5)
    ]
    mock_users_model.find_user_by_key_excluding_id.return_value = []

    # When
    result = users_controller.update_user(user_id, user_data)

    # Then
    mock_users_model.get_user_by_id.assert_called_with(user_id)
    mock_users_model.update_user.assert_called_with(user_id, user_data)

    expected_result = {"status_code": 200, "message": "User updated successfully"}
    assert result == expected_result


def test_fail_update_user_id_not_found(mock_users_controller):
    """
        Given not existing user ID and new user data
        When update_user function is called
        Then the user isn`t updated successfully
        And status 404 is returned
        """
    # Given
    users_controller, mock_users_model = mock_users_controller

    user_id = 'not_existing_id'
    user_data = {
        'email': 'pika@example.com',
    }

    mock_users_model.get_user_by_id.return_value = None
    mock_users_model.update_user.return_value = None
    mock_users_model.find_user_by_key_excluding_id.return_value = []

    # When
    result = users_controller.update_user(user_id, user_data)

    # Then
    expected_result = {"status_code": 400,
                       "message": "User with this ID does not exist, you cannot update a user that does not exist"}
    assert result["status_code"] == expected_result["status_code"]


def test_fail_update_user_incorrect_key(mock_users_controller):
    """
        Given existing user ID and incorrect data key
        When update_user function is called
        Then the user isn`t updated successfully
        And the user data remains unchanged
    """
    # Given
    users_controller, mock_users_model = mock_users_controller

    mock_users_model.get_user_by_id.return_value = 1
    mock_users_model.update_user.return_value = None
    mock_users_model.find_user_by_key_excluding_id.return_value = []
    user_id = 1
    user_data = {
        'incorrect_key': 'Pika',
    }

    # When
    result = users_controller.update_user(user_id, user_data)

    # Then
    expected_result = {"status_code": 400, "message": "Invalid key: 'Unexpected keys found: incorrect_key'"}
    assert result == expected_result


def test_fail_update_user_incorrect_value(mock_users_controller):
    """
        Given existing user ID and incorrect data value
        When update_user function is called
        Then the user isn`t updated successfully
        And the user data remains unchanged
        """
    # Given
    users_controller, mock_users_model = mock_users_controller

    mock_users_model.get_user_by_id.return_value = 1
    mock_users_model.update_user.return_value = None
    mock_users_model.find_user_by_key_excluding_id.return_value = []
    user_id = 1
    user_data = {
        'max_loans': 'incorrect_value',
    }

    # When
    result = users_controller.update_user(user_id, user_data)

    # Then
    expected_result = {"status_code": 400, "message": 'Invalid data type: Invalid type for max_loans. Expected int, '
                                                      'got str.'}
    assert result == expected_result


def test_update_user_check_unique_field(mock_users_controller):
    """
            Given existing user ID and existing email
            When update_user function is called
            Then the user isn`t updated successfully
            And a dictionary with status code 400 is returned
            """
    # Given
    user_id = 1
    user_data = {'email': 'example@hola.com'}
    users_controller, mock_users_model = mock_users_controller
    mock_users_model.get_user_by_id.return_value = 1
    users_controller.check_unique_fields = Mock()
    users_controller.check_unique_fields.return_value = False

    expected_result = {"status_code": 400, "message": "Conflict detected with existing data. Update aborted."}
    # When
    result = users_controller.update_user(user_id, user_data)
    # Then
    assert result == expected_result






