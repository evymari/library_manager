from config.DBConnection import DBConnection


class UpdateUsersModel:
    def __init__(self):
        self.db = DBConnection()

    def update_user(self, user_id, user_data):
        try:
            query = """
                UPDATE users
                SET dni = %s, name = %s, surname = %s, email = %s, phone = %s, address = %s, status = %s, current_loans = %s, max_loans = %s
                WHERE id = %s
            """
            params = (
                user_data.get("dni"),
                user_data.get("name"),
                user_data.get("surname"),
                user_data.get("email"),
                user_data.get("phone"),
                user_data.get("address"),
                user_data.get("status"),
                user_data.get("current_loans"),
                user_data.get("max_loans"),
                user_id
            )
            return self.db.execute_query(query, params)
        except Exception as e:
            print(f"Error: {e}")
