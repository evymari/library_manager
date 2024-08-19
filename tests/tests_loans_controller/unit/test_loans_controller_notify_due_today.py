def test_notify_due_today_success(mock_loans_controller_with_notification_service):
    """
    Scenario: Notify users with loans due today
      Given there are loans due today
      When the notify_due_today function is called
      Then each user with a loan due today should receive a notification email
    """
    # Given
    loans_controller, mock_loan_model, mock_notification_service = mock_loans_controller_with_notification_service

    loan_data = [
        {"user_id": 1, "book_id": 1, "due_date": "2024-08-15"},
        {"user_id": 2, "book_id": 2, "due_date": "2024-08-15"}
    ]

    mock_loan_model.get_loans_due_soon.return_value = loan_data

    # When
    loans_controller.notify_due_today()

    # Then
    mock_loan_model.get_loans_due_soon.assert_called_with(0)
    assert mock_notification_service.send_due_today_email.call_count == len(loan_data)
    mock_notification_service.send_due_today_email.assert_any_call(1, 1, "2024-08-15")
    mock_notification_service.send_due_today_email.assert_any_call(2, 2, "2024-08-15")


def test_notify_due_today_no_loans(mock_loans_controller_with_notification_service):
    """
    Scenario: No loans due today
      Given there are no loans due today
      When the notify_due_today function is called
      Then no notification emails should be sent
    """
    # Given
    loans_controller, mock_loan_model, mock_notification_service = mock_loans_controller_with_notification_service

    mock_loan_model.get_loans_due_soon.return_value = []

    # When
    loans_controller.notify_due_today()

    # Then
    mock_loan_model.get_loans_due_soon.assert_called_with(0)
    mock_notification_service.send_due_today_email.assert_not_called()


def test_notify_due_today_error(mock_loans_controller_with_notification_service):
    """
    Scenario: Error during notification
      Given an error occurs while fetching loans due today
      When the notify_due_today function is called
      Then the error should be logged and no notification emails should be sent
    """
    # Given
    loans_controller, mock_loan_model, mock_notification_service = mock_loans_controller_with_notification_service

    mock_loan_model.get_loans_due_soon.side_effect = Exception("Database error")

    # When
    loans_controller.notify_due_today()

    # Then
    mock_loan_model.get_loans_due_soon.assert_called_with(0)
    mock_notification_service.send_due_today_email.assert_not_called()
