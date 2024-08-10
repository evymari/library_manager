from datetime import date


class BooksValidator:
    def __init__(self):
        self.expected_types = {
            "stock": int,
            "isbn13": str,
            "author": str,
            "original_publication_year": date,
            "title": str,
            "summary": str,
            "genre_id": int,
            "availability": bool,
            "best_seller": bool
        }
        self.allowed_fields = {
            "stock": "stock = %s",
            "isbn13": "isbn13 = %s",
            "author": "author = %s",
            "original_publication_year": "original_publication_year = %s",
            "title": "title = %s",
            "summary": "summary = %s",
            "genre_id": "genre_id = %s",
            "availability": "availability = %s",
            "best_seller": "best_seller = %s",
        }

    def validate_update_data(self, update_data):
        # update-data needs to be a dictionary to contain key-value pair
        if not isinstance(update_data, dict):
            raise TypeError("update_data must be a dictionary.")

        valid_fields = self.validate_update_fields(update_data)
        self.validate_data_type(valid_fields)

        return valid_fields

    def validate_update_fields(self, update_data):
        # validate field is correct
        valid_fields = {}
        invalid_fields = []

        for key, value in update_data.items():
            if key in self.allowed_fields:
                valid_fields[key] = value
            else:
                invalid_fields.append(key)

        if invalid_fields:
            raise ValueError(f"Invalid fields found: {', '.join(invalid_fields)}")
        return valid_fields

    def validate_data_type(self, valid_fields):
        # validate type of data
        for key, value in valid_fields.items():
            expected_type = self.expected_types.get(key)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(
                    f"Invalid type for {key}. Expected {expected_type.__name__}, got {type(value).__name__}.")

        return True
# check that necessary fields must have information