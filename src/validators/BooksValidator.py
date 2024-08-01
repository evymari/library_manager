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


    def validate_update_data(self, update_data):
        # return True if all fields are valid, otherwise False
        if not isinstance(update_data, dict):
            raise TypeError("update_data must be a dictionary.")

        allowed_fields = {
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

        valid_fields = {}
        invalid_fields = []

        for key, value in update_data.items():
            if key in allowed_fields:
                valid_fields[key] = value
            else:
                invalid_fields.append(key)

        if invalid_fields:
            raise ValueError(f"Invalid fields found: {', '.join(invalid_fields)}")

        # validate type of data
        for key, value in valid_fields.items():
            expected_type = self.expected_types.get(key)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(
                    f"Invalid type for {key}. Expected {expected_type.__name__}, got {type(value).__name__}.")

        return valid_fields
