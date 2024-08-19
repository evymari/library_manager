from email_validator import EmailNotValidError, validate_email


class UsersValidator:
    def __init__(self):
        self.expected_types = {
            "dni": str,
            "name": str,
            "surname": str,
            "email": str,
            "phone": str,
            "password": str,
            "address": str,
            "status": str,
            "current_loans": int,
            "max_loans": int,
        }

    def data_validator(self, data):
        for key, value in data.items():
            if key in self.expected_types:
                if not isinstance(value, self.expected_types[key]):
                    raise TypeError(
                        f"Invalid type for {key}. Expected {self.expected_types[key].__name__}, got {type(value).__name__}.")
            else:
                raise KeyError(f"Unexpected key {key} found in data.")
        return True

    @staticmethod
    def validate_email(email):
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email format: {e}")
