from typing import TYPE_CHECKING

from .authors import author_created

if TYPE_CHECKING:
    from app.lib.worker import WorkerFunction

functions: list["WorkerFunction"] = [author_created]
