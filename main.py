from models.LoansModel import LoansModel
from src.controllers.LoansController import LoansController


loan_model = LoansModel()

print(loan_model.create_loan({"book_id": 'invalid_data', "user_id": 12, "due_date": "2024-12-31"}))
