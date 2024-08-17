from src.controllers.UsersController import UsersController


# borrar, son solo comprobaciones.
def main():
    user_controller = UsersController()

    """user_data_update = {

        "current_loans": 0
    }

    update_response = user_controller.update_user(1, user_data_update)
    print("Update User Response:", update_response)"""

    delete_response = user_controller.delete_user(1)
    print("Delete User Response:", delete_response)


if __name__ == "__main__":
    main()
