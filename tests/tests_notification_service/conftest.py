import pytest
from unittest.mock import Mock
from src.services.NotificationService import NotificationService


@pytest.fixture
def notification_service_with_user_mock():
    notification_service = NotificationService()

    mock_user_model = Mock()
    notification_service.user_model = mock_user_model

    return notification_service, mock_user_model


@pytest.fixture
def notification_service_with_book_mock():
    notification_service = NotificationService()

    mock_book_model = Mock()
    notification_service.book_model = mock_book_model

    return notification_service, mock_book_model


@pytest.fixture
def notification_service_with_mocks():
    notification_service = NotificationService()

    notification_service.get_user_email = Mock()
    notification_service.get_book_title = Mock()
    notification_service.send_email = Mock()

    return notification_service