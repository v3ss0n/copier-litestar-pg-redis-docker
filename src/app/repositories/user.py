from app.models.user import User, UserReadModel

from .base import AbstractBaseRepository


class UserRepository(AbstractBaseRepository[User, UserReadModel]):
    db_model = User
    return_model = UserReadModel
