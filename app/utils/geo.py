"""Geospatial helper utilities."""

from typing import Tuple
from shapely.geometry import box, shape
from shapely.wkt import loads as wkt_loads


def bbox_from_wkt(wkt: str) -> Tuple[float, float, float, float]:
    """Return (min_lon, min_lat, max_lon, max_lat) for a WKT geometry."""
    geom = wkt_loads(wkt)
    return geom.bounds


def geojson_to_wkt(geojson_geometry: dict) -> str:
    """Convert a GeoJSON geometry dict to WKT string."""
    return shape(geojson_geometry).wkt


def bbox_to_wkt(min_lon: float, min_lat: float, max_lon: float, max_lat: float) -> str:
    return box(min_lon, min_lat, max_lon, max_lat).wkt
