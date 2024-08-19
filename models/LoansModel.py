from datetime import datetime
from models.GeneralModel import GeneralModel


class LoansModel(GeneralModel):
    def __init__(self):
        super().__init__('loans')

    # CREATE
    def create_loan(self, loan_data):
        return self.create(loan_data)

    # READ
    def get_loans(self, filters=None, limit=None):
        result = self.read(filters)
        if limit is not None and result:
            return result[:limit]
        return result

    def get_loan_by_id(self, loan_id):
        filters = {"loan_id": loan_id}
        result = self.read(filters)
        if result:
            return {
                "loan_id": result[0][0],
                "book_id": result[0][1],
                "user_id": result[0][2],
                "status": result[0][3],
                "start_loan_date": result[0][4],
                "due_date": result[0][5],
                "return_date": result[0][6],
            }
        return None

    def get_loans_by_user_id(self, user_id):
        filters = {"user_id": user_id}
        return self.read(filters)

    def get_loans_due_soon(self, days_before_due):
        try:
            query = """
                SELECT * FROM loans 
                WHERE due_date = CURRENT_DATE + INTERVAL %s DAY
                AND status = 'loaned';
            """
            return self.db.execute_query(query, (days_before_due,))
        except Exception as e:
            print(f"Error fetching loans due in {days_before_due} days: {e}")
            return []

    def get_overdue_loans(self, days_overdue):
        try:
            query = """
                SELECT * FROM loans 
                WHERE due_date < CURRENT_DATE - INTERVAL %s DAY
                AND status = 'loaned';
            """
            return self.db.execute_query(query, (days_overdue,))
        except Exception as e:
            print(f"Error fetching overdue loans for {days_overdue} days: {e}")
            return []

    # UPDATE
    def update_return_date(self, loan_id):
        update_data = {"return_date": datetime.now()}
        filters = {"loan_id": loan_id}
        return self.update(update_data, filters)

    def update_loan_status(self, loan_id, status):
        update_data = {"status": status}
        filters = {"loan_id": loan_id}
        return self.update(update_data, filters)

    # DELETE
    def delete_loan(self, loan_id):
        filters = {"loan_id": loan_id}
        return self.delete(filters)

    # EXTRA FUNCTIONALITY
    def is_return_late(self, loan_id):
        try:
            loan = self.get_loan_by_id(loan_id)

            if not loan:
                raise ValueError("Loan not found")

            due_date = loan["due_date"]
            return_date = loan["return_date"]
            if return_date is None:
                return_date = datetime.now()
            return return_date > due_date
        except ValueError as ve:
            print(f"ValueError encountered: {str(ve)}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
