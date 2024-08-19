from models.GeneralModel import GeneralModel


class GenresModel(GeneralModel):
    def __init__(self):
        super().__init__('genres')

    # CREATE
    def create_genre(self, genre_data):
        return self.create(genre_data)

    # READ
    def get_genre_id(self, genre_name):
        filters = {"genre_name": genre_name}
        result = self.read(filters, limit=1)
        return result[0][0] if result else None

    def get_genre_by_id(self, genre_id):
        filters = {"genre_id": genre_id}
        result = self.read(filters, limit=1)
        if result:
            return {
                "genre_id": result[0][0],
                "genre_name": result[0][1]
            }
        return None

    def get_all_genres(self, limit=None):
        return self.read(limit=limit)

    # UPDATE
    def update_genre(self, genre_id, update_data):
        filters = {"genre_id": genre_id}
        return self.update(update_data, filters)

    # DELETE
    def delete_genre(self, genre_id):
        filters = {"genre_id": genre_id}
        return self.delete(filters)
