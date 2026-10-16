# -*- coding: utf-8 -*-
"""Unit tests for the public API: the colorimetry, the confusion geometry, and the
properties the paper rests on. None of these need external data.
"""
import math

import pytest

from plateaudit import COPUNCTAL, angle_to_confusion, hex_to_rgb, srgb_to_xy


# --------------------------------------------------------------------------- parsing
@pytest.mark.parametrize("text,expected", [
    ("#d7191c", (215, 25, 28)),
    ("#000000", (0, 0, 0)),
    ("#ffffff", (255, 255, 255)),
])
def test_hex_to_rgb(text, expected):
    assert hex_to_rgb(text) == expected


def test_hex_parsing_is_case_insensitive():
    assert hex_to_rgb("#D7191C") == hex_to_rgb("#d7191c")


# ----------------------------------------------------------------------- colorimetry
def test_srgb_to_xy_known_value():
    """A fixed point. If the transform drifts, this is where it shows."""
    xy = srgb_to_xy(hex_to_rgb("#d7191c"))
    x, y = float(xy[0][0]), float(xy[0][1])
    assert x == pytest.approx(0.61679449, abs=1e-6)
    assert y == pytest.approx(0.32858317, abs=1e-6)


def test_chromaticity_is_normalised():
    """x and y are a chromaticity: both in [0, 1] and x + y <= 1 for real stimuli."""
    for text in ("#d7191c", "#1a9641", "#2166ac", "#808080"):
        xy = srgb_to_xy(hex_to_rgb(text))
        x, y = float(xy[0][0]), float(xy[0][1])
        assert 0.0 <= x <= 1.0, text
        assert 0.0 <= y <= 1.0, text
        assert x + y <= 1.0 + 1e-9, text


def test_greys_sit_near_the_white_point():
    """Any neutral must land on one chromaticity regardless of lightness."""
    a = srgb_to_xy(hex_to_rgb("#404040"))
    b = srgb_to_xy(hex_to_rgb("#c0c0c0"))
    assert float(a[0][0]) == pytest.approx(float(b[0][0]), abs=1e-6)
    assert float(a[0][1]) == pytest.approx(float(b[0][1]), abs=1e-6)


# ------------------------------------------------------------- confusion-line geometry
def test_copunctal_points_present_for_all_three_deficiencies():
    assert set(COPUNCTAL) == {"protan", "deutan", "tritan"}
    for axis, (x, y) in COPUNCTAL.items():
        assert isinstance(x, float) and isinstance(y, float), axis


def test_a_direction_along_the_confusion_line_reads_as_zero():
    """THE defining property. A spread pointing straight at the copunctal point is, by
    definition, along the confusion line, so the angle to it must be ~0 degrees.

    The paper's argument is that the copunctal constants are not free parameters. This is
    the cheapest expression of that: get the constant wrong and this stops being zero.
    """
    for axis, (cx, cy) in COPUNCTAL.items():
        mean = (0.33, 0.33)
        direction = (cx - mean[0], cy - mean[1])
        assert angle_to_confusion(mean, direction, axis) == pytest.approx(0.0, abs=1e-6), axis


def test_direction_is_unsigned_and_folded_to_a_quadrant():
    """Pointing away from the copunctal point is the same line, so it must also read 0."""
    for axis, (cx, cy) in COPUNCTAL.items():
        mean = (0.33, 0.33)
        away = (mean[0] - cx, mean[1] - cy)
        assert angle_to_confusion(mean, away, axis) == pytest.approx(0.0, abs=1e-6), axis


def test_perpendicular_reads_as_ninety_degrees():
    """The other extreme, which bounds the scale at both ends."""
    for axis, (cx, cy) in COPUNCTAL.items():
        mean = (0.33, 0.33)
        dx, dy = cx - mean[0], cy - mean[1]
        assert angle_to_confusion(mean, (-dy, dx), axis) == pytest.approx(90.0, abs=1e-6), axis


def test_angle_is_always_within_zero_to_ninety():
    """Whatever is fed in, the reported angle is a folded magnitude."""
    for axis in COPUNCTAL:
        for deg in range(0, 360, 7):
            r = math.radians(deg)
            a = angle_to_confusion((0.33, 0.33), (math.cos(r), math.sin(r)), axis)
            assert 0.0 - 1e-9 <= a <= 90.0 + 1e-9, (axis, deg, a)
