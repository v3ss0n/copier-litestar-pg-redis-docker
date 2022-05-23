from typing import cast

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return cast(bool, pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    """
    Return hash of `password`.

    Parameters
    ----------
    password : str

    Returns
    -------
    str
    """
    return pwd_context.hash(password)  # type:ignore[no-any-return]
