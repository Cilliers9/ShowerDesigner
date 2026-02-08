# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Walk-in shower enclosure assembly — App::Part containing a fixed glass
panel with an optional support bar.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.AssemblyBase import AssemblyController
from freecad.ShowerDesigner.Models.ChildProxies import SupportBarChild
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    SUPPORT_BAR_SPECS,
    HARDWARE_FINISHES,
)


def _setupHardwareVP(obj, finish="Chrome"):
    from freecad.ShowerDesigner.Models.HardwareViewProvider import (
        setupHardwareViewProvider,
    )
    setupHardwareViewProvider(obj, finish)


class WalkInEnclosureAssembly(AssemblyController):
    """
    Assembly controller for a walk-in shower enclosure.

    Creates an App::Part containing:
      - VarSet with all user-editable properties
      - FixedPanel (nested App::Part — FixedPanel assembly)
      - Optional SupportBar child
    """

    def __init__(self, part_obj):
        super().__init__(part_obj)
        vs = self._getOrCreateVarSet(part_obj)
        self._setupVarSetProperties(vs)
        self._createFixedPanel(part_obj)

    def _setupVarSetProperties(self, vs):
        # Dimensions
        vs.addProperty(
            "App::PropertyLength", "Width", "Dimensions",
            "Width of the glass panel"
        ).Width = 1000
        vs.addProperty(
            "App::PropertyLength", "Height", "Dimensions",
            "Height of the enclosure"
        ).Height = 2000
        vs.addProperty(
            "App::PropertyLength", "GlassThickness", "Glass",
            "Thickness of glass panel"
        ).GlassThickness = 10

        # Glass
        vs.addProperty(
            "App::PropertyEnumeration", "GlassType", "Glass", "Type of glass"
        )
        vs.GlassType = ["Clear", "Frosted", "Bronze", "Grey", "Reeded", "Low-Iron"]
        vs.GlassType = "Clear"

        # Support bar
        vs.addProperty(
            "App::PropertyBool", "ShowSupportBar", "Support Bar",
            "Add support bar"
        ).ShowSupportBar = True
        vs.addProperty(
            "App::PropertyEnumeration", "SupportBarType", "Support Bar",
            "Type of support bar"
        )
        vs.SupportBarType = list(SUPPORT_BAR_SPECS.keys())
        vs.SupportBarType = "Horizontal"
        vs.addProperty(
            "App::PropertyLength", "SupportBarHeight", "Support Bar",
            "Height of support bar from floor"
        ).SupportBarHeight = 1900
        vs.addProperty(
            "App::PropertyLength", "SupportBarDiameter", "Support Bar",
            "Diameter of support bar"
        ).SupportBarDiameter = 16

        # Hardware display
        vs.addProperty(
            "App::PropertyEnumeration", "HardwareFinish", "Hardware Display",
            "Finish for all hardware"
        )
        vs.HardwareFinish = HARDWARE_FINISHES[:]
        vs.HardwareFinish = "Chrome"

    def _createFixedPanel(self, part_obj):
        """Create the nested fixed panel assembly."""
        from freecad.ShowerDesigner.Models.FixedPanel import FixedPanelAssembly

        doc = part_obj.Document
        panel = doc.addObject("App::Part", "Panel")
        FixedPanelAssembly(panel)
        part_obj.addObject(panel)
        self._manifest["Panel"] = panel.Name

    # ------------------------------------------------------------------
    # execute
    # ------------------------------------------------------------------

    def assemblyExecute(self, part_obj):
        vs = self._getVarSet(part_obj)
        if vs is None:
            return

        width = vs.Width.Value
        height = vs.Height.Value
        thickness = vs.GlassThickness.Value

        if width <= 0 or height <= 0 or thickness <= 0:
            App.Console.PrintError("Invalid enclosure dimensions\n")
            return

        # --- Update fixed panel ---
        panel = self._getChild(part_obj, "Panel")
        if panel:
            panel_vs = self._getNestedVarSet(panel)
            if panel_vs:
                panel_vs.Width = width
                panel_vs.Height = height
                panel_vs.Thickness = thickness
                if hasattr(panel_vs, "GlassType"):
                    panel_vs.GlassType = vs.GlassType
                if hasattr(panel_vs, "HardwareFinish"):
                    panel_vs.HardwareFinish = vs.HardwareFinish

        # --- Support bar ---
        finish = vs.HardwareFinish
        if vs.ShowSupportBar:
            self._updateSupportBar(part_obj, vs)
        else:
            if self._hasChild(part_obj, "SupportBar"):
                self._removeChild(part_obj, "SupportBar")

        self._updateAllHardwareFinish(part_obj, finish)

    def _updateSupportBar(self, part_obj, vs):
        if not self._hasChild(part_obj, "SupportBar"):
            self._addChild(
                part_obj, "SupportBar", SupportBarChild,
                lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
            )

        child = self._getChild(part_obj, "SupportBar")
        if child is None:
            return

        child.BarType = vs.SupportBarType
        child.Length = vs.Width.Value
        child.Diameter = vs.SupportBarDiameter.Value

        thickness = vs.GlassThickness.Value
        bar_height = vs.SupportBarHeight.Value

        # Position: horizontal bar across the top of the panel
        child.Placement = App.Placement(
            App.Vector(0, thickness / 2, bar_height),
            App.Rotation(App.Vector(0, 0, 1), 0)
        )

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

def createWalkInEnclosure(name="WalkInEnclosure"):
    """
    Create a new walk-in enclosure assembly in the active document.

    Args:
        name: Name for the assembly (default: "WalkInEnclosure")

    Returns:
        App::Part assembly object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    part = doc.addObject("App::Part", name)
    WalkInEnclosureAssembly(part)

    doc.recompute()
    App.Console.PrintMessage(f"Walk-in enclosure '{name}' created\n")
    return part
