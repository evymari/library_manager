from src.data_validators.GeneralValidator import GeneralValidator
from email_validator import validate_email, EmailNotValidError


class UsersValidator(GeneralValidator):
    def __init__(self):
        super().__init__(
            expected_types={
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
        )

    def data_validator(self, data):
        self.validate_data_is_dict(data)
        self.validate_keys(data)
        self.validate_data_type(data)
        return True

    @staticmethod
    def validate_email_address(email):
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email format: {e}")
