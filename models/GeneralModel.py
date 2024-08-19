from config.DBConnection import DBConnection
from models.IModel import IModel


class GeneralModel(IModel):
    def __init__(self, table_name):
        self.db = DBConnection()
        self.table_name = table_name

    def create(self, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders}) RETURNING id;"
        params = tuple(data.values())

        try:
            result = self.db.execute_query(query, params)
            return result[0][0] if result else None
        except Exception as e:
            print(f"Error creating in {self.table_name}: {e}")
            return None

    def read(self, filters=None, limit=None):
        query = f"SELECT * FROM {self.table_name} WHERE 1=1"
        params = []

        if filters:
            for key, value in filters.items():
                query += f" AND {key} = %s"
                params.append(value)

        if limit is not None:
            query += f" LIMIT %s"
            params.append(limit)

        try:
            return self.db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error reading from {self.table_name}: {e}")
            return None

    def update(self, update_data, filters):
        update_fields = ', '.join(f"{key} = %s" for key in update_data.keys())
        params = list(update_data.values())

        query = f"UPDATE {self.table_name} SET {update_fields} WHERE 1=1"
        for key, value in filters.items():
            query += f" AND {key} = %s"
            params.append(value)

        try:
            return self.db.execute_CUD_query(query, tuple(params))
        except Exception as e:
            print(f"Error updating {self.table_name}: {e}")
            return None

    def delete(self, filters):
        query = f"DELETE FROM {self.table_name} WHERE 1=1"
        params = []

        for key, value in filters.items():
            query += f" AND {key} = %s"
            params.append(value)

        try:
            return self.db.execute_CUD_query(query, tuple(params))
        except Exception as e:
            print(f"Error deleting from {self.table_name}: {e}")
            return None
