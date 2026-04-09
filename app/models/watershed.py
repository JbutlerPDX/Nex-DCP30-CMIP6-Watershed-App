"""Watershed ORM model (HUC4 / HUC8 / HUC12 boundaries)."""

from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.base import Base


class Watershed(Base):
    __tablename__ = "watersheds"

    id = Column(Integer, primary_key=True, index=True)
    huc_code = Column(String(12), unique=True, nullable=False, index=True)
    huc_level = Column(Integer, nullable=False)  # 4, 8, or 12
    name = Column(String(255), nullable=False)
    area_sq_km = Column(Float)
    centroid_lat = Column(Float)
    centroid_lon = Column(Float)
    # Stored as WKT or use PostGIS geometry column for production
    geometry_wkt = Column(Text)

    climate_records = relationship("ClimateRecord", back_populates="watershed")
