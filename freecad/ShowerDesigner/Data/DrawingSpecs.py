# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Drawing specification constants and helpers for TechDraw glass order drawings.

Pure Python — no FreeCAD imports.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# A4 Portrait page layout (mm)
# ---------------------------------------------------------------------------

PAGE_WIDTH = 210.0
PAGE_HEIGHT = 297.0

# Drawing area bounds (inside frame, above title block)
DRAWING_MARGIN_LEFT = 15.0
DRAWING_MARGIN_RIGHT = 10.0
DRAWING_MARGIN_TOP = 15.0
TITLE_BLOCK_HEIGHT = 55.0
DRAWING_MARGIN_BOTTOM = TITLE_BLOCK_HEIGHT + 10.0

DRAWING_AREA_WIDTH = PAGE_WIDTH - DRAWING_MARGIN_LEFT - DRAWING_MARGIN_RIGHT
DRAWING_AREA_HEIGHT = PAGE_HEIGHT - DRAWING_MARGIN_TOP - DRAWING_MARGIN_BOTTOM

# Center of drawing area (for view placement)
DRAWING_CENTER_X = DRAWING_MARGIN_LEFT + DRAWING_AREA_WIDTH / 2.0
DRAWING_CENTER_Y = DRAWING_MARGIN_TOP + DRAWING_AREA_HEIGHT / 2.0

# Dimension offset from glass outline (mm on page)
DIM_OFFSET_PAGE = 12.0

# ---------------------------------------------------------------------------
# Standard drawing scales (largest to smallest)
# ---------------------------------------------------------------------------

STANDARD_SCALES = [
    1 / 1, 1 / 2, 1 / 2.5, 1 / 5, 1 / 10,
    1 / 15, 1 / 20, 1 / 25, 1 / 50,
]

# ---------------------------------------------------------------------------
# Template file mapping: proxy class name → SVG template filename
# ---------------------------------------------------------------------------

TEMPLATE_MAP = {
    "FixedPanelAssembly": "A4_Portrait_Panel.svg",
    "HingedDoorAssembly": "A4_Portrait_Door.svg",
    "SlidingDoorAssembly": "A4_Portrait_Panel.svg",
    "BiFoldDoorAssembly": "A4_Portrait_Door.svg",
    # Fallback for unknown types
    "_default": "A4_Portrait_Blank.svg",
    # Assembly overview page
    "_assembly": "A4_Portrait_Assembly.svg",
}

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class HardwareCutout:
    """A hardware cutout or mounting point on a glass panel."""

    hw_type: str  # "Hinge", "Clamp", "Handle", "SupportBar"
    label: str  # Human-readable, e.g. "Top Hinge"
    position_x: float  # mm from left edge of glass
    position_z: float  # mm from bottom edge of glass
    cutout_width: float = 0.0  # mm (0 = no cutout, just a position marker)
    cutout_depth: float = 0.0  # mm
    corner_radius: float = 0.0  # mm


@dataclass
class PanelDrawingInfo:
    """All information needed to draw one panel's order sheet."""

    label: str  # Panel name / label
    panel_type: str  # Controller proxy class name
    width: float  # Glass width (mm)
    height: float  # Glass height (mm)
    thickness: float  # Glass thickness (mm)
    glass_type: str  # "Clear", "Frosted", etc.
    edge_finish: str  # "Bright_Polish", etc.
    tempering: str  # "Tempered", etc.
    cutouts: list[HardwareCutout] = field(default_factory=list)
    part_label: str = ""  # Parent App::Part label


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def calculateScale(panel_width: float, panel_height: float) -> float:
    """Return a standard scale that fits the panel in the drawing area.

    Leaves room for dimensions around the panel outline.
    """
    if panel_width <= 0 or panel_height <= 0:
        return 1 / 10

    # Reserve space for dimension lines (in page-mm)
    usable_width = DRAWING_AREA_WIDTH - 2 * DIM_OFFSET_PAGE - 10
    usable_height = DRAWING_AREA_HEIGHT - 2 * DIM_OFFSET_PAGE - 10

    # Required scale to fit each axis
    scale_x = usable_width / panel_width
    scale_y = usable_height / panel_height
    required = min(scale_x, scale_y)

    # Pick the largest standard scale that still fits
    for s in STANDARD_SCALES:
        if s <= required:
            return s

    return STANDARD_SCALES[-1]


def scaleLabel(scale: float) -> str:
    """Format a scale value as '1:N' string."""
    if scale <= 0:
        return "1:1"
    inv = 1.0 / scale
    # Use integer if close to whole number
    if abs(inv - round(inv)) < 0.01:
        return f"1:{int(round(inv))}"
    return f"1:{inv:.1f}"
