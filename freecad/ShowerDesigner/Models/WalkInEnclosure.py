# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Walk-in shower enclosure assembly — App::Part containing one or two fixed
glass panels with optional support bars.

Configurations:
  - Single: one panel along the X axis
  - Double-L: two panels at 90° (L-shape)
  - Double-Parallel: two facing panels with a walkway gap
"""

import math

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.AssemblyBase import AssemblyController
from freecad.ShowerDesigner.Models.ChildProxies import (
    SupportBarChild,
    GlassShelfChild,
    ClampChild,
)
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    SUPPORT_BAR_SPECS,
    HARDWARE_FINISHES,
    GLASS_SHELF_SPECS,
    SHELF_CLAMP_MAPPING,
)


def _setupHardwareVP(obj, finish="Chrome"):
    from freecad.ShowerDesigner.Models.HardwareViewProvider import (
        setupHardwareViewProvider,
    )
    setupHardwareViewProvider(obj, finish)


def _setupGlassVP(obj):
    from freecad.ShowerDesigner.Models.GlassPanelViewProvider import setupViewProvider
    setupViewProvider(obj)


_SUPPORT_BAR_INSET = 75  # mm from free corner edge of fixed panel


class WalkInEnclosureAssembly(AssemblyController):
    """
    Assembly controller for a walk-in shower enclosure.

    Creates an App::Part containing:
      - VarSet with all user-editable properties
      - One or two FixedPanel nested assemblies depending on PanelConfiguration
      - Optional SupportBar child(ren)
    """

    def __init__(self, part_obj):
        super().__init__(part_obj)
        vs = self._getOrCreateVarSet(part_obj)
        self._setupVarSetProperties(vs)
        self._ensurePanel(part_obj, "Panel")
        self._manifest["_panelConfig"] = "Single"

    def _setupVarSetProperties(self, vs):
        # Layout
        vs.addProperty(
            "App::PropertyEnumeration", "PanelConfiguration", "Layout",
            "Panel arrangement"
        )
        vs.PanelConfiguration = ["Single", "Double-L", "Double-Parallel"]
        vs.PanelConfiguration = "Single"
        vs.addProperty(
            "App::PropertyEnumeration", "LJointSide", "Layout",
            "Which end of Panel 1 the L-joint panel attaches to"
        )
        vs.LJointSide = ["Left", "Right"]
        vs.LJointSide = "Left"

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
            "App::PropertyLength", "Depth", "Dimensions",
            "Depth for Double-L arm or Double-Parallel gap"
        ).Depth = 900
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

        # Glass shelf
        vs.addProperty(
            "App::PropertyBool", "ShowGlassShelf", "Glass Shelf",
            "Add a glass shelf"
        ).ShowGlassShelf = False
        vs.addProperty(
            "App::PropertyEnumeration", "ShelfPosition", "Glass Shelf",
            "Where to place the shelf"
        )
        vs.ShelfPosition = ["Position 1", "Position 2"]
        vs.ShelfPosition = "Position 1"
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

    def _ensureLayout(self, part_obj, vs):
        """Rebuild panels when PanelConfiguration changes."""
        wanted = getattr(vs, "PanelConfiguration", "Single")
        current = self._manifest.get("_panelConfig", "Single")
        if current == wanted:
            return

        # Remove all existing panels, support bars, and shelf
        for role in ("Panel", "Panel1", "Panel2"):
            if role in self._manifest:
                self._removeNestedAssembly(part_obj, role)
        for role in ("SupportBar", "SupportBar2"):
            if self._hasChild(part_obj, role):
                self._removeChild(part_obj, role)
        if self._hasChild(part_obj, "GlassShelf"):
            self._removeChild(part_obj, "GlassShelf")
        self._syncChildCount(part_obj, "ShelfClamp", 0, ClampChild)

        # Create panels for new config
        if wanted == "Single":
            self._ensurePanel(part_obj, "Panel")
        else:
            self._ensurePanel(part_obj, "Panel1")
            self._ensurePanel(part_obj, "Panel2")

        self._manifest["_panelConfig"] = wanted

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _propagateToPanel(self, panel, vs, panel_width):
        """Propagate VarSet values to a nested FixedPanel assembly."""
        panel_vs = self._getNestedVarSet(panel)
        if panel_vs is None:
            return
        panel_vs.Width = panel_width
        panel_vs.Height = vs.Height.Value
        panel_vs.Thickness = vs.GlassThickness.Value
        if hasattr(panel_vs, "GlassType"):
            panel_vs.GlassType = vs.GlassType
        if hasattr(panel_vs, "HardwareFinish"):
            panel_vs.HardwareFinish = vs.HardwareFinish

    def _getNestedVarSet(self, part_obj):
        """Get VarSet from a nested assembly."""
        for child in part_obj.Group:
            if child.TypeId == "App::VarSet":
                return child
        return None

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
        depth = getattr(vs, "Depth", None)
        depth = depth.Value if depth is not None else 900

        if width <= 0 or height <= 0 or thickness <= 0:
            App.Console.PrintError("Invalid enclosure dimensions\n")
            return

        # Rebuild panels if configuration changed
        self._ensureLayout(part_obj, vs)

        config = getattr(vs, "PanelConfiguration", "Single")
        l_side = getattr(vs, "LJointSide", "Left")
        finish = vs.HardwareFinish

        if config == "Single":
            panel = self._getChild(part_obj, "Panel")
            if panel:
                self._propagateToPanel(panel, vs, width)
                panel.Placement = App.Placement(
                    App.Vector(0, 0, 0),
                    App.Rotation(App.Vector(0, 0, 1), 0),
                )

        elif config == "Double-L":
            panel1 = self._getChild(part_obj, "Panel1")
            panel2 = self._getChild(part_obj, "Panel2")
            if panel1:
                self._propagateToPanel(panel1, vs, width)
                panel1.Placement = App.Placement(
                    App.Vector(0, 0, 0),
                    App.Rotation(App.Vector(0, 0, 1), 0),
                )
            if panel2:
                self._propagateToPanel(panel2, vs, depth)
                if l_side == "Left":
                    panel2.Placement = App.Placement(
                        App.Vector(0, thickness, 0),
                        App.Rotation(App.Vector(0, 0, 1), 90),
                    )
                else:
                    panel2.Placement = App.Placement(
                        App.Vector(width, thickness, 0),
                        App.Rotation(App.Vector(0, 0, 1), 90),
                    )

        elif config == "Double-Parallel":
            panel1 = self._getChild(part_obj, "Panel1")
            panel2 = self._getChild(part_obj, "Panel2")
            if panel1:
                self._propagateToPanel(panel1, vs, width)
                panel1.Placement = App.Placement(
                    App.Vector(0, 0, 0),
                    App.Rotation(App.Vector(0, 0, 1), 0),
                )
            if panel2:
                self._propagateToPanel(panel2, vs, width)
                panel2.Placement = App.Placement(
                    App.Vector(0, depth, 0),
                    App.Rotation(App.Vector(0, 0, 1), 0),
                )

        # Support bars
        if vs.ShowSupportBar:
            self._updateSupportBars(
                part_obj, vs, config, width, depth, height, thickness, l_side,
            )
        else:
            for role in ("SupportBar", "SupportBar2"):
                if self._hasChild(part_obj, role):
                    self._removeChild(part_obj, role)

        # Glass shelf
        if vs.ShowGlassShelf:
            self._updateGlassShelf(
                part_obj, vs, config, width, depth, thickness, l_side,
            )
        else:
            if self._hasChild(part_obj, "GlassShelf"):
                self._removeChild(part_obj, "GlassShelf")
            self._syncChildCount(part_obj, "ShelfClamp", 0, ClampChild)

        self._updateAllHardwareFinish(part_obj, finish)

    # ------------------------------------------------------------------
    # Support bars
    # ------------------------------------------------------------------

    def _ensureSupportBar(self, part_obj, vs, role):
        """Create a support bar child if it doesn't exist."""
        if not self._hasChild(part_obj, role):
            self._addChild(
                part_obj, role, SupportBarChild,
                lambda obj: _setupHardwareVP(obj, vs.HardwareFinish),
            )
        return self._getChild(part_obj, role)

    def _updateSupportBars(self, part_obj, vs, config, width, depth, height,
                           thickness, l_side="Left"):
        bar_height = vs.SupportBarHeight.Value

        if config == "Double-L":
            # Single perpendicular bar on Panel 1 only (like CornerEnclosure).
            # Sits at top edge of glass, inset 75 mm from the free corner,
            # runs perpendicular to Panel 1 toward the back wall.
            inset = _SUPPORT_BAR_INSET
            bar1 = self._ensureSupportBar(part_obj, vs, "SupportBar")
            if bar1:
                bar1.BarType = vs.SupportBarType
                bar1.Length = depth - thickness
                bar1.Diameter = vs.SupportBarDiameter.Value
                if l_side == "Left":
                    # Panel 2 at x=0; free edge of Panel 1 at x=width
                    bar1.Placement = App.Placement(
                        App.Vector(width - inset, thickness / 2, height),
                        App.Rotation(App.Vector(0, 0, 1), 0),
                    )
                else:
                    # Panel 2 at x=width; free edge of Panel 1 at x=0
                    bar1.Placement = App.Placement(
                        App.Vector(inset, thickness / 2, height),
                        App.Rotation(App.Vector(0, 0, 1), 0),
                    )
            # No second bar for Double-L
            if self._hasChild(part_obj, "SupportBar2"):
                self._removeChild(part_obj, "SupportBar2")

        else:
            # Single / Double-Parallel: horizontal bar along panel top
            bar1 = self._ensureSupportBar(part_obj, vs, "SupportBar")
            if bar1:
                bar1.BarType = vs.SupportBarType
                bar1.Length = width
                bar1.Diameter = vs.SupportBarDiameter.Value
                bar1.Placement = App.Placement(
                    App.Vector(0, thickness / 2, bar_height),
                    App.Rotation(App.Vector(0, 0, 1), 0),
                )

            if config == "Single":
                if self._hasChild(part_obj, "SupportBar2"):
                    self._removeChild(part_obj, "SupportBar2")

            elif config == "Double-Parallel":
                bar2 = self._ensureSupportBar(part_obj, vs, "SupportBar2")
                if bar2:
                    bar2.BarType = vs.SupportBarType
                    bar2.Length = width
                    bar2.Diameter = vs.SupportBarDiameter.Value
                    bar2.Placement = App.Placement(
                        App.Vector(0, depth + thickness / 2, bar_height),
                        App.Rotation(App.Vector(0, 0, 1), 0),
                    )

    # ------------------------------------------------------------------
    # Glass shelf
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

    def _getShelfPositionInfo(self, config, position, width, depth, thickness,
                              l_side="Left"):
        """Return placement info for a shelf at the given position.

        Returns dict with: origin (Vector), rotation (float, degrees around Z),
        edge1_surface ("wall"/"glass"), edge2_surface ("wall"/"glass"),
        and the list of allowed positions for the current config.

        Single panel layout::

                    Back Wall
              (0,D)+----------+(W,D)
                  |            |
            Left  |            |  Right
            Wall  |            |  Wall
                  |            |
              (0,0)+----------+(W,0)
                  Panel (glass)

        Double-L Left layout::

                    Back Wall
              (0,D)+----------+(W,D)
                  |            |
           Panel2 |            |  Right
           (glass)|            |  Wall
              (0,t)+----------+(W,0)
                  Panel1 (glass)

        Double-L Right layout::

                    Back Wall
              (0,D)+----------+(W,D)
                  |            |
            Left  |            | Panel2
            Wall  |            | (glass)
              (0,0)+----------+(W,t)
                  Panel1 (glass)

        Double-Parallel layout::

              (0,D)+----------+(W,D)
                  Panel2 (glass)
            Left  |            |  Right
            Wall  |  Walkway   |  Wall
              (0,0)+----------+(W,0)
                  Panel1 (glass)
        """
        if config == "Single":
            mapping = {
                "Position 1": {
                    "origin": App.Vector(0, 0, 0),
                    "rotation": 0,
                    "edge1_surface": "glass",   # panel at y=0
                    "edge2_surface": "wall",    # left wall at x=0
                },
                "Position 2": {
                    "origin": App.Vector(width, 0, 0),
                    "rotation": 90,
                    "edge1_surface": "wall",    # right wall at x=W
                    "edge2_surface": "glass",   # panel at y=0
                },
            }
            allowed = ["Position 1", "Position 2"]

        elif config == "Double-L":
            if l_side == "Left":
                mapping = {
                    "Position 1": {
                        "origin": App.Vector(0, 0, 0),
                        "rotation": 0,
                        "edge1_surface": "glass",   # panel1 at y=0
                        "edge2_surface": "glass",   # panel2 at x=0
                    },
                    "Position 2": {
                        "origin": App.Vector(width, 0, 0),
                        "rotation": 90,
                        "edge1_surface": "wall",    # right wall at x=W
                        "edge2_surface": "glass",   # panel1 at y=0
                    },
                    "Position 3": {
                        "origin": App.Vector(0, depth, 0),
                        "rotation": 270,
                        "edge1_surface": "glass",   # panel2 at x=0
                        "edge2_surface": "wall",    # back wall at y=D
                    },
                }
            else:  # Right
                mapping = {
                    "Position 1": {
                        "origin": App.Vector(0, 0, 0),
                        "rotation": 0,
                        "edge1_surface": "glass",   # panel1 at y=0
                        "edge2_surface": "wall",    # left wall at x=0
                    },
                    "Position 2": {
                        "origin": App.Vector(width, 0, 0),
                        "rotation": 90,
                        "edge1_surface": "glass",   # panel2 at x=W
                        "edge2_surface": "glass",   # panel1 at y=0
                    },
                    "Position 3": {
                        "origin": App.Vector(width, depth, 0),
                        "rotation": 180,
                        "edge1_surface": "wall",    # back wall at y=D
                        "edge2_surface": "glass",   # panel2 at x=W
                    },
                }
            allowed = ["Position 1", "Position 2", "Position 3"]

        else:  # Double-Parallel
            mapping = {
                "Position 1": {
                    "origin": App.Vector(0, 0, 0),
                    "rotation": 0,
                    "edge1_surface": "glass",   # panel1 at y=0
                    "edge2_surface": "wall",    # left wall at x=0
                },
                "Position 2": {
                    "origin": App.Vector(width, 0, 0),
                    "rotation": 90,
                    "edge1_surface": "wall",    # right wall at x=W
                    "edge2_surface": "glass",   # panel1 at y=0
                },
                "Position 3": {
                    "origin": App.Vector(width, depth, 0),
                    "rotation": 180,
                    "edge1_surface": "glass",   # panel2 at y=D
                    "edge2_surface": "wall",    # right wall at x=W
                },
                "Position 4": {
                    "origin": App.Vector(0, depth, 0),
                    "rotation": 270,
                    "edge1_surface": "wall",    # left wall at x=0
                    "edge2_surface": "glass",   # panel2 at y=D
                },
            }
            allowed = ["Position 1", "Position 2", "Position 3", "Position 4"]

        info = mapping.get(position, mapping[allowed[0]])
        info["allowed"] = allowed
        return info

    def _updateGlassShelf(self, part_obj, vs, config, width, depth, thickness,
                          l_side="Left"):
        """Create or update the glass shelf and its two clamps."""
        info = self._getShelfPositionInfo(
            config, vs.ShelfPosition, width, depth, thickness, l_side,
        )

        # Filter shelf positions to those valid for this config
        self._filterEnum(vs, "ShelfPosition", info["allowed"])

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
        rad = math.radians(rot)

        # Clamp 1 on edge 1
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

        # Clamp 2 on edge 2
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
