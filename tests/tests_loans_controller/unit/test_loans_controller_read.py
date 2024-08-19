import datetime
import pytest


def set_mock_response(mock_loan_model, response):
    mock_loan_model.get_loans.return_value = response


def assert_success_result(result, expected_length, expected_filters):
    assert result["status_code"] == 200
    assert len(result["data"]) == expected_length
    for loan in result["data"]:
        for key, value in expected_filters.items():
            assert loan[key] == value


@pytest.mark.parametrize("filters, expected_data, expected_filters", [
    ({"book_id": 1},
     [(1, 1, 1, 'loaned', datetime.date(2024, 7, 30), datetime.date(2022, 12, 31)),
      (2, 1, 1, 'loaned', datetime.date(2024, 7, 30), datetime.date(2022, 12, 31)),
      (3, 1, 1, 'loaned', datetime.date(2024, 7, 30), datetime.date(2022, 12, 31)),
      (5, 1, 1, 'loaned', datetime.date(2024, 7, 31), datetime.date(2022, 12, 31))],
     {"book_id": 1}),
    ({"user_id": 1},
     [(1, 1, 1, 'loaned', datetime.date(2024, 7, 30), datetime.date(2022, 12, 31)),
      (2, 1, 1, 'loaned', datetime.date(2024, 7, 30), datetime.date(2022, 12, 31)),
      (3, 1, 1, 'loaned', datetime.date(2024, 7, 30), datetime.date(2022, 12, 31)),
      (5, 1, 1, 'loaned', datetime.date(2024, 7, 31), datetime.date(2022, 12, 31))],
     {"user_id": 1}),
    ({"loan_id": 1},
     [(1, 1, 1, 'loaned', datetime.date(2024, 7, 30), datetime.date(2022, 12, 31))],
     {"loan_id": 1}),
    ({"status": "loaned"},
     [(1, 1, 1, 'loaned', datetime.date(2024, 7, 30), datetime.date(2022, 12, 31))],
     {"status": "loaned"}),
    ({"start_loan_date": "2024-07-30", "due_date": "2022-12-31"},
     [(1, 1, 1, 'loaned', datetime.date(2024, 7, 30), datetime.date(2022, 12, 31))],
     {}),
    ({"book_id": 1, },
     [(1, 1, 1, 'loaned', datetime.date(2024, 7, 30), datetime.date(2022, 12, 31))],
     {}),
    ({"book_id": 1, "status": "loaned"},
     [(1, 1, 1, 'loaned', datetime.date(2024, 7, 30), datetime.date(2022, 12, 31))],
     {"book_id": 1, "status": "loaned"})
])
def test_get_loans(mock_loans_controller_with_loan_model, filters, expected_data, expected_filters):
    """
    Given: I provide filters such as book_id, user_id, etc.
    When: The get_loans method is called
    Then: The response should be checked for correctness and the data should match the filters.
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model
    set_mock_response(mock_loan_model, expected_data)

    result = loans_controller.get_loans(filters, None)

    mock_loan_model.get_loans.assert_called_with(filters, None)
    assert_success_result(result, len(expected_data), expected_filters)


def test_get_loans_not_found(mock_loans_controller_with_loan_model):
    """
        Given: I provide invalid filters such as book_id = "invalid"
        When: The get_loans method is called
        Then: The response should be checked return a 400 error
        And:  The message should be "No loans found".
    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model
    set_mock_response(mock_loan_model, None)

    filters = {"book_id": "invalid"}
    result = loans_controller.get_loans(filters, None)

    mock_loan_model.get_loans.assert_called_with(filters, None)
    assert result["status_code"] == 400
    assert result["message"] == "No loans found"


def test_get_loans_no_filters(mock_loans_controller_with_loan_model):
    """
        Given: I do not provide any filters
        When: The get_loans method is called
        Then: The response should be checked return a 400 error
        And:  The message should be "Invalid filter".

    """
    loans_controller, mock_loan_model = mock_loans_controller_with_loan_model
    set_mock_response(mock_loan_model, [(1, 1, 1, 'loaned', datetime.date(2024, 7, 30), datetime.date(2022, 12, 31))])

    filters = {"invalid": "invalid"}
    result = loans_controller.get_loans(filters, None)

    assert result["status_code"] == 400
    assert result["message"] == 'Invalid filter: invalid'
