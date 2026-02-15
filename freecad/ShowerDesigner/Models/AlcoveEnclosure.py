# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Alcove shower enclosure assembly — App::Part containing a single door
spanning the alcove opening.  The alcove walls provide side containment,
so only one panel/door is needed.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.AssemblyBase import AssemblyController
from freecad.ShowerDesigner.Data.HardwareSpecs import HARDWARE_FINISHES


class AlcoveEnclosureAssembly(AssemblyController):
    """
    Assembly controller for an alcove shower enclosure.

    Creates an App::Part containing:
      - VarSet with all user-editable properties
      - Door (nested App::Part — HingedDoor, SlidingDoor, or BiFoldDoor)
    """

    def __init__(self, part_obj):
        super().__init__(part_obj)
        vs = self._getOrCreateVarSet(part_obj)
        self._setupVarSetProperties(vs)
        self._createDoor(part_obj, vs)

    def _setupVarSetProperties(self, vs):
        # Dimensions
        vs.addProperty(
            "App::PropertyLength", "Width", "Dimensions",
            "Width of the alcove opening"
        ).Width = 1200
        vs.addProperty(
            "App::PropertyLength", "Height", "Dimensions",
            "Height of the enclosure"
        ).Height = 2000
        vs.addProperty(
            "App::PropertyLength", "GlassThickness", "Glass",
            "Thickness of glass door"
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
            "Type of door"
        )
        vs.DoorType = ["SlidingDoor", "HingedDoor", "BiFoldDoor"]
        vs.DoorType = "SlidingDoor"

        # Hardware display
        vs.addProperty(
            "App::PropertyEnumeration", "HardwareFinish", "Hardware Display",
            "Finish for all hardware"
        )
        vs.HardwareFinish = HARDWARE_FINISHES[:]
        vs.HardwareFinish = "Chrome"

    def _createDoor(self, part_obj, vs):
        """Create the door assembly based on DoorType."""
        doc = part_obj.Document
        door_type = vs.DoorType

        if door_type == "HingedDoor":
            from freecad.ShowerDesigner.Models.HingedDoor import HingedDoorAssembly
            door = doc.addObject("App::Part", "Door")
            HingedDoorAssembly(door)
        elif door_type == "BiFoldDoor":
            from freecad.ShowerDesigner.Models.BiFoldDoor import BiFoldDoorAssembly
            door = doc.addObject("App::Part", "Door")
            BiFoldDoorAssembly(door)
        else:
            from freecad.ShowerDesigner.Models.SlidingDoor import SlidingDoorAssembly
            door = doc.addObject("App::Part", "Door")
            SlidingDoorAssembly(door)

        part_obj.addObject(door)
        self._manifest["Door"] = door.Name

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

        # --- Update door ---
        door = self._getChild(part_obj, "Door")
        if door:
            door_vs = self._getNestedVarSet(door)
            if door_vs:
                door_vs.Width = width
                door_vs.Height = height
                door_vs.Thickness = thickness
                if hasattr(door_vs, "GlassType"):
                    door_vs.GlassType = vs.GlassType
                if hasattr(door_vs, "HardwareFinish"):
                    door_vs.HardwareFinish = vs.HardwareFinish

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

def createAlcoveEnclosure(name="AlcoveEnclosure"):
    """
    Create a new alcove enclosure assembly in the active document.

    Args:
        name: Name for the assembly (default: "AlcoveEnclosure")

    Returns:
        App::Part assembly object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    part = doc.addObject("App::Part", name)
    AlcoveEnclosureAssembly(part)

    doc.recompute()
    App.Console.PrintMessage(f"Alcove enclosure '{name}' created\n")
    return part
