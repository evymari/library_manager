from unittest.mock import Mock
import pytest


@pytest.fixture
def setup_loans_controller(mock_loans_controller_with_user_and_book_mode_and_loan_model):
    """
    Fixture to setup the LoansController and mocks.
    """
    loans_controller, mock_loan_model, mock_user_model, mock_book_model = mock_loans_controller_with_user_and_book_mode_and_loan_model

    def configure_mocks(user_data=None, book_stock=None, loan_id=1):
        # Mock the verify_user_data and verify_book_data methods
        loans_controller.verify_user_data = Mock(return_value=user_data)
        loans_controller.verify_book_data = Mock(return_value=book_stock)

        # Mock the creation of a loan and updates
        mock_loan_model.create_loan.return_value = loan_id
        loans_controller.update_user_loans_count = Mock()
        loans_controller.update_book_stock = Mock()

    return loans_controller, mock_loan_model, mock_user_model, mock_book_model, configure_mocks


def test_lend_book_success(setup_loans_controller):
    """
       Given correct data and valid states
       When lend_book function is called
       Then a loan should be created successfully
    """
    loans_controller, mock_loan_model, mock_user_model, mock_book_model, configure_mocks = setup_loans_controller

    user_id = 1
    book_id = 1
    due_date = "2022-12-31"

    user_data = {"name": "John Doe", "id": 1, "status": "active", "current_loans": 0, "max_loans": 5}
    stock = 10

    configure_mocks(user_data=user_data, book_stock=stock)

    result = loans_controller.lend_book(user_id, book_id, due_date)

    # Assert the calls to mocks
    loans_controller.verify_user_data.assert_called_with(user_id)
    loans_controller.verify_book_data.assert_called_with(book_id)
    mock_loan_model.create_loan.assert_called_with({
        "book_id": book_id,
        "user_id": user_id,
        "due_date": due_date
    })
    loans_controller.update_user_loans_count.assert_called_with(user_id, user_data, 1)
    loans_controller.update_book_stock.assert_called_with(book_id, -1)

    assert result == {
        "status_code": 201,
        "message": "Loan created successfully",
        "data": {"loan_id": 1}
    }


def test_lend_book_fail_wrong_data_type_user_id(setup_loans_controller):
    """
       Given incorrect user_id
       When lend_book function is called
       Then a status code 400 with a message "User ID and Book ID must be integers." should be returned
    """
    loans_controller, mock_loan_model, mock_user_model, mock_book_model, configure_mocks = setup_loans_controller

    user_id = "wrong_id"
    book_id = 1
    due_date = "2022-12-31"

    configure_mocks()

    result = loans_controller.lend_book(user_id, book_id, due_date)

    loans_controller.verify_user_data.assert_not_called()
    loans_controller.verify_book_data.assert_not_called()
    mock_loan_model.create_loan.assert_not_called()
    loans_controller.update_user_loans_count.assert_not_called()
    loans_controller.update_book_stock.assert_not_called()

    assert result == {"status_code": 400, "message": "User ID and Book ID must be integers."}


def test_lend_book_invalid_data_type_due_date(setup_loans_controller):
    """
       Given incorrect due_date
       When lend_book function is called
       Then a status code 400 with a message "Due date must be a valid date string." should be returned
    """
    loans_controller, mock_loan_model, mock_user_model, mock_book_model, configure_mocks = setup_loans_controller

    user_id = 1
    book_id = 1
    due_date = "wrong_date"

    configure_mocks()

    result = loans_controller.lend_book(user_id, book_id, due_date)

    loans_controller.verify_user_data.assert_not_called()
    loans_controller.verify_book_data.assert_not_called()
    mock_loan_model.create_loan.assert_not_called()
    loans_controller.update_user_loans_count.assert_not_called()
    loans_controller.update_book_stock.assert_not_called()

    assert result == {"status_code": 400, "message": "Due date must be a valid date string."}


