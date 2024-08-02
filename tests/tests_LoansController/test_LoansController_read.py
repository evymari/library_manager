import datetime

import pytest
from src.controllers.LoansController import LoansController

loans_controller = LoansController()


def test_get_loans_by_book_id():
    """
    Given: a book id
    When: the get loans function is called
    Then: the loans for that book should be returned
    """
    filters = {"book_id": 1}
    result = loans_controller.get_loans(filters)

    assert result["status_code"] == 200
    assert len(result["data"]) > 0
    for loan in result["data"]:
        assert loan["book_id"] == 1


def test_get_loans_by_user_id():
    """
      Given: a user id
      When: the get loans function is called
      Then: the loans for that book should be returned
      """
    filters = {"user_id": 1}
    result = loans_controller.get_loans(filters)

    assert result["status_code"] == 200
    assert len(result["data"]) > 0
    for loan in result["data"]:
        assert loan["user_id"] == 1


def test_get_loans_by_loan_id():
    """
      Given: a loan id
      When: the get loans function is called
      Then: the loans for that book should be returned
      """
    filters = {"loan_id": 1}
    result = loans_controller.get_loans(filters)

    assert result["status_code"] == 200
    assert len(result["data"]) > 0
    for loan in result["data"]:
        assert loan["loan_id"] == 1


def test_get_loans_by_status():
    """
      Given: a status
      When: the get loans function is called
      Then: the loans for that book should be returned
      """
    filters = {"status": "loaned"}
    result = loans_controller.get_loans(filters)

    assert result["status_code"] == 200
    assert len(result["data"]) > 0
    for loan in result["data"]:
        assert loan["status"] == "loaned"


def test_get_loans_by_date_range():
    """
      Given: a date range
      When: the get loans function is called
      Then: the loans for that book should be returned
      """
    filters = {"start_loan_date": "2024-07-30", "due_date": "2022-12-31"}
    result = loans_controller.get_loans(filters)

    assert result["status_code"] == 200
    assert len(result["data"]) > 0


def test_get_loans_not_found():
    """
      Given: a wrong book id
      When: the get loans function is called
      Then: an error should be returned
      """
    filters = {"book_id": 999999999999999999}
    result = loans_controller.get_loans(filters)

    assert result["status_code"] == 404
    assert result["message"] == "No loans found"


def test_get_loans_no_filters():
    """
      Given: no filters
      When: the get loans function is called
      Then: an error should be returned
      """
    result = loans_controller.get_loans({"invalid": "invalid"})

    assert result["status_code"] == 400
    assert result["message"] == "Invalid filter"


def test_get_loans_invalid_value_type():
    """
      Given: a wrong book id
      When: the get loans function is called
      Then: an error should be returned
      """
    filters = {"book_id": "invalid"}
    result = loans_controller.get_loans(filters)

    assert result["status_code"] == 404
    assert result["message"] == "No loans found"


def test_get_loans_with_limit():
    """
    Given: valid filters and a limit
    When: the get loans function is called with a limit
    Then: only the limited number of loans should be returned
    """
    controller = LoansController()
    filters = {
        "status": "loaned",
        "start_loan_date": datetime.date(2024, 7, 1),
        "return_date": datetime.date(2024, 7, 31)
    }
    limit = 5
    result = controller.get_loans(filters, limit)

    assert result["status_code"] == 200
    assert len(result["data"]) <= limit
    for loan in result["data"]:
        assert loan["status"] == "loaned"
        assert filters["start_loan_date"] <= loan["start_loan_date"] <= filters["return_date"]
