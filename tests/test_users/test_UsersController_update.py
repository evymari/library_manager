import pytest
from src.controllers.UsersController import UsersController


@pytest.fixture
def controller():
    return UsersController()


def test_update_user(controller):
    """
    Given an existing user ID and new user data
    When update_user function is called
    Then the user is updated successfully
    And status 200 is returned
    """
    # Given
    user_id = 1
    user_data = {
        'dni': '12345678A',
        'name': 'Pika',
        'surname': 'Chu',
        'email': 'pika@example.com',
        'phone': '123456789',
        'address': '123 Pokemon St',
        'status': 'active',
        'current_loans': 0,
        'max_loans': 5,
    }

    # When
    result = controller.update_user(user_id, user_data)

    # Then
    expected_result = {"status_code": 200, "message": "User updated successfully"}
    assert result["status_code"] == expected_result["status_code"]


def test_fail_update_user_id_not_found(controller):
    """
        Given not existing user ID and new user data
        When update_user function is called
        Then the user isn`t updated successfully
        And status 404 is returned
        """
    # Given
    user_id = 999
    user_data = {
        'dni': '12345678A',
        'name': 'Pika',
        'surname': 'Chu',
        'email': 'pika@example.com',
        'current_loans': 4,
    }

    # When
    result = controller.update_user(user_id, user_data)

    # Then
    expected_result = {"status_code": 404, "message": "User with this ID does not exist, you cannot update a user that does not exist"}
    assert result["status_code"] == expected_result["status_code"]


def test_fail_update_user_incorrect_key(controller):
    """
        Given existing user ID and incorrect data key
        When update_user function is called
        Then the user isn`t updated successfully
        And the user data remains unchanged
        """
    # Given
    user_id = 1
    user_data = {
        'dni': '12345678A',
        'nombre': 'Pika',
        'surname': 'Chu',
        'email': 'pika@example.com',
    }

    # When
    result = controller.update_user(user_id, user_data)

    # Then
    expected_result = {"status_code": 422, "message": "User isn't updated successfully"}
    assert result == expected_result["status_code"]


def test_fail_update_user_incorrect_value(controller):
    """
        Given existing user ID and incorrect data value
        When update_user function is called
        Then the user isn`t updated successfully
        And the user data remains unchanged
        """
    # Given
    user_id = 1
    user_data = {
        'dni': '12345678A',
        'name': 8,
        'surname': 'Chu',
        'email': 'pika@example.com',
        'current_loans': 4,
    }

    # When
    result = controller.update_user(user_id, user_data)

    # Then
    expected_result = {"status_code": 422, "message": "User isn't updated successfully"}
    assert result["status_code"] == expected_result["status_code"]


def test_fail_data_validator_incorrect_key(controller):
    """
        Given incorrect data key
        When data_validator function is called
        Then a key error is raise
        """
    # Given
    user_data = {
        'incorrect_key': 'Pika',
    }

    # When and Then
    expected_result = {"status_code": 404}
    result = controller.data_validator(user_data)
    assert result["status_code"] == expected_result["status_code"]
    """with pytest.raises(ValueError):
        controller.data_validator(user_data)"""


def test_fail_data_validator_incorrect_value(controller):
    """
        Given incorrect data value
        When data_validator function is called
        Then a type error is raised
        """
    # Given
    user_data = {
        "name": 8
    }

    # When and Then
    with pytest.raises(TypeError):
        controller.data_validator(user_data)


def test_pass_data_validator(controller):
    """
        Given correct data
        When data_validator function is called
        Then return true
        """
    # Given
    user_data = {
        'dni': '12345678A',
        'name': 'Pika',
        'surname': 'Chu',
        'email': 'pika@example.com',
        'phone': '123456789',
        'address': '123 Pokemon St',
        'status': 'active',
        'current_loans': 0,
        'max_loans': 5,
    }

    # When and Then
    result = controller.data_validator(user_data)
    expected_result = True
    assert result == expected_result
