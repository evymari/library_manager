from config.DBConnection import DBConnection


class UsersModel:
    def __init__(self):
        self.db = DBConnection()

    def update_user(self, user_id, updates):

        set_clause = ", ".join(f"{key} = %s" for key in updates.keys())
        params = list(updates.values())
        params.append(user_id)
        query = f"UPDATE users SET {set_clause} WHERE id = %s RETURNING *;"


        try:
            result = self.db.execute_query(query, params)
            return result[0]
        except Exception as e:
            print(f"Error updating user {user_id}: {e}")
            return None