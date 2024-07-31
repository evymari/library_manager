from models.UsersModel import UsersModel
import logging


class UsersController:
    def __init__(self):
        self.user_model = UsersModel()
        logging.basicConfig(level=logging.INFO)

    def update_user(self, user_id, user_data):
        try:
            if self.data_validator(user_data):
                result = self.user_model.update_user(user_id, user_data)
                logging.info(f"Update result: {result}")
                if not result:
                    raise ValueError("Error updating user")
                else:
                    return {"status_code": 200, "message": "User updated successfully"}
        except ValueError as ve:
            logging.error(f"Value Error: {ve}")
            return {"status_code": 500, "message": str(ve)}
        except Exception as e:
            logging.error(f"Error: {e}")
            return {"status_code": 400, "message": "Error updating user"}

    def data_validator(self, data):
        expected_types = {
            "dni": str,
            "name": str,
            "surname": str,
            "email": str,
            "phone": str,
            "password": str,
            "address": str,
            "status": str,
            "current_loans": int,
            "max_loans": int
        }
        for key, value in data.items():
            if key in expected_types:
                if not isinstance(value, expected_types[key]):
                    raise TypeError(
                        f"Invalid type for {key}. Expected {expected_types[key].__name__}, got {type(value).__name__}.")
            else:
                raise KeyError(f"Unexpected key {key} found in data.")
        return True

    """add-user"""

    def add_user(self, data):
        if self.data_validator(data):
            try:
                result = self.user_model.create_user(data)
                return result

            except Exception as e:
                return f"Error creating user {e}"


