from config.DBConnection import DBConnection
from models.UsersModel import UsersModel
from src.controllers.UsersController import UsersController

"""borrar todo esto cuando todo esté explicado y verificado"""


def potato():
    user_controller = UsersController()

    user_id = 1

    user_data = {
        "email": "pikachupikapika@example.com",
    }

    result = user_controller.update_user(user_id, user_data)
    print(result)


if __name__ == "__main__":
    potato()
