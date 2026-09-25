import re


class Validator:
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PHONE_REGEX = re.compile(r'^\+?[\d\s\-()]{7,15}$')

    @staticmethod
    def validate_email(email):
        if not email or not isinstance(email, str):
            return False, "Email is required"
        email = email.strip()
        if not Validator.EMAIL_REGEX.match(email):
            return False, "Invalid email format"
        return True, ""

    @staticmethod
    def validate_phone(phone):
        if not phone:
            return True, ""
        phone = phone.strip()
        if not Validator.PHONE_REGEX.match(phone):
            return False, "Invalid phone format"
        return True, ""

    @staticmethod
    def validate_name(name):
        if not name or not isinstance(name, str):
            return False, "Name is required"
        name = name.strip()
        if len(name) < 2:
            return False, "Name too short"
        if len(name) > 50:
            return False, "Name too long"
        return True, ""

    @staticmethod
    def validate_password(password):
        if not password or not isinstance(password, str):
            return False, "Password is required"
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password needs an uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password needs a lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password needs a number"
        return True, ""

    @staticmethod
    def validate_message(text, max_length=None):
        if not text or not isinstance(text, str):
            return False, "Message cannot be empty"
        text = text.strip()
        if len(text) == 0:
            return False, "Message cannot be empty"
        if max_length and len(text) > max_length:
            return False, f"Message exceeds {max_length} characters"
        return True, ""

    @staticmethod
    def sanitize_input(text):
        if not text or not isinstance(text, str):
            return ""
        return text.strip()
