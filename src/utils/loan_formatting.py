def format_loans(loans):
    return [
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
