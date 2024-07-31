from config.DBConnection import DBConnection
from src.controllers.BooksController import BooksController
from src.controllers.UsersController import UsersController

"""prueba Ana"""
user_data = {
        'dni': '12345678A',
        'name': 'Pika',
        'surname': 'Chu',
        'email': 'pika@example.com',
        'phone': '123456789',
        'address': '123 Pokemon St',
        'status': 'active',
        'current_loans': 0,
        'max_loans': 5
    }

controller = UsersController()
print(controller.add_user(user_data))

