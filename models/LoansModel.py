from config.DBConnection import DBConnection


class LoansModel:
    def __init__(self):
        self.db = DBConnection()

    def create_loan(self, loan_data):
        try:
            query = "INSERT INTO loans(book_id, user_id, due_date) VALUES(%s, %s, %s) RETURNING loan_id"
            params = (
                loan_data.get("book_id"),
                loan_data.get("user_id"),
                loan_data.get("due_date"),
            )
            result = self.db.execute_query(query, params)
            if result:
                return result[0][0]
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
