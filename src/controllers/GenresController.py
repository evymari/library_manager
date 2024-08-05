from models.GenresModel import GenresModel


class GenresController:
    def __init__(self):
        self.genres_models = GenresModel()

    def get_genresId(self, genre_name):
        try:
            result = self.genres_models.get_genre_id(genre_name)
            return result

        except Exception as e:
            print(f"Error: {e}")
