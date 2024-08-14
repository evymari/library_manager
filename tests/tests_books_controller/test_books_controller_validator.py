import pytest
from src.data_validators.BooksValidator import BooksValidator


def test_get_book_by_isbn_book_exists(mock_books_controller_with_model):
    """
        Given book isbn
        When book exists using get_book_by_isbn function
        Then return existing book id
    """
    books_controller, mock_books_model = mock_books_controller_with_model
    isbn = "9781501156786"
    mock_books_model.get_book_by_isbn.return_value = [(235,)]
    result = books_controller.books_model.get_book_by_isbn(isbn)[0][0]
    mock_books_model.get_book_by_isbn.assert_called_once_with(isbn)
    expected_result = 235
    assert result == expected_result


def test_get_book_by_isbn_book_does_not_exist(mock_books_controller_with_model):
    """
        Given book isbn
        When book does not exist using get_book_by_isbn function
        Then return empty list
    """
    books_controller, mock_books_model = mock_books_controller_with_model
    isbn = "978150111515"
    mock_books_model.get_book_by_isbn.return_value = []
    result = books_controller.books_model.get_book_by_isbn(isbn)
    mock_books_model.get_book_by_isbn.assert_called_once_with(isbn)
    expected_result = []
    assert result == expected_result


def test_update_stock_correctly(mock_books_controller_with_model):
    """
    Given book isbn
    when update_stock function is called
    then stock should be incremented by 1
    """
    books_controller, mock_books_model = mock_books_controller_with_model
    isbn = "9780142412084"
    initial_stock = 2
    mock_books_model.get_book_by_isbn.return_value = [(None, initial_stock)]
    books_controller.books_model.update_stock(isbn)
    updated_stock = initial_stock + 1
    mock_books_model.get_book_by_isbn.return_value = [(None, updated_stock)]
    final_stock = books_controller.books_model.get_book_by_isbn(isbn)[0][1]
    mock_books_model.get_book_by_isbn.assert_any_call(isbn)
    mock_books_model.update_stock.assert_called_once_with(isbn)
    assert final_stock == updated_stock


def test_validate_keys_with_valid_keys():
    """
    Given valid keys in the data
    When validate_keys function is called
    Then no exception is raised
    And test passes
    """
    validator = BooksValidator()
    valid_data = {
        "isbn13": "9780142412084",
        "author": "Roald Dahl",
        "title": "George's Marvelous Medicine",
        "original_publication_year": "1981",
        "stock": 10,
        "genre_id": 16,
        "availability": True,
        "best_seller": False
    }
    validator.validate_keys(valid_data)


def test_validate_keys_fail_with_invalid_key():
    """
    Given invalid key in the data
    When validate_keys function is called
    Then a KeyError exception is raised
    And an error response should be returned
    """
    validator = BooksValidator()
    invalid_data = {
        "isbn13": "9780142412084",
        "author": "Roald Dahl",
        "title": "George's Marvelous Medicine",
        "invalid_key": "This key is not expected"
    }

    with pytest.raises(KeyError, match="Unexpected keys found: invalid_key"):
        validator.validate_keys(invalid_data)


def test_pass_validate_data_type():
    """
    Given data with valid data type
    When validate_data_type function is called
    Then data is validated
    And data should be unchanged
    """
    validator = BooksValidator()
    data = {
        "isbn13": "9780142412084",
        "author": "Roald Dahl",
        "title": "George's Marvelous Medicine",
        "stock": 10,
        "genre_id": 16,
        "availability": True,
        "best_seller": False
    }
    result = validator.validate_data_type(data)
    assert result == data

def test_fail_validate_data_type_invalid_data_type():
    """
    Given data with invalid data type
    When validate_data_type function is called
    Then a TypeError should be raised
    """
    validator = BooksValidator()
    data = {
        "isbn13": 9780142412084,
    }
    with pytest.raises(TypeError, match="Invalid type for isbn13. Expected str, got int."):
        validator.validate_data_type(data)

def test_pass_validate_data_type_original_publication_year():
    """
    Given valid date format for original_publication_year
    When validate_data_type function is called
    Then date is parsed and validated
    And test should pass
    """
    validator = BooksValidator()
    data = {
        "original_publication_year": "13101981",
    }
    result = validator.validate_data_type(data)
    assert result == data


def test_fail_validate_data_type_invalid_original_publication_year():
    """
    Given invalid date format for original_publication_year
    When validate_data_type function is called
    Then
    """
    validator = BooksValidator()
    data = {
        "original_publication_year": "1981",
    }
    with pytest.raises(ValueError, match="Invalid date format for 1981. Expected format is DDMMYYYY."):
        validator.validate_data_type(data)


def test_validate_required_fields_all_present():
    """
    Given all required data
    When validate_required_fields function is called
    Then no exception should be raised
    And test passes
    """
    validator = BooksValidator()
    data = {
        "isbn13": "9780142412084",
        "author": "Roald Dahl",
        "title": "George's Marvelous Medicine",
    }
    try:
        validator.validate_data_type(data)
    except ValueError:
        pytest.fail("ValueError raised")


def test_fail_validate_required_fields_missing_fields():
    """
    Given required fields are missing
    When validate_required_fields function is called
    Then a ValueError should be raised
    """
    validator = BooksValidator()
    data = {
        "author": "Roald Dahl",
        "title": "George's Marvelous Medicine",
    }
    with pytest.raises(ValueError, match="Required fields missing or empty: isbn13"):
        validator.validate_required_fields(data)


def test_fail_validate_required_fields_empty_values():
    """
    Given required fields keys but have empty values
    When validate_required_fields function is called
    Then a ValueError should be raised
    """
    validator = BooksValidator()
    data = {
        "isbn13": "",
        "author": "",
        "title": "George's Marvelous Medicine",
    }
    with pytest.raises(ValueError, match="Required fields missing or empty: isbn13, author"):
        validator.validate_required_fields(data)


def test_pass_validate_required_fields_update_missing_required_fields():
    """
    Given data with missing required fields
    When validate_required_fields function is called with is_update=True
    Then no exception should be raised
    And test should pass
    """
    validator = BooksValidator()
    data = {
        "title": "George's Marvelous Medicine",
    }
    try:
        validator.validate_required_fields(data, is_update=True)
    except ValueError:
        pytest.fail("ValueError raised")

def test_fail_validate_required_fields_update_with_empty_values():
    """
    Given required fields keys but have empty values
    When validate_required_fields function is called with is_update=True
    Then a ValueError should be raised
    """
    validator = BooksValidator()
    data = {
        "isbn13": "",
        "author": "",
        "title": "George's Marvelous Medicine",
    }
    with pytest.raises(ValueError, match="Required fields missing or empty: isbn13, author"):
        validator.validate_required_fields(data, is_update=True)


# integration testing - book_data_validator

def test_book_data_validator_pass():
    """
    Given correct and valid book data
    When data validator function is called
    Then data should pass all validation checks
    And data should remain unchanged
    """
    validator = BooksValidator()
    book_data = {
        "stock": 1,
        "isbn13": "9780142412084",
        "author": "Roald Dahl",
        "original_publication_year": "13101981",
        "title": "George's Marvelous Medicine",
        "summary": "George's Marvelous Medicine by Roald Dahl is a children's book about a boy named George who concocts a magical potion to cure his grandmother's nastiness, leading to unexpected and humorous results.",
        "genre_id": 16,
        "availability": True,
        "best_seller": False
    }

    result = validator.book_data_validator(book_data)
    assert result == book_data

# falta: test with missing required fields, invalid data types, and also for validate_update_data




