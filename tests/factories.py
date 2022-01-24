from pydantic_factories import ModelFactory

from app.models import UserCreateDTO


class UserCreateDTOFactory(ModelFactory[UserCreateDTO]):
    __model__ = UserCreateDTO
    __allow_none_optionals__ = False
