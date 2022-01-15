from typing import List

from pydantic import UUID4
from starlite import Controller, Partial, get, post, put, patch, delete

from app.models import User

from app import repositories as repos


class UserController(Controller):
    path = "/users"

    @post()
    async def create_user(self, data: User) -> User:
        return await repos.user.create(obj_in=data)

    @get()
    async def list_users(self) -> List[User]:
        return await repos.user.get(id=7)

    @put(path="/{user_id:uuid}")
    async def update_user(self, user_id: UUID4, data: Partial[User]) -> User:
        return await User(username="test")

    @delete(path="/{user_id:uuid}")
    async def delete_user(self, user_id: UUID4) -> User:
        return await User(username="test")
