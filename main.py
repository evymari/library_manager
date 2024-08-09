from src.controllers.LoansController import LoansController

loans_controller = LoansController()

print(loans_controller.lend_book("wrong_id", 1, "2022-01-01"))

