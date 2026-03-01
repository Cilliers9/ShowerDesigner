# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
FreeCAD tree walker that extracts Cut List / BOM items from assemblies.

Walks App::Part containers recursively, inspecting each child's Proxy
class to determine the hardware type and look up catalogue specs.
"""

from __future__ import annotations

import FreeCAD as App

from freecad.ShowerDesigner.Data.CutList import CutListItem
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    BEVEL_HINGE_SPECS,
    CATALOGUE_HANDLE_SPECS,
    CHANNEL_SPECS,
    CLAMP_SPECS,
    FLOOR_GUIDE_SPECS,
    HINGE_SPECS,
    MONZA_BIFOLD_HINGE_SPECS,
    SLIDER_SYSTEM_SPECS,
    SUPPORT_BAR_SPECS,
)

# Proxy class names that are visualization-only (no BOM entry)
_SKIP_PROXIES = {"SwingArcChild", "GhostChild"}


class CutListExtractor:
    """Walk a ShowerDesigner object tree and extract BOM items."""

    def extract(self, obj) -> list[CutListItem]:
        """Extract from any ShowerDesigner object (enclosure, door, or panel).

        Handles:
        - App::Part containers (assemblies) — walks Group recursively
        - Part::FeaturePython with Proxy — extracts single item
        """
        items: list[CutListItem] = []

        type_id = obj.TypeId if hasattr(obj, "TypeId") else ""

        if type_id == "App::Part":
            component_name = obj.Label
            items.extend(self._walkPart(obj, component_name))
        elif hasattr(obj, "Proxy") and obj.Proxy is not None:
            item = self._extractChild(obj, obj.Label)
            if item is not None:
                items.append(item)

        return items

    def _walkPart(self, part_obj, component_name: str) -> list[CutListItem]:
        """Walk an App::Part container's Group."""
        items: list[CutListItem] = []
        group = getattr(part_obj, "Group", [])

        for child in group:
            child_type = child.TypeId if hasattr(child, "TypeId") else ""

            # Skip VarSets and controller objects
            if child_type == "App::VarSet":
                continue
            if hasattr(child, "Label") and child.Label.startswith("_Controller"):
                continue

            # Nested App::Part → recurse (e.g. FixedPanel inside CornerEnclosure)
            if child_type == "App::Part":
                items.extend(self._walkPart(child, child.Label))
                continue

            # Part::FeaturePython → extract child
            if hasattr(child, "Proxy") and child.Proxy is not None:
                item = self._extractChild(child, component_name)
                if item is not None:
                    items.append(item)

        return items

    def _extractChild(self, child_obj, component_name: str) -> CutListItem | None:
        """Extract a BOM item from a single child object by its proxy class name."""
        proxy = child_obj.Proxy
        if proxy is None:
            return None

        proxy_name = proxy.__class__.__name__

        if proxy_name in _SKIP_PROXIES:
            return None

        if proxy_name == "GlassChild":
            return self._extractGlass(child_obj, component_name)
        if proxy_name == "HingeChild":
            return self._extractHinge(child_obj, component_name)
        if proxy_name == "HandleChild":
            return self._extractHandle(child_obj, component_name)
        if proxy_name == "ClampChild":
            return self._extractClamp(child_obj, component_name)
        if proxy_name == "SupportBarChild":
            return self._extractSupportBar(child_obj, component_name)
        if proxy_name == "ChannelChild":
            return self._extractChannel(child_obj, component_name)
        if proxy_name == "SliderTrackChild":
            return self._extractSliderTrack(child_obj, component_name)
        if proxy_name == "SliderRollerChild":
            # Roller is part of the slider system — covered by track components
            return None
        if proxy_name == "SliderFloorGuideChild":
            return self._extractFloorGuide(child_obj, component_name)
        if proxy_name == "MonzaWallHingeChild":
            return self._extractMonzaHinge(
                child_obj, component_name, "monza_90_wall_to_glass"
            )
        if proxy_name == "MonzaFoldHingeChild":
            return self._extractMonzaHinge(
                child_obj, component_name, "monza_180_glass_to_glass"
            )
        if proxy_name == "AntiLiftPinChild":
            return self._extractAntiLiftPin(child_obj, component_name)

        # Unknown proxy — skip silently
        return None

    # ------------------------------------------------------------------
    # Per-type extractors
    # ------------------------------------------------------------------

    def _extractGlass(self, obj, component_name: str) -> CutListItem:
        width = obj.Width.Value
        height = obj.Height.Value
        thickness = obj.Thickness.Value
        glass_type = obj.GlassType if hasattr(obj, "GlassType") else "Clear"

        description = f"{glass_type} {thickness:.0f}mm"
        return CutListItem(
            category="Glass",
            component=component_name,
            description=description,
            width=width,
            height=height,
            quantity=1,
            unit="pc",
        )

    def _extractHinge(self, obj, component_name: str) -> CutListItem:
        hinge_type = obj.HingeType

        # Bevel hinge
        if hinge_type in BEVEL_HINGE_SPECS:
            spec = BEVEL_HINGE_SPECS[hinge_type]
            codes = spec.get("product_codes", [])
            code = codes[0]["code"] if codes else ""
            finish = codes[0].get("finish", "") if codes else ""
            return CutListItem(
                category="Hinge",
                component=component_name,
                description=spec["name"],
                product_code=code,
                quantity=1,
                unit="pc",
                notes=finish,
            )

        # Legacy hinge
        if hinge_type in HINGE_SPECS:
            spec = HINGE_SPECS[hinge_type]
            mounting = spec.get("mounting_type", "")
            description = f"{hinge_type.replace('_', ' ').title()} ({mounting})"
            return CutListItem(
                category="Hinge",
                component=component_name,
                description=description,
                quantity=1,
                unit="pc",
            )

        return CutListItem(
            category="Hinge",
            component=component_name,
            description=hinge_type,
            quantity=1,
            unit="pc",
        )

    def _extractHandle(self, obj, component_name: str) -> CutListItem:
        handle_type = obj.HandleType

        if handle_type in CATALOGUE_HANDLE_SPECS:
            spec = CATALOGUE_HANDLE_SPECS[handle_type]
            codes = spec.get("product_codes", [])
            code = codes[0]["code"] if codes else ""
            finish = codes[0].get("finish", "") if codes else ""
            return CutListItem(
                category="Handle",
                component=component_name,
                description=spec["name"],
                product_code=code,
                quantity=1,
                unit="pc",
                notes=finish,
            )

        return CutListItem(
            category="Handle",
            component=component_name,
            description=handle_type.replace("_", " ").title(),
            quantity=1,
            unit="pc",
        )

    def _extractClamp(self, obj, component_name: str) -> CutListItem:
        clamp_type = obj.ClampType

        if clamp_type in CLAMP_SPECS:
            spec = CLAMP_SPECS[clamp_type]
            codes = spec.get("product_codes", [])
            code = codes[0]["code"] if codes else ""
            finish = codes[0].get("finish", "") if codes else ""
            mounting = spec.get("default_mounting", "")
            description = f"{clamp_type.replace('_', ' ')} ({mounting})"
            return CutListItem(
                category="Clamp",
                component=component_name,
                description=description,
                product_code=code,
                quantity=1,
                unit="pc",
                notes=finish,
            )

        return CutListItem(
            category="Clamp",
            component=component_name,
            description=clamp_type,
            quantity=1,
            unit="pc",
        )

    def _extractSupportBar(self, obj, component_name: str) -> CutListItem:
        bar_type = obj.BarType
        length = obj.Length.Value

        description = f"{bar_type} Support Bar"
        return CutListItem(
            category="Support Bar",
            component=component_name,
            description=description,
            width=length,
            quantity=1,
            unit="pc",
            notes=f"{length:.0f}mm cut length",
        )

    def _extractChannel(self, obj, component_name: str) -> CutListItem:
        location = obj.ChannelLocation
        length = obj.ChannelLength.Value

        spec = CHANNEL_SPECS.get(location, CHANNEL_SPECS["wall"])
        description = f"{location.title()} Channel ({spec['width']}x{spec['depth']}mm)"
        return CutListItem(
            category="Channel",
            component=component_name,
            description=description,
            width=length,
            quantity=1,
            unit="pc",
            notes=f"{length:.0f}mm cut length",
        )

    def _extractSliderTrack(self, obj, component_name: str) -> CutListItem:
        system_key = obj.SliderSystem
        spec = SLIDER_SYSTEM_SPECS.get(system_key)
        if spec is None:
            return CutListItem(
                category="Slider",
                component=component_name,
                description=system_key,
                quantity=1,
                unit="pc",
            )

        name = spec["name"]
        codes = spec.get("product_codes", [])
        code = codes[0]["code"] if codes else ""

        track_length = obj.TrackLength.Value
        return CutListItem(
            category="Slider",
            component=component_name,
            description=f"{name} Track",
            product_code=code,
            width=track_length,
            quantity=1,
            unit="pc",
            notes=f"{track_length:.0f}mm cut length",
        )

    def _extractFloorGuide(self, obj, component_name: str) -> CutListItem:
        return CutListItem(
            category="Slider",
            component=component_name,
            description="Floor Guide",
            product_code=FLOOR_GUIDE_SPECS["code"],
            quantity=1,
            unit="pc",
        )

    def _extractMonzaHinge(
        self, obj, component_name: str, spec_key: str
    ) -> CutListItem:
        spec = MONZA_BIFOLD_HINGE_SPECS.get(spec_key, {})
        name = spec.get("name", spec_key.replace("_", " ").title())
        codes = spec.get("product_codes", [])
        code = codes[0]["code"] if codes else ""
        finish = codes[0].get("finish", "") if codes else ""
        return CutListItem(
            category="Hinge",
            component=component_name,
            description=name,
            product_code=code,
            quantity=1,
            unit="pc",
            notes=finish,
        )

    def _extractAntiLiftPin(self, obj, component_name: str) -> CutListItem:
        spec = SLIDER_SYSTEM_SPECS.get("edge_slider", {})
        components = spec.get("components", {})
        pin_info = components.get("anti_lift_pin", {})
        return CutListItem(
            category="Slider",
            component=component_name,
            description="Anti-Lift Pin",
            product_code=pin_info.get("code", ""),
            quantity=1,
            unit="pc",
        )
