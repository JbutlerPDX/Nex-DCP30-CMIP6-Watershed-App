"""Unit conversion helpers for NEX-DCP30 variables."""


def kelvin_to_celsius(k: float) -> float:
    return k - 273.15


def kelvin_to_fahrenheit(k: float) -> float:
    return (k - 273.15) * 9 / 5 + 32


def pr_to_mm_per_day(pr_kg_m2_s: float) -> float:
    """Convert precipitation from kg/m²/s to mm/day."""
    return pr_kg_m2_s * 86400
