import ormar

from base import Base


class User(Base):
    class Meta(ormar.ModelMeta):
        abstract = True
        tablename = "users"

    username: str = ormar.String(max_length=50, unique=True, index=True)
    is_active: bool = ormar.Boolean(default=True)


class UserDB(User):
    hashed_password: str = ormar.String(max_length=256)


class UserCreate(User):
    class Meta(ormar.ModelMeta):
        abstract = True

    password: str = ormar.String(max_length=30)
