from src.controllers.LoansController import LoansController
from models.LoansModel import LoansModel
from models.UsersModel import UsersModel
from models.BooksModel import BooksModel

loans_controller = LoansController()
user_model = UsersModel()
loans_model = LoansModel()
book_model = BooksModel()

print(loans_controller.return_book(16))






