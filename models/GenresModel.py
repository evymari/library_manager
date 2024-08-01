from config.DBConnection import DBConnection

class GenresModel:
    def __init__(self):
        self.db = DBConnection()

    def get_genre_id(self, genre_name):
        try:
            query = "SELECT genre_id FROM genres WHERE genre = %s"
            params = (genre_name,)
            result = self.db.execute_query(query, params)
            if result:
                return result[0][0]
            else:
                print(f"Error: Genre '{genre_name}' not found")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
