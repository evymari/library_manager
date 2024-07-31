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

