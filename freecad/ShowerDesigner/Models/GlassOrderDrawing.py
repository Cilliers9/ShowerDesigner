# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
TechDraw glass order drawing generator.

Walks ShowerDesigner assembly trees (same pattern as CutListExtractor),
extracts per-panel information, and creates TechDraw pages with
dimensioned front-view projections suitable for glass ordering.
"""

from __future__ import annotations

import os
from datetime import date

import FreeCAD as App

from freecad.ShowerDesigner.Data.DrawingSpecs import (
    DRAWING_CENTER_X,
    DRAWING_CENTER_Y,
    DIM_OFFSET_PAGE,
    TEMPLATE_MAP,
    HardwareCutout,
    PanelDrawingInfo,
    calculateScale,
    scaleLabel,
)

# Template directory relative to this file
_TEMPLATE_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "Resources",
    "Documents", "Drawing templates",
)

# Proxy class names that produce no drawing output
_SKIP_PROXIES = {
    "SwingArcChild", "GhostChild", "ChannelChild",
    "SliderTrackChild", "SliderRollerChild", "SliderFloorGuideChild",
    "AntiLiftPinChild", "GlassShelfChild",
}

# Proxy names that represent hardware items on glass
_HARDWARE_PROXIES = {
    "HingeChild": "Hinge",
    "MonzaWallHingeChild": "Hinge",
    "MonzaFoldHingeChild": "Hinge",
    "HandleChild": "Handle",
    "ClampChild": "Clamp",
    "SupportBarChild": "Support Bar",
}


class GlassOrderDrawingGenerator:
    """Generate TechDraw glass order pages from ShowerDesigner assemblies."""

    def generate(self, assembly_obj) -> list:
        """Generate TechDraw pages for an assembly.

        Args:
            assembly_obj: Top-level App::Part enclosure or sub-assembly.

        Returns:
            List of created TechDraw::DrawPage objects.
        """
        panel_infos = self._extractPanelInfos(assembly_obj)
        if not panel_infos:
            App.Console.PrintMessage(
                "Glass Order Drawings: No glass panels found.\n"
            )
            return []

        doc = assembly_obj.Document
        pages = []

        # Assembly overview page
        overview = self._createAssemblyOverviewPage(
            doc, assembly_obj, panel_infos
        )
        if overview is not None:
            pages.append(overview)

        # Per-panel pages
        for idx, info in enumerate(panel_infos):
            page = self._createPanelPage(
                doc, info, idx + 1, len(panel_infos), assembly_obj.Label
            )
            if page is not None:
                pages.append(page)

        doc.recompute()
        return pages

    # ------------------------------------------------------------------
    # Panel info extraction (tree walk)
    # ------------------------------------------------------------------

    def _extractPanelInfos(self, obj) -> list[PanelDrawingInfo]:
        """Walk the object tree and collect PanelDrawingInfo for each panel."""
        infos: list[PanelDrawingInfo] = []
        type_id = getattr(obj, "TypeId", "")

        if type_id == "App::Part":
            infos.extend(self._walkPart(obj, obj.Label, App.Placement()))
        return infos

    def _walkPart(
        self, part_obj, component_name: str, parent_placement
    ) -> list[PanelDrawingInfo]:
        """Walk an App::Part container's Group."""
        infos: list[PanelDrawingInfo] = []
        group = getattr(part_obj, "Group", [])
        varset = None
        controller = None
        glass_child = None
        hardware_children = []

        world_placement = parent_placement.multiply(part_obj.Placement)

        for child in group:
            child_type = getattr(child, "TypeId", "")

            if child_type == "App::VarSet":
                varset = child
                continue
            if hasattr(child, "Label") and child.Label.startswith("_Controller"):
                controller = child
                continue

            # Nested App::Part → recurse
            if child_type == "App::Part":
                infos.extend(self._walkPart(child, child.Label, world_placement))
                continue

            # Part::FeaturePython → classify
            if hasattr(child, "Proxy") and child.Proxy is not None:
                proxy_name = child.Proxy.__class__.__name__
                if proxy_name in _SKIP_PROXIES:
                    continue
                if proxy_name == "GlassChild":
                    glass_child = child
                elif proxy_name in _HARDWARE_PROXIES:
                    hardware_children.append(child)

        # If this part has a glass child, build a PanelDrawingInfo
        if glass_child is not None and varset is not None:
            info = self._buildPanelInfo(
                part_obj, varset, controller, glass_child,
                hardware_children, world_placement,
            )
            if info is not None:
                infos.append(info)

        return infos

    def _buildPanelInfo(
        self, part_obj, varset, controller, glass_child,
        hardware_children, world_placement,
    ) -> PanelDrawingInfo | None:
        """Build a PanelDrawingInfo from extracted tree objects."""
        width = glass_child.Width.Value if hasattr(glass_child, "Width") else 0
        height = glass_child.Height.Value if hasattr(glass_child, "Height") else 0
        if width <= 0 or height <= 0:
            return None

        thickness = (
            varset.Thickness.Value if hasattr(varset, "Thickness") else 8
        )
        glass_type = getattr(varset, "GlassType", "Clear")
        edge_finish = getattr(varset, "EdgeFinish", "Bright_Polish")
        tempering = getattr(varset, "TemperType", "Tempered")

        # Determine panel type from controller proxy
        panel_type = ""
        if controller is not None and hasattr(controller, "Proxy") and controller.Proxy is not None:
            panel_type = controller.Proxy.__class__.__name__

        # Extract hardware cutout positions relative to glass
        cutouts = self._extractHardwareCutouts(
            glass_child, hardware_children, world_placement
        )

        return PanelDrawingInfo(
            label=part_obj.Label,
            panel_type=panel_type,
            width=width,
            height=height,
            thickness=thickness,
            glass_type=glass_type,
            edge_finish=edge_finish,
            tempering=tempering,
            cutouts=cutouts,
            part_label=part_obj.Label,
        )

    def _extractHardwareCutouts(
        self, glass_child, hardware_children, world_placement,
    ) -> list[HardwareCutout]:
        """Compute hardware positions relative to the glass panel origin."""
        cutouts: list[HardwareCutout] = []

        # Glass panel world placement
        glass_world = world_placement.multiply(glass_child.Placement)
        glass_base = glass_world.Base
        glass_rot = glass_world.Rotation

        # Local axes of the glass panel
        local_x = glass_rot.multVec(App.Vector(1, 0, 0))  # width direction
        local_z = glass_rot.multVec(App.Vector(0, 0, 1))  # height direction

        for hw_child in hardware_children:
            proxy = hw_child.Proxy
            if proxy is None:
                continue
            proxy_name = proxy.__class__.__name__
            hw_type = _HARDWARE_PROXIES.get(proxy_name, "Unknown")

            # Hardware world position
            hw_world = world_placement.multiply(hw_child.Placement)
            hw_base = hw_world.Base

            # Vector from glass origin to hardware
            delta = hw_base - glass_base

            # Project onto glass local axes for 2D position
            pos_x = delta.dot(local_x)
            pos_z = delta.dot(local_z)

            # Get cutout dimensions from the hardware specs
            cutout_w, cutout_d, corner_r = self._getHardwareCutoutDims(
                hw_child, proxy_name
            )

            cutouts.append(HardwareCutout(
                hw_type=hw_type,
                label=hw_child.Label,
                position_x=pos_x,
                position_z=pos_z,
                cutout_width=cutout_w,
                cutout_depth=cutout_d,
                corner_radius=corner_r,
            ))

        return cutouts

    def _getHardwareCutoutDims(self, hw_child, proxy_name):
        """Look up cutout dimensions from hardware specs."""
        cutout_w = 0.0
        cutout_d = 0.0
        corner_r = 0.0

        if proxy_name == "HingeChild":
            from freecad.ShowerDesigner.Data.HardwareSpecs import BEVEL_HINGE_SPECS
            hinge_type = getattr(hw_child, "HingeType", "")
            spec = BEVEL_HINGE_SPECS.get(hinge_type)
            if spec is not None:
                dims = spec.get("dimensions", {})
                cutout_w = dims.get("glass_cutout_width", 0)
                cutout_d = dims.get("glass_cutout_depth", 0)
                corner_r = dims.get("cutout_radius", 0)

        elif proxy_name == "ClampChild":
            from freecad.ShowerDesigner.Data.HardwareSpecs import CLAMP_SPECS
            clamp_type = getattr(hw_child, "ClampType", "")
            spec = CLAMP_SPECS.get(clamp_type)
            if spec is not None:
                dims = spec.get("dimensions", {})
                cutout_d = dims.get("cutout_depth", 0)
                corner_r = dims.get("cutout_radius", 0)
                cutout_w = dims.get("base_size", 0)

        return cutout_w, cutout_d, corner_r

    # ------------------------------------------------------------------
    # TechDraw page creation
    # ------------------------------------------------------------------

    def _getTemplatePath(self, key: str) -> str:
        """Resolve a template key to an absolute SVG path."""
        filename = TEMPLATE_MAP.get(key, TEMPLATE_MAP["_default"])
        path = os.path.normpath(os.path.join(_TEMPLATE_DIR, filename))
        if not os.path.isfile(path):
            # Fall back to blank template
            path = os.path.normpath(
                os.path.join(_TEMPLATE_DIR, TEMPLATE_MAP["_default"])
            )
        return path

    def _createAssemblyOverviewPage(
        self, doc, assembly_obj, panel_infos: list[PanelDrawingInfo],
    ):
        """Create an overview page projecting the entire assembly."""
        template_path = self._getTemplatePath("_assembly")
        if not os.path.isfile(template_path):
            App.Console.PrintWarning(
                "Glass Order Drawings: Assembly template not found, skipping overview.\n"
            )
            return None

        page = doc.addObject("TechDraw::DrawPage", "GlassOrder_Overview")
        page.Label = f"{assembly_obj.Label} — Overview"

        tpl = doc.addObject("TechDraw::DrawSVGTemplate", "Template_Overview")
        tpl.Template = template_path
        page.Template = tpl

        # Project the entire assembly — front view (looking along -Y)
        view = doc.addObject("TechDraw::DrawViewPart", "View_Overview")
        view.Source = [assembly_obj]
        view.Direction = App.Vector(0, -1, 0)
        view.X = DRAWING_CENTER_X
        view.Y = DRAWING_CENTER_Y

        # Calculate scale from assembly bounding box
        bbox = assembly_obj.Shape.BoundBox if hasattr(assembly_obj, "Shape") else None
        if bbox is not None and bbox.XLength > 0 and bbox.ZLength > 0:
            view.Scale = calculateScale(bbox.XLength, bbox.ZLength)
        else:
            view.Scale = 1 / 20

        page.addView(view)

        # Fill title block
        self._fillTitleBlock(tpl, {
            "title": f"{assembly_obj.Label} — Assembly Overview",
            "identification_number": assembly_obj.Label,
            "scale": scaleLabel(view.Scale),
            "sheet_number": f"1 / {len(panel_infos) + 1}",
            "part_material": "",
        })

        return page

    def _createPanelPage(
        self, doc, info: PanelDrawingInfo, page_num: int,
        total_panels: int, assembly_label: str,
    ):
        """Create a single panel drawing page with front view and dimensions."""
        template_path = self._getTemplatePath(info.panel_type)

        page_name = f"GlassOrder_{info.label.replace(' ', '_')}"
        page = doc.addObject("TechDraw::DrawPage", page_name)
        page.Label = f"{info.label} — Glass Order"

        tpl = doc.addObject(
            "TechDraw::DrawSVGTemplate",
            f"Template_{info.label.replace(' ', '_')}",
        )
        tpl.Template = template_path
        page.Template = tpl

        # Front view of the glass panel shape — find the GlassChild in the part
        glass_obj = self._findGlassChild(doc, info.part_label)

        scale = calculateScale(info.width, info.height)

        if glass_obj is not None:
            view = doc.addObject("TechDraw::DrawViewPart", f"View_{page_name}")
            view.Source = [glass_obj]
            view.Direction = App.Vector(0, -1, 0)
            view.Scale = scale
            view.X = DRAWING_CENTER_X
            view.Y = DRAWING_CENTER_Y
            page.addView(view)

            # Width dimension (horizontal, below the view)
            self._addDimension(
                doc, page, info.width, info.height, scale,
                direction="horizontal",
                label=f"Dim_W_{page_name}",
                value_mm=info.width,
            )

            # Height dimension (vertical, to the left of the view)
            self._addDimension(
                doc, page, info.width, info.height, scale,
                direction="vertical",
                label=f"Dim_H_{page_name}",
                value_mm=info.height,
            )

        # Hardware position annotations
        for cutout in info.cutouts:
            self._addHardwareAnnotation(doc, page, info, cutout, scale)

        # Material string for title block
        material = f"{info.glass_type} {info.thickness:.0f}mm {info.tempering}"

        # Fill title block
        self._fillTitleBlock(tpl, {
            "title": info.label,
            "identification_number": assembly_label,
            "scale": scaleLabel(scale),
            "sheet_number": f"{page_num + 1} / {total_panels + 1}",
            "part_material": material,
        })

        return page

    def _findGlassChild(self, doc, part_label: str):
        """Find the GlassChild object inside a named App::Part."""
        part_obj = None
        for obj in doc.Objects:
            if obj.Label == part_label and getattr(obj, "TypeId", "") == "App::Part":
                part_obj = obj
                break
        if part_obj is None:
            return None

        for child in getattr(part_obj, "Group", []):
            if (
                hasattr(child, "Proxy")
                and child.Proxy is not None
                and child.Proxy.__class__.__name__ == "GlassChild"
            ):
                return child
        return None

    def _addDimension(
        self, doc, page, info_width, info_height, scale, direction, label,
        value_mm,
    ):
        """Add a dimension annotation to the page.

        Uses DrawViewAnnotation positioned beside the projected view.
        """
        ann = doc.addObject("TechDraw::DrawViewAnnotation", label)

        half_w = (info_width * scale) / 2
        half_h = (info_height * scale) / 2

        if direction == "horizontal":
            # Position centered below the view
            ann.X = DRAWING_CENTER_X
            ann.Y = DRAWING_CENTER_Y + half_h + DIM_OFFSET_PAGE
            ann.Text = [f"\u2194 {value_mm:.0f}"]
        else:
            # Position centered to the left of the view
            ann.X = DRAWING_CENTER_X - half_w - DIM_OFFSET_PAGE
            ann.Y = DRAWING_CENTER_Y
            ann.Text = [f"\u2195 {value_mm:.0f}"]

        ann.Scale = 1.0
        if hasattr(ann, "TextSize"):
            ann.TextSize = 5.0
        if hasattr(ann, "Font"):
            ann.Font = "osifont"

        page.addView(ann)

    def _addHardwareAnnotation(
        self, doc, page, info: PanelDrawingInfo,
        cutout: HardwareCutout, scale: float,
    ):
        """Add an annotation for a hardware position on the panel page."""
        # Calculate position on page relative to view center
        # Glass origin is bottom-left; view center maps to glass center
        offset_x = (cutout.position_x - info.width / 2) * scale
        offset_z = (cutout.position_z - info.height / 2) * scale

        page_x = DRAWING_CENTER_X + offset_x
        page_y = DRAWING_CENTER_Y - offset_z  # Y is inverted on page

        ann_name = f"Ann_{cutout.label.replace(' ', '_')}"
        ann = doc.addObject("TechDraw::DrawViewAnnotation", ann_name)

        # Build annotation text
        lines = [cutout.label]
        lines.append(f"  X: {cutout.position_x:.0f}mm")
        lines.append(f"  Z: {cutout.position_z:.0f}mm")
        if cutout.cutout_width > 0:
            lines.append(
                f"  Cutout: {cutout.cutout_width:.0f}x{cutout.cutout_depth:.0f}mm"
            )
            if cutout.corner_radius > 0:
                lines.append(f"  R{cutout.corner_radius:.0f}")

        ann.Text = lines
        ann.X = page_x + DIM_OFFSET_PAGE
        ann.Y = page_y
        ann.Scale = 1.0
        if hasattr(ann, "TextSize"):
            ann.TextSize = 3.5
        if hasattr(ann, "Font"):
            ann.Font = "osifont"

        page.addView(ann)

    def _fillTitleBlock(self, template, fields: dict):
        """Populate editable SVG text fields in a TechDraw template."""
        today = date.today().strftime("%Y-%m-%d")

        # Get creator from FreeCAD preferences if available
        creator = ""
        try:
            params = App.ParamGet(
                "User parameter:BaseApp/Preferences/Document"
            )
            creator = params.GetString("prefAuthor", "")
        except Exception:
            pass

        defaults = {
            "date_of_issue": today,
            "creator": creator,
            "document_type": "Glass Order Drawing",
            "general_tolerances": "+/- 1mm",
            "language_code": "EN",
            "revision_index": "A",
        }
        defaults.update(fields)

        for field_name, value in defaults.items():
            try:
                template.setEditFieldContent(field_name, str(value))
            except Exception:
                # Field may not exist in this template variant
                pass
