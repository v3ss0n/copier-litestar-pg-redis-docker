from typing import List

from pydantic import UUID4
from starlite import Controller, Partial, get, post, put, patch, delete

from app.models import User, UserDB

from app import models, repositories as repos


class UserController(Controller):
    path = "/users"

    @post()
    async def create_user(self, data: UserDB) -> User:

    @get()
    async def list_users(self) -> List[User]:
        pass

    @put(path="/{user_id:uuid}")
    async def update_user(self, user_id: UUID4, data: Partial[UserDB]) -> User:
        pass

    @delete(path="/{user_id:uuid}")
    async def delete_user(self, user_id: UUID4) -> User:
        pass
