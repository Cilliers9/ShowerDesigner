# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Fixed glass panel assembly — App::Part containing glass + mounting hardware.

Each piece of hardware (clamp, channel) is its own Part::FeaturePython
with an individual ViewProvider, allowing independent display control.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.AssemblyBase import AssemblyController
from freecad.ShowerDesigner.Models.ChildProxies import (
    GlassChild,
    ClampChild,
    ChannelChild,
)
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    CLAMP_SPECS,
    CLAMP_PLACEMENT_DEFAULTS,
    CHANNEL_SPECS,
    HARDWARE_FINISHES,
)
from freecad.ShowerDesigner.Data.GlassSpecs import GLASS_SPECS


def _setupGlassVP(obj):
    """Attach the glass ViewProvider to a child object."""
    from freecad.ShowerDesigner.Models.GlassPanelViewProvider import setupViewProvider
    setupViewProvider(obj)


def _setupHardwareVP(obj, finish="Chrome"):
    """Attach the hardware ViewProvider to a child object."""
    from freecad.ShowerDesigner.Models.HardwareViewProvider import (
        setupHardwareViewProvider,
    )
    setupHardwareViewProvider(obj, finish)


class FixedPanelAssembly(AssemblyController):
    """
    Assembly controller for a fixed glass panel with mounting hardware.

    Creates an App::Part containing:
      - VarSet with all user-editable properties
      - Glass child (Part::FeaturePython + GlassPanelViewProvider)
      - Wall clamp/channel children (Part::FeaturePython + HardwareViewProvider)
      - Floor clamp/channel children (Part::FeaturePython + HardwareViewProvider)
    """

    def __init__(self, part_obj):
        super().__init__(part_obj)
        vs = self._getOrCreateVarSet(part_obj)
        self._setupVarSetProperties(vs)
        self._addChild(part_obj, "Glass", GlassChild, _setupGlassVP)

    # ------------------------------------------------------------------
    # VarSet property setup
    # ------------------------------------------------------------------

    def _setupVarSetProperties(self, vs):
        """Add all user-facing properties to the VarSet."""
        # Dimensions
        vs.addProperty(
            "App::PropertyLength", "Width", "Dimensions", "Panel width"
        ).Width = 900
        vs.addProperty(
            "App::PropertyLength", "Height", "Dimensions", "Panel height"
        ).Height = 2000
        vs.addProperty(
            "App::PropertyLength", "Thickness", "Dimensions", "Glass thickness"
        ).Thickness = 8

        # Glass
        vs.addProperty(
            "App::PropertyEnumeration", "GlassType", "Glass", "Type of glass"
        )
        vs.GlassType = ["Clear", "Frosted", "Bronze", "Grey", "Reeded", "Low-Iron"]
        vs.GlassType = "Clear"
        vs.addProperty(
            "App::PropertyEnumeration", "EdgeFinish", "Glass", "Edge finish type"
        )
        vs.EdgeFinish = ["Bright_Polish", "Dull_Polish"]
        vs.EdgeFinish = "Bright_Polish"
        vs.addProperty(
            "App::PropertyEnumeration", "TemperType", "Glass", "Tempering type"
        )
        vs.TemperType = ["Tempered", "Laminated", "None"]
        vs.TemperType = "Tempered"

        # Wall hardware
        vs.addProperty(
            "App::PropertyEnumeration", "WallHardware", "Wall Hardware",
            "Type of wall mounting hardware"
        )
        vs.WallHardware = ["None", "Channel", "Clamp"]
        vs.WallHardware = "Clamp"
        vs.addProperty(
            "App::PropertyEnumeration", "WallMountEdge", "Wall Hardware",
            "Which edge(s) to mount wall hardware"
        )
        vs.WallMountEdge = ["Left", "Right", "Both"]
        vs.WallMountEdge = "Left"
        vs.addProperty(
            "App::PropertyInteger", "WallClampCount", "Wall Hardware",
            "Number of wall clamps per edge (1-4)"
        ).WallClampCount = 2
        vs.addProperty(
            "App::PropertyLength", "WallClampOffsetTop", "Wall Hardware",
            "Distance from top edge to first clamp"
        ).WallClampOffsetTop = CLAMP_PLACEMENT_DEFAULTS["wall_offset_top"]
        vs.addProperty(
            "App::PropertyLength", "WallClampOffsetBottom", "Wall Hardware",
            "Distance from bottom edge to last clamp"
        ).WallClampOffsetBottom = CLAMP_PLACEMENT_DEFAULTS["wall_offset_bottom"]
        vs.addProperty(
            "App::PropertyEnumeration", "WallClampType", "Wall Hardware",
            "Shape of wall clamp"
        )
        vs.WallClampType = list(CLAMP_SPECS.keys())
        vs.WallClampType = "L_Clamp"

        # Channel dimensions
        vs.addProperty(
            "App::PropertyLength", "ChannelWidth", "Wall Hardware",
            "Width of wall channel (if using channel)"
        ).ChannelWidth = CHANNEL_SPECS["wall"]["width"]
        vs.addProperty(
            "App::PropertyLength", "ChannelDepth", "Wall Hardware",
            "Depth of wall channel"
        ).ChannelDepth = CHANNEL_SPECS["wall"]["depth"]

        # Floor hardware
        vs.addProperty(
            "App::PropertyEnumeration", "FloorHardware", "Floor Hardware",
            "Type of floor mounting hardware"
        )
        vs.FloorHardware = ["None", "Channel", "Clamp"]
        vs.FloorHardware = "Clamp"
        vs.addProperty(
            "App::PropertyInteger", "FloorClampCount", "Floor Hardware",
            "Number of floor clamps (1-4)"
        ).FloorClampCount = 2
        vs.addProperty(
            "App::PropertyLength", "FloorClampOffsetLeft", "Floor Hardware",
            "Distance from left edge to first clamp"
        ).FloorClampOffsetLeft = CLAMP_PLACEMENT_DEFAULTS["floor_offset_start"]
        vs.addProperty(
            "App::PropertyLength", "FloorClampOffsetRight", "Floor Hardware",
            "Distance from right edge to last clamp"
        ).FloorClampOffsetRight = CLAMP_PLACEMENT_DEFAULTS["floor_offset_end"]
        vs.addProperty(
            "App::PropertyEnumeration", "FloorClampType", "Floor Hardware",
            "Shape of floor clamp"
        )
        vs.FloorClampType = list(CLAMP_SPECS.keys())
        vs.FloorClampType = "U_Clamp"

        # Hardware display
        vs.addProperty(
            "App::PropertyEnumeration", "HardwareFinish", "Hardware Display",
            "Finish for all hardware"
        )
        vs.HardwareFinish = HARDWARE_FINISHES[:]
        vs.HardwareFinish = "Chrome"
        vs.addProperty(
            "App::PropertyBool", "ShowHardware", "Hardware Display",
            "Show hardware in 3D view"
        ).ShowHardware = True

        # Calculated (read-only)
        vs.addProperty(
            "App::PropertyFloat", "Weight", "Calculated",
            "Weight of the panel in kg"
        )
        vs.setEditorMode("Weight", 1)
        vs.addProperty(
            "App::PropertyFloat", "Area", "Calculated",
            "Area of the panel in m²"
        )
        vs.setEditorMode("Area", 1)

    # ------------------------------------------------------------------
    # execute — rebuild children when VarSet changes
    # ------------------------------------------------------------------

    def assemblyExecute(self, part_obj):
        vs = self._getVarSet(part_obj)
        if vs is None:
            return

        width = vs.Width.Value
        height = vs.Height.Value
        thickness = vs.Thickness.Value
        if width <= 0 or height <= 0 or thickness <= 0:
            App.Console.PrintError("Invalid panel dimensions\n")
            return

        # --- Update Glass child ---
        glass = self._getChild(part_obj, "Glass")
        if glass:
            glass.Width = width
            glass.Height = height
            glass.Thickness = thickness
            if hasattr(glass, "GlassType"):
                glass.GlassType = vs.GlassType

        show_hw = vs.ShowHardware
        finish = vs.HardwareFinish

        # --- Wall hardware ---
        if show_hw and vs.WallHardware == "Clamp":
            self._updateWallClamps(part_obj, vs)
        else:
            self._removeWallClamps(part_obj)

        if show_hw and vs.WallHardware == "Channel":
            self._updateWallChannels(part_obj, vs)
        else:
            self._removeWallChannels(part_obj)

        # --- Floor hardware ---
        if show_hw and vs.FloorHardware == "Clamp":
            self._updateFloorClamps(part_obj, vs)
        else:
            self._removeFloorClamps(part_obj)

        if show_hw and vs.FloorHardware == "Channel":
            self._updateFloorChannel(part_obj, vs)
        else:
            self._removeFloorChannel(part_obj)

        # --- Hardware finish ---
        self._updateAllHardwareFinish(part_obj, finish)

        # --- Calculated properties ---
        self._updateCalculatedProperties(vs)

    # ------------------------------------------------------------------
    # Wall clamp management
    # ------------------------------------------------------------------

    def _updateWallClamps(self, part_obj, vs):
        width = vs.Width.Value
        height = vs.Height.Value
        clamp_count = vs.WallClampCount
        mount_edge = vs.WallMountEdge
        clamp_type = vs.WallClampType

        # Total clamps needed across edges
        edges = []
        if mount_edge in ["Left", "Both"]:
            edges.append("Left")
        if mount_edge in ["Right", "Both"]:
            edges.append("Right")

        # Calculate vertical positions
        positions = _calculateClampPositions(
            height, clamp_count,
            vs.WallClampOffsetTop.Value, vs.WallClampOffsetBottom.Value
        )

        # Determine total child count and sync
        total = len(edges) * len(positions)
        self._syncChildCount(
            part_obj, "WallClamp", total, ClampChild,
            lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
        )

        # Position each clamp
        idx = 1
        for edge in edges:
            for z_pos in positions:
                child = self._getChild(part_obj, f"WallClamp{idx}")
                if child:
                    child.ClampType = clamp_type
                    if edge == "Left":
                        rot = App.Rotation(App.Vector(0, 1, 0), 90)
                        child.Placement = App.Placement(
                            App.Vector(20, 0, z_pos), rot
                        )
                    else:  # Right
                        rot = App.Rotation(App.Vector(0, 1, 0), -90)
                        child.Placement = App.Placement(
                            App.Vector(width - 20, 0, z_pos), rot
                        )
                idx += 1

    def _removeWallClamps(self, part_obj):
        self._syncChildCount(part_obj, "WallClamp", 0, ClampChild)

    # ------------------------------------------------------------------
    # Wall channel management
    # ------------------------------------------------------------------

    def _updateWallChannels(self, part_obj, vs):
        width = vs.Width.Value
        height = vs.Height.Value
        mount_edge = vs.WallMountEdge

        edges = []
        if mount_edge in ["Left", "Both"]:
            edges.append("Left")
        if mount_edge in ["Right", "Both"]:
            edges.append("Right")

        self._syncChildCount(
            part_obj, "WallChannel", len(edges), ChannelChild,
            lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
        )

        for i, edge in enumerate(edges):
            child = self._getChild(part_obj, f"WallChannel{i + 1}")
            if child:
                child.ChannelLocation = "wall"
                child.ChannelLength = height
                channel_depth = vs.ChannelDepth.Value
                if edge == "Left":
                    child.Placement = App.Placement(
                        App.Vector(-2, 13, 0),
                        App.Rotation(App.Vector(0,0,1), -90)
                    )
                else:
                    child.Placement = App.Placement(
                        App.Vector(width + 2, -2, 0),
                        App.Rotation(App.Vector(0,0,1), 90)
                    )

    def _removeWallChannels(self, part_obj):
        self._syncChildCount(part_obj, "WallChannel", 0, ChannelChild)

    # ------------------------------------------------------------------
    # Floor clamp management
    # ------------------------------------------------------------------

    def _updateFloorClamps(self, part_obj, vs):
        width = vs.Width.Value
        clamp_count = vs.FloorClampCount
        clamp_type = vs.FloorClampType

        positions = _calculateClampPositions(
            width, clamp_count,
            vs.FloorClampOffsetLeft.Value, vs.FloorClampOffsetRight.Value
        )

        self._syncChildCount(
            part_obj, "FloorClamp", len(positions), ClampChild,
            lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
        )

        for i, x_pos in enumerate(positions):
            child = self._getChild(part_obj, f"FloorClamp{i + 1}")
            if child:
                child.ClampType = clamp_type
                child.Placement = App.Placement(
                    App.Vector(x_pos, 0, 20), App.Rotation()
                )

    def _removeFloorClamps(self, part_obj):
        self._syncChildCount(part_obj, "FloorClamp", 0, ClampChild)

    # ------------------------------------------------------------------
    # Floor channel management
    # ------------------------------------------------------------------

    def _updateFloorChannel(self, part_obj, vs):
        width = vs.Width.Value

        if not self._hasChild(part_obj, "FloorChannel1"):
            self._addChild(
                part_obj, "FloorChannel1", ChannelChild,
                lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
            )

        child = self._getChild(part_obj, "FloorChannel1")
        if child:
            child.ChannelLocation = "floor"
            child.ChannelLength = width
            child.Placement = App.Placement(
                App.Vector(0, -2, -2),
                App.Rotation(0, 90, 0)
            )
            child.Placement.Rotation = App.Rotation(App.Vector(1, 0, 0), 90) * child.Placement.Rotation

    def _removeFloorChannel(self, part_obj):
        if self._hasChild(part_obj, "FloorChannel1"):
            self._removeChild(part_obj, "FloorChannel1")

    # ------------------------------------------------------------------
    # Calculated properties
    # ------------------------------------------------------------------

    def _updateCalculatedProperties(self, vs):
        try:
            width_m = vs.Width.Value / 1000.0
            height_m = vs.Height.Value / 1000.0
            area = width_m * height_m
            if hasattr(vs, "Area"):
                vs.Area = area

            thickness_key = f"{int(vs.Thickness.Value)}mm"
            if thickness_key in GLASS_SPECS:
                weight_per_m2 = GLASS_SPECS[thickness_key]["weight_kg_m2"]
                weight = area * weight_per_m2
            else:
                weight = area * 2.5 * vs.Thickness.Value
            if hasattr(vs, "Weight"):
                vs.Weight = weight
        except Exception as e:
            App.Console.PrintWarning(
                f"Error updating calculated properties: {e}\n"
            )

    # ------------------------------------------------------------------
    # onChanged — validate VarSet property edits
    # ------------------------------------------------------------------

    def assemblyOnChanged(self, part_obj, prop):
        pass


# ======================================================================
# Helper
# ======================================================================

def _calculateClampPositions(total_length, clamp_count, offset_start, offset_end):
    """Calculate evenly-spaced clamp positions along a length."""
    if clamp_count == 1:
        return [total_length / 2]
    elif clamp_count == 2:
        return [offset_start, total_length - offset_end]
    else:
        available = total_length - offset_start - offset_end
        spacing = available / (clamp_count - 1)
        return [offset_start + i * spacing for i in range(clamp_count)]


# ======================================================================
# Factory function
# ======================================================================

def createFixedPanel(name="FixedPanel"):
    """
    Create a new fixed panel assembly in the active document.

    Args:
        name: Name for the assembly (default: "FixedPanel")

    Returns:
        App::Part assembly object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    part = doc.addObject("App::Part", name)
    FixedPanelAssembly(part)

    doc.recompute()
    App.Console.PrintMessage(f"Fixed panel '{name}' created\n")
    return part
