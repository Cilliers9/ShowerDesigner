# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Corner shower enclosure assembly — App::Part containing a fixed back panel
and a door (hinged or sliding) at 90 degrees.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.AssemblyBase import AssemblyController
from freecad.ShowerDesigner.Data.HardwareSpecs import HARDWARE_FINISHES


class CornerEnclosureAssembly(AssemblyController):
    """
    Assembly controller for a corner shower enclosure.

    Creates an App::Part containing:
      - VarSet with all user-editable properties
      - BackPanel (nested App::Part — FixedPanel assembly)
      - SidePanel (nested App::Part — FixedPanel or Door assembly)
    """

    def __init__(self, part_obj):
        super().__init__(part_obj)
        vs = self._getOrCreateVarSet(part_obj)
        self._setupVarSetProperties(vs)
        self._createNestedPanels(part_obj, vs)

    def _setupVarSetProperties(self, vs):
        # Dimensions
        vs.addProperty(
            "App::PropertyLength", "Width", "Dimensions",
            "Width of the enclosure (back panel)"
        ).Width = 900
        vs.addProperty(
            "App::PropertyLength", "Depth", "Dimensions",
            "Depth of the enclosure (side panel)"
        ).Depth = 900
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

        # Door configuration
        vs.addProperty(
            "App::PropertyEnumeration", "DoorType", "Door Configuration",
            "Type of door on the side panel"
        )
        vs.DoorType = ["HingedDoor", "SlidingDoor", "FixedPanel"]
        vs.DoorType = "HingedDoor"
        vs.addProperty(
            "App::PropertyEnumeration", "DoorSide", "Door Configuration",
            "Which side the door is on"
        )
        vs.DoorSide = ["Left", "Right"]
        vs.DoorSide = "Right"

        # Hardware display
        vs.addProperty(
            "App::PropertyEnumeration", "HardwareFinish", "Hardware Display",
            "Finish for all hardware"
        )
        vs.HardwareFinish = HARDWARE_FINISHES[:]
        vs.HardwareFinish = "Chrome"

    def _createNestedPanels(self, part_obj, vs):
        """Create the nested panel assemblies."""
        from freecad.ShowerDesigner.Models.FixedPanel import FixedPanelAssembly

        # Back panel — always a fixed panel
        doc = part_obj.Document
        back = doc.addObject("App::Part", "BackPanel")
        FixedPanelAssembly(back)
        part_obj.addObject(back)
        self._manifest["BackPanel"] = back.Name

        # Side panel — created based on DoorType
        self._createSidePanel(part_obj, vs)

    def _createSidePanel(self, part_obj, vs):
        doc = part_obj.Document
        door_type = vs.DoorType

        if door_type == "HingedDoor":
            from freecad.ShowerDesigner.Models.HingedDoor import HingedDoorAssembly
            side = doc.addObject("App::Part", "SidePanel")
            HingedDoorAssembly(side)
        elif door_type == "SlidingDoor":
            from freecad.ShowerDesigner.Models.SlidingDoor import SlidingDoorAssembly
            side = doc.addObject("App::Part", "SidePanel")
            SlidingDoorAssembly(side)
        else:
            from freecad.ShowerDesigner.Models.FixedPanel import FixedPanelAssembly
            side = doc.addObject("App::Part", "SidePanel")
            FixedPanelAssembly(side)

        part_obj.addObject(side)
        self._manifest["SidePanel"] = side.Name

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

        # --- Update back panel ---
        back = self._getChild(part_obj, "BackPanel")
        if back:
            back_vs = self._getNestedVarSet(back)
            if back_vs:
                back_vs.Width = width
                back_vs.Height = height
                back_vs.Thickness = thickness
                if hasattr(back_vs, "GlassType"):
                    back_vs.GlassType = vs.GlassType
                if hasattr(back_vs, "HardwareFinish"):
                    back_vs.HardwareFinish = vs.HardwareFinish
            # Position back panel along the back wall
            back.Placement = App.Placement(
                App.Vector(0, depth - thickness, 0), App.Rotation()
            )

        # --- Update side panel ---
        side = self._getChild(part_obj, "SidePanel")
        if side:
            side_vs = self._getNestedVarSet(side)
            if side_vs:
                side_vs.Width = depth
                side_vs.Height = height
                side_vs.Thickness = thickness
                if hasattr(side_vs, "GlassType"):
                    side_vs.GlassType = vs.GlassType
                if hasattr(side_vs, "HardwareFinish"):
                    side_vs.HardwareFinish = vs.HardwareFinish
            # Position side panel along the side wall (rotated 90 degrees)
            if vs.DoorSide == "Right":
                side.Placement = App.Placement(
                    App.Vector(width, 0, 0),
                    App.Rotation(App.Vector(0, 0, 1), 90)
                )
            else:
                side.Placement = App.Placement(
                    App.Vector(0, 0, 0),
                    App.Rotation(App.Vector(0, 0, 1), -90)
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

def createCornerEnclosure(name="CornerEnclosure"):
    """
    Create a new corner enclosure assembly in the active document.

    Args:
        name: Name for the assembly (default: "CornerEnclosure")

    Returns:
        App::Part assembly object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    part = doc.addObject("App::Part", name)
    CornerEnclosureAssembly(part)

    doc.recompute()
    App.Console.PrintMessage(f"Corner enclosure '{name}' created\n")
    return part
