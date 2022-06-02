from app.models.user import User, UserModel

from .base import AbstractBaseRepository


class UserRepository(AbstractBaseRepository[User, UserModel]):
    db_model = User
    return_model = UserModel
