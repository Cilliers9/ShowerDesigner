# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Corner shower enclosure assembly — App::Part containing a fixed panel
and a door (hinged or sliding) at 90 degrees.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.AssemblyBase import AssemblyController
from freecad.ShowerDesigner.Data.HardwareSpecs import HARDWARE_FINISHES
from freecad.ShowerDesigner.Data.SealSpecs import (
    getCornerDoorConstraints,
    getReturnPanelMagnetDeduction,
)


class CornerEnclosureAssembly(AssemblyController):
    """
    Assembly controller for a corner shower enclosure.

    Creates an App::Part containing:
      - VarSet with all user-editable properties
      - FixedPanel (nested App::Part — FixedPanel assembly)
      - DoorPanel (nested App::Part — FixedPanel or Door assembly)
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
            "Width of the enclosure"
        ).Width = 900
        vs.addProperty(
            "App::PropertyLength", "Depth", "Dimensions",
            "Depth of the enclosure"
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
            "Type of door on the door panel"
        )
        vs.DoorType = ["HingedDoor", "FixedPanel"]
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

        # Fixed panel — always a fixed panel
        doc = part_obj.Document
        fixed = doc.addObject("App::Part", "FixedPanel")
        FixedPanelAssembly(fixed)
        part_obj.addObject(fixed)
        self._manifest["FixedPanel"] = fixed.Name

        # Door panel — created based on DoorType
        self._createDoorPanel(part_obj, vs)

    def _createDoorPanel(self, part_obj, vs):
        doc = part_obj.Document
        door_type = vs.DoorType

        if door_type == "HingedDoor":
            from freecad.ShowerDesigner.Models.HingedDoor import HingedDoorAssembly
            door = doc.addObject("App::Part", "DoorPanel")
            HingedDoorAssembly(door)
        else:
            from freecad.ShowerDesigner.Models.FixedPanel import FixedPanelAssembly
            door = doc.addObject("App::Part", "DoorPanel")
            FixedPanelAssembly(door)

        part_obj.addObject(door)
        self._manifest["DoorPanel"] = door.Name

    # ------------------------------------------------------------------
    # Door constraint helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _filterEnum(varset, prop, allowed):
        """Save current enum value, set new list, restore if still valid."""
        current = getattr(varset, prop)
        setattr(varset, prop, allowed)
        if current in allowed:
            setattr(varset, prop, current)
        else:
            setattr(varset, prop, allowed[0])

    def _applyDoorConstraints(self, door_vs, closes_on_panel):
        """Filter MountingType, DoorSeal, and set ClosingAgainst on the door."""
        constraints = getCornerDoorConstraints(closes_on_panel)

        if hasattr(door_vs, "MountingType"):
            self._filterEnum(door_vs, "MountingType", constraints["mounting_types"])

        if hasattr(door_vs, "DoorSeal"):
            self._filterEnum(door_vs, "DoorSeal", constraints["seal_options"])

        if hasattr(door_vs, "ClosingAgainst"):
            door_vs.ClosingAgainst = constraints["closing_against"]

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

        door_right = vs.DoorSide == "Right"

        # --- Apply door constraints & check seal for fixed panel deduction ---
        fixed_panel_seal_ded = 0.0
        door = self._getChild(part_obj, "DoorPanel")
        if door:
            door_vs = self._getNestedVarSet(door)
            if door_vs and hasattr(door_vs, "HingeSide"):
                closes_on_panel = vs.DoorSide == door_vs.HingeSide
                self._applyDoorConstraints(door_vs, closes_on_panel)
                if (
                    closes_on_panel
                    and hasattr(door_vs, "DoorSeal")
                    and door_vs.DoorSeal == "Magnet Seal"
                ):
                    fixed_panel_seal_ded = getReturnPanelMagnetDeduction(
                        thickness
                    )

        # --- Update fixed panel ---
        fixed = self._getChild(part_obj, "FixedPanel")
        if fixed:
            fixed_vs = self._getNestedVarSet(fixed)
            if fixed_vs:
                fixed_vs.Width = width if door_right else depth
                fixed_vs.Height = height
                fixed_vs.Thickness = thickness
                if hasattr(fixed_vs, "SealDeduction"):
                    fixed_vs.SealDeduction = fixed_panel_seal_ded
                if hasattr(fixed_vs, "GlassType"):
                    fixed_vs.GlassType = vs.GlassType
                if hasattr(fixed_vs, "HardwareFinish"):
                    fixed_vs.HardwareFinish = vs.HardwareFinish
            if door_right:
                # Fixed panel on origin
                fixed_vs.WallMountEdge = "Left"
                fixed.Placement = App.Placement(
                    App.Vector(0, 0, 0),
                    App.Rotation(App.Vector(0, 0, 1), 0)
                )
            else:
                # Fixed panel on the right
                fixed_vs.WallMountEdge = "Right"
                fixed.Placement = App.Placement(
                    App.Vector(width, 0, 0),
                    App.Rotation(App.Vector(0, 0, 1), 90)
                )
        # --- Update door panel (door) ---
        door = self._getChild(part_obj, "DoorPanel")
        if door:
            door_vs = self._getNestedVarSet(door)
            if door_vs:
                door_vs.Width = (depth - thickness) if door_right else (width - thickness)
                door_vs.Height = height
                door_vs.Thickness = thickness
                if hasattr(door_vs, "GlassType"):
                    door_vs.GlassType = vs.GlassType
                if hasattr(door_vs, "HardwareFinish"):
                    door_vs.HardwareFinish = vs.HardwareFinish
            if door_right:
                # Door on right
                door.Placement = App.Placement(
                    App.Vector(width, thickness, 0),
                    App.Rotation(App.Vector(0, 0, 1), 90)
                )
            else:
                # Door at origin
                door.Placement = App.Placement(
                    App.Vector(0, 0, 0),
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
