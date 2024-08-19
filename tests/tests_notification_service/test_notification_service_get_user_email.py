def test_get_user_email_success(notification_service_with_user_mock):
    """
    Scenario: Successfully get user email
      Given a valid user ID
      When the get_user_email function is called
      Then the user's email should be returned
    """
    # Given
    notification_service, mock_user_model = notification_service_with_user_mock
    user_id = 1
    mock_user_model.get_user_by_id.return_value = {"id": user_id, "email": "user@example.com"}

    # When
    email = notification_service.get_user_email(user_id)

    # Then
    mock_user_model.get_user_by_id.assert_called_with(user_id)
    assert email == "user@example.com"


def test_get_user_email_user_not_found(notification_service_with_user_mock):
    """
    Scenario: User not found
      Given an invalid user ID
      When the get_user_email function is called
      Then None should be returned
    """
    # Given
    notification_service, mock_user_model = notification_service_with_user_mock
    user_id = 999
    mock_user_model.get_user_by_id.return_value = None

    # When
    email = notification_service.get_user_email(user_id)

    # Then
    mock_user_model.get_user_by_id.assert_called_with(user_id)
    assert email is None


def test_get_user_email_internal_error(notification_service_with_user_mock):
    """
    Scenario: Internal error
      Given a user ID
      When an unexpected error occurs in get_user_email
      Then None should be returned
    """
    # Given
    notification_service, mock_user_model = notification_service_with_user_mock
    user_id = 1
    mock_user_model.get_user_by_id.side_effect = Exception("Database connection failed")

    # When
    email = notification_service.get_user_email(user_id)

    # Then
    mock_user_model.get_user_by_id.assert_called_with(user_id)
    assert email is None