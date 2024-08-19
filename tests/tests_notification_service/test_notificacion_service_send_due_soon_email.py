def test_send_due_soon_email_success(notification_service_with_mocks):
    """
    Scenario: Successfully send due soon email
      Given a valid user ID, book ID, and due date
      When the send_due_soon_email function is called
      Then the email should be sent with the correct subject and message
    """
    # Given
    notification_service = notification_service_with_mocks
    user_id = 1
    book_id = 1
    due_date = "2024-08-20"

    notification_service.get_user_email.return_value = "user@example.com"
    notification_service.get_book_title.return_value = "The Great Gatsby"

    subject = "Reminder: Book Due Soon"
    message = f"Dear user, the book 'The Great Gatsby' is due on {due_date}. Please return it on time."

    # When
    notification_service.send_due_soon_email(user_id, book_id, due_date)

    # Then
    notification_service.get_user_email.assert_called_with(user_id)
    notification_service.get_book_title.assert_called_with(book_id)
    notification_service.send_email.assert_called_with("user@example.com", subject, message)


def test_send_due_soon_email_user_email_error(notification_service_with_mocks):
    """
    Scenario: Error in getting user email
      Given an invalid user ID
      When the send_due_soon_email function is called
      Then the function should return None
      And no email should be sent
    """
    # Given
    notification_service = notification_service_with_mocks
    user_id = 999
    book_id = 1
    due_date = "2024-08-20"

    notification_service.get_user_email.return_value = None
    notification_service.get_book_title.return_value = "The Great Gatsby"

    # When
    result = notification_service.send_due_soon_email(user_id, book_id, due_date)

    # Then
    notification_service.get_user_email.assert_called_with(user_id)
    notification_service.get_book_title.assert_not_called()
    notification_service.send_email.assert_not_called()
    assert result is None


def test_send_due_soon_email_book_title_error(notification_service_with_mocks):
    """
    Scenario: Error in getting book title
      Given an invalid book ID
      When the send_due_soon_email function is called
      Then the function should return None
      And no email should be sent
    """
    # Given
    notification_service = notification_service_with_mocks
    user_id = 1
    book_id = 999
    due_date = "2024-08-20"

    notification_service.get_user_email.return_value = "user@example.com"
    notification_service.get_book_title.return_value = None

    # When
    result = notification_service.send_due_soon_email(user_id, book_id, due_date)

    # Then
    notification_service.get_user_email.assert_called_with(user_id)
    notification_service.get_book_title.assert_called_with(book_id)
    notification_service.send_email.assert_not_called()
    assert result is None

