import pytest
from unittest.mock import Mock
from models.BooksModel import BooksModel
from src.controllers.BooksController import BooksController
from src.data_validators.BooksValidator import BooksValidator


# create a fixture of an instance of the BooksController()
"""@pytest.fixture
def mock_books_controller():
    books_controller = BooksController()
    return books_controller"""


@pytest.fixture
def mock_books_controller_with_model():
    books_controller = BooksController()
    mock_books_model = Mock(spec=BooksModel)
    books_controller.books_model = mock_books_model  # replaces books_model with mock
    return books_controller, mock_books_model
