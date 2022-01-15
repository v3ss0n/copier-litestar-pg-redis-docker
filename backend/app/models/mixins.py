import datetime
from sqlalchemy import Column, DateTime


class DateFieldsMixins:
    created_date: datetime.datetime = Column(DateTime, default=datetime.datetime.now)
    updated_date: datetime.datetime = Column(DateTime, default=datetime.datetime.now)
