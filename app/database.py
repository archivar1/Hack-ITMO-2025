from typing import Dict, Optional
from app.models import User, Product


class Database:
    def __init__(self):
        self._users: Dict[int, User] = {}

    def get_user(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def create_user(self, user_id: int, username: Optional[str] = None) -> User:
        user = User(user_id=user_id, username=username)
        self._users[user_id] = user
        return user

    def update_user(self, user: User) -> User:
        self._users[user.user_id] = user
        return user

    def user_exists(self, user_id: int) -> bool:
        return user_id in self._users

    def set_product(self, user_id: int, product: Product) -> bool:
        if user_id in self._users:
            self._users[user_id].current_product = product
            return True
        return False

    def get_product(self, user_id: int) -> Optional[Product]:
        if user_id in self._users:
            return self._users[user_id].current_product
        return None
