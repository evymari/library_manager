class LoansLogicalValidator:

    @staticmethod
    def check_book_stock(book_stock):
        if book_stock <= 0:
            raise ValueError("Book is out of stock")

    @staticmethod
    def is_user_active(user_data):
        return user_data["status"] == "active"

    @staticmethod
    def has_reached_max_loans(user_data):
        return user_data["current_loans"] >= user_data["max_loans"]