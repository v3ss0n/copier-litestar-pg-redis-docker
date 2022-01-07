from pydantic import UUID4

import ormar
import uuid

from app.db.session import SessionLocal
from app.db.db import database, metadata
from .mixins import DateFieldsMixins


class Base(ormar.Model, DateFieldsMixins):
    class Meta:
        abstract = True
        database = database
        metadata = metadata

    id: UUID4 = ormar.UUID(primary_key=True, default=uuid.uuid4)
