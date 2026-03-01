# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Alcove shower enclosure assembly — App::Part containing a single door
spanning the alcove opening, or a fixed panel + door inline layout.
The alcove walls provide side containment.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.AssemblyBase import AssemblyController
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    HARDWARE_FINISHES,
    SLIDER_SYSTEM_SPECS,
)
from freecad.ShowerDesigner.Data.PanelConstraints import validatePanelToPanelGap


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
        vs.DoorType = [
            "SlidingDoor", "HingedDoor", "BiFoldDoor",
            "FixedPanel+HingedDoor", "FixedPanel+SlidingDoor",
        ]
        vs.DoorType = "SlidingDoor"

        # Inline layout options (FixedPanel+Door)
        vs.addProperty(
            "App::PropertyLength", "DoorWidth", "Door Configuration",
            "Width of the door in inline layout"
        ).DoorWidth = 700
        vs.addProperty(
            "App::PropertyEnumeration", "PanelSide", "Door Configuration",
            "Which side the fixed panel is on"
        )
        vs.PanelSide = ["Left", "Right"]
        vs.PanelSide = "Left"

        # Hardware display
        vs.addProperty(
            "App::PropertyEnumeration", "HardwareFinish", "Hardware Display",
            "Finish for all hardware"
        )
        vs.HardwareFinish = HARDWARE_FINISHES[:]
        vs.HardwareFinish = "Chrome"

    # Map inline DoorType values to the door assembly class they use
    _INLINE_DOOR_TYPES = {
        "FixedPanel+HingedDoor": "HingedDoor",
        "FixedPanel+SlidingDoor": "SlidingDoor",
    }

    def _createDoor(self, part_obj, vs):
        """Create the door assembly based on DoorType."""
        door_type = vs.DoorType

        if door_type in self._INLINE_DOOR_TYPES:
            self._createInlineLayout(part_obj, door_type)
            return

        doc = part_obj.Document

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
        self._manifest["_doorType"] = door_type

    def _createInlineLayout(self, part_obj, door_type):
        """Create a fixed panel + door side by side."""
        from freecad.ShowerDesigner.Models.FixedPanel import FixedPanelAssembly

        inner = self._INLINE_DOOR_TYPES[door_type]
        if inner == "HingedDoor":
            from freecad.ShowerDesigner.Models.HingedDoor import HingedDoorAssembly
            DoorAssembly = HingedDoorAssembly
        else:
            from freecad.ShowerDesigner.Models.SlidingDoor import SlidingDoorAssembly
            DoorAssembly = SlidingDoorAssembly

        doc = part_obj.Document

        panel = doc.addObject("App::Part", "Panel")
        FixedPanelAssembly(panel)
        part_obj.addObject(panel)
        self._manifest["Panel"] = panel.Name

        door = doc.addObject("App::Part", "Door")
        DoorAssembly(door)
        part_obj.addObject(door)
        self._manifest["Door"] = door.Name
        self._manifest["_doorType"] = door_type

    # ------------------------------------------------------------------
    # Layout management
    # ------------------------------------------------------------------

    def _removeNestedAssembly(self, part_obj, role):
        """Remove a nested App::Part assembly and all its children."""
        name = self._manifest.pop(role, None)
        if name is None:
            return
        doc = part_obj.Document
        obj = doc.getObject(name)
        if obj is None:
            return
        # Remove all children inside the nested Part first
        for child in list(obj.Group):
            obj.removeObject(child)
            doc.removeObject(child.Name)
        part_obj.removeObject(obj)
        doc.removeObject(name)

    def _ensureLayout(self, part_obj, vs):
        """Rebuild children if DoorType doesn't match current layout."""
        current = self._manifest.get("_doorType")
        wanted = vs.DoorType

        if current == wanted:
            return  # layout already matches

        # Tear down existing children
        self._removeNestedAssembly(part_obj, "Door")
        if "Panel" in self._manifest:
            self._removeNestedAssembly(part_obj, "Panel")

        # Rebuild
        self._createDoor(part_obj, vs)

    # ------------------------------------------------------------------
    # execute
    # ------------------------------------------------------------------

    def assemblyExecute(self, part_obj):
        vs = self._getVarSet(part_obj)
        if vs is None:
            return

        self._ensureLayout(part_obj, vs)

        width = vs.Width.Value
        height = vs.Height.Value
        thickness = vs.GlassThickness.Value

        if width <= 0 or height <= 0 or thickness <= 0:
            App.Console.PrintError("Invalid enclosure dimensions\n")
            return

        if vs.DoorType in self._INLINE_DOOR_TYPES:
            self._executeInlineLayout(part_obj, vs, width, height, thickness)
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

    def _executeInlineLayout(self, part_obj, vs, width, height, thickness):
        """Update the fixed panel + door inline layout."""
        door_width = vs.DoorWidth.Value
        door_type = vs.DoorType

        # For sliding door layouts, get overlap/clearance from slider specs
        overlap = 0
        clearance = 0
        door = self._getChild(part_obj, "Door")
        if door_type == "FixedPanel+SlidingDoor" and door:
            door_vs = self._getNestedVarSet(door)
            if door_vs and hasattr(door_vs, "SliderSystem"):
                spec = SLIDER_SYSTEM_SPECS.get(door_vs.SliderSystem, {})
                overlap = spec.get("fixed_door_overlap", 0)
                clearance = spec.get("fixed_door_clearance", 0)

        panel_width = width - door_width + overlap

        if panel_width <= 0 or door_width <= 0:
            App.Console.PrintError(
                "AlcoveEnclosure: DoorWidth must be less than total Width\n"
            )
            return

        panel_side = vs.PanelSide

        # --- Update fixed panel ---
        panel = self._getChild(part_obj, "Panel")
        if panel:
            panel_vs = self._getNestedVarSet(panel)
            if panel_vs:
                panel_vs.Width = panel_width
                panel_vs.Height = height
                panel_vs.Thickness = thickness
                if hasattr(panel_vs, "GlassType"):
                    panel_vs.GlassType = vs.GlassType
                if hasattr(panel_vs, "HardwareFinish"):
                    panel_vs.HardwareFinish = vs.HardwareFinish

        # --- Update door ---
        if door:
            door_vs = self._getNestedVarSet(door)
            if door_vs:
                door_vs.Width = door_width
                door_vs.Height = height
                door_vs.Thickness = thickness
                if hasattr(door_vs, "GlassType"):
                    door_vs.GlassType = vs.GlassType
                if hasattr(door_vs, "HardwareFinish"):
                    door_vs.HardwareFinish = vs.HardwareFinish

        # --- Position based on PanelSide ---
        # For sliding: fixed panel in front (Y=0), door behind (Y=clearance).
        # Panel overlaps the door edge by `overlap` mm.
        door_y = clearance
        if panel_side == "Left":
            if panel:
                panel.Placement = App.Placement(
                    App.Vector(0, 0, 0), App.Rotation()
                )
            if door:
                door.Placement = App.Placement(
                    App.Vector(panel_width - overlap, door_y, 0), App.Rotation()
                )
        else:
            if door:
                door.Placement = App.Placement(
                    App.Vector(0, door_y, 0), App.Rotation()
                )
            if panel:
                panel.Placement = App.Placement(
                    App.Vector(door_width - overlap, 0, 0), App.Rotation()
                )

        # --- Validate panel-to-panel gap (fixed panel ↔ door) ---
        # In inline layouts the panels are adjacent; the gap is determined
        # by the overlap/clearance values.  When overlap == 0 the nominal
        # gap is 0 (butted), otherwise validate the effective gap.
        if overlap == 0 and clearance == 0:
            gap = thickness  # butt joint, gap equals glass thickness
            valid, msg = validatePanelToPanelGap(gap)
            if not valid:
                App.Console.PrintWarning(f"AlcoveEnclosure: {msg}\n")

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
