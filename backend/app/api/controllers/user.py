from typing import List

from pydantic import UUID4
from starlite import Controller, Partial, get, post, put, patch, delete

from app.models import User, UserDB

from app import models, repositories as repos


class UserController(Controller):
    path = "/users"

    @post()
    async def create_user(self, data: UserDB) -> User:
        return User(username="test")

    @get()
    async def list_users(self) -> List[User]:
        return User(username="test")

    @put(path="/{user_id:uuid}")
    async def update_user(self, user_id: UUID4, data: Partial[UserDB]) -> User:
        return User(username="test")

    @delete(path="/{user_id:uuid}")
    async def delete_user(self, user_id: UUID4) -> User:
        return User(username="test")
