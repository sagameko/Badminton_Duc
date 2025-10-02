"""
Secure storage module for encrypted credentials
"""
import json
import os
from pathlib import Path
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()


class SecureStorage:
    """Handles encrypted storage of PerfectGym credentials"""

    def __init__(self, storage_file: str = "credentials.json"):
        self.storage_file = Path(storage_file)
        encryption_key = os.getenv("ENCRYPTION_KEY")

        if not encryption_key:
            # Generate a new key if not exists
            encryption_key = Fernet.generate_key().decode()
            print(f"⚠️  No encryption key found. Generated new key: {encryption_key}")
            print("⚠️  Add this to your .env file as ENCRYPTION_KEY")

        self.cipher = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)

    def save_credentials(self, username: str, email: str, password: str) -> None:
        """Save encrypted PerfectGym credentials for a user"""
        credentials = self._load_all_credentials()

        # Encrypt the password
        encrypted_password = self.cipher.encrypt(password.encode()).decode()

        credentials[username] = {
            "email": email,
            "password": encrypted_password
        }

        with open(self.storage_file, 'w') as f:
            json.dump(credentials, f, indent=2)

    def get_credentials(self, username: str) -> dict:
        """Retrieve and decrypt PerfectGym credentials for a user"""
        credentials = self._load_all_credentials()

        if username not in credentials:
            return None

        user_creds = credentials[username]

        # Decrypt the password
        decrypted_password = self.cipher.decrypt(user_creds["password"].encode()).decode()

        return {
            "email": user_creds["email"],
            "password": decrypted_password
        }

    def has_credentials(self, username: str) -> bool:
        """Check if user has saved PerfectGym credentials"""
        credentials = self._load_all_credentials()
        return username in credentials

    def delete_credentials(self, username: str) -> None:
        """Delete PerfectGym credentials for a user"""
        credentials = self._load_all_credentials()
        if username in credentials:
            del credentials[username]
            with open(self.storage_file, 'w') as f:
                json.dump(credentials, f, indent=2)

    def _load_all_credentials(self) -> dict:
        """Load all credentials from storage"""
        if not self.storage_file.exists():
            return {}

        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
