from models.LoansModel import LoansModel


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
                return {"status_code": 400, "message": error_message}

            loans = self.loan_model.get_loans(filters, limit)
            if not loans:
                return {"status_code": 404, "message": "No loans found"}

            loans_data = [
                {
                    "loan_id": loan[0],
                    "book_id": loan[1],
                    "user_id": loan[2],
                    "status": loan[3],
                    "start_loan_date": loan[4],
                    "return_date": loan[5],
                    "due_date": loan[5],
                } for loan in loans
            ]

            return {"status_code": 200, "data": loans_data}
        except ValueError as ve:
            return {"status_code": 400, "message": str(ve)}
        except Exception as e:
            return {"status_code": 500, "message": "Internal server error"}

