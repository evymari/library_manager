from datetime import datetime


class GeneralValidator:
    def __init__(self, expected_types=None, allowed_fields=None, required_fields=None):
        self.expected_types = expected_types or {}
        self.allowed_fields = allowed_fields or {}
        self.required_fields = required_fields or []

    @staticmethod
    def validate_data_is_dict(data):
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary.")

    def validate_keys(self, data):
        invalid_keys = [key for key in data if key not in self.expected_types]
        if invalid_keys:
            raise KeyError(f"Unexpected keys found: {', '.join(invalid_keys)}")

    def validate_data_type(self, data):
        for key, value in data.items():
            if key in self.expected_types:
                expected_type = self.expected_types[key]
                if key == "original_publication_year" and isinstance(value, str):
                    value = self.parse_date(value)
                    data[key] = value
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Invalid type for {key}. Expected {expected_type.__name__}, got {type(value).__name__}.")
        return data

    def validate_update_fields(self, update_data):
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
                if field in data and not data[field]:
                    missing_fields.append(field)
            else:
                if field not in data or not data[field]:
                    missing_fields.append(field)
        if missing_fields:
            raise ValueError(f"Required fields missing or empty: {', '.join(missing_fields)}")

    @staticmethod
    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, '%d%m%Y').date()
        except ValueError:
            raise ValueError(f"Invalid date format for {date_str}. Expected format is DDMMYYYY.")
