import pytest


def test_update_book_stock(mock_loans_controller_with_book_model):
    """
    Given an existing book with sufficient stock
    When update_book_stock is called
    Then the stock should be updated successfully
    """

    loans_controller, mock_book_model = mock_loans_controller_with_book_model
    mock_book_model.update_stock_by_id.return_value = True

    book_id = 1
    result = loans_controller.update_book_stock(book_id)

    mock_book_model.update_stock_by_id.assert_called_with(book_id, -1)
    assert result is True


def test_update_book_stock_failure(mock_loans_controller_with_book_model):
    """
    Given an existing book with insufficient stock
    When update_book_stock is called
    Then the stock should not be updated
    """

    loans_controller, mock_book_model = mock_loans_controller_with_book_model
    mock_book_model.update_stock_by_id.return_value = False

    book_id = 1

    with pytest.raises(ValueError) as e:
        loans_controller.update_book_stock(book_id)
        assert str(e.value) == "Failed to update book stock"

   