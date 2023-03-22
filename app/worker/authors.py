import json

from app.domain import authors

__all__ = ["author_created"]


async def author_created(_: dict, *, data: dict) -> None:
    """Send an email when a new Author is created.

    Args:
        _: SAQ context.
        data: The created author object.

    Returns:
        The author object.
    """
    await authors.Service.send_author_created_email(json.dumps(data))
