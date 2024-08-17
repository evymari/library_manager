from src.controllers.UsersController import UsersController


# borrar, son solo comprobaciones.
def main():
    user_controller = UsersController()

    user_data_update = {

        "max_loans": 5
    }

    update_response = user_controller.update_user(21, user_data_update)
    print("Update User Response:", update_response)

    delete_response = user_controller.delete_user(1)
    print("Delete User Response:", delete_response)

    valid_email = user_controller.validate_email("valid@example.com")
    print("Valid Email Test:", valid_email)

    try:
        invalid_email = user_controller.validate_email("invalid-email")
        print("Invalid Email Test:", invalid_email)
    except ValueError as e:
        print("Caught an error for invalid email:", str(e))


if __name__ == "__main__":
    main()
