from models.GeneralModel import GeneralModel


class UsersModel(GeneralModel):
    def __init__(self):
        super().__init__('users')

    # CREATE
    def create_user(self, user_data):
        return self.create(user_data)

    # READ
    def get_user_by_id(self, user_id):
        filters = {"id": user_id}
        result = self.read(filters, limit=1)
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

    def find_user_by_key_excluding_id(self, user_id, value, key):
        filters = {key: value}
        query = f"SELECT id FROM {self.table_name} WHERE {key} = %s AND id != %s LIMIT 1;"
        params = (value, user_id)
        try:
            result = self.db.execute_query(query, params)
            return result
        except Exception as e:
            print(f"Error getting user {user_id}: {e}")
            return None

    def get_user_by_dni(self, dni):
        filters = {"dni": dni}
        result = self.read(filters, limit=1)
        return result[0][0] if result else None

    def get_user_email(self, email):
        filters = {"email": email}
        result = self.read(filters, limit=1)
        return result[0][0] if result else None

    # UPDATE
    def update_user(self, user_id, updates):
        filters = {"id": user_id}
        return self.update(updates, filters)

    def update_user_loans_count(self, user_id, new_loans_count):
        updates = {"current_loans": new_loans_count}
        filters = {"id": user_id}
        return self.update(updates, filters)

    def suspend_user(self, user_id):
        updates = {"status": "suspended"}
        filters = {"id": user_id}
        return self.update(updates, filters)

    # DELETE
    def delete_user(self, user_id):
        filters = {"id": user_id}
        return self.delete(filters)

    # EXTRA FUNCTIONALITY
    @staticmethod
    def has_reached_max_loans(user_data):
        return user_data["current_loans"] >= user_data["max_loans"]

    @staticmethod
    def is_user_active(user_data):
        return user_data["status"] == "active"
