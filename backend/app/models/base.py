import databases
import sqlalchemy
import datetime

from typing import UUID4

import ormar

from app.db.session import SessionLocal
from mixins import DateFieldsMixins

metadata = sqlalchemy.MetaData()
database = SessionLocal()


class Base(ormar.Model, DateFieldsMixins):
    class Meta:
        abstract = True
        database = database
        metadata = metadata

    id: UUID4 = ormar.UUID(primary_key=True)
