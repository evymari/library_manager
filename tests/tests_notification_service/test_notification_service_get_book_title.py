def test_get_book_title_success(notification_service_with_book_mock):
    """
    Scenario: Successfully get book title
      Given a valid book ID
      When the get_book_title function is called
      Then the book's title should be returned
    """
    # Given
    notification_service, mock_book_model = notification_service_with_book_mock
    book_id = 1
    mock_book_model.get_book_by_id.return_value = {"id": book_id, "title": "The Great Gatsby"}

    # When
    title = notification_service.get_book_title(book_id)

    # Then
    mock_book_model.get_book_by_id.assert_called_with(book_id)
    assert title == "The Great Gatsby"


def test_get_book_title_book_not_found(notification_service_with_book_mock):
    """
    Scenario: Book not found
      Given an invalid book ID
      When the get_book_title function is called
      Then None should be returned
    """
    # Given
    notification_service, mock_book_model = notification_service_with_book_mock
    book_id = 999
    mock_book_model.get_book_by_id.return_value = None

    # When
    title = notification_service.get_book_title(book_id)

    # Then
    mock_book_model.get_book_by_id.assert_called_with(book_id)
    assert title is None


def test_get_book_title_internal_error(notification_service_with_book_mock):
    """
    Scenario: Internal error
      Given a book ID
      When an unexpected error occurs in get_book_title
      Then None should be returned
    """
    # Given
    notification_service, mock_book_model = notification_service_with_book_mock
    book_id = 1
    mock_book_model.get_book_by_id.side_effect = Exception("Database connection failed")

    # When
    title = notification_service.get_book_title(book_id)

    # Then
    mock_book_model.get_book_by_id.assert_called_with(book_id)
    assert title is None