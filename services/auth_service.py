import hashlib
from typing import Optional, List
from utils.data_manager import DataManager
from models.user import User

class AuthService:
    def __init__(self):
        self._load_users()

    def _load_users(self):
        data = DataManager.load_data("users.json")
        self.users = {user_data["user_id"]: User.from_dict(user_data) for user_data in data}

    def _save_users(self):
        data = [user.to_dict() for user in self.users.values()]
        DataManager.save_data("users.json", data)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username: str, password: str, role: str = "customer") -> bool:
        # Check if username exists
        for u in self.users.values():
            if u.username == username:
                return False
                
        user_id = f"USR{len(self.users) + 1:04d}"
        new_user = User(user_id, username, self._hash_password(password), role)
        self.users[user_id] = new_user
        self._save_users()
        self.log_activity(user_id, "Registered new account.")
        return True

    def login(self, username: str, password: str) -> Optional[User]:
        password_hash = self._hash_password(password)
        for u in self.users.values():
            if u.username == username and u.password_hash == password_hash:
                self.log_activity(u.user_id, "Logged in.")
                return u
        return None

    def update_user_data(self, user: User):
        self.users[user.user_id] = user
        self._save_users()

    def log_activity(self, user_id: str, action: str):
        import datetime
        logs = DataManager.load_data("activity_logs.json")
        if not isinstance(logs, list): logs = []
        logs.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "user_id": user_id,
            "action": action
        })
        DataManager.save_data("activity_logs.json", logs)
