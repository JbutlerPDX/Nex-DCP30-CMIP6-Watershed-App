"""Unit tests for utility functions."""

import pytest
from app.utils.units import kelvin_to_celsius, pr_to_mm_per_day


def test_kelvin_to_celsius():
    assert kelvin_to_celsius(273.15) == pytest.approx(0.0)
    assert kelvin_to_celsius(373.15) == pytest.approx(100.0)


def test_pr_to_mm_per_day():
    # 1 kg/m²/s ≈ 86400 mm/day
    assert pr_to_mm_per_day(1.0) == pytest.approx(86400.0)
    assert pr_to_mm_per_day(0.0) == pytest.approx(0.0)
