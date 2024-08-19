def test_send_overdue_email_success(notification_service_with_mocks):
    """
    Scenario: Successfully send overdue email
      Given a valid user ID and book ID
      When the send_overdue_email function is called
      Then the email should be sent with the correct subject and message
    """
    # Given
    notification_service = notification_service_with_mocks
    user_id = 1
    book_id = 1

    notification_service.get_user_email.return_value = "user@example.com"
    notification_service.get_book_title.return_value = "The Great Gatsby"

    subject = "Overdue Notice: Book Not Returned"
    message = ("Dear user, the book 'The Great Gatsby' was due but has not been returned. "
               "Please return it as soon as possible.")

    # When
    notification_service.send_overdue_email(user_id, book_id)

    # Then
    notification_service.get_user_email.assert_called_with(user_id)
    notification_service.get_book_title.assert_called_with(book_id)
    notification_service.send_email.assert_called_with("user@example.com", subject, message)


def test_send_overdue_email_user_email_error(notification_service_with_mocks):
    """
    Scenario: Error in getting user email
      Given an invalid user ID
      When the send_overdue_email function is called
      Then no email should be sent
      And a ValueError should be raised
    """
    # Given
    notification_service = notification_service_with_mocks
    user_id = 999
    book_id = 1

    notification_service.get_user_email.return_value = None
    notification_service.get_book_title.return_value = "The Great Gatsby"

    # When
    result = notification_service.send_overdue_email(user_id, book_id)

    # Then
    notification_service.get_user_email.assert_called_with(user_id)
    notification_service.get_book_title.assert_not_called()
    notification_service.send_email.assert_not_called()
    assert result is None


def test_send_overdue_email_book_title_error(notification_service_with_mocks):
    """
    Scenario: Error in getting book title
      Given an invalid book ID
      When the send_overdue_email function is called
      Then no email should be sent
      And a ValueError should be raised
    """
    # Given
    notification_service = notification_service_with_mocks
    user_id = 1
    book_id = 999

    notification_service.get_user_email.return_value = "user@example.com"
    notification_service.get_book_title.return_value = None

    # When
    result = notification_service.send_overdue_email(user_id, book_id)

    # Then
    notification_service.get_user_email.assert_called_with(user_id)
    notification_service.get_book_title.assert_called_with(book_id)
    notification_service.send_email.assert_not_called()
    assert result is None
