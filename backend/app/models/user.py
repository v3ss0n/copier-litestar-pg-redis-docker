import ormar

from .base import Base, BaseMeta


class User(Base):
    class Meta(BaseMeta):
        abstract = True
        tablename = "users"

    username: str = ormar.String(max_length=50, unique=True, index=True)
    is_active: bool = ormar.Boolean(default=True)


class UserDB(User):
    class Meta(BaseMeta):
        tablename = "users"

    hashed_password: str = ormar.String(max_length=256)


class UserCreate(User):
    class Meta:
        abstract = True

    password: str = ormar.String(max_length=30)
