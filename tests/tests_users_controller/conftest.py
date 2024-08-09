import pytest
from unittest.mock import Mock
from src.controllers.UsersController import UsersController
from models.UsersModel import UsersModel


@pytest.fixture
def mock_users_controller():
    mock_users_model = Mock(spec=UsersModel)
    users_controller = UsersController()
    users_controller.user_model = mock_users_model
    return users_controller, mock_users_model