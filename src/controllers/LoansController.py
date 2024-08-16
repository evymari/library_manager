from models.LoansModel import LoansModel
from models.UsersModel import UsersModel
from models.BooksModel import BooksModel
from src.utils.loan_formatting import format_loans
from src.data_validators.LoansDataValidator import LoansDataValidator
from src.logical_validators.LoansLogicalValidator import LoansLogicalValidator


class LoansController:
    def __init__(self):
        self.loan_model = LoansModel()
        self.users_model = UsersModel()
        self.books_model = BooksModel()
        self.loan_data_validator = LoansDataValidator()
        self.loan_logical_validator = LoansLogicalValidator()

    def create_loan(self, user_id, book_id, due_date):
        loan_data = {
            "book_id": book_id,
            "user_id": user_id,
            "due_date": due_date
        }
        try:
            loan_id = self.loan_model.create_loan(loan_data)
            if not loan_id:
                raise ValueError("Failed to create loan.")
            return loan_id
        except ValueError as ve:
            raise ve
        except Exception as e:
            if "Invalid input syntax" in str(e):
                raise ValueError("Invalid input syntax for loan creation")
            raise Exception("Internal server error: " + str(e))

    def lend_book(self, user_id, book_id, due_date):
        try:
            self.loan_data_validator.validate_ids(user_id, book_id)
            self.loan_data_validator.validate_due_date(due_date)

            user_data = self.verify_user_data(user_id)
            book_stock = self.verify_book_data(book_id)

            loan_id = self.create_loan(user_id, book_id, due_date)

            self.update_user_loans_count(user_id, user_data)
            self.update_book_stock(book_id)

            return {
                "status_code": 201,
                "message": "Loan created successfully",
                "data": {"loan_id": loan_id}
            }
        except ValueError as ve:
            return {"status_code": 400, "message": str(ve)}
        except Exception as e:
            return {"status_code": 500, "message": "Internal server error: " + str(e)}

    def verify_user_data(self, user_id):
        user_data = self.users_model.get_user_by_id(user_id)
        if not user_data:
            raise ValueError("User not found")
        if not self.loan_logical_validator.is_user_active(user_data):
            raise ValueError("User is not active")
        if self.loan_logical_validator.has_reached_max_loans(user_data):
            raise ValueError("User has reached maximum loans")
        return user_data

    def verify_book_data(self, book_id):
        book_stock = self.books_model.get_book_stock(book_id)
        if book_stock is None:
            raise ValueError("Book not found")
        self.loan_logical_validator.check_book_stock(book_stock)
        return book_stock

    def update_user_loans_count(self, user_id, user_data):
        result = self.users_model.update_user_loans_count(user_id, user_data["current_loans"] + 1)
        if not result:
            raise ValueError("Failed to update user loans count")
        return result

    def update_book_stock(self, book_id):
        result = self.books_model.update_stock_by_id(book_id, -1)
        if not result:
            raise ValueError("Failed to update book stock")
        return result

    def get_loans(self, filters, limit=None):
        try:
            is_valid, error_message = self.loan_data_validator.validate_filters(filters)
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

    def delete_loan(self, loan_id):
        try:
            loan_data = self.loan_model.get_loan_by_id(loan_id)
            if not loan_data:
                raise ValueError("loan not found")
            self.loan_model.delete_loan(loan_id)
            return {"status_code": 200, "message": "loan deleted successfully"}
        except ValueError as ve:
            return {"status_code": 400, "message": str(ve)}
        except Exception as e:
            return {"status_code": 500, "message": "Internal server error"}
