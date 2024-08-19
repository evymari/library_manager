def test_notify_overdue_success(mock_loans_controller_with_notification_service):
    """
    Scenario: Notify users with overdue loans
      Given there are loans overdue by 3 or more days
      When the notify_overdue function is called
      Then each user with an overdue loan should receive a notification email
    """
    # Given
    loans_controller, mock_loan_model, mock_notification_service = mock_loans_controller_with_notification_service

    loan_data = [
        {"user_id": 1, "book_id": 1},
        {"user_id": 2, "book_id": 2}
    ]

    mock_loan_model.get_overdue_loans.return_value = loan_data

    # When
    loans_controller.notify_overdue()

    # Then
    mock_loan_model.get_overdue_loans.assert_called_with(3)
    assert mock_notification_service.send_overdue_email.call_count == len(loan_data)
    mock_notification_service.send_overdue_email.assert_any_call(1, 1)
    mock_notification_service.send_overdue_email.assert_any_call(2, 2)


def test_notify_overdue_no_loans(mock_loans_controller_with_notification_service):
    """
    Scenario: No overdue loans
      Given there are no loans overdue by 3 or more days
      When the notify_overdue function is called
      Then no notification emails should be sent
    """
    # Given
    loans_controller, mock_loan_model, mock_notification_service = mock_loans_controller_with_notification_service

    mock_loan_model.get_overdue_loans.return_value = []

    # When
    loans_controller.notify_overdue()

    # Then
    mock_loan_model.get_overdue_loans.assert_called_with(3)
    mock_notification_service.send_overdue_email.assert_not_called()


def test_notify_overdue_error(mock_loans_controller_with_notification_service):
    """
    Scenario: Error during notification
      Given an error occurs while fetching overdue loans
      When the notify_overdue function is called
      Then the error should be logged and no notification emails should be sent
    """
    # Given
    loans_controller, mock_loan_model, mock_notification_service = mock_loans_controller_with_notification_service

    mock_loan_model.get_overdue_loans.side_effect = Exception("Database error")

    # When
    loans_controller.notify_overdue()

    # Then
    mock_loan_model.get_overdue_loans.assert_called_with(3)
    mock_notification_service.send_overdue_email.assert_not_called()
