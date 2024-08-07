from src.controllers.UsersController import UsersController
from models.UsersModel import UsersModel


users_controller = UsersController()
users_model = UsersModel()



"""print(users_model.update_user(1, {"email": "pika@example.com"}))"""
print(users_model.get_user_by_id(1))
print(users_controller.update_user(1, {"email": "pika@example.com"}))
