def test_notify_due_soon_success(mock_loans_controller_with_notification_service):
    """
    Scenario: Notify users with loans due soon
      Given there are loans due in 5 days
      When the notify_due_soon function is called
      Then each user with a loan due in 5 days should receive a notification email
    """
    # Given
    loans_controller, mock_loan_model, mock_notification_service = mock_loans_controller_with_notification_service

    loan_data = [
        {"user_id": 1, "book_id": 1, "due_date": "2024-08-20"},
        {"user_id": 2, "book_id": 2, "due_date": "2024-08-20"}
    ]

    mock_loan_model.get_loans_due_soon.return_value = loan_data

    # When
    loans_controller.notify_due_soon()

    # Then
    mock_loan_model.get_loans_due_soon.assert_called_with(5)
    assert mock_notification_service.send_due_soon_email.call_count == len(loan_data)
    mock_notification_service.send_due_soon_email.assert_any_call(1, 1, "2024-08-20")
    mock_notification_service.send_due_soon_email.assert_any_call(2, 2, "2024-08-20")


def test_notify_due_soon_no_loans(mock_loans_controller_with_notification_service):
    """
    Scenario: No loans due soon
      Given there are no loans due in 5 days
      When the notify_due_soon function is called
      Then no notification emails should be sent
    """
    # Given
    loans_controller, mock_loan_model, mock_notification_service = mock_loans_controller_with_notification_service

    mock_loan_model.get_loans_due_soon.return_value = []

    # When
    loans_controller.notify_due_soon()

    # Then
    mock_loan_model.get_loans_due_soon.assert_called_with(5)
    mock_notification_service.send_due_soon_email.assert_not_called()


def test_notify_due_soon_error(mock_loans_controller_with_notification_service):
    """
    Scenario: Error during notification
      Given an error occurs while fetching loans due soon
      When the notify_due_soon function is called
      Then the error should be logged and no notification emails should be sent
    """
    # Given
    loans_controller, mock_loan_model, mock_notification_service = mock_loans_controller_with_notification_service

    mock_loan_model.get_loans_due_soon.side_effect = Exception("Database error")

    # When
    loans_controller.notify_due_soon()

    # Then
    mock_loan_model.get_loans_due_soon.assert_called_with(5)
    mock_notification_service.send_due_soon_email.assert_not_called()

