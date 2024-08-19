import pytest
from src.data_validators.UsersValidator import UsersValidator


@pytest.fixture
def users_validator():
    return UsersValidator()


def test_data_validator_success(users_validator):
    """
    Scenario: Validate correct user data types
      Given a dictionary with correct user data types
      When the data_validator function is called
      Then it should return True
    """
    # Given
    valid_data = {
        "dni": "12345678X",
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "password": "securepassword",
        "address": "123 Street Name",
        "status": "active",
        "current_loans": 2,
        "max_loans": 5
    }

    # When
    result = users_validator.data_validator(valid_data)

    # Then
    assert result is True


def test_data_validator_invalid_type(users_validator):
    """
    Scenario: Invalid data type in user data
      Given a dictionary with an incorrect data type
      When the data_validator function is called
      Then it should raise a TypeError
    """
    # Given
    invalid_data = {
        "dni": "12345678X",
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "password": "securepassword",
        "address": "123 Street Name",
        "status": "active",
        "current_loans": "two",  # Should be an int, not a str
        "max_loans": 5
    }

    # When / Then
    with pytest.raises(TypeError, match="Invalid type for current_loans. Expected int, got str."):
        users_validator.data_validator(invalid_data)


def test_data_validator_invalid_value_type(users_validator):
    """
    Scenario: Invalid data type in user data
      Given a dictionary with an incorrect data type
      When the data_validator function is called
      Then it should raise a TypeError
    """
    # Given
    invalid_data = {
        "dni": "12345678X",
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "password": "securepassword",
        "address": "123 Street Name",
        "status": "active",
        "current_loans": "two",  # Should be an int, not a str
        "max_loans": 5
    }

    # When / Then
    with pytest.raises(TypeError, match="Invalid type for current_loans. Expected int, got str."):
        users_validator.data_validator(invalid_data)


def test_data_validator_unexpected_key(users_validator):
    """
    Scenario: Unexpected key in user data
      Given a dictionary with an unexpected key
      When the data_validator function is called
      Then it should raise a KeyError
    """
    # Given
    invalid_data = {
        "dni": "12345678X",
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "password": "securepassword",
        "address": "123 Street Name",
        "status": "active",
        "current_loans": 2,
        "max_loans": 5,
        "unexpected_key": "unexpected_value"  # Key not expected in the schema
    }

    # When / Then
    with pytest.raises(KeyError, match="'Unexpected keys found: unexpected_key'"):
        users_validator.data_validator(invalid_data)
