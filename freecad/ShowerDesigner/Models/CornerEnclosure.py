# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Corner shower enclosure assembly — App::Part containing a fixed panel
and a door (hinged or sliding) at 90 degrees.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.AssemblyBase import AssemblyController
from freecad.ShowerDesigner.Models.ChildProxies import (
    SupportBarChild,
    GlassShelfChild,
    ClampChild,
)
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    HARDWARE_FINISHES,
    SUPPORT_BAR_SPECS,
    GLASS_SHELF_SPECS,
    SHELF_CLAMP_MAPPING,
)
from freecad.ShowerDesigner.Data.SealSpecs import (
    getCornerDoorConstraints,
    getReturnPanelMagnetDeduction,
)
from freecad.ShowerDesigner.Data.PanelConstraints import (
    validatePanelToPanelGap,
    PANEL_TO_PANEL_GAP,
)


def _setupHardwareVP(obj, finish="Chrome"):
    from freecad.ShowerDesigner.Models.HardwareViewProvider import (
        setupHardwareViewProvider,
    )
    setupHardwareViewProvider(obj, finish)


def _setupGlassVP(obj):
    from freecad.ShowerDesigner.Models.GlassPanelViewProvider import setupViewProvider
    setupViewProvider(obj)


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
        vs.addProperty(
            "App::PropertyEnumeration", "HingeSide", "Door Configuration",
            "Which side the hinges are on"
        )
        vs.HingeSide = ["Left", "Right"]
        vs.HingeSide = "Left"

        # Layout
        vs.addProperty(
            "App::PropertyEnumeration", "InlinePanelLayout", "Layout",
            "Inline fixed panels flanking the door on the door-side wall"
        )
        vs.InlinePanelLayout = ["None", "Wall Side", "Corner Side", "Both Sides"]
        vs.InlinePanelLayout = "None"
        vs.addProperty(
            "App::PropertyLength", "WallInlineWidth", "Layout",
            "Width of inline panel near the far bathroom wall"
        ).WallInlineWidth = 300
        vs.addProperty(
            "App::PropertyLength", "CornerInlineWidth", "Layout",
            "Width of inline panel near the corner junction"
        ).CornerInlineWidth = 300

        # Support bar
        vs.addProperty(
            "App::PropertyBool", "ShowSupportBar", "Support Bar",
            "Add support bar to stabilize fixed panel"
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
        self._manifest["_doorType"] = vs.DoorType

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
        for child in list(obj.Group):
            obj.removeObject(child)
            doc.removeObject(child.Name)
        part_obj.removeObject(obj)
        doc.removeObject(name)

    def _ensureLayout(self, part_obj, vs):
        """Rebuild door panel if DoorType has changed."""
        current = self._manifest.get("_doorType")
        wanted = vs.DoorType
        if current == wanted:
            return
        self._removeNestedAssembly(part_obj, "DoorPanel")
        self._createDoorPanel(part_obj, vs)

    def _ensurePanel(self, part_obj, role):
        """Create a FixedPanel nested assembly for *role* if it doesn't exist."""
        if role in self._manifest:
            name = self._manifest[role]
            if part_obj.Document.getObject(name) is not None:
                return
        from freecad.ShowerDesigner.Models.FixedPanel import FixedPanelAssembly

        doc = part_obj.Document
        panel = doc.addObject("App::Part", role)
        FixedPanelAssembly(panel)
        part_obj.addObject(panel)
        self._manifest[role] = panel.Name

    def _ensureInlinePanels(self, part_obj, layout):
        """Create/remove WallInline and CornerInline based on layout enum."""
        want_wall = layout in ("Wall Side", "Both Sides")
        want_corner = layout in ("Corner Side", "Both Sides")

        if want_wall:
            self._ensurePanel(part_obj, "WallInline")
        elif "WallInline" in self._manifest:
            self._removeNestedAssembly(part_obj, "WallInline")

        if want_corner:
            self._ensurePanel(part_obj, "CornerInline")
        elif "CornerInline" in self._manifest:
            self._removeNestedAssembly(part_obj, "CornerInline")

    # ------------------------------------------------------------------
    # Support bar
    # ------------------------------------------------------------------

    _SUPPORT_BAR_INSET = 75  # mm from free corner edge of fixed panel

    def _updateSupportBar(self, part_obj, vs, door_right, width, depth,
                          height, thickness):
        """Create or update the support bar child.

        The bar sits at the top edge of the fixed panel glass, 75 mm
        inset from the free corner edge, and runs perpendicular to the
        fixed panel toward the door-side wall.
        """
        if not self._hasChild(part_obj, "SupportBar"):
            self._addChild(
                part_obj, "SupportBar", SupportBarChild,
                lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
            )

        child = self._getChild(part_obj, "SupportBar")
        if child is None:
            return

        child.BarType = vs.SupportBarType
        child.Diameter = vs.SupportBarDiameter.Value

        inset = self._SUPPORT_BAR_INSET

        if door_right:
            # Fixed panel along X (y=0). Free corner at x=width.
            # Bar runs along +Y from fixed panel toward door-side wall.
            bar_length = depth - thickness
            child.Length = bar_length
            child.Placement = App.Placement(
                App.Vector(width - inset, thickness / 2, height),
                App.Rotation(App.Vector(0, 0, 1), 0)
            )
        else:
            # Fixed panel along Y at x=width (rotated 90°).
            # Free corner is at low Y (y=0, corner junction).
            # Bar runs along +X from door-side wall toward fixed panel.
            bar_length = width - thickness
            child.Length = bar_length
            child.Placement = App.Placement(
                App.Vector(width - thickness / 2, inset, height),
                App.Rotation(App.Vector(0, 0, 1), 90)
            )

    # ------------------------------------------------------------------
    # Glass shelf
    # ------------------------------------------------------------------

    def _getShelfCornerInfo(self, position, door_right, width, depth, thickness):
        """Return placement info for a shelf at the given corner position.

        Returns dict with: origin (Vector), rotation (float, degrees around Z),
        edge1_surface ("wall"/"glass"), edge2_surface ("wall"/"glass").

        Corner layout (DoorSide=Right)::

                Back Wall (top)
          (0,D)+------------------+(W,D)
              | Pos 4      Pos 3 |
          Left|                  | Door (glass)
          Wall|                  |
              | Pos 1      Pos 2 |
          (0,0)+------------------+(W,0)
                Fixed Panel (glass)
        """
        # DoorSide=Right base mapping
        # Edge 1 = along X (y=0 in shelf local), Edge 2 = along Y (x=0 in shelf local)
        mapping_right = {
            "Position 1": {
                "origin": App.Vector(0, 0, 0),
                "rotation": 0,
                "edge1_surface": "glass",   # fixed panel at y=0
                "edge2_surface": "wall",    # left wall at x=0
            },
            "Position 2": {
                "origin": App.Vector(width, 0, 0),
                "rotation": 90,
                "edge1_surface": "glass",   # door at x=W
                "edge2_surface": "glass",   # fixed panel at y=0
            },
            "Position 3": {
                "origin": App.Vector(width, depth, 0),
                "rotation": 180,
                "edge1_surface": "wall",    # back wall at y=D
                "edge2_surface": "glass",   # door at x=W
            },
            "Position 4": {
                "origin": App.Vector(0, depth, 0),
                "rotation": 270,
                "edge1_surface": "wall",    # left wall at x=0
                "edge2_surface": "wall",    # back wall at y=D
            },
        }

        # DoorSide=Left: door on left (x=0), fixed panel on right (x=W)
        mapping_left = {
            "Position 1": {
                "origin": App.Vector(0, 0, 0),
                "rotation": 0,
                "edge1_surface": "glass",   # fixed panel at y=0
                "edge2_surface": "glass",   # door at x=0
            },
            "Position 2": {
                "origin": App.Vector(width, 0, 0),
                "rotation": 90,
                "edge1_surface": "wall",    # right wall at x=W
                "edge2_surface": "glass",   # fixed panel at y=0
            },
            "Position 3": {
                "origin": App.Vector(width, depth, 0),
                "rotation": 180,
                "edge1_surface": "wall",    # back wall at y=D
                "edge2_surface": "wall",    # right wall at x=W
            },
            "Position 4": {
                "origin": App.Vector(0, depth, 0),
                "rotation": 270,
                "edge1_surface": "glass",   # door at x=0
                "edge2_surface": "wall",    # back wall at y=D
            },
        }

        mapping = mapping_right if door_right else mapping_left
        return mapping.get(position, mapping["Position 4"])

    def _updateGlassShelf(self, part_obj, vs, door_right, width, depth,
                          height, thickness):
        """Create or update the glass shelf and its two clamps."""
        info = self._getShelfCornerInfo(
            vs.ShelfPosition, door_right, width, depth, thickness,
        )

        # --- Shelf ---
        if not self._hasChild(part_obj, "GlassShelf"):
            self._addChild(part_obj, "GlassShelf", GlassShelfChild, _setupGlassVP)

        shelf = self._getChild(part_obj, "GlassShelf")
        if shelf is None:
            return

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

        # Clamp 1 on edge 1 (along X), positioned edge_length - inset from corner
        clamp1 = self._getChild(part_obj, "ShelfClamp1")
        if clamp1:
            clamp1.ClampType = SHELF_CLAMP_MAPPING[info["edge1_surface"]]
            import math
            rad = math.radians(rot)
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
        """Filter MountingType, ClosingSeal, and set ClosingAgainst on the door."""
        constraints = getCornerDoorConstraints(closes_on_panel)

        if hasattr(door_vs, "MountingType"):
            self._filterEnum(door_vs, "MountingType", constraints["mounting_types"])

        if hasattr(door_vs, "ClosingSeal"):
            self._filterEnum(door_vs, "ClosingSeal", constraints["seal_options"])

        if hasattr(door_vs, "ClosingAgainst"):
            door_vs.ClosingAgainst = constraints["closing_against"]

    # ------------------------------------------------------------------
    # execute
    # ------------------------------------------------------------------

    def assemblyExecute(self, part_obj):
        vs = self._getVarSet(part_obj)
        if vs is None:
            return

        self._ensureLayout(part_obj, vs)

        width = vs.Width.Value
        depth = vs.Depth.Value
        height = vs.Height.Value
        thickness = vs.GlassThickness.Value

        if width <= 0 or depth <= 0 or height <= 0 or thickness <= 0:
            App.Console.PrintError("Invalid enclosure dimensions\n")
            return

        door_right = vs.DoorSide == "Right"
        fixed_panel_width = width if door_right else depth

        # --- Apply door constraints & seal deductions ---
        # Determine what the door closes against: the fixed/return panel,
        # an inline panel, or the wall.
        fixed_panel_seal_ded = 0.0
        closing_inline_role = None       # "CornerInline" or "WallInline"

        layout = vs.InlinePanelLayout
        has_corner_inline = layout in ("Corner Side", "Both Sides")
        has_wall_inline = layout in ("Wall Side", "Both Sides")

        door = self._getChild(part_obj, "DoorPanel")
        if door:
            door_vs = self._getNestedVarSet(door)
            if door_vs and hasattr(door_vs, "HingeSide"):
                closes_on_panel = vs.DoorSide == vs.HingeSide
                self._applyDoorConstraints(door_vs, closes_on_panel)

                # Check if an inline panel intercepts the closing side
                if closes_on_panel and has_corner_inline:
                    # Door closes toward corner → corner inline intercepts
                    closing_inline_role = "CornerInline"
                    if hasattr(door_vs, "ClosingAgainst"):
                        door_vs.ClosingAgainst = "Inline Panel"
                elif not closes_on_panel and has_wall_inline:
                    # Door closes toward wall → wall inline intercepts
                    closing_inline_role = "WallInline"
                    if hasattr(door_vs, "ClosingAgainst"):
                        door_vs.ClosingAgainst = "Inline Panel"

                # Seal deduction for the fixed/return panel.
                # Only applies when the door closes directly on the
                # fixed panel (no inline in between).  When an inline
                # intercepts, the door's own deduction (from
                # DOOR_SEAL_DEDUCTIONS["Inline Panel"]) already gives
                # the correct gap — no panel-side deduction needed.
                if not closing_inline_role and closes_on_panel:
                    is_magnet = (
                        hasattr(door_vs, "ClosingSeal")
                        and door_vs.ClosingSeal in (
                            "90/180 Magnet Seal", "135 Magnet Seal",
                            "180 Flat Magnet Seal",
                        )
                    )
                    if is_magnet:
                        fixed_panel_seal_ded = (
                            getReturnPanelMagnetDeduction(thickness)
                        )

        # --- Update fixed panel ---
        fixed = self._getChild(part_obj, "FixedPanel")
        if fixed:
            fixed_vs = self._getNestedVarSet(fixed)
            if fixed_vs:
                fixed_vs.Width = fixed_panel_width
                fixed_vs.Height = height
                fixed_vs.Thickness = thickness
                if hasattr(fixed_vs, "SealDeduction"):
                    fixed_vs.SealDeduction = fixed_panel_seal_ded
                if hasattr(fixed_vs, "GlassType"):
                    fixed_vs.GlassType = vs.GlassType
                if hasattr(fixed_vs, "HardwareFinish"):
                    fixed_vs.HardwareFinish = vs.HardwareFinish
            if door_right:
                fixed_vs.WallMountEdge = "Left"
                fixed.Placement = App.Placement(
                    App.Vector(0, 0, 0),
                    App.Rotation(App.Vector(0, 0, 1), 0)
                )
            else:
                fixed_vs.WallMountEdge = "Right"
                fixed.Placement = App.Placement(
                    App.Vector(width, 0, 0),
                    App.Rotation(App.Vector(0, 0, 1), 90)
                )

        # --- Inline panel layout ---
        self._ensureInlinePanels(part_obj, layout)

        wall_ret_w = (
            vs.WallInlineWidth.Value
            if layout in ("Wall Side", "Both Sides") else 0
        )
        corner_ret_w = (
            vs.CornerInlineWidth.Value
            if layout in ("Corner Side", "Both Sides") else 0
        )

        # Door-side wall span (excludes glass thickness at corner junction)
        door_wall_span = (depth - thickness) if door_right else (width - thickness)
        door_width = door_wall_span - wall_ret_w - corner_ret_w

        if door_width <= 0:
            App.Console.PrintError(
                "CornerEnclosure: inline panels leave no room for the door\n"
            )
            return

        # --- Inline panel on hinge side → lock mounting type ---
        hinge_side = vs.HingeSide
        hinge_on_corner = (
            (door_right and hinge_side == "Left")
            or (not door_right and hinge_side == "Right")
        )
        inline_on_hinge = (
            (hinge_on_corner and corner_ret_w > 0)
            or (not hinge_on_corner and wall_ret_w > 0)
        )

        # --- Update door panel ---
        door = self._getChild(part_obj, "DoorPanel")
        if door:
            door_vs = self._getNestedVarSet(door)
            if door_vs:
                door_vs.Width = door_width
                door_vs.Height = height
                door_vs.Thickness = thickness
                if hasattr(door_vs, "HingeSide"):
                    door_vs.HingeSide = vs.HingeSide
                if inline_on_hinge and hasattr(door_vs, "MountingType"):
                    self._filterEnum(
                        door_vs, "MountingType",
                        ["Glass Mounted", "Pivot"],
                    )
                if hasattr(door_vs, "GlassType"):
                    door_vs.GlassType = vs.GlassType
                if hasattr(door_vs, "HardwareFinish"):
                    door_vs.HardwareFinish = vs.HardwareFinish
            if door_right:
                door.Placement = App.Placement(
                    App.Vector(width, thickness + corner_ret_w, 0),
                    App.Rotation(App.Vector(0, 0, 1), 90)
                )
            else:
                door.Placement = App.Placement(
                    App.Vector(wall_ret_w, 0, 0),
                    App.Rotation(App.Vector(0, 0, 1), 0)
                )

        # --- Helper to configure an inline panel ---
        def _configInline(role, panel_width, wall_mount_edge, placement,
                          corner_inline=False):
            panel = self._getChild(part_obj, role)
            if panel is None:
                return
            panel_vs = self._getNestedVarSet(panel)
            if panel_vs:
                panel_vs.Width = panel_width
                panel_vs.Height = height
                panel_vs.Thickness = thickness
                panel_vs.WallMountEdge = wall_mount_edge
                if corner_inline:
                    if hasattr(panel_vs, "WallHardware"):
                        panel_vs.WallHardware = "Clamp"
                    if hasattr(panel_vs, "WallClampType"):
                        self._filterEnum(
                            panel_vs, "WallClampType", ["90DEG_G2G_Clamp"],
                        )
                if hasattr(panel_vs, "SealDeduction"):
                    panel_vs.SealDeduction = 0.0
                if hasattr(panel_vs, "GlassType"):
                    panel_vs.GlassType = vs.GlassType
                if hasattr(panel_vs, "HardwareFinish"):
                    panel_vs.HardwareFinish = vs.HardwareFinish
            panel.Placement = placement

        # --- Position inline panels ---
        rot90 = App.Rotation(App.Vector(0, 0, 1), 90)
        rot0 = App.Rotation(App.Vector(0, 0, 1), 0)

        if door_right:
            # Door wall runs along Y axis at x=width, rotated 90°
            if layout in ("Corner Side", "Both Sides"):
                _configInline(
                    "CornerInline", corner_ret_w, "Left",
                    App.Placement(App.Vector(width, thickness, 0), rot90),
                    corner_inline=True,
                )
            if layout in ("Wall Side", "Both Sides"):
                _configInline(
                    "WallInline", wall_ret_w, "Right",
                    App.Placement(
                        App.Vector(width, depth - wall_ret_w, 0), rot90
                    ),
                )
        else:
            # Door wall runs along X axis at y=0, no rotation
            if layout in ("Wall Side", "Both Sides"):
                _configInline(
                    "WallInline", wall_ret_w, "Left",
                    App.Placement(App.Vector(0, 0, 0), rot0),
                )
            if layout in ("Corner Side", "Both Sides"):
                _configInline(
                    "CornerInline", corner_ret_w, "Right",
                    App.Placement(
                        App.Vector(width - thickness - corner_ret_w, 0, 0),
                        rot0,
                    ),
                    corner_inline=True,
                )

        # --- Support bar ---
        if vs.ShowSupportBar:
            self._updateSupportBar(
                part_obj, vs, door_right, width, depth, height, thickness,
            )
        else:
            if self._hasChild(part_obj, "SupportBar"):
                self._removeChild(part_obj, "SupportBar")

        # --- Glass shelf ---
        # Shelf cannot be placed in corners adjacent to the door,
        # unless an inline panel separates the shelf from the door.
        if door_right:
            allowed_shelf = ["Position 1", "Position 4"]
            if has_corner_inline:
                allowed_shelf.append("Position 2")
            if has_wall_inline:
                allowed_shelf.append("Position 3")
        else:
            allowed_shelf = ["Position 2", "Position 3"]
            if has_corner_inline:
                allowed_shelf.append("Position 1")
            if has_wall_inline:
                allowed_shelf.append("Position 4")
        self._filterEnum(vs, "ShelfPosition", allowed_shelf)

        if vs.ShowGlassShelf:
            self._updateGlassShelf(
                part_obj, vs, door_right, width, depth, height, thickness,
            )
        else:
            if self._hasChild(part_obj, "GlassShelf"):
                self._removeChild(part_obj, "GlassShelf")
            self._syncChildCount(part_obj, "ShelfClamp", 0, ClampChild)

        # --- Hardware finish propagation ---
        self._updateAllHardwareFinish(part_obj, vs.HardwareFinish)

        # --- Validate panel-to-panel gap (fixed panel ↔ door panel) ---
        gap = thickness
        valid, msg = validatePanelToPanelGap(gap)
        if not valid:
            App.Console.PrintWarning(f"CornerEnclosure: {msg}\n")

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
