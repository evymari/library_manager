import psycopg2
from email_validator import validate_email, EmailNotValidError

from models.UsersModel import UsersModel
import logging


class UsersController:
    def __init__(self):
        self.user_model = UsersModel()
        logging.basicConfig(level=logging.INFO)

    def update_user(self, user_id, user_data):
        try:
            current_user_data = self.user_model.get_user_by_id(user_id)
            if not current_user_data:
                raise ValueError(
                    f"Upsss...User with ID {user_id} does not exist, you cannot update a user that does not exist")

            if not self.check_unique_fields(user_id, user_data):
                raise ValueError("Conflict detected with existing data. Update aborted.")

            if not self.data_validator(user_data):
                raise ValueError('Ínvalid data')

            if "email" in user_data:
                if not self.validate_email(user_data["email"]):
                    raise ValueError('´Not valid email input')

            result = self.user_model.update_user(user_id, user_data)
            if result:
                return {
                    "status_code": 200,
                    "message": f"User update successfully"
                }
        except ValueError as ve:
            logging.error(f"Value Error: {ve}")
            return {"status_code": 404, "message": str(ve)}
        except KeyError as ke:
            logging.error(f"Key Error: {ke}")
            return {"status_code": 422, "message": f"Invalid key: {ke}"}
        except TypeError as te:
            logging.error(f"Type Error: {te}")
            return {"status_code": 422, "message": f"Invalid data type: {te}"}
        except psycopg2.IntegrityError as e:
            logging.error(f"Integrity Error: {e}")
            return {"status_code": 400, "message": "Integrity error updating user, possibly due to duplicate entry"}
        except Exception as e:
            logging.error(f"Error: {e}")
            return {"status_code": 500, "message": "Error updating user"}

    def check_unique_fields(self, user_id, user_data):
        for key, value in user_data.items():
            if key in ["dni", "email"]:
                result = self.user_model.find_user_by_key_excluding_id(user_id, value, key)
                if result and len(result) > 0:
                    return False
        return True

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
            "max_loans": int,
        }
        for key, value in data.items():
            if key in expected_types:
                if not isinstance(value, expected_types[key]):
                    raise TypeError(
                        f"Invalid type for {key}. Expected {expected_types[key].__name__}, got {type(value).__name__}.")
                return True
            else:
                raise KeyError(f"Unexpected key {key} found in data.")


    def validate_email(self, email):
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email format: {e}")

        return True

    """add-user"""

    def add_user(self, data):
        try:
            if self.data_validator(data):
                dni = data.get("dni")
                email = data.get("email")
                if self.user_model.get_user_dni(dni):
                    raise ValueError("user already exists")
                if self.user_model.get_user_email(email):
                    print(email)
                    raise ValueError("email already exists")

                result = self.user_model.create_user(data)
                if result:
                    return dict(status_code=200, message="User created successfully")
        except ValueError as e:
            return dict(status_code=400, message=f"error: {e}")
        except Exception as e:
            return dict(status_code=500, message=f"error: {e}")





