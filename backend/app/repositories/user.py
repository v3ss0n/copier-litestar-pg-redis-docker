from typing import Optional

from app.core.security import get_password_hash, verify_password
from app.db.session import get_db
from app.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session

from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    # @self.database.transaction()
    async def create(self, obj_in: User) -> Optional[User]:
        try:
            # db_obj = await User.objects.create(
            #     username=obj_in.username,
            #     hashed_password=get_password_hash(obj_in.password),
            # )
            hashed_password = get_password_hash(obj_in.password)

            db_obj = User.objects.create(username=obj_in.username, hashed_password=hashed_password)
        except:
            raise Exception  # todo
        else:
            return await db_obj

    async def get_by_username(self, username: str, db: Session = get_db) -> Optional[User]:
        return await db.execute(select(User).where(User.username == username)).first()

    # @self.database.transaction()
    async def authenticate(self, username: str, password: str) -> Optional[User]:  # todo remove hashed_pass
        user = await self.get_by_username(username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None  # todo unauth
        return user


user = UserRepository(User)
