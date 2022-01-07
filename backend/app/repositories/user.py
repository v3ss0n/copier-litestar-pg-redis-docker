from base import BaseRepository
from app.models.user import User, UserDB

class UserRepository(BaseRepository[User, UserDB]):
    pass
