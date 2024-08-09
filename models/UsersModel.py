import psycopg2

from config.DBConnection import DBConnection


class UsersModel:
    def __init__(self):
        self.db = DBConnection()

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = %s LIMIT 1;"
        try:
            result = self.db.execute_query(query, (user_id,))
            if result:
                return result[0]
            return None
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
            print("Result from update_user in UsersModel: " + str(result))
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

    def update_user_loans_count(self, user_id, new_loans_count):
        query = "UPDATE users SET current_loans = %s WHERE id = %s RETURNING id;"
        params = (new_loans_count, user_id)
        try:
            result = self.db.execute_query(query, params)
            if result:
                return result[0][0]
            return None
        except psycopg2.IntegrityError as e:
            print(f"IntegrityError updating loans count for user {user_id}: {e}")
            return None
        except Exception as e:
            print(f"Error updating loans count for user {user_id}: {e}")
            return None

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id = %s RETURNING id;"
        try:
            result = self.db.execute_query(query, (user_id,))
            if result:
                return result[0][0]  # Devuelve el ID del usuario eliminado
            return None  # Si no se elimina ningún usuario
        except psycopg2.IntegrityError as e:
            print(f"IntegrityError deleting user {user_id}: {e}")
            return None
        except Exception as e:
            print(f"Error deleting user {user_id}: {e}")
            return None
