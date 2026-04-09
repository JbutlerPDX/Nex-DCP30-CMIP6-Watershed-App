"""SQLAlchemy declarative base and model imports."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models here so Alembic can detect them
#from app.models.watershed import Watershed  # noqa: F401, E402
#from app.models.climate_record import ClimateRecord  # noqa: F401, E402
