import hashlib
import secrets
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionManager:
    def __init__(self):
        self._salt = None

    def generate_salt(self):
        return secrets.token_bytes(16)

    def hash_password(self, password, salt=None):
        if salt is None:
            salt = self.generate_salt()
        elif isinstance(salt, str):
            salt = bytes.fromhex(salt)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key.decode(), salt.hex()

    def verify_password(self, password, stored_hash, salt_hex):
        try:
            computed_hash, _ = self.hash_password(password, salt_hex)
            return secrets.compare_digest(computed_hash, stored_hash)
        except Exception:
            return False

    def generate_key(self, password, salt=None):
        if salt is None:
            salt = self.generate_salt()
        elif isinstance(salt, str):
            salt = bytes.fromhex(salt)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    def encrypt_message(self, plaintext, key):
        try:
            f = Fernet(key)
            encrypted = f.encrypt(plaintext.encode())
            return encrypted.decode()
        except Exception:
            return plaintext

    def decrypt_message(self, ciphertext, key):
        try:
            f = Fernet(key)
            decrypted = f.decrypt(ciphertext.encode())
            return decrypted.decode()
        except Exception:
            return ciphertext

    @staticmethod
    def simple_hash(data):
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def generate_user_id(name, extra=""):
        unique = f"{name}{extra}{secrets.token_hex(8)}"
        return hashlib.md5(unique.encode()).hexdigest()[:12]
