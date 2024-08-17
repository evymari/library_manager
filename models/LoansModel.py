import psycopg2
from datetime import datetime
from psycopg2 import errors
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
        except errors.InvalidTextRepresentation as e:
            print(f"Invalid input syntax: {e}")
            return None
        except psycopg2.IntegrityError as e:
            print(f"Integrity error: {e}")
            return None
        except psycopg2.ProgrammingError as e:
            print(f"Programming error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def get_loans(self, filters, limit=None):
        try:
            query = "SELECT loans.* FROM loans"
            params = []
            joins = []
            conditions = []

            if "loan_id" in filters:
                conditions.append("loans.loan_id = %s")
                params.append(filters["loan_id"])

            if "book_id" in filters:
                conditions.append("loans.book_id = %s")
                params.append(filters["book_id"])

            if "user_id" in filters:
                conditions.append("loans.user_id = %s")
                params.append(filters["user_id"])

            if "start_loan_date" in filters and "return_date" in filters:
                conditions.append("loans.start_loan_date BETWEEN %s AND %s")
                params.extend([filters["start_loan_date"], filters["return_date"]])

            if "due_date" in filters:
                conditions.append("loans.due_date = %s")
                params.append(filters["due_date"])

            if "status" in filters:
                conditions.append("loans.status = %s")
                params.append(filters["status"])

            if joins:
                query += " " + " ".join(joins)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            if limit is not None:
                query += " LIMIT %s"
                params.append(limit)

            return self.db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting loans: {e}")
            return None

    def update_return_date(self, loan_id):
        try:
            query = "UPDATE loans SET return_date = NOW() WHERE loan_id = %s RETURNING loan_id"
            params = (loan_id,)
            result = self.db.execute_query(query, params)
            if result:
                return result[0][0]
            return None
        except Exception as e:
            print(f"Error updating return date: {e}")
            return None

    def update_loan_status(self, loan_id, status):
        try:
            query = "UPDATE loans SET status = %s WHERE loan_id = %s RETURNING loan_id"
            params = (status, loan_id)
            result = self.db.execute_query(query, params)
            if result:
                return result[0][0]
            return None
        except Exception as e:
            print(f"Error updating loan status: {e}")
            return None

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

    def get_loan_by_id(self, loan_id):
        try:
            query = "SELECT * FROM loans WHERE loan_id = %s"
            params = (loan_id,)
            result = self.db.execute_query(query, params)
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
        except ValueError as ve:
            print(f"ValueError encountered: {str(ve)}")
            return None
        except Exception as e:
            print(f"Error getting loan by id: {e}")
            return None

    # añadido para la verificación de delete users, que no se borre el usuario si tiene loans pendientes
    # borrar este comentario una vez visto y entendido el porque de esto.
    def get_loans_by_user_id(self, user_id):
        try:
            print(f"Querying loans for user_id: {user_id}")
            query = "SELECT * FROM loans WHERE user_id = %s"
            params = (user_id,)
            results = self.db.execute_query(query, params)
            print("verifies the results of the loans:", results)  # Verifica los resultados aquí
            return results
        except Exception as e:
            print(f"Error executing manual query: {e}")
            return None
