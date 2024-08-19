
import pytest
from unittest.mock import Mock
from src.controllers.LoansController import LoansController
from src.services.NotificationService import NotificationService
from models.LoansModel import LoansModel


@pytest.fixture
def loans_controller(mock_loan_model, notification_service):
    loans_controller = LoansController()
    loans_controller.loan_model = mock_loan_model
    loans_controller.notification_service = notification_service
    return loans_controller


@pytest.fixture
def notification_service():
    return NotificationService()


@pytest.fixture
def mock_loan_model():
    mock_loan_model = Mock(spec=LoansModel)
    return mock_loan_model
