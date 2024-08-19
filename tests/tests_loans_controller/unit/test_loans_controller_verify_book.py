import pytest


def test_verify_book_success(mock_loans_controller_with_book_model):
    """
    Given an existing book
    And the book has stock
    When verify_book_data function is called
    Then the book stock is verified
    """
    loans_controller, mock_book_model = mock_loans_controller_with_book_model
    mock_book_model.get_book_stock.return_value = 10

    book_id = 1
    result = loans_controller.verify_book_data(book_id)

    mock_book_model.get_book_stock.assert_called_with(book_id)
    assert result == 10


def test_verify_book_no_stock(mock_loans_controller_with_book_model):
    """
    Given an existing book
    And the book has no stock
    When verify_book_data function is called
    Then a ValueError with the message "Book is out of stock" is raised
    """
    loans_controller, mock_book_model = mock_loans_controller_with_book_model
    mock_book_model.get_book_stock.return_value = 0
    mock_book_model.check_stock.side_effect = ValueError("Stock cannot be negative")

    book_id = 1
    with pytest.raises(ValueError) as e:
        loans_controller.verify_book_data(book_id)
    assert str(e.value) == "Stock cannot be negative"


def test_verify_book_not_found(mock_loans_controller_with_book_model):
    """
    Given an non-existing book
    When verify_book_data function is called
    Then a ValueError with the message "Book not found" is raised
    """

    loans_controller, mock_book_model = mock_loans_controller_with_book_model
    mock_book_model.get_book_stock.return_value = None

    book_id = 1
    with pytest.raises(ValueError) as e:
        loans_controller.verify_book_data(book_id)
    assert str(e.value) == "Book not found"
