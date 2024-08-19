from datetime import date
from src.data_validators.GeneralValidator import GeneralValidator


class BooksValidator(GeneralValidator):
    def __init__(self):
        super().__init__(
            expected_types={
                "stock": int,
                "isbn13": str,
                "author": str,
                "original_publication_year": date,
                "title": str,
                "summary": str,
                "genre_id": int,
                "availability": bool,
                "best_seller": bool
            },
            allowed_fields={
                "stock": "stock = %s",
                "isbn13": "isbn13 = %s",
                "author": "author = %s",
                "original_publication_year": "original_publication_year = %s",
                "title": "title = %s",
                "summary": "summary = %s",
                "genre_id": "genre_id = %s",
                "availability": "availability = %s",
                "best_seller": "best_seller = %s",
            },
            required_fields=["isbn13", "author", "title"]
        )

    def book_data_validator(self, book_data):
        self.validate_data_is_dict(book_data)
        self.validate_keys(book_data)
        book_data = self.validate_data_type(book_data)
        self.validate_required_fields(book_data)
        return book_data

    def validate_update_data(self, update_data):
        self.validate_data_is_dict(update_data)
        valid_fields = self.validate_update_fields(update_data)
        self.validate_data_type(valid_fields)
        self.validate_required_fields(update_data, is_update=True)
        return valid_fields

