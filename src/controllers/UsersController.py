import psycopg2
from email_validator import validate_email, EmailNotValidError

from models.UsersModel import UsersModel

from models.LoansModel import LoansModel


class UsersController:
    def __init__(self):
        self.user_model = UsersModel()
        self.loans_model = LoansModel()

    def update_user(self, user_id, user_data):
        print('Inside update_user in UsersController' + str(user_data))
        try:
            current_user_data = self.user_model.get_user_by_id(user_id)
            if not current_user_data:
                raise ValueError(
                    f"User with ID {user_id} does not exist")

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
                    "message": f"User updated successfully"
                }
        except ValueError as ve:
            return {"status_code": 404, "message": str(ve)}
        except KeyError as ke:
            return {"status_code": 422, "message": f"Invalid key: {ke}"}
        except TypeError as te:
            return {"status_code": 422, "message": f"Invalid data type: {te}"}
        except psycopg2.IntegrityError as e:
            return {"status_code": 400, "message": "Integrity error updating user, possibly due to duplicate entry"}
        except Exception as e:
            return {"status_code": 500, "message": f"Error updating user: {e}"}

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

    @staticmethod
    def validate_email(email):
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email format: {e}")

    def delete_user(self, user_id):
        user = self.user_model.get_user_by_id(user_id)
        if not user:
            return {"status_code": 404, "message": f"User with ID {user_id} does not exist."}

        if user['status'] == 'inactive':
            return {
                "status_code": 403,
                "message": "Cannot delete an inactive user due to data retention policy."
            }

        if user['status'] == 'suspended':
            return {
                "status_code": 403,
                "message": "Cannot delete a suspended user due to data retention policy."
            }

        print(f"Checking active loans for user_id: {user_id}")
        loans = self.loans_model.get_loans_by_user_id(user_id)
        print("Loans found for user:", loans)

        if loans and len(loans) > 0:
            return {"status_code": 400, "message": "Cannot delete user with active loans."}

        try:
            deleted_user_id = self.user_model.delete_user(user_id)
            if not deleted_user_id:
                raise ValueError(f"User with ID {user_id} could not be deleted")
            return {"status_code": 200, "message": f"User with ID {deleted_user_id} deleted successfully"}
        except ValueError as ve:
            return {"status_code": 404, "message": str(ve)}
        except Exception as e:
            return {"status_code": 500, "message": f"Internal server error: {e}"}

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





