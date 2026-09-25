import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.encryption import EncryptionManager


class TestEncryptionManager(unittest.TestCase):
    def setUp(self):
        self.enc = EncryptionManager()

    def test_hash_password(self):
        password = "SecurePass123"
        pwd_hash, salt = self.enc.hash_password(password)
        self.assertNotEqual(pwd_hash, "")
        self.assertNotEqual(salt, "")

    def test_verify_password_correct(self):
        password = "SecurePass123"
        pwd_hash, salt = self.enc.hash_password(password)
        result = self.enc.verify_password(password, pwd_hash, salt)
        self.assertTrue(result)

    def test_verify_password_incorrect(self):
        password = "SecurePass123"
        pwd_hash, salt = self.enc.hash_password(password)
        result = self.enc.verify_password("WrongPassword", pwd_hash, salt)
        self.assertFalse(result)

    def test_encrypt_decrypt_message(self):
        key, salt = self.enc.generate_key("testpassword")
        original = "Hello, World!"
        encrypted = self.enc.encrypt_message(original, key)
        self.assertNotEqual(encrypted, original)
        decrypted = self.enc.decrypt_message(encrypted, key)
        self.assertEqual(decrypted, original)

    def test_generate_user_id(self):
        uid1 = self.enc.generate_user_id("Alice")
        uid2 = self.enc.generate_user_id("Alice")
        self.assertEqual(len(uid1), 12)
        self.assertNotEqual(uid1, uid2)

    def test_simple_hash(self):
        h1 = self.enc.simple_hash("test")
        h2 = self.enc.simple_hash("test")
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 64)


if __name__ == '__main__':
    unittest.main()
