from src.controllers.LoansController import LoansController

loans = LoansController()

print(loans.get_loans({}))
