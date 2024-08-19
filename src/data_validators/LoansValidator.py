from datetime import datetime
from src.data_validators.GeneralValidator import GeneralValidator


class LoansValidator(GeneralValidator):
    def __init__(self):
        super().__init__(
            expected_types={
                "loan_id": int,
                "book_id": int,
                "user_id": int,
                "status": str,
                "start_loan_date": datetime,
                "return_date": datetime,
                "due_date": datetime,
            }
        )

    @staticmethod
    def validate_ids(user_id, book_id):
        if not isinstance(user_id, int) or not isinstance(book_id, int):
            raise ValueError("User ID and Book ID must be integers.")

    def validate_due_date(self, due_date):
        if not self._is_valid_date(due_date):
            raise ValueError("Due date must be a valid date string.")

    @staticmethod
    def _is_valid_date(date_str):
        date_formats = ["%Y-%m-%d", "%d-%m-%Y"]
        for date_format in date_formats:
            try:
                datetime.strptime(date_str, date_format)
                return True
            except ValueError:
                continue
        return False

    @staticmethod
    def validate_filters(filters):
        valid_filters = {"loan_id", "book_id", "user_id", "status", "start_loan_date", "return_date", "due_date"}
        for key in filters.keys():
            if key not in valid_filters:
                return False, f"Invalid filter: {key}"
        return True, ""
