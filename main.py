from src.controllers.UsersController import UsersController


def main():
    user_controller = UsersController()

    user_id = 99

    response = user_controller.delete_user(user_id)

    print(response)


if __name__ == "__main__":
    main()


