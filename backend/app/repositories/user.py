from typing import Optional

from base import BaseRepository
from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserDB, UserCreate


class UserRepository(BaseRepository[User, UserDB]):
    @self.database.transaction()
    async def create(self, obj_in: UserCreate) -> Optional[User]:
        try:
            db_obj = await UserDB.objects.create(
                username=obj_in.username,
                hashed_password=get_password_hash(obj_in.password),
            )
        except:
            raise Exception  # todo
        else:
            return self.get(id=db_obj.id)

    @self.database.transaction()
    async def authenticate(self, username: str, password: str) -> Optional[User]:
        user = await UserDB.objects.get(username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
        # return await User.objects.get(
        #     id=user.id
        # )  # todo: do I need to do this or will framework try to wrap data to the return type? (do I need to clean out the password)


user = UserRepository(User, UserDB)
