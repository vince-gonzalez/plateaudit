# -*- coding: utf-8 -*-
"""plateaudit: measuring pseudoisochromatic colour-vision plates from the stimulus a
browser actually delivers.

The chain runs from SVG path data through colorimetry to confusion-line geometry:

    svg_dot_geometry       dot position, radius and declared fill from SVG path data
    svg_plate_colorimetry  linear sRGB to Smith & Pokorny cone excitations; confusion
                           directions constructed rather than retrieved from a table
    plate_colorimetry      the same measurement from a raster image
    plate_dots             dot recovery from pixels, used to check the SVG path
    confusion_axis         confusion-line machinery
    confusion_geometry     geometry on those lines
    figure_recovery        figure/ground recovery checks
    local_pairing          pairs figure dots with the ground dots that border them
    audit_delivered_plates the audit over a set of delivered plates
    make_figures           redraws the paper's figures, refusing to write if a value moved
    reviewer_checks        resampling uncertainty, 2,000 replicates

Every tool carries a self-test that must pass before it runs, and each self-test includes
a positive control: a colour group known to lie off the confusion axis is required to be
reported off axis, so a check that cannot detect the defect it exists to catch fails
rather than passes.

The colorimetry is Dain's procedure over Smith & Pokorny fundamentals. The contribution
is that the chain is executable and checkable, not that the colorimetry is new.
"""

__version__ = "0.1.0"

from .svg_plate_colorimetry import COPUNCTAL, angle_to_confusion, hex_to_rgb, srgb_to_xy
from .svg_dot_geometry import drop_backdrop, extract
from .local_pairing import assign_groups, local_pairs

__all__ = [
    "COPUNCTAL",
    "angle_to_confusion",
    "assign_groups",
    "drop_backdrop",
    "extract",
    "hex_to_rgb",
    "local_pairs",
    "srgb_to_xy",
    "__version__",
]
