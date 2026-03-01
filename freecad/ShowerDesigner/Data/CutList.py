# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Cut List / Bill of Materials data structures and formatters.

Pure Python — no FreeCAD imports. The extractor (Models/CutListExtractor.py)
populates CutListItem instances; this module handles aggregation and output.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass, field


@dataclass
class CutListItem:
    """Single line item in a cut list / bill of materials."""

    category: str  # "Glass", "Hinge", "Handle", "Clamp", "Support Bar", etc.
    component: str  # Parent context: "Fixed Panel", "Hinged Door", etc.
    description: str  # "Clear Tempered 10mm", "Bevel 90° Wall-to-Glass Hinge", etc.
    product_code: str = ""  # From catalogue specs (or "" if none)
    width: float = 0.0  # mm (glass only, 0 for hardware)
    height: float = 0.0  # mm (glass only, 0 for hardware)
    quantity: int = 1
    unit: str = "pc"  # "pc", "mm"
    notes: str = ""  # Finish, edge info, etc.


def _itemKey(item: CutListItem) -> tuple:
    """Key for grouping identical items during aggregation."""
    return (
        item.category,
        item.description,
        item.product_code,
        item.width,
        item.height,
        item.unit,
        item.notes,
    )


def aggregateItems(items: list[CutListItem]) -> list[CutListItem]:
    """Merge identical items (same category+description+product_code+dims) by summing quantities."""
    groups: dict[tuple, CutListItem] = {}
    for item in items:
        key = _itemKey(item)
        if key in groups:
            groups[key].quantity += item.quantity
            # Merge component names if different
            existing = groups[key].component
            if item.component and item.component not in existing:
                groups[key].component = f"{existing}, {item.component}"
        else:
            # Copy so we don't mutate the original
            groups[key] = CutListItem(
                category=item.category,
                component=item.component,
                description=item.description,
                product_code=item.product_code,
                width=item.width,
                height=item.height,
                quantity=item.quantity,
                unit=item.unit,
                notes=item.notes,
            )
    return list(groups.values())


_CSV_HEADERS = [
    "Category",
    "Component",
    "Description",
    "Product Code",
    "Width (mm)",
    "Height (mm)",
    "Qty",
    "Unit",
    "Notes",
]


def toCSV(items: list[CutListItem]) -> str:
    """Format items as a CSV string with header row."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(_CSV_HEADERS)
    for item in items:
        writer.writerow([
            item.category,
            item.component,
            item.description,
            item.product_code,
            f"{item.width:.0f}" if item.width else "",
            f"{item.height:.0f}" if item.height else "",
            item.quantity,
            item.unit,
            item.notes,
        ])
    return buf.getvalue()


def toTable(items: list[CutListItem]) -> list[list[str]]:
    """Format as list of rows (header + data) for Qt table display."""
    rows: list[list[str]] = [list(_CSV_HEADERS)]
    for item in items:
        rows.append([
            item.category,
            item.component,
            item.description,
            item.product_code,
            f"{item.width:.0f}" if item.width else "",
            f"{item.height:.0f}" if item.height else "",
            str(item.quantity),
            item.unit,
            item.notes,
        ])
    return rows


def toConsoleTable(items: list[CutListItem]) -> str:
    """Format as a fixed-width console table string."""
    rows = toTable(items)
    if len(rows) <= 1:
        return "  (no items)\n"

    # Calculate column widths
    col_widths = [0] * len(rows[0])
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    lines = []
    # Header
    header = "  ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(rows[0]))
    lines.append(header)
    lines.append("-" * len(header))
    # Data rows
    for row in rows[1:]:
        lines.append("  ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(row)))

    return "\n".join(lines) + "\n"
