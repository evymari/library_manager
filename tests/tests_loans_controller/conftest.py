import pytest
from unittest.mock import Mock
from src.controllers.LoansController import LoansController
from models.LoansModel import LoansModel


@pytest.fixture
def mock_loans_controller():
    mock_loan_model = Mock(spec=LoansModel)
    loans_controller = LoansController()
    loans_controller.loan_model = mock_loan_model
    return loans_controller, mock_loan_model
