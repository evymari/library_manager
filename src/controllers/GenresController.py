from models.GenresModel import GenresModel


class GenresController:
    def __init__(self):
        self.genres_model = GenresModel()

    def get_genre_id(self, genre_name):
        try:
            genre_id = self.genres_model.get_genre_id(genre_name)
            return genre_id
        except Exception as e:
            print(f"Error getting genre_id: {e}")
