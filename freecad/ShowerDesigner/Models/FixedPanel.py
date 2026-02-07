# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Fixed glass panel with wall and floor hardware mounting.

This module provides a FixedPanel class that extends GlassPanel with
wall and floor mounting hardware (channels or clamps).
"""
from ssl import ALERT_DESCRIPTION_NO_RENEGOTIATION

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.GlassPanel import GlassPanel
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    CLAMP_SPECS,
    CLAMP_PLACEMENT_DEFAULTS,
    CHANNEL_SPECS,
)
from freecad.ShowerDesigner.Models.Clamp import createClampShape


class FixedPanel(GlassPanel):
    """
    Parametric fixed glass panel with wall and floor mounting hardware.

    Extends the base GlassPanel with hardware mounting options including
    wall channels/clamps and floor channels/clamps for secure installation.
    """

    def __init__(self, obj):
        """
        Initialize the fixed panel object with hardware properties.

        Args:
            obj: FreeCAD document object
        """
        # Initialize base GlassPanel
        super().__init__(obj)

        # Override attachment type to Fixed
        obj.AttachmentType = "Fixed"

        # Wall hardware properties
        obj.addProperty(
            "App::PropertyEnumeration",
            "WallHardware",
            "Wall Hardware",
            "Type of wall mounting hardware"
        )
        obj.WallHardware = ["None", "Channel", "Clamp"]
        obj.WallHardware = "Clamp"

        obj.addProperty(
            "App::PropertyEnumeration",
            "WallMountEdge",
            "Wall Hardware",
            "Which edge(s) to mount wall hardware"
        )
        obj.WallMountEdge = ["Left", "Right", "Both"]
        obj.WallMountEdge = "Left"

        obj.addProperty(
            "App::PropertyInteger",
            "WallClampCount",
            "Wall Hardware",
            "Number of wall clamps per edge (1-4)"
        )
        obj.WallClampCount = 2

        obj.addProperty(
            "App::PropertyLength",
            "WallClampOffsetTop",
            "Wall Hardware",
            "Distance from top edge to first clamp"
        ).WallClampOffsetTop = CLAMP_PLACEMENT_DEFAULTS["wall_offset_top"]

        obj.addProperty(
            "App::PropertyLength",
            "WallClampOffsetBottom",
            "Wall Hardware",
            "Distance from bottom edge to last clamp"
        ).WallClampOffsetBottom = CLAMP_PLACEMENT_DEFAULTS["wall_offset_bottom"]

        obj.addProperty(
            "App::PropertyLength",
            "ChannelWidth",
            "Wall Hardware",
            "Width of wall channel (if using channel)"
        ).ChannelWidth = CHANNEL_SPECS["wall"]["width"]

        obj.addProperty(
            "App::PropertyLength",
            "ChannelDepth",
            "Wall Hardware",
            "Depth of wall channel"
        ).ChannelDepth = CHANNEL_SPECS["wall"]["depth"]

        # Floor hardware properties
        obj.addProperty(
            "App::PropertyEnumeration",
            "FloorHardware",
            "Floor Hardware",
            "Type of floor mounting hardware"
        )
        obj.FloorHardware = ["None", "Channel", "Clamp"]
        obj.FloorHardware = "Clamp"

        obj.addProperty(
            "App::PropertyInteger",
            "FloorClampCount",
            "Floor Hardware",
            "Number of floor clamps (1-2)"
        )
        obj.FloorClampCount = 2

        obj.addProperty(
            "App::PropertyLength",
            "FloorClampOffsetLeft",
            "Floor Hardware",
            "Distance from left edge to first clamp"
        ).FloorClampOffsetLeft = CLAMP_PLACEMENT_DEFAULTS["floor_offset_start"]

        obj.addProperty(
            "App::PropertyLength",
            "FloorClampOffsetRight",
            "Floor Hardware",
            "Distance from right edge to last clamp"
        ).FloorClampOffsetRight = CLAMP_PLACEMENT_DEFAULTS["floor_offset_end"]

        obj.addProperty(
            "App::PropertyEnumeration",
            "WallClampType",
            "Wall Hardware",
            "Shape of wall clamp"
        )
        obj.WallClampType = list(CLAMP_SPECS.keys())
        obj.WallClampType = "L_Clamp"

        obj.addProperty(
            "App::PropertyEnumeration",
            "FloorClampType",
            "Floor Hardware",
            "Shape of floor clamp"
        )
        obj.FloorClampType = list(CLAMP_SPECS.keys())
        obj.FloorClampType = "U_Clamp"

        _clamp_bb = CLAMP_SPECS["L_Clamp"]["bounding_box"]

        obj.addProperty(
            "App::PropertyLength",
            "ClampDiameter",
            "Hardware Display",
            "Width/diameter of clamp hardware"
        ).ClampDiameter = _clamp_bb["width"]

        obj.addProperty(
            "App::PropertyLength",
            "ClampThickness",
            "Hardware Display",
            "Depth/thickness of clamp hardware"
        ).ClampThickness = _clamp_bb["depth"]

        obj.addProperty(
            "App::PropertyBool",
            "ShowHardware",
            "Hardware Display",
            "Show hardware in 3D view"
        ).ShowHardware = True

    def execute(self, obj):
        """
        Rebuild the geometry when properties change.

        Creates the glass panel and adds hardware visualization if enabled.

        Args:
            obj: FreeCAD document object
        """
        # Get dimensions
        width = obj.Width.Value
        height = obj.Height.Value
        thickness = obj.Thickness.Value

        # Validate dimensions
        if width <= 0 or height <= 0 or thickness <= 0:
            App.Console.PrintError("Invalid panel dimensions\n")
            return

        # Create the glass panel shape
        panel = Part.makeBox(width, thickness, height)
        shapes = [panel]

        # Add hardware if enabled
        if obj.ShowHardware:
            # Add wall hardware
            if obj.WallHardware == "Channel":
                wall_channels = self._createWallChannel(obj)
                shapes.extend(wall_channels)
            elif obj.WallHardware == "Clamp":
                wall_clamps = self._createWallClamps(obj)
                shapes.extend(wall_clamps)

            # Add floor hardware
            if obj.FloorHardware == "Channel":
                floor_channel = self._createFloorChannel(obj)
                if floor_channel:
                    shapes.append(floor_channel)
            elif obj.FloorHardware == "Clamp":
                floor_clamps = self._createFloorClamps(obj)
                shapes.extend(floor_clamps)

        # Combine all shapes
        if len(shapes) > 1:
            compound = Part.makeCompound(shapes)
            obj.Shape = compound
        else:
            obj.Shape = shapes[0]

        # Apply position and rotation
        obj.Placement.Base = obj.Position
        new_rotation = App.Rotation(App.Vector(0, 0, 1), obj.Rotation)
        obj.Placement.Rotation = new_rotation

        # Update calculated properties
        self._updateCalculatedProperties(obj)

    def _createWallChannel(self, obj):
        """
        Create wall-mounted channel hardware on left, right, or both edges.

        Args:
            obj: FreeCAD document object

        Returns:
            List of Part shapes for wall channels
        """
        channels = []

        try:
            width = obj.Width.Value
            height = obj.Height.Value
            thickness = obj.Thickness.Value
            channel_width = obj.ChannelWidth.Value
            channel_depth = obj.ChannelDepth.Value
            mount_edge = obj.WallMountEdge

            def create_single_channel():
                """Create a single U-channel profile."""
                # Outer rectangle
                outer = Part.makeBox(channel_width, channel_depth, height)
                # Inner rectangle (slightly smaller for wall thickness)
                inner_width = channel_width - 4  # 3mm on each side
                inner_depth = channel_depth - 2  # back wall
                inner = Part.makeBox(inner_width, inner_depth, height)
                inner.translate(App.Vector(2, 2, 0))
                # Subtract inner from outer to create channel
                return outer.cut(inner)

            # Create channel(s) based on mount edge setting
            if mount_edge in ["Left", "Both"]:
                left_channel = create_single_channel()
                # Position at left edge of panel
                left_channel.translate(App.Vector(-2,
                                                  2, 0))
                channels.append(left_channel)

            if mount_edge in ["Right", "Both"]:
                right_channel = create_single_channel()
                # Position at right edge of panel
                right_channel.translate(App.Vector(width - channel_depth + 2,
                                                   2, 0))
                channels.append(right_channel)

        except Exception as e:
            App.Console.PrintWarning(f"Error creating wall channel: {e}\n")

        return channels

    def _createWallClamps(self, obj):
        """
        Create wall-mounted clamp hardware on left, right, or both edges.

        Args:
            obj: FreeCAD document object

        Returns:
            List of Part shapes for wall clamps
        """
        clamps = []

        try:
            width = obj.Width.Value
            height = obj.Height.Value
            thickness = obj.Thickness.Value
            clamp_count = max(1, min(4, obj.WallClampCount))
            offset_top = obj.WallClampOffsetTop.Value
            offset_bottom = obj.WallClampOffsetBottom.Value
            mount_edge = obj.WallMountEdge

            # Calculate clamp positions along height
            positions = self._calculateClampPositions(
                height, clamp_count, offset_top, offset_bottom
            )

            clamp_w = obj.ClampDiameter.Value
            clamp_d = obj.ClampThickness.Value
            clamp_h = clamp_w  # Square face

            # Create clamps on left edge
            if mount_edge in ["Left", "Both"]:
                for z_pos in positions:
                    clamp = createClampShape(obj.WallClampType)
                    rotation = App.Rotation(App.Vector(0, 1, 0), 90)
                    clamp.Placement.Rotation = rotation
                    clamp.translate(App.Vector(20,
                                              0,
                                              z_pos))
                    clamps.append(clamp)

            # Create clamps on right edge
            if mount_edge in ["Right", "Both"]:
                for z_pos in positions:
                    clamp = createClampShape(obj.WallClampType)
                    rotation = App.Rotation(App.Vector(0, 1, 0), -90)
                    clamp.Placement.Rotation = rotation
                    clamp.translate(App.Vector(width - 20,
                                              0,
                                              z_pos))
                    clamps.append(clamp)

        except Exception as e:
            App.Console.PrintWarning(f"Error creating wall clamps: {e}\n")

        return clamps

    def _createFloorChannel(self, obj):
        """
        Create floor-mounted channel hardware.

        Args:
            obj: FreeCAD document object

        Returns:
            Part shape for floor channel
        """
        try:
            width = obj.Width.Value
            thickness = obj.Thickness.Value
            channel_width = obj.ChannelWidth.Value
            channel_depth = obj.ChannelDepth.Value

            # Create U-channel profile oriented horizontally
            # Outer rectangle
            outer = Part.makeBox(width, channel_depth, channel_width)
            # Inner rectangle
            inner_width = width - 4  # 3mm on each side
            inner_depth = channel_depth - 2  # back wall
            inner = Part.makeBox(inner_width, inner_depth, channel_width)
            inner.translate(App.Vector(0, 2, 2))

            # Subtract inner from outer to create channel
            channel = outer.cut(inner)

            # Position at bottom of panel
            channel.translate(App.Vector(0, -2, -2))

            return channel

        except Exception as e:
            App.Console.PrintWarning(f"Error creating floor channel: {e}\n")
            return None

    def _createFloorClamps(self, obj):
        """
        Create floor-mounted clamp hardware.

        Args:
            obj: FreeCAD document object

        Returns:
            List of Part shapes for floor clamps
        """
        clamps = []

        try:
            width = obj.Width.Value
            thickness = obj.Thickness.Value
            clamp_count = max(2, min(4, obj.FloorClampCount))
            offset_left = obj.FloorClampOffsetLeft.Value
            offset_right = obj.FloorClampOffsetRight.Value
            diameter = obj.ClampDiameter.Value
            clamp_thickness = obj.ClampThickness.Value

            # Calculate clamp positions along width
            positions = self._calculateClampPositions(
                width, clamp_count, offset_left, offset_right
            )

            clamp_w = diameter
            clamp_d = clamp_thickness

            # Create clamp at each position
            for x_pos in positions:
                clamp = createClampShape(obj.FloorClampType)
                clamp.translate(App.Vector(x_pos,
                                          0,
                                          20))
                clamps.append(clamp)

        except Exception as e:
            App.Console.PrintWarning(f"Error creating floor clamps: {e}\n")

        return clamps

    def _calculateClampPositions(self, total_length, clamp_count,
                                 offset_start, offset_end):
        """
        Calculate evenly-spaced clamp positions.

        Args:
            total_length: Total length to distribute clamps across
            clamp_count: Number of clamps
            offset_start: Offset from start edge
            offset_end: Offset from end edge

        Returns:
            List of positions in mm
        """
        positions = []

        if clamp_count == 1:
            # Single clamp at center
            positions.append(total_length / 2)
        elif clamp_count == 2:
            # Two clamps at offsets from edges
            positions.append(offset_start)
            positions.append(total_length - offset_end)
        else:
            # Multiple clamps evenly distributed
            # Calculate available space
            available_length = total_length - offset_start - offset_end

            # Distribute evenly
            if clamp_count > 2:
                spacing = available_length / (clamp_count - 1)
                for i in range(clamp_count):
                    positions.append(offset_start + i * spacing)

        return positions

    def onChanged(self, obj, prop):
        """
        Called when a property changes.

        Args:
            obj: FreeCAD document object
            prop: Name of the property that changed
        """
        # Call parent onChanged
        super().onChanged(obj, prop)

        # Validate clamp counts
        if prop == "WallClampCount":
            if hasattr(obj, "WallClampCount"):
                if obj.WallClampCount < 2:
                    obj.WallClampCount = 2
                elif obj.WallClampCount > 4:
                    obj.WallClampCount = 4

        if prop == "FloorClampCount":
            if hasattr(obj, "FloorClampCount"):
                if obj.FloorClampCount < 2:
                    obj.FloorClampCount = 2
                elif obj.FloorClampCount > 4:
                    obj.FloorClampCount = 4


def createFixedPanel(name="FixedPanel"):
    """
    Create a new fixed panel in the active document.

    Args:
        name: Name for the panel object (default: "FixedPanel")

    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    obj = doc.addObject("Part::FeaturePython", name)
    FixedPanel(obj)

    if App.GuiUp:
        # Use custom view provider if available
        try:
            from freecad.ShowerDesigner.Models.GlassPanelViewProvider import setupViewProvider
            setupViewProvider(obj)
        except:
            # Fallback to simple view provider
            obj.ViewObject.Proxy = 0
            obj.ViewObject.Transparency = 70

    doc.recompute()

    App.Console.PrintMessage(f"Fixed panel '{name}' created\n")
    return obj
