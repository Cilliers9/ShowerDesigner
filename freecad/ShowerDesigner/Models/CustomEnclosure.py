# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Custom shower enclosure assembly — App::Part that serves as a flexible
container for arbitrary panel and door assemblies.

Users can add/remove panels and doors to build any enclosure shape.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.AssemblyBase import AssemblyController
from freecad.ShowerDesigner.Data.HardwareSpecs import HARDWARE_FINISHES
from freecad.ShowerDesigner.Data.PanelConstraints import validatePanelToPanelGap


class CustomEnclosureAssembly(AssemblyController):
    """
    Assembly controller for a custom shower enclosure.

    Creates an App::Part containing:
      - VarSet with user-editable properties
      - Starts with 2 FixedPanel assemblies at 90 degrees as a baseline

    Additional panels/doors can be added via commands or scripting.
    """

    def __init__(self, part_obj):
        super().__init__(part_obj)
        vs = self._getOrCreateVarSet(part_obj)
        self._setupVarSetProperties(vs)
        self._createDefaultPanels(part_obj, vs)

    def _setupVarSetProperties(self, vs):
        # Dimensions
        vs.addProperty(
            "App::PropertyLength", "Width", "Dimensions",
            "Default width for new panels"
        ).Width = 1000
        vs.addProperty(
            "App::PropertyLength", "Depth", "Dimensions",
            "Default depth for new panels"
        ).Depth = 1000
        vs.addProperty(
            "App::PropertyLength", "Height", "Dimensions",
            "Height of the enclosure"
        ).Height = 2000
        vs.addProperty(
            "App::PropertyLength", "GlassThickness", "Glass",
            "Thickness of glass panels"
        ).GlassThickness = 8

        # Glass
        vs.addProperty(
            "App::PropertyEnumeration", "GlassType", "Glass", "Type of glass"
        )
        vs.GlassType = ["Clear", "Frosted", "Bronze", "Grey", "Reeded", "Low-Iron"]
        vs.GlassType = "Clear"

        # Configuration
        vs.addProperty(
            "App::PropertyInteger", "PanelCount", "Configuration",
            "Number of panels in the enclosure"
        ).PanelCount = 2

        # Hardware display
        vs.addProperty(
            "App::PropertyEnumeration", "HardwareFinish", "Hardware Display",
            "Finish for all hardware"
        )
        vs.HardwareFinish = HARDWARE_FINISHES[:]
        vs.HardwareFinish = "Chrome"

    def _createDefaultPanels(self, part_obj, vs):
        """Create 2 fixed panels as a starting point."""
        from freecad.ShowerDesigner.Models.FixedPanel import FixedPanelAssembly

        doc = part_obj.Document

        # Panel 1 — back wall
        p1 = doc.addObject("App::Part", "Panel1")
        FixedPanelAssembly(p1)
        part_obj.addObject(p1)
        self._manifest["Panel1"] = p1.Name

        # Panel 2 — side wall
        p2 = doc.addObject("App::Part", "Panel2")
        FixedPanelAssembly(p2)
        part_obj.addObject(p2)
        self._manifest["Panel2"] = p2.Name

    # ------------------------------------------------------------------
    # execute
    # ------------------------------------------------------------------

    def assemblyExecute(self, part_obj):
        vs = self._getVarSet(part_obj)
        if vs is None:
            return

        width = vs.Width.Value
        depth = vs.Depth.Value
        height = vs.Height.Value
        thickness = vs.GlassThickness.Value

        if width <= 0 or depth <= 0 or height <= 0 or thickness <= 0:
            App.Console.PrintError("Invalid enclosure dimensions\n")
            return

        panel_count = max(1, vs.PanelCount)

        # Sync panel count
        self._syncPanelCount(part_obj, vs, panel_count)

        # Update panel 1 (back wall)
        p1 = self._getChild(part_obj, "Panel1")
        if p1:
            p1_vs = self._getNestedVarSet(p1)
            if p1_vs:
                p1_vs.Width = width
                p1_vs.Height = height
                p1_vs.Thickness = thickness
                if hasattr(p1_vs, "GlassType"):
                    p1_vs.GlassType = vs.GlassType
                if hasattr(p1_vs, "HardwareFinish"):
                    p1_vs.HardwareFinish = vs.HardwareFinish
            p1.Placement = App.Placement(
                App.Vector(0, depth - thickness, 0), App.Rotation()
            )

        # Update panel 2 (side wall) if it exists
        if panel_count >= 2:
            p2 = self._getChild(part_obj, "Panel2")
            if p2:
                p2_vs = self._getNestedVarSet(p2)
                if p2_vs:
                    p2_vs.Width = depth
                    p2_vs.Height = height
                    p2_vs.Thickness = thickness
                    if hasattr(p2_vs, "GlassType"):
                        p2_vs.GlassType = vs.GlassType
                    if hasattr(p2_vs, "HardwareFinish"):
                        p2_vs.HardwareFinish = vs.HardwareFinish
                p2.Placement = App.Placement(
                    App.Vector(0, 0, 0), App.Rotation()
                )

        # --- Validate panel-to-panel gap (Panel1 ↔ Panel2) ---
        if panel_count >= 2:
            # Panels meet at a corner; gap = glass thickness
            gap = thickness
            valid, msg = validatePanelToPanelGap(gap)
            if not valid:
                App.Console.PrintWarning(f"CustomEnclosure: {msg}\n")

        # Additional panels (3+) are positioned manually by user

    def _syncPanelCount(self, part_obj, vs, desired_count):
        """Add or remove panel assemblies to match desired count."""
        from freecad.ShowerDesigner.Models.FixedPanel import FixedPanelAssembly

        # Find existing panel roles
        existing = sorted(
            [k for k in self._manifest
             if k.startswith("Panel") and k[5:].isdigit()]
        )
        current_count = len(existing)

        # Remove excess panels
        for i in range(current_count, desired_count, -1):
            role = f"Panel{i}"
            name = self._manifest.pop(role, None)
            if name:
                doc = part_obj.Document
                obj = doc.getObject(name)
                if obj:
                    part_obj.removeObject(obj)
                    doc.removeObject(name)

        # Add missing panels
        for i in range(current_count + 1, desired_count + 1):
            doc = part_obj.Document
            role = f"Panel{i}"
            panel = doc.addObject("App::Part", role)
            FixedPanelAssembly(panel)
            part_obj.addObject(panel)
            self._manifest[role] = panel.Name

    def _getNestedVarSet(self, part_obj):
        """Get VarSet from a nested assembly."""
        for child in part_obj.Group:
            if child.TypeId == "App::VarSet":
                return child
        return None

    def assemblyOnChanged(self, part_obj, prop):
        pass


# ======================================================================
# Factory function
# ======================================================================

def createCustomEnclosure(name="CustomEnclosure"):
    """
    Create a new custom enclosure assembly in the active document.

    Args:
        name: Name for the assembly (default: "CustomEnclosure")

    Returns:
        App::Part assembly object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    part = doc.addObject("App::Part", name)
    CustomEnclosureAssembly(part)

    doc.recompute()
    App.Console.PrintMessage(f"Custom enclosure '{name}' created\n")
    return part
