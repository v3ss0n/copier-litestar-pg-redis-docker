from typing import List, Optional

from pydantic import UUID4
from starlite import Controller, Partial, get, post, put, patch, delete

from app.models import User, UserRead, UserCreate

from app import repositories as repos


class UserController(Controller):
    path = "/users"

    @post()
    async def create_user(self, data: UserCreate) -> Optional[UserRead]:
        return await repos.user.create(obj_in=data)

    @get()
    async def list_users(self, offset: int = 0, limit: int = 100) -> List[UserRead]:
        return await repos.user.get_multi(offset=offset, limit=limit)

    @get()
    async def get_user(self, id: int) -> Optional[UserRead]:
        return await repos.user.get(id=id)

    @put(path="/{user_id:uuid}")
    async def update_user(
        self, user_id: UUID4, data: Partial[UserCreate]
    ) -> Optional[UserRead]:
        return await repos.user.update(id=user_id, obj_in=data)

    @delete(path="/{user_id:uuid}")
    async def delete_user(self, user_id: UUID4) -> Optional[UserRead]:
        return await repos.user.delete(id=user_id)
