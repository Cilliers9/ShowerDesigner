# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
FreeCAD tree walker that extracts dimension annotations from assemblies.

Walks App::Part containers recursively (same pattern as CutListExtractor),
collecting DimensionItem instances for overall enclosure dimensions,
individual glass panel sizes, and hardware positions.
"""

from __future__ import annotations

import FreeCAD as App

from freecad.ShowerDesigner.Data.DimensionSpecs import (
    DIM_OFFSET_HARDWARE,
    DIM_OFFSET_OVERALL,
    DIM_OFFSET_PANEL,
    DimensionItem,
)

# Proxy class names that produce no dimension annotations
_SKIP_PROXIES = {"SwingArcChild", "GhostChild", "ChannelChild", "ClampChild"}


class DimensionExtractor:
    """Walk a ShowerDesigner object tree and extract dimension annotations."""

    def extract(self, obj) -> list[DimensionItem]:
        """Extract dimensions from any ShowerDesigner object.

        Handles:
        - App::Part containers (enclosures) — walks Group recursively
        - Part::FeaturePython with Proxy — extracts single item
        """
        items: list[DimensionItem] = []

        type_id = obj.TypeId if hasattr(obj, "TypeId") else ""

        if type_id == "App::Part":
            items.extend(self._walkPart(obj, obj.Label, App.Placement()))
        elif hasattr(obj, "Proxy") and obj.Proxy is not None:
            items.extend(
                self._extractChild(obj, obj.Label, App.Placement())
            )

        return items

    def _walkPart(
        self, part_obj, component_name: str, parent_placement: App.Placement
    ) -> list[DimensionItem]:
        """Walk an App::Part container's Group."""
        items: list[DimensionItem] = []
        group = getattr(part_obj, "Group", [])
        varset = None

        # Compose this part's world placement
        world_placement = parent_placement.multiply(part_obj.Placement)

        for child in group:
            child_type = child.TypeId if hasattr(child, "TypeId") else ""

            if child_type == "App::VarSet":
                varset = child
                continue
            if hasattr(child, "Label") and child.Label.startswith("_Controller"):
                continue

            # Nested App::Part → recurse
            if child_type == "App::Part":
                items.extend(
                    self._walkPart(child, child.Label, world_placement)
                )
                continue

            # Part::FeaturePython → extract child
            if hasattr(child, "Proxy") and child.Proxy is not None:
                items.extend(
                    self._extractChild(child, component_name, world_placement)
                )

        # Extract overall dimensions from the top-level VarSet only
        if varset is not None and parent_placement.isIdentity():
            items.extend(
                self._extractOverallDimensions(varset, world_placement)
            )

        return items

    def _extractChild(
        self, child_obj, component_name: str, parent_placement: App.Placement
    ) -> list[DimensionItem]:
        """Extract dimension annotations from a single child object."""
        proxy = child_obj.Proxy
        if proxy is None:
            return []

        proxy_name = proxy.__class__.__name__

        if proxy_name in _SKIP_PROXIES:
            return []

        if proxy_name == "GlassChild":
            return self._extractPanelDimensions(
                child_obj, component_name, parent_placement
            )
        if proxy_name in (
            "HingeChild", "MonzaWallHingeChild", "MonzaFoldHingeChild"
        ):
            return self._extractHardwarePosition(
                child_obj, component_name, parent_placement, "Hinge"
            )
        if proxy_name == "HandleChild":
            return self._extractHardwarePosition(
                child_obj, component_name, parent_placement, "Handle"
            )
        if proxy_name == "SupportBarChild":
            return self._extractHardwarePosition(
                child_obj, component_name, parent_placement, "Support Bar"
            )

        return []

    # ------------------------------------------------------------------
    # Per-type extractors
    # ------------------------------------------------------------------

    def _extractOverallDimensions(
        self, varset, world_placement: App.Placement
    ) -> list[DimensionItem]:
        """Extract enclosure Width, Height, Depth from VarSet."""
        items: list[DimensionItem] = []
        origin = world_placement.Base

        width = varset.Width.Value if hasattr(varset, "Width") else 0
        height = varset.Height.Value if hasattr(varset, "Height") else 0
        depth = varset.Depth.Value if hasattr(varset, "Depth") else 0

        ox, oy, oz = origin.x, origin.y, origin.z

        if width > 0:
            items.append(DimensionItem(
                category="Overall",
                label="Width",
                p1=(ox, oy, oz),
                p2=(ox + width, oy, oz),
                offset_direction=(0.0, -1.0, 0.0),
                offset_distance=DIM_OFFSET_OVERALL,
            ))

        if height > 0:
            items.append(DimensionItem(
                category="Overall",
                label="Height",
                p1=(ox, oy, oz),
                p2=(ox, oy, oz + height),
                offset_direction=(-1.0, 0.0, 0.0),
                offset_distance=DIM_OFFSET_OVERALL,
            ))

        if depth > 0:
            items.append(DimensionItem(
                category="Overall",
                label="Depth",
                p1=(ox, oy, oz),
                p2=(ox, oy + depth, oz),
                offset_direction=(-1.0, 0.0, 0.0),
                offset_distance=DIM_OFFSET_OVERALL,
            ))

        return items

    def _extractPanelDimensions(
        self, obj, component_name: str, parent_placement: App.Placement
    ) -> list[DimensionItem]:
        """Extract width and height dimensions from a GlassChild."""
        items: list[DimensionItem] = []

        width = obj.Width.Value if hasattr(obj, "Width") else 0
        height = obj.Height.Value if hasattr(obj, "Height") else 0

        if width <= 0 and height <= 0:
            return items

        # Compute world position of the glass panel's origin
        world_pl = parent_placement.multiply(obj.Placement)
        base = world_pl.Base
        rot = world_pl.Rotation

        # Glass panel local X axis = width direction, local Z axis = height direction
        local_x = rot.multVec(App.Vector(1, 0, 0))
        local_z = rot.multVec(App.Vector(0, 0, 1))
        # Offset direction perpendicular to the panel face (local Y)
        local_y = rot.multVec(App.Vector(0, 1, 0))

        bx, by, bz = base.x, base.y, base.z

        if width > 0:
            p1 = (bx, by, bz)
            end = base + local_x * width
            p2 = (end.x, end.y, end.z)
            off = (local_y.x, local_y.y, local_y.z)
            items.append(DimensionItem(
                category="Panel",
                label=f"{component_name} Width",
                p1=p1,
                p2=p2,
                offset_direction=off,
                offset_distance=DIM_OFFSET_PANEL,
            ))

        if height > 0:
            p1 = (bx, by, bz)
            end = base + local_z * height
            p2 = (end.x, end.y, end.z)
            off = (local_y.x, local_y.y, local_y.z)
            items.append(DimensionItem(
                category="Panel",
                label=f"{component_name} Height",
                p1=p1,
                p2=p2,
                offset_direction=off,
                offset_distance=DIM_OFFSET_PANEL,
            ))

        return items

    def _extractHardwarePosition(
        self,
        obj,
        component_name: str,
        parent_placement: App.Placement,
        hw_type: str,
    ) -> list[DimensionItem]:
        """Extract hardware height-from-floor dimension."""
        world_pl = parent_placement.multiply(obj.Placement)
        z = world_pl.Base.z
        if z <= 0:
            return []

        bx, by = world_pl.Base.x, world_pl.Base.y

        return [DimensionItem(
            category="Hardware",
            label=f"{obj.Label} Height",
            p1=(bx, by, 0.0),
            p2=(bx, by, z),
            offset_direction=(1.0, 0.0, 0.0),
            offset_distance=DIM_OFFSET_HARDWARE,
        )]
