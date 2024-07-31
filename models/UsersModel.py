import psycopg2

from config.DBConnection import DBConnection

"""borrar comentarios cuando todo esté explicado"""


def tuple_to_dict(user_tuple):
    columns = ["id", "dni", "name", "surname", "email", "phone", "address", "status", "current_loans", "max_loans"]
    return dict(zip(columns, user_tuple))


class UsersModel:
    def __init__(self):
        self.db = DBConnection()

    def user_exists(self, user_id):
        query = "SELECT 1 FROM users WHERE id = %s LIMIT 1;"
        try:
            result = self.db.execute_query(query, (user_id,))
            return len(result) > 0
        except Exception as e:
            print(f"Error checking user existence: {e}")
            return False

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = %s LIMIT 1;"
        try:
            result = self.db.execute_query(query, (user_id,))
            if result and len(result) > 0:
                return tuple_to_dict(result[0])  # Convertir tupla a diccionario
            else:
                return None
        except Exception as e:
            print(f"Error retrieving user data {user_id}: {e}")
            return None

    def update_user(self, user_id, updates):
        if not self.user_exists(user_id):
            print(f"User with ID {user_id} does not exist.")
            return None

        set_clause = ", ".join(f"{key} = %s" for key in updates.keys())
        params = list(updates.values())
        params.append(user_id)
        query = f"UPDATE users SET {set_clause} WHERE id = %s RETURNING *;"
        try:
            result = self.db.execute_query(query, params)
            if result and len(result) > 0:
                return tuple_to_dict(result[0])
            else:
                return None
        except psycopg2.IntegrityError as e:
            print(f"IntegrityError updating user {user_id}: {e}")
            return None
        except Exception as e:
            print(f"Error updating user {user_id}: {e}")
            return None
