import pytest
from src.controllers.UsersController import UsersController

controller = UsersController()


def test_add_user_successful():
    """
        Given a new data and correct user data
        When add_user function is called
        Then the user is created successfully
        And
    """
    """Given"""
    user_data = {
        'dni': '12326321C',
        'name': 'Pika',
        'surname': 'Chu',
        'email': '2@example.com',
        'phone': '123456789',
        'address': '123 Pokemon St',
        'status': 'active',
        'current_loans': 0,
        'max_loans': 5
    }

    expected_result = dict(status_code=200, message="User created successfully")
    result = controller.add_user(user_data)
    assert result == expected_result

def test_add_user_dni_already_exists():
    """
          Given a new data and correct user data
          When add_user function is called
          Then the user is created successfully
          And
      """
    """Given"""
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

    expected_result = dict(status_code=400, message="error: user already exists")
    result = controller.add_user(user_data)
    assert result == expected_result



def test_add_user_email_already_exists():
    """
          Given a new data and correct user data
          When add_user function is called
          Then the user is created successfully
          And
      """
    """Given"""
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

    expected_result = dict(status_code=400, message="error: email already exists")
    result = controller.add_user(user_data)
    assert result == expected_result

def test_add_user_incorrect_data_value():
    """
          Given a new data and incorrect data value
          When add_user function is called
          Then an error status_code 500 is returned
          And
      """
    """Given"""
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

    expected_result = {"status_code":500}
    result = controller.add_user(user_data)
    assert result["status_code"] == expected_result["status_code"]

def test_add_user_incorrect_key():
    """
          Given a new data and incorrect key
          When add_user function is called
          Then
          And
      """
    """Given"""
    user_data = {
        'incorrect_key': '87654321C',
        'name': 'Pika',
        'surname': 'Chu',
        'email': 'olas@example.com',
        'phone': '123456789',
        'address': '123 Pokemon St',
        'status': 'active',
        'current_loans': 0,
        'max_loans': 5
    }

    expected_result = {"status_code":500}
    result = controller.add_user(user_data)
    assert result["status_code"] == expected_result["status_code"]