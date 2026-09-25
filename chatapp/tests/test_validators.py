import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.validators import Validator


class TestValidator(unittest.TestCase):
    def test_validate_email_valid(self):
        valid, err = Validator.validate_email("test@example.com")
        self.assertTrue(valid)
        self.assertEqual(err, "")

    def test_validate_email_invalid(self):
        valid, err = Validator.validate_email("invalid-email")
        self.assertFalse(valid)
        self.assertIn("Invalid", err)

    def test_validate_email_empty(self):
        valid, _ = Validator.validate_email("")
        self.assertFalse(valid)

    def test_validate_phone_valid(self):
        valid, err = Validator.validate_phone("+1 234 567 890")
        self.assertTrue(valid)
        self.assertEqual(err, "")

    def test_validate_phone_empty_ok(self):
        valid, _ = Validator.validate_phone("")
        self.assertTrue(valid)

    def test_validate_name_valid(self):
        valid, err = Validator.validate_name("Alice")
        self.assertTrue(valid)
        self.assertEqual(err, "")

    def test_validate_name_too_short(self):
        valid, err = Validator.validate_name("A")
        self.assertFalse(valid)
        self.assertIn("short", err)

    def test_validate_name_empty(self):
        valid, _ = Validator.validate_name("")
        self.assertFalse(valid)

    def test_validate_password_valid(self):
        valid, err = Validator.validate_password("StrongPass1")
        self.assertTrue(valid)
        self.assertEqual(err, "")

    def test_validate_password_too_short(self):
        valid, err = Validator.validate_password("Ab1")
        self.assertFalse(valid)
        self.assertIn("8 characters", err)

    def test_validate_password_no_uppercase(self):
        valid, err = Validator.validate_password("lowercase1")
        self.assertFalse(valid)
        self.assertIn("uppercase", err)

    def test_validate_password_no_number(self):
        valid, err = Validator.validate_password("NoNumberHere")
        self.assertFalse(valid)
        self.assertIn("number", err)

    def test_validate_message_valid(self):
        valid, _ = Validator.validate_message("Hello!")
        self.assertTrue(valid)

    def test_validate_message_empty(self):
        valid, _ = Validator.validate_message("")
        self.assertFalse(valid)

    def test_validate_message_with_limit(self):
        valid, _ = Validator.validate_message("x" * 100, max_length=50)
        self.assertFalse(valid)
        valid, _ = Validator.validate_message("short", max_length=50)
        self.assertTrue(valid)

    def test_sanitize_input(self):
        self.assertEqual(Validator.sanitize_input("  hello  "), "hello")
        self.assertEqual(Validator.sanitize_input(None), "")
        self.assertEqual(Validator.sanitize_input(123), "")


if __name__ == '__main__':
    unittest.main()
