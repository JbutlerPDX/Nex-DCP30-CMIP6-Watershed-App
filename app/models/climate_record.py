"""Aggregated climate record ORM model for watershed-level statistics."""

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class ClimateRecord(Base):
    """
    Pre-aggregated daily climate statistics per watershed.
    Populated by the ETL pipeline that reads NEX-DCP30 NetCDF files.
    """
    __tablename__ = "climate_records"

    id = Column(Integer, primary_key=True, index=True)
    watershed_id = Column(Integer, ForeignKey("watersheds.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    model = Column(String(64), nullable=False, index=True)
    scenario = Column(String(32), nullable=False, index=True)  # historical, ssp245, ssp585
    variable = Column(String(32), nullable=False, index=True)  # tasmax, tasmin, pr

    # Spatial aggregate statistics over the watershed pixels
    value_mean = Column(Float)
    value_min = Column(Float)
    value_max = Column(Float)
    value_std = Column(Float)
    pixel_count = Column(Integer)

    watershed = relationship("Watershed", back_populates="climate_records")
