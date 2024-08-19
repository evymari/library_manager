from datetime import date, datetime


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
        self.required_fields = ["isbn13", "author", "title"]

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

    def validate_data_is_dict(self, data):
        # update-data needs to be a dictionary to contain key-value pair
        if not isinstance(data, dict):
            raise TypeError("update_data must be a dictionary.")

    def validate_keys(self, data):
        # check that keys are expected
        invalid_keys = [key for key in data if key not in self.expected_types]
        if invalid_keys:
            raise KeyError(f"Unexpected keys found: {', '.join(invalid_keys)}")

    def validate_data_type(self, data):
        # validate type of data
        for key, value in data.items():
            if key == "original_publication_year":
                value = self.parse_date(value)
                data[key] = value
            expected_type = self.expected_types.get(key)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(
                    f"Invalid type for {key}. Expected {expected_type.__name__}, got {type(value).__name__}.")
        return data

    def parse_date(self, date_str):
        try:
            parsed_date = datetime.strptime(date_str, '%d%m%Y').date()
            return parsed_date
        except ValueError:
            raise ValueError(f"Invalid date format for {date_str}. Expected format is DDMMYYYY.")

    def validate_update_fields(self, update_data):
        # check that keys to update are valid
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

    def validate_required_fields(self, data, is_update=False):
        missing_fields = []
        for field in self.required_fields:
            if is_update:
                # if required key is in the data, and value associate is empty (falsy)
                if field in data and not data[field]:
                    missing_fields.append(field)
            else:
                if field not in data or not data[field]:
                    missing_fields.append(field)
        if missing_fields:
            raise ValueError(f"Required fields missing or empty: {', '.join(missing_fields)}")
