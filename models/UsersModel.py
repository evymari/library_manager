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
                return {
                    "id": result[0][0],
                    "dni": result[0][1],
                    "name": result[0][2],
                    "last_name": result[0][3],
                    "email": result[0][4],
                    "phone": result[0][5],
                    "address": result[0][6],
                    "current_loans": result[0][8],
                    "status": result[0][7],
                    "max_loans": result[0][9]
                }
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

    @staticmethod
    def has_reached_max_loans(user_data):
        return user_data["current_loans"] >= user_data["max_loans"]

    @staticmethod
    def is_user_active(user_data):
        return user_data["status"] == "active"

    def suspend_user(self, user_id):
        query = "UPDATE users SET status = 'suspended' WHERE id = %s RETURNING id;"
        params = (user_id,)
        try:
            result = self.db.execute_query(query, params)
            if result:
                return result[0][0]
            return None
        except psycopg2.IntegrityError as e:
            print(f"IntegrityError suspending user {user_id}: {e}")
            return None
        except Exception as e:
            print(f"Error suspending user {user_id}: {e}")
            return None

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id = %s RETURNING id;"
        try:
            result = self.db.execute_query(query, (user_id,))
            return result[0][0] if result else None
        except psycopg2.IntegrityError as e:
            raise RuntimeError(f"IntegrityError deleting user {user_id}: {e}")
        except Exception as e:
            raise RuntimeError(f"Error deleting user {user_id}: {e}")
