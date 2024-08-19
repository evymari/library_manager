import pytest
from src.controllers.UsersController import UsersController

controller = UsersController()


def test_add_user_successful(mock_users_controller):
    """
        Given a new data and correct user data
        When add_user function is called
        Then the user is created successfully
        And
    """
    #Given
    user_data = {
        'dni': '42326321C',
        'name': 'Pika',
        'surname': 'Chu',
        'email': '3@example.com',
        'phone': '123456789',
        'address': '123 Pokemon St',
        'status': 'active',
        'current_loans': 0,
        'max_loans': 5
    }
    users_controller, mock_users_model = mock_users_controller
    mock_users_model.get_user_by_dni.return_value = None
    mock_users_model.get_user_email.return_value = None
    mock_users_model.create_user.return_value = ('42326321C', 'Pika', 'Chu', '3@example.com', '123456789', '123 Pokemon St', 'active', 0, 5 )

    expected_result = dict(status_code=200, message="User created successfully")

    result = users_controller.add_user(user_data)
    mock_users_model.get_user_by_dni.assert_called_with(user_data['dni'])
    mock_users_model.get_user_email.assert_called_with(user_data['email'])
    mock_users_model.create_user.assert_called_with(user_data)
    assert result == expected_result

def test_add_user_dni_already_exists(mock_users_controller):
    """
          Given a new data and correct user data
          When add_user function is called
          Then the user is created successfully
          And
      """
    #Given
    user_data = {
        'dni': '87654321C',
        'name': 'Pika',
        'surname': 'Chu',
        'email': 'olas@example.com',
        'phone': '123456789',
        'address': '123 Pokemon St',
        'status': 'active',
        'current_loans': 0,
        'max_loans': 5
    }

    users_controller, mock_users_model = mock_users_controller
    mock_users_model.get_user_by_dni.return_value = '87654321C'
    expected_result = dict(status_code=400, message="Error: user already exists")
    result = users_controller.add_user(user_data)

    mock_users_model.get_user_by_dni.assert_called_with(user_data['dni'])
    mock_users_model.get_user_email.assert_not_called()
    mock_users_model.create_user.assert_not_called()
    assert result == expected_result



def test_add_user_email_already_exists(mock_users_controller):
    """
          Given a new data and correct user data
          When add_user function is called
          Then the user is created successfully
          And
      """
    #Given
    user_data = {
        'dni': '13654321C',
        'name': 'Pika',
        'surname': 'Chu',
        'email': 'olas@example.com',
        'phone': '123456789',
        'address': '123 Pokemon St',
        'status': 'active',
        'current_loans': 0,
        'max_loans': 5
    }

    users_controller, mock_users_model = mock_users_controller
    mock_users_model.get_user_by_dni.return_value = None
    mock_users_model.get_user_email.return_value = 'olas@example.com'

    expected_result = dict(status_code=400, message="Error: email already exists")
    result = users_controller.add_user(user_data)

    mock_users_model.get_user_by_dni.assert_called_with(user_data['dni'])
    mock_users_model.get_user_email.assert_called_with(user_data['email'])
    mock_users_model.create_user.assert_not_called()
    assert result == expected_result

def test_add_user_incorrect_data_value(mock_users_controller):
    """
          Given a new data and incorrect data value
          When add_user function is called
          Then an error status_code 500 is returned
          And
      """
    #Given
    user_data = {
        'dni': '87654321C',
        'name': 'Pika',
        'surname': 'Chu',
        'email': 'olas@example.com',
        'phone': '123456789',
        'address': '123 Pokemon St',
        'status': 'active',
        'current_loans': "incorrect_value_type",
        'max_loans': 5
    }

    users_controller, mock_users_model = mock_users_controller

    expected_result = {"status_code": 400, "message": "Validation error: Invalid type for current_loans. Expected int, got str."}
    result = users_controller.add_user(user_data)
    mock_users_model.get_user_by_dni.assert_not_called()
    mock_users_model.get_user_email.assert_not_called()
    mock_users_model.create_user.assert_not_called()
    assert result == expected_result

def test_add_user_incorrect_key(mock_users_controller):
    """
          Given a new data and incorrect key
          When add_user function is called
          Then
          And
      """
    #Given
    user_data = {
        'unexpected_key': '87654321C',
        'name': 'Pika',
        'surname': 'Chu',
        'email': 'olas@example.com',
        'phone': '123456789',
        'address': '123 Pokemon St',
        'status': 'active',
        'current_loans': 0,
        'max_loans': 5
    }
    users_controller, mock_users_model = mock_users_controller
    expected_result = {"status_code": 400,
                       "message": "Validation error: Unexpected key unexpected_key found in data."}
    result = users_controller.add_user(user_data)

    mock_users_model.get_user_by_dni.assert_not_called()
    mock_users_model.get_user_email.assert_not_called()
    mock_users_model.create_user.assert_not_called()

    assert result["status_code"] == expected_result["status_code"]