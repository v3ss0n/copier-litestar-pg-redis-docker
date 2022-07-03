from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
