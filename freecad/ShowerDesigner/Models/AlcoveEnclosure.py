# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Alcove shower enclosure assembly — App::Part containing a single door
spanning the alcove opening, or a fixed panel + door inline layout.
The alcove walls provide side containment.
"""

import math
import FreeCAD as App
from freecad.ShowerDesigner.Models.AssemblyBase import AssemblyController
from freecad.ShowerDesigner.Models.ChildProxies import GlassShelfChild, ClampChild
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    HARDWARE_FINISHES,
    SLIDER_SYSTEM_SPECS,
    GLASS_SHELF_SPECS,
    SHELF_CLAMP_MAPPING,
)
from freecad.ShowerDesigner.Data.PanelConstraints import validatePanelToPanelGap
from freecad.ShowerDesigner.Data.SealSpecs import getReturnPanelMagnetDeduction

_MAGNET_SEALS = frozenset({
    "90/180 Magnet Seal", "135 Magnet Seal", "180 Flat Magnet Seal",
})


def _setupHardwareVP(obj, finish="Chrome"):
    from freecad.ShowerDesigner.Models.HardwareViewProvider import (
        setupHardwareViewProvider,
    )
    setupHardwareViewProvider(obj, finish)


def _setupGlassVP(obj):
    from freecad.ShowerDesigner.Models.GlassPanelViewProvider import setupViewProvider
    setupViewProvider(obj)


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
            "App::PropertyLength", "Depth", "Dimensions",
            "Depth of the alcove (front to back wall)"
        ).Depth = 900
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
            "FixedPanel+HingedDoor+FixedPanel",
            "FixedPanel+SlidingDoor+FixedPanel",
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
        vs.addProperty(
            "App::PropertyEnumeration", "HingeSide", "Door Configuration",
            "Which side the door hinges are on"
        )
        vs.HingeSide = ["Left", "Right"]
        vs.HingeSide = "Left"

        # Slider configuration
        vs.addProperty(
            "App::PropertyEnumeration", "SliderSystem", "Door Configuration",
            "Catalogue slider system"
        )
        vs.SliderSystem = list(SLIDER_SYSTEM_SPECS.keys())
        vs.SliderSystem = "edge_slider"

        # 3-panel layout options
        vs.addProperty(
            "App::PropertyLength", "LeftPanelWidth", "Door Configuration",
            "Width of left fixed panel (3-panel layout)"
        ).LeftPanelWidth = 300
        vs.addProperty(
            "App::PropertyLength", "RightPanelWidth", "Door Configuration",
            "Width of right fixed panel (3-panel layout)"
        ).RightPanelWidth = 300

        # Glass shelf
        vs.addProperty(
            "App::PropertyBool", "ShowGlassShelf", "Glass Shelf",
            "Add a corner glass shelf"
        ).ShowGlassShelf = False
        vs.addProperty(
            "App::PropertyEnumeration", "ShelfPosition", "Glass Shelf",
            "Which corner to place the shelf"
        )
        vs.ShelfPosition = ["Position 1", "Position 2", "Position 3", "Position 4"]
        vs.ShelfPosition = "Position 4"
        vs.addProperty(
            "App::PropertyLength", "ShelfHeightFromFloor", "Glass Shelf",
            "Height of shelf from floor"
        ).ShelfHeightFromFloor = GLASS_SHELF_SPECS["default_height_from_floor"]
        vs.addProperty(
            "App::PropertyLength", "ShelfWidth", "Glass Shelf",
            "Shelf extent along edge 1"
        ).ShelfWidth = GLASS_SHELF_SPECS["default_width"]
        vs.addProperty(
            "App::PropertyLength", "ShelfDepth", "Glass Shelf",
            "Shelf extent along edge 2"
        ).ShelfDepth = GLASS_SHELF_SPECS["default_depth"]

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
        "FixedPanel+HingedDoor+FixedPanel": "HingedDoor",
        "FixedPanel+SlidingDoor+FixedPanel": "SlidingDoor",
    }

    _THREE_PANEL_TYPES = {
        "FixedPanel+HingedDoor+FixedPanel",
        "FixedPanel+SlidingDoor+FixedPanel",
    }

    # ------------------------------------------------------------------
    # Glass shelf
    # ------------------------------------------------------------------

    def _getShelfCornerInfo(self, position, width, depth):
        """Return placement info for a shelf at the given corner position.

        Alcove layout (top-down)::

                Back Wall (top)
          (0,D)+------------------+(W,D)
              | Pos 4      Pos 3 |
          Left|                  | Right Wall
          Wall|                  |
              | Pos 1      Pos 2 |
          (0,0)+------------------+(W,0)
                Door/Panel (glass, front)

        Back corners (3, 4) are wall-wall. Front corners (1, 2) are wall-glass.
        """
        # Edge 1 = along X (y=0 in shelf local), Edge 2 = along Y (x=0 in shelf local)
        mapping = {
            "Position 1": {
                "origin": App.Vector(0, 0, 0),
                "rotation": 0,
                "edge1_surface": "glass",   # front glass at y=0
                "edge2_surface": "wall",    # left wall at x=0
            },
            "Position 2": {
                "origin": App.Vector(width, 0, 0),
                "rotation": 90,
                "edge1_surface": "wall",    # right wall at x=W
                "edge2_surface": "glass",   # front glass at y=0
            },
            "Position 3": {
                "origin": App.Vector(width, depth, 0),
                "rotation": 180,
                "edge1_surface": "wall",
                "edge2_surface": "wall",
            },
            "Position 4": {
                "origin": App.Vector(0, depth, 0),
                "rotation": 270,
                "edge1_surface": "wall",
                "edge2_surface": "wall",
            },
        }
        return mapping.get(position, mapping["Position 4"])

    def _updateGlassShelf(self, part_obj, vs, width, depth):
        """Create or update the glass shelf and its two clamps."""
        info = self._getShelfCornerInfo(vs.ShelfPosition, width, depth)

        # --- Shelf ---
        if not self._hasChild(part_obj, "GlassShelf"):
            self._addChild(part_obj, "GlassShelf", GlassShelfChild, _setupGlassVP)

        shelf = self._getChild(part_obj, "GlassShelf")
        if shelf is None:
            return

        thickness = vs.GlassThickness.Value
        shelf.Width = vs.ShelfWidth.Value
        shelf.Depth = vs.ShelfDepth.Value
        shelf.Thickness = thickness
        shelf.GlassType = vs.GlassType
        shelf.Edge1Type = info["edge1_surface"].capitalize()
        shelf.Edge2Type = info["edge2_surface"].capitalize()
        shelf.PanelThickness = thickness
        shelf.Placement = App.Placement(
            App.Vector(
                info["origin"].x,
                info["origin"].y,
                vs.ShelfHeightFromFloor.Value,
            ),
            App.Rotation(App.Vector(0, 0, 1), info["rotation"]),
        )

        # --- Clamps (2) ---
        self._syncChildCount(
            part_obj, "ShelfClamp", 2, ClampChild,
            lambda obj: _setupHardwareVP(obj, vs.HardwareFinish),
        )

        clamp_inset = GLASS_SHELF_SPECS["clamp_inset"]
        shelf_w = vs.ShelfWidth.Value
        shelf_d = vs.ShelfDepth.Value
        rot = info["rotation"]
        origin = info["origin"]
        z = vs.ShelfHeightFromFloor.Value + thickness
        rad = math.radians(rot)

        # Clamp 1 on edge 1 (along X), positioned edge_length - inset from corner
        clamp1 = self._getChild(part_obj, "ShelfClamp1")
        if clamp1:
            clamp1.ClampType = SHELF_CLAMP_MAPPING[info["edge1_surface"]]
            g2g_offset = 8 if info["edge1_surface"] == "glass" else 0
            lx, ly = shelf_w - clamp_inset, g2g_offset
            wx = origin.x + lx * math.cos(rad) - ly * math.sin(rad)
            wy = origin.y + lx * math.sin(rad) + ly * math.cos(rad)
            clamp1.Placement = App.Placement(
                App.Vector(wx, wy, z),
                App.Rotation(0 + rot, 0, -90),
            )

        # Clamp 2 on edge 2 (along Y), positioned edge_length - inset from corner
        clamp2 = self._getChild(part_obj, "ShelfClamp2")
        if clamp2:
            clamp2.ClampType = SHELF_CLAMP_MAPPING[info["edge2_surface"]]
            g2g_offset = 8 if info["edge2_surface"] == "glass" else 0
            lx, ly = g2g_offset, shelf_d - clamp_inset
            wx = origin.x + lx * math.cos(rad) - ly * math.sin(rad)
            wy = origin.y + lx * math.sin(rad) + ly * math.cos(rad)
            clamp2.Placement = App.Placement(
                App.Vector(wx, wy, z),
                App.Rotation(-90 + rot, 0, -90),
            )

    # ------------------------------------------------------------------
    # Constraint helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _filterEnum(varset, prop, allowed):
        """Set enum list to *allowed*, preserving current value if still valid."""
        current = getattr(varset, prop)
        setattr(varset, prop, allowed)
        if current in allowed:
            setattr(varset, prop, current)
        else:
            setattr(varset, prop, allowed[0])

    @staticmethod
    def _isMagnetSeal(door_vs):
        """Return True if the door's ClosingSeal is a magnet seal."""
        return (
            hasattr(door_vs, "ClosingSeal")
            and door_vs.ClosingSeal in _MAGNET_SEALS
        )

    def _propagateSealDeduction(self, panel_part, thickness, is_magnet):
        """Set SealDeduction on a fixed panel based on magnet seal state."""
        panel_vs = self._getNestedVarSet(panel_part)
        if panel_vs and hasattr(panel_vs, "SealDeduction"):
            panel_vs.SealDeduction = (
                getReturnPanelMagnetDeduction(thickness) if is_magnet else 0.0
            )

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
        """Create a fixed panel + door (+ optional second panel) side by side."""
        from freecad.ShowerDesigner.Models.FixedPanel import FixedPanelAssembly

        inner = self._INLINE_DOOR_TYPES[door_type]
        if inner == "HingedDoor":
            from freecad.ShowerDesigner.Models.HingedDoor import HingedDoorAssembly
            DoorAssembly = HingedDoorAssembly
        else:
            from freecad.ShowerDesigner.Models.SlidingDoor import SlidingDoorAssembly
            DoorAssembly = SlidingDoorAssembly

        doc = part_obj.Document
        is_three = door_type in self._THREE_PANEL_TYPES

        if is_three:
            left = doc.addObject("App::Part", "LeftPanel")
            FixedPanelAssembly(left)
            part_obj.addObject(left)
            self._manifest["LeftPanel"] = left.Name
        else:
            panel = doc.addObject("App::Part", "Panel")
            FixedPanelAssembly(panel)
            part_obj.addObject(panel)
            self._manifest["Panel"] = panel.Name

        door = doc.addObject("App::Part", "Door")
        DoorAssembly(door)
        part_obj.addObject(door)
        self._manifest["Door"] = door.Name
        self._manifest["_doorType"] = door_type

        if is_three:
            right = doc.addObject("App::Part", "RightPanel")
            FixedPanelAssembly(right)
            part_obj.addObject(right)
            self._manifest["RightPanel"] = right.Name

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
        for role in ("Panel", "LeftPanel", "RightPanel"):
            if role in self._manifest:
                self._removeNestedAssembly(part_obj, role)

        # Default door width to half enclosure for sliding + panel layouts
        if wanted in ("FixedPanel+SlidingDoor", "FixedPanel+SlidingDoor+FixedPanel"):
            vs.DoorWidth = vs.Width.Value / 2

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

        if vs.DoorType in self._THREE_PANEL_TYPES:
            self._executeThreePanelLayout(part_obj, vs, width, height, thickness)
        elif vs.DoorType in self._INLINE_DOOR_TYPES:
            self._executeInlineLayout(part_obj, vs, width, height, thickness)
        else:
            # --- Single door fills the entire opening ---
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
                    if hasattr(door_vs, "HingeSide"):
                        door_vs.HingeSide = vs.HingeSide
                    if hasattr(door_vs, "SliderSystem"):
                        door_vs.SliderSystem = vs.SliderSystem
                    if hasattr(door_vs, "ClosingAgainst"):
                        door_vs.ClosingAgainst = "Wall"
                    # Both sides are walls for single door
                    if hasattr(door_vs, "MountingType"):
                        self._filterEnum(
                            door_vs, "MountingType", ["Wall Mounted", "Pivot"]
                        )
                    # Default to half-plate 90° wall-to-glass hinge
                    if hasattr(door_vs, "HingeModel"):
                        from freecad.ShowerDesigner.Data.HardwareSpecs import (
                            getHingeModelsForVariant,
                        )
                        wall_models = getHingeModelsForVariant("Wall Mounted")
                        self._filterEnum(door_vs, "HingeModel", wall_models)
                        if "bevel_90_wall_to_glass_half" in wall_models:
                            door_vs.HingeModel = "bevel_90_wall_to_glass_half"

        # --- Glass shelf ---
        # Back corners are always safe.  Front corners are only allowed
        # when a fixed inline panel separates the shelf from the door,
        # and only for hinged doors (sliding doors travel over the panel).
        allowed_shelf = ["Position 3", "Position 4"]
        is_hinged_inline = vs.DoorType in (
            "FixedPanel+HingedDoor", "FixedPanel+HingedDoor+FixedPanel",
        )
        if is_hinged_inline:
            if vs.DoorType in self._THREE_PANEL_TYPES:
                # Center door — panels on both sides
                allowed_shelf.extend(["Position 1", "Position 2"])
            elif vs.PanelSide == "Left":
                allowed_shelf.append("Position 1")
            else:
                allowed_shelf.append("Position 2")
        self._filterEnum(vs, "ShelfPosition", allowed_shelf)

        depth = vs.Depth.Value if hasattr(vs, "Depth") else 900
        if vs.ShowGlassShelf:
            self._updateGlassShelf(part_obj, vs, width, depth)
        else:
            if self._hasChild(part_obj, "GlassShelf"):
                self._removeChild(part_obj, "GlassShelf")
            self._syncChildCount(part_obj, "ShelfClamp", 0, ClampChild)

        self._updateAllHardwareFinish(part_obj, vs.HardwareFinish)

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
        panel = self._getChild(part_obj, "Panel")

        # --- Determine door constraints for hinged doors ---
        # Hinge on panel side → Glass Mounted/Pivot, closes against Wall
        # Hinge on wall side → Wall Mounted/Pivot, closes against Inline Panel
        is_magnet = False
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
                if hasattr(door_vs, "HingeSide"):
                    door_vs.HingeSide = vs.HingeSide
                if hasattr(door_vs, "SlideDirection"):
                    door_vs.SlideDirection = panel_side
                if hasattr(door_vs, "SliderSystem"):
                    door_vs.SliderSystem = vs.SliderSystem
                if hasattr(door_vs, "TrackWidthOverride"):
                    door_vs.TrackWidthOverride = width
                if hasattr(door_vs, "TrackXOffset"):
                    if panel_side == "Left":
                        door_vs.TrackXOffset = -(panel_width - overlap)
                    else:
                        door_vs.TrackXOffset = 0

                # HingedDoor constraint logic
                if hasattr(door_vs, "HingeSide"):
                    hinge_on_panel = panel_side == door_vs.HingeSide
                    if hinge_on_panel:
                        if hasattr(door_vs, "MountingType"):
                            self._filterEnum(
                                door_vs, "MountingType",
                                ["Glass Mounted", "Pivot"],
                            )
                        # 180° G2G is the only option when hinging on glass
                        if hasattr(door_vs, "HingeModel"):
                            self._filterEnum(
                                door_vs, "HingeModel",
                                ["bevel_180_glass_to_glass"],
                            )
                        if hasattr(door_vs, "ClosingAgainst"):
                            door_vs.ClosingAgainst = "Wall"
                    else:
                        if hasattr(door_vs, "MountingType"):
                            self._filterEnum(
                                door_vs, "MountingType",
                                ["Wall Mounted", "Pivot"],
                            )
                        # Default to half-plate 90° wall-to-glass hinge
                        if hasattr(door_vs, "HingeModel"):
                            from freecad.ShowerDesigner.Data.HardwareSpecs import (
                                getHingeModelsForVariant,
                            )
                            wall_models = getHingeModelsForVariant("Wall Mounted")
                            self._filterEnum(door_vs, "HingeModel", wall_models)
                            if "bevel_90_wall_to_glass_half" in wall_models:
                                door_vs.HingeModel = "bevel_90_wall_to_glass_half"
                        if hasattr(door_vs, "ClosingAgainst"):
                            door_vs.ClosingAgainst = "Inline Panel"
                elif hasattr(door_vs, "ClosingAgainst"):
                    # SlidingDoor closes against wall (panel is behind)
                    if hasattr(door_vs, "SlideDirection"):
                        door_vs.ClosingAgainst = "Wall"
                    else:
                        # BiFoldDoor — closes toward panel
                        door_vs.ClosingAgainst = "Inline Panel"

                is_magnet = self._isMagnetSeal(door_vs)

        # --- Update fixed panel ---
        if panel:
            panel_vs = self._getNestedVarSet(panel)
            if panel_vs:
                panel_vs.Width = panel_width
                panel_vs.Height = height
                panel_vs.Thickness = thickness
                if hasattr(panel_vs, "WallMountEdge"):
                    panel_vs.WallMountEdge = panel_side
                if hasattr(panel_vs, "GlassType"):
                    panel_vs.GlassType = vs.GlassType
                if hasattr(panel_vs, "HardwareFinish"):
                    panel_vs.HardwareFinish = vs.HardwareFinish
            # No panel seal deduction — door deductions alone create the gap
            self._propagateSealDeduction(panel, thickness, False)

        # --- Position based on PanelSide ---
        # For sliding: fixed panel in front (Y=0), door behind (Y=clearance).
        # Panel overlaps the door edge by `overlap` mm.
        door_y = clearance + thickness if clearance > 0 else 0
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
        if overlap == 0 and clearance == 0:
            gap = thickness
            valid, msg = validatePanelToPanelGap(gap)
            if not valid:
                App.Console.PrintWarning(f"AlcoveEnclosure: {msg}\n")

    def _executeThreePanelLayout(self, part_obj, vs, width, height, thickness):
        """Update LeftPanel + Door + RightPanel layout."""
        left_w = vs.LeftPanelWidth.Value
        right_w = vs.RightPanelWidth.Value

        # Get overlap from slider specs for sliding door layouts
        overlap = 0
        door = self._getChild(part_obj, "Door")
        if door:
            door_vs = self._getNestedVarSet(door)
            if door_vs and hasattr(door_vs, "SliderSystem"):
                spec = SLIDER_SYSTEM_SPECS.get(door_vs.SliderSystem, {})
                overlap = spec.get("fixed_door_overlap", 0)

        door_width = width - left_w - right_w + overlap * 2

        if door_width <= 0:
            App.Console.PrintError(
                "AlcoveEnclosure: Door width is zero or negative in 3-panel "
                "layout — reduce LeftPanelWidth or RightPanelWidth\n"
            )
            return

        # --- Update door (first, to read seal state for panel deductions) ---
        is_magnet = False
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
                if hasattr(door_vs, "HingeSide"):
                    door_vs.HingeSide = vs.HingeSide
                if hasattr(door_vs, "SliderSystem"):
                    door_vs.SliderSystem = vs.SliderSystem
                if hasattr(door_vs, "TrackWidthOverride"):
                    door_vs.TrackWidthOverride = width
                if hasattr(door_vs, "TrackXOffset"):
                    door_vs.TrackXOffset = -(left_w - overlap)
                if hasattr(door_vs, "ClosingAgainst"):
                    door_vs.ClosingAgainst = "Inline Panel"
                # Center sliding door: no closing seal needed
                if hasattr(door_vs, "SlideDirection") and hasattr(door_vs, "ClosingSeal"):
                    door_vs.ClosingSeal = "No Seal"
                # Both sides are panels → Glass Mounted/Pivot, 180° G2G hinge
                if hasattr(door_vs, "MountingType"):
                    self._filterEnum(
                        door_vs, "MountingType", ["Glass Mounted", "Pivot"]
                    )
                if hasattr(door_vs, "HingeModel"):
                    self._filterEnum(
                        door_vs, "HingeModel",
                        ["bevel_180_glass_to_glass"],
                    )
                is_magnet = self._isMagnetSeal(door_vs)

        # --- Update left panel ---
        left = self._getChild(part_obj, "LeftPanel")
        if left:
            left_vs = self._getNestedVarSet(left)
            if left_vs:
                left_vs.Width = left_w
                left_vs.Height = height
                left_vs.Thickness = thickness
                if hasattr(left_vs, "WallMountEdge"):
                    left_vs.WallMountEdge = "Left"
                if hasattr(left_vs, "GlassType"):
                    left_vs.GlassType = vs.GlassType
                if hasattr(left_vs, "HardwareFinish"):
                    left_vs.HardwareFinish = vs.HardwareFinish
            # No panel seal deduction — door deductions alone create the gap
            self._propagateSealDeduction(left, thickness, False)

        # --- Update right panel ---
        right = self._getChild(part_obj, "RightPanel")
        if right:
            right_vs = self._getNestedVarSet(right)
            if right_vs:
                right_vs.Width = right_w
                right_vs.Height = height
                right_vs.Thickness = thickness
                if hasattr(right_vs, "WallMountEdge"):
                    right_vs.WallMountEdge = "Right"
                if hasattr(right_vs, "GlassType"):
                    right_vs.GlassType = vs.GlassType
                if hasattr(right_vs, "HardwareFinish"):
                    right_vs.HardwareFinish = vs.HardwareFinish
            # No panel seal deduction — door deductions alone create the gap
            self._propagateSealDeduction(right, thickness, False)

        # --- Position ---
        # For sliding doors, offset in Y by clearance + glass thickness
        door_y = 0
        if door and vs.DoorType in self._THREE_PANEL_TYPES:
            door_vs = self._getNestedVarSet(door)
            if door_vs and hasattr(door_vs, "SliderSystem"):
                spec = SLIDER_SYSTEM_SPECS.get(door_vs.SliderSystem, {})
                clearance = spec.get("fixed_door_clearance", 0)
                if clearance > 0:
                    door_y = clearance + thickness

        if left:
            left.Placement = App.Placement(
                App.Vector(0, 0, 0), App.Rotation()
            )
        if door:
            door.Placement = App.Placement(
                App.Vector(left_w - overlap, door_y, 0), App.Rotation()
            )
        if right:
            right.Placement = App.Placement(
                App.Vector(width - right_w, 0, 0), App.Rotation()
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
