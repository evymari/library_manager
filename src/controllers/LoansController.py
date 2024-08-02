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


