from models.users.UpdateUsersModel import UpdateUsersModel


class UpdateUsersController:
    def __init__(self):
        self.user_model = UpdateUsersModel()

    def update_user(self, user_id, user_data):
        try:
            self.user_model.update_user(user_id, user_data)
            print(f"User updated: {user_data['name']}")
            return dict(status_code=200, message="User updated successfully")
        except Exception as e:
            print(f"Error: {e}")
            return dict(status_code=500, message="Error updating user")
