import psycopg2
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

    def delete_loan(self, loan_id):
        try:
            query = "DELETE FROM loans WHERE loan_id = %s"
            params = (loan_id,)
            self.db.execute_query(query, params)

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

    def get_loan_by_id(self, loan_id):
        query = "SELECT * FROM loans WHERE loan_id = %s"
        params = (loan_id,)
        result = self.db.execute_query(query, params)
        if result:
            return result[0]
        return None
