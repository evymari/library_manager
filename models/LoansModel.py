from config.DBConnection import DBConnection


class LoansModel:
    def __init__(self):
        self.db = DBConnection()

    def get_loans(self, filters, limit=None):
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