def test_lend_book_user_does_not_exist(setup_loans_controller):
    """
       Given user that does not exist
       When lend_book function is called
       Then a status code 400 with a message "User not found" should be returned
    """
    loans_controller, mock_loan_model, mock_user_model, mock_book_model, configure_mocks = setup_loans_controller

    user_id = 1
    book_id = 1
    due_date = "2022-12-31"

    loans_controller.verify_user_data = Mock(side_effect=ValueError("User not found"))
    loans_controller.verify_book_data = Mock()

    result = loans_controller.lend_book(user_id, book_id, due_date)

    loans_controller.verify_user_data.assert_called_with(user_id)
    loans_controller.verify_book_data.assert_not_called()
    mock_loan_model.create_loan.assert_not_called()

    assert result == {"status_code": 400, "message": "User not found"}


def test_lend_book_book_does_not_exist(setup_loans_controller):
    """
       Given book that does not exist
       When lend_book function is called
       Then a status code 400 with a message "Book not found" should be returned
    """
    loans_controller, mock_loan_model, mock_user_model, mock_book_model, configure_mocks = setup_loans_controller

    user_id = 1
    book_id = 1
    due_date = "2022-12-31"

    loans_controller.verify_user_data = Mock()
    loans_controller.verify_book_data = Mock(side_effect=ValueError("Book not found"))

    result = loans_controller.lend_book(user_id, book_id, due_date)

    loans_controller.verify_user_data.assert_called_with(user_id)
    loans_controller.verify_book_data.assert_called_with(book_id)
    mock_loan_model.create_loan.assert_not_called()

    assert result == {"status_code": 400, "message": "Book not found"}


def test_lend_book_does_not_have_stock(setup_loans_controller):
    """
       Given book that does not have stock
       When lend_book function is called
       Then a status code 400 with a message "Book is out of stock" should be returned
    """
    loans_controller, mock_loan_model, mock_user_model, mock_book_model, configure_mocks = setup_loans_controller

    user_id = 1
    book_id = 1
    due_date = "2022-12-31"

    loans_controller.verify_user_data = Mock()
    loans_controller.verify_book_data = Mock(side_effect=ValueError("Book is out of stock"))
    result = loans_controller.lend_book(user_id, book_id, due_date)

    loans_controller.verify_user_data.assert_called_with(user_id)
    loans_controller.verify_book_data.assert_called_with(book_id)
    mock_loan_model.create_loan.assert_not_called()

    assert result == {"status_code": 400, "message": "Book is out of stock"}


def test_lend_book_user_not_active(setup_loans_controller):
    """
       Given user that is not active
       When lend_book function is called
       Then a status code 400 with a message "User is not active" should be returned
    """
    loans_controller, mock_loan_model, mock_user_model, mock_book_model, configure_mocks = setup_loans_controller

    user_id = 1
    book_id = 1
    due_date = "2022-12-31"

    loans_controller.verify_user_data = Mock(side_effect=ValueError("User is not active"))
    loans_controller.verify_book_data = Mock()
    result = loans_controller.lend_book(user_id, book_id, due_date)

    loans_controller.verify_user_data.assert_called_with(user_id)
    loans_controller.verify_book_data.assert_not_called()
    mock_loan_model.create_loan.assert_not_called()

    assert result == {"status_code": 400, "message": "User is not active"}


def test_lend_book_user_has_reached_max_loans(setup_loans_controller):
    """
       Given user that has reached maximum loans
       When lend_book function is called
       Then a status code 400 with a message "User has reached maximum loans" should be returned
    """
    loans_controller, mock_loan_model, mock_user_model, mock_book_model, configure_mocks = setup_loans_controller

    user_id = 1
    book_id = 1
    due_date = "2022-12-31"

    loans_controller.verify_user_data = Mock(side_effect=ValueError("User has reached maximum loans"))
    loans_controller.verify_book_data = Mock()
    result = loans_controller.lend_book(user_id, book_id, due_date)

    loans_controller.verify_user_data.assert_called_with(user_id)
    loans_controller.verify_book_data.assert_not_called()
    mock_loan_model.create_loan.assert_not_called()

    assert result == {"status_code": 400, "message": "User has reached maximum loans"}
