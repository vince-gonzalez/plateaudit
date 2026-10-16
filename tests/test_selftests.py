# -*- coding: utf-8 -*-
"""The self-tests, promoted from CLI flags to the test suite.

Each module in this package carries a self-test that must pass before the module will run,
and each of those includes a POSITIVE CONTROL: a colour group known to lie off the confusion
axis is required to be reported off axis. The purpose is that a check which cannot detect the
defect it exists to catch should fail rather than pass.

Those controls previously only ran when somebody remembered to type `--self-test`. Here they
run on every commit, which is what JOSS asks for and what makes the claim checkable.
"""
import os

import pytest

from plateaudit import plate_colorimetry, svg_plate_colorimetry

SVG_DIR = os.environ.get("PLATEAUDIT_SVG_DIR")


def test_svg_colorimetry_self_test_passes(tmp_path):
    """The SVG path reproduces the known deviations of palettes we control.

    The positive control inside this one matters more than the agreement: an earlier raster
    control passed while sharing a false assumption with the method it was checking.
    """
    assert svg_plate_colorimetry.self_test(str(tmp_path)) is True


def test_image_method_agrees_with_declared_ranges(tmp_path):
    """The image method must reproduce the declared-range method on a stimulus we control.

    This agreement is the only thing that licenses using the image method on plates whose
    markup we cannot read.
    """
    ok, rows = plate_colorimetry.self_test(str(tmp_path))
    assert ok is True
    assert rows, "self_test returned no rows to compare"


def test_positive_control_is_actually_present(tmp_path):
    """Guard the guard.

    A suite that only asserts PASS cannot tell a working control from a deleted one. The
    pre-fix palette is deliberately broken and must still be measured OFF axis. If this
    stops failing-as-expected, the control has stopped controlling anything.
    """
    ok, rows = plate_colorimetry.self_test(str(tmp_path))
    assert ok is True
    broken = [r for r in rows if "pre_fix" in str(r["palette"])]
    assert broken, (
        "the known-broken pre-fix palette is missing from the self-test; "
        "without it the self-test cannot demonstrate that it can fail"
    )
    for r in broken:
        for key in ("declared_deg", "image_deg"):
            assert float(r[key]) > 25.0, (
                "the pre-fix palette measured %.1f deg on %s, which reads as ON axis. "
                "It is known to be off axis; a control that now passes it is broken."
                % (float(r[key]), key)
            )


@pytest.mark.skipif(not SVG_DIR, reason="needs the plate SVGs, which are not redistributed")
def test_raster_pipeline_recovers_declared_fills():
    """The raster pipeline must recover what the SVG's declared fills already say.

    Ground truth comes from reading the fills as text; the raster pipeline never sees them.
    Set PLATEAUDIT_SVG_DIR to run this. The plate SVGs are deliberately not redistributed
    with this package.
    """
    from plateaudit import plate_dots
    assert plate_dots.self_test(SVG_DIR) is True
