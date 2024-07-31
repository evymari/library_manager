
import psycopg2
from email_validator import validate_email, EmailNotValidError

from models.UsersModel import UsersModel
import logging

"""borrar comentarios cuando todo esté explicado"""


class UsersController:
    def __init__(self):
        self.user_model = UsersModel()
        logging.basicConfig(level=logging.INFO)

    def update_user(self, user_id, user_data):
        try:
            if not self.user_model.user_exists(user_id):
                raise ValueError(
                    f"Upsss...User with ID {user_id} does not exist, you cannot update a user that does not exist")

            # Obtener los datos actuales del usuario
            current_user_data = self.user_model.get_user_by_id(user_id)
            if not current_user_data:
                raise ValueError(f"Cannot retrieve current data for user with ID {user_id}")
                #No se pueden recuperar los datos actuales del usuario con ID(comentarios para yo entender,jeje)

            # Verificar unicidad de los campos si por error se hace update de un id que no corresponde
            if not self.check_unique_fields(user_id, user_data, current_user_data):
                raise ValueError("Conflict detected with existing data. Update aborted.")

            # Actualizar solo los campos proporcionados, excluyendo 'id' para que no cambie el id
            updated_user_data = {**current_user_data, **user_data}
            if 'id' in updated_user_data:
                del updated_user_data['id']

            if self.data_validator(updated_user_data):
                result = self.user_model.update_user(user_id, updated_user_data)
                logging.info(f"Update result: {result}")

                if not result:
                    raise ValueError("Error updating user")
                else:
                    # Generar mensaje específico para los cambios realizados
                    changes = {key: user_data[key] for key in user_data}
                    changes_message = ", ".join(
                        [f'Congratulations =) "{key}": "{value}" has been updated successfully.' for key, value in
                         changes.items()])

                    return {
                        "status_code": 200,
                        "message": f"{changes_message}. In case you don't remember this is all the data we have: {result}"
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

    def check_unique_fields(self, user_id, user_data, current_user_data):
        for key, value in user_data.items():
            if key in ["dni", "email"]:  # Agrega otros campos únicos si es necesario
                if value != current_user_data[key]:  # Solo verifica si el valor es diferente del actual
                    query = f"SELECT id FROM users WHERE {key} = %s AND id != %s LIMIT 1;"
                    params = (value, user_id)
                    result = self.user_model.db.execute_query(query, params)
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
            "max_loans": int
        }
        for key, value in data.items():
            if key in expected_types:
                if not isinstance(value, expected_types[key]):
                    raise TypeError(
                        f"Invalid type for {key}. Expected {expected_types[key].__name__}, got {type(value).__name__}.")
            else:
                raise KeyError(f"Unexpected key {key} found in data.")
        # Validación adicional para el campo email
        if "email" in data:
            try:
                validate_email(data["email"], check_deliverability=False)
            except EmailNotValidError as e:
                raise ValueError(f"Invalid email format: {e}")
        return True
