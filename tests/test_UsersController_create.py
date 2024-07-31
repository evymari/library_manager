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
        'dni': '12345678A',
        'name': 'Pika',
        'surname': 'Chu',
        'email': 'pika@example.com',
        'phone': '123456789',
        'address': '123 Pokemon St',
        'status': 'active',
        'current_loans': 0,
        'max_loans': 5
    }

    expected_result = {True}
    result = controller.add_user(user_data)
    assert result == expected_result
