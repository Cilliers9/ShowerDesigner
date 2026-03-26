# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Dimension annotation data structures and constants.

Pure Python — no FreeCAD imports. The extractor (Models/DimensionExtractor.py)
populates DimensionItem instances; the MeasureCommand creates Draft dimensions
from them.
"""

from __future__ import annotations

from dataclasses import dataclass


# Offset distances from measured geometry (mm)
DIM_OFFSET_OVERALL = 150.0
DIM_OFFSET_PANEL = 80.0
DIM_OFFSET_HARDWARE = 50.0

# Category styling — (R, G, B) tuples for Draft dimension colors
DIM_COLORS = {
    "Overall": (0.0, 0.0, 0.8),   # Blue
    "Panel": (0.0, 0.0, 0.0),     # Black
    "Hardware": (0.8, 0.0, 0.0),  # Red
}


@dataclass
class DimensionItem:
    """A single 3D dimension annotation to create."""

    category: str  # "Overall", "Panel", "Hardware"
    label: str  # Human-readable label, e.g. "Width", "Panel 1 Height"
    p1: tuple[float, float, float]  # Start point (x, y, z)
    p2: tuple[float, float, float]  # End point (x, y, z)
    offset_direction: tuple[float, float, float]  # Unit vector for dimension line offset
    offset_distance: float  # Distance to offset the dimension line (mm)
