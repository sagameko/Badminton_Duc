"""
User authentication module for the Streamlit app
"""
import json
import bcrypt
from pathlib import Path
from typing import Optional


class UserAuth:
    """Handles user authentication for the Streamlit app"""

    def __init__(self, users_file: str = "users.json"):
        self.users_file = Path(users_file)
        self._ensure_users_file()

    def _ensure_users_file(self) -> None:
        """Create users file if it doesn't exist"""
        if not self.users_file.exists():
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

    def _load_users(self) -> dict:
        """Load users from file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _save_users(self, users: dict) -> None:
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user"""
        users = self._load_users()

        if username in users:
            return False  # User already exists

        # Hash the password
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        users[username] = {
            "password_hash": password_hash
        }

        self._save_users(users)
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user"""
        users = self._load_users()

        if username not in users:
            return False

        stored_hash = users[username]["password_hash"].encode()
        return bcrypt.checkpw(password.encode(), stored_hash)

    def user_exists(self, username: str) -> bool:
        """Check if a user exists"""
        users = self._load_users()
        return username in users

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        if not self.authenticate(username, old_password):
            return False

        users = self._load_users()
        new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        users[username]["password_hash"] = new_hash
        self._save_users(users)
        return True
