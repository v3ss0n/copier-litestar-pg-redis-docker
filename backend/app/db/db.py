import sqlalchemy
import databases

from app.core.config import settings

metadata = sqlalchemy.MetaData()
database = databases.Database(settings.DATABASE_URI)
