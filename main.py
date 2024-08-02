from config.DBConnection import DBConnection
from models.UsersModel import UsersModel
from src.controllers.UsersController import UsersController


user_controller = UsersController()

user_id = 1

user_data = {
    "invalid_key": "pikachuka@example.com",
}

result = user_controller.update_user(user_id, user_data)
print(result)



