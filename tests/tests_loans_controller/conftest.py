import pytest
from unittest.mock import Mock
from models.LoansModel import LoansModel
from models.UsersModel import UsersModel
from models.BooksModel import BooksModel
from src.controllers.LoansController import LoansController


@pytest.fixture
def mock_loans_controller():
    loans_controller = LoansController()
    return loans_controller


@pytest.fixture
def mock_loans_controller_with_loan_model(mock_loans_controller):
    loans_controller = mock_loans_controller
    mock_loan_model = Mock(spec=LoansModel)
    loans_controller.loan_model = mock_loan_model
    return loans_controller, mock_loan_model


@pytest.fixture
def mock_loans_controller_with_user_model(mock_loans_controller):
    loans_controller = mock_loans_controller
    mock_user_model = Mock(spec=UsersModel)
    loans_controller.users_model = mock_user_model
    return loans_controller, mock_user_model,


@pytest.fixture
def mock_loans_controller_with_book_model(mock_loans_controller):
    loans_controller = mock_loans_controller
    mock_book_model = Mock(spec=BooksModel)
    loans_controller.books_model = mock_book_model
    return loans_controller, mock_book_model


@pytest.fixture
def mock_loans_controller_with_user_and_book_mode_and_loan_model():
    mock_loan_model = Mock(spec=LoansModel)
    mock_user_model = Mock(spec=UsersModel)
    mock_book_model = Mock(spec=BooksModel)
    loans_controller = LoansController()
    loans_controller.loan_model = mock_loan_model
    loans_controller.users_model = mock_user_model
    loans_controller.books_model = mock_book_model
    return loans_controller, mock_loan_model, mock_user_model, mock_book_model
