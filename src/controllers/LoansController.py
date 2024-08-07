from models.LoansModel import LoansModel
from src.utils.loan_formatting import format_loans


class LoansController:
    def __init__(self):
        self.loan_model = LoansModel()

    def create_loan(self, loan_data):
        try:
            loan_id = self.loan_model.create_loan(loan_data)
            if not loan_id:
                raise ValueError("Failed to create loan due to an unknown error.")
            return {
                "status_code": 201,
                "message": "Loan created successfully",
                "data": {"loan_id": loan_id}
            }
        except ValueError as ve:
            return {"status_code": 400, "message": str(ve)}
        except Exception as e:
            return {"status_code": 500, "message": "Internal server error"}

    def validate_filters(self, filters):
        valid_filters = {"loan_id", "book_id", "user_id", "status", "start_loan_date", "return_date", "due_date"}
        for key in filters.keys():
            if key not in valid_filters:
                return False, f"Invalid filter"
        return True, ""

    def get_loans(self, filters, limit=None):
        try:
            is_valid, error_message = self.validate_filters(filters)
            if not is_valid:
                raise ValueError(error_message)

            loans = self.loan_model.get_loans(filters, limit)
            if not loans:
                raise ValueError("No loans found")

            formatted_loans = format_loans(loans)

            return {"status_code": 200, "data": formatted_loans}
        except ValueError as ve:
            return {"status_code": 400, "message": str(ve)}
        except Exception as e:
            return {"status_code": 500, "message": "Internal server error"}

