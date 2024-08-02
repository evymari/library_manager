from config.DBConnection import DBConnection

class GenresModel:
    def __init__(self):
        self.db_connection = DBConnection()

    def get_genre_id(self, genre_name):
        query = "SELECT genre_id FROM genres WHERE genre_name = %s"
        params = (genre_name,)
        try:
            result = self.db_connection.execute_query(query, params)
            return  result[0][0]
        except Exception as e:
            print(f"Error: {e}")
            return None