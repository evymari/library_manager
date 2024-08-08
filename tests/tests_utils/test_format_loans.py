import pytest
from datetime import date
from src.utils.loan_formatting import format_loans


def test_format_loans():
    """
    Given a list of loans in tuples
    When the format_loans function is called
    Then loans are formatted correctly in a list of dictionaries

    """
    raw_loans = [
        (1, 1, 1, 'loaned', date(2024, 7, 30), date(2022, 12, 31)),
        (2, 2, 2, 'returned', date(2024, 8, 1), date(2022, 12, 31))
    ]
    expected_result = [
        {
            "loan_id": 1,
            "book_id": 1,
            "user_id": 1,
            "status": 'loaned',
            "start_loan_date": date(2024, 7, 30),
            "return_date": date(2022, 12, 31),
            "due_date": date(2022, 12, 31),
        },
        {
            "loan_id": 2,
            "book_id": 2,
            "user_id": 2,
            "status": 'returned',
            "start_loan_date": date(2024, 8, 1),
            "return_date": date(2022, 12, 31),
            "due_date": date(2022, 12, 31),
        }
    ]
    formatted_loans = format_loans(raw_loans)
    assert formatted_loans == expected_result


def test_format_loans_empty():
    """
     Given a list of loans empty
     When the format_loans function is called
     Then it returns an empty list

     """
    formatted_loans = format_loans([])
    assert formatted_loans == []


def test_format_loans_invalid_data():
    """
    Given a list of loans with invalid data
    When the format_loans function is called
    Then loans are formatted correctly in a list of dictionaries

    """
    raw_loans = [
        (1, 'invalid_book_id', 1, 'loaned', date(2024, 7, 30), date(2022, 12, 31))
    ]
    expected_result = [
        {
            "loan_id": 1,
            "book_id": 'invalid_book_id',
            "user_id": 1,
            "status": 'loaned',
            "start_loan_date": date(2024, 7, 30),
            "return_date": date(2022, 12, 31),
            "due_date": date(2022, 12, 31),
        }
    ]
    formatted_loans = format_loans(raw_loans)
    assert formatted_loans == expected_result


