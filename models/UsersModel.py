import psycopg2

from config.DBConnection import DBConnection


class UsersModel:
    def __init__(self):
        self.db = DBConnection()

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = %s LIMIT 1;"
        try:
            result = self.db.execute_query(query, (user_id,))
            return result[0][0]
        except Exception as e:
            print(f"Error retrieving user data {user_id}: {e}")
            return None

    def update_user(self, user_id, updates):

        set_clause = ", ".join(f"{key} = %s" for key in updates.keys())
        params = list(updates.values())
        params.append(user_id)
        query = f"UPDATE users SET {set_clause} WHERE id = %s RETURNING *;"

        try:
            result = self.db.execute_query(query, params)
            return result
        except psycopg2.IntegrityError as e:
            print(f"IntegrityError updating user {user_id}: {e}")
            return None
        except Exception as e:
            print(f"Error updating user {user_id}: {e}")
            return None

    def find_user_by_key_excluding_id(self, user_id, value, key):
        query = f"SELECT id FROM users WHERE {key} = %s AND id != %s LIMIT 1;"
        params = (value, user_id)
        try:
            result = self.db.execute_query(query, params)
            return result
        except Exception as e:
            print(f"Error getting user {user_id}: {e}")
            return None


    def create_user(self, data):
        query = ("INSERT INTO users (dni, name, surname, email, phone, address, status, current_loans, max_loans) "
                 "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id")
        params = (data.get("dni"),
                  data.get("name"),
                  data.get("surname"),
                  data.get("email"),
                  data.get("phone", None),
                  data.get("address", None),
                  data.get("status", "active"),
                  data.get("current_loans", 0),
                  data.get("max_loans", 5))

        try:
            result = self.db.execute_CUD_query(query, params)
            return result

        except Exception as e:
            print(f"Error creating user {e}")
            return None

    """find out if user is already registered"""

    def get_user_dni(self, dni):

        # select user dni from sql
        query = "SELECT dni FROM users WHERE dni = %s;"
        params = (dni,)

        # Check if DNI already exists in the data dictionary
        try:
            result = self.db.execute_query(query, params)
            if result:
                return result
        except Exception as e:
            return f"An error occurred while getting user: {e}"

    def get_user_email(self, email):

        query = "SELECT email FROM users WHERE email = %s;"
        params = (email,)

        try:
            result = self.db.execute_query(query, params)
            if result:
                return result
        except Exception as e:
            return f"An error occurred while getting user: {e}"


