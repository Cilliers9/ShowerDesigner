# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Hinged shower door with swing direction and hardware mounting.

This module provides a HingedDoor class that extends GlassPanel with
hinge hardware, handle placement, and swing arc visualization.
"""

import FreeCAD as App
import Part
import math
from freecad.ShowerDesigner.Models.GlassPanel import GlassPanel


class HingedDoor(GlassPanel):
    """
    Parametric hinged shower door with hardware and swing visualization.

    Extends the base GlassPanel with door-specific properties including
    swing direction, hinge placement, handle positioning, and optional
    swing arc visualization for clearance checking.
    """

    def __init__(self, obj):
        """
        Initialize the hinged door with hardware properties.

        Args:
            obj: FreeCAD document object
        """
        # Initialize base GlassPanel
        super().__init__(obj)

        # Override attachment type to Hinged
        obj.AttachmentType = "Hinged"

        # Door configuration properties
        obj.addProperty(
            "App::PropertyEnumeration",
            "SwingDirection",
            "Door Configuration",
            "Direction the door swings when opening"
        )
        obj.SwingDirection = ["Inward", "Outward"]
        obj.SwingDirection = "Inward"

        obj.addProperty(
            "App::PropertyEnumeration",
            "HingeSide",
            "Door Configuration",
            "Which side the hinges are mounted"
        )
        obj.HingeSide = ["Left", "Right"]
        obj.HingeSide = "Left"

        obj.addProperty(
            "App::PropertyAngle",
            "OpeningAngle",
            "Door Configuration",
            "Maximum opening angle (max 110 degrees)"
        ).OpeningAngle = 90

        # Hinge hardware properties
        obj.addProperty(
            "App::PropertyInteger",
            "HingeCount",
            "Hinge Hardware",
            "Number of hinges (2-3)"
        )
        obj.HingeCount = 2

        obj.addProperty(
            "App::PropertyLength",
            "HingeOffsetTop",
            "Hinge Hardware",
            "Distance from top edge to top hinge"
        ).HingeOffsetTop = 300  # mm

        obj.addProperty(
            "App::PropertyLength",
            "HingeOffsetBottom",
            "Hinge Hardware",
            "Distance from bottom edge to bottom hinge"
        ).HingeOffsetBottom = 300  # mm

        obj.addProperty(
            "App::PropertyEnumeration",
            "HingeFinish",
            "Hinge Hardware",
            "Finish/color of hinge hardware"
        )
        obj.HingeFinish = ["Chrome", "Brushed-Nickel", "Matte-Black", "Gold"]
        obj.HingeFinish = "Chrome"

        # Handle hardware properties
        obj.addProperty(
            "App::PropertyEnumeration",
            "HandleType",
            "Handle Hardware",
            "Type of door handle"
        )
        obj.HandleType = ["None", "Knob", "Bar", "Pull"]
        obj.HandleType = "Bar"

        obj.addProperty(
            "App::PropertyLength",
            "HandleHeight",
            "Handle Hardware",
            "Height of handle from floor"
        ).HandleHeight = 1050  # mm - ergonomic height

        obj.addProperty(
            "App::PropertyLength",
            "HandleOffset",
            "Handle Hardware",
            "Distance from handle to door edge"
        ).HandleOffset = 75  # mm

        obj.addProperty(
            "App::PropertyLength",
            "HandleLength",
            "Handle Hardware",
            "Length of bar handle (for Bar type)"
        ).HandleLength = 300  # mm

        # Hardware display properties
        obj.addProperty(
            "App::PropertyBool",
            "ShowHardware",
            "Hardware Display",
            "Show hardware in 3D view"
        ).ShowHardware = True

        obj.addProperty(
            "App::PropertyBool",
            "ShowSwingArc",
            "Hardware Display",
            "Show swing arc on floor plane"
        ).ShowSwingArc = False

        obj.addProperty(
            "App::PropertyLength",
            "HingeWidth",
            "Hardware Display",
            "Width of hinge hardware visualization"
        ).HingeWidth = 65  # mm

        obj.addProperty(
            "App::PropertyLength",
            "HingeDepth",
            "Hardware Display",
            "Depth of hinge hardware visualization"
        ).HingeDepth = 20  # mm

        obj.addProperty(
            "App::PropertyLength",
            "HingeHeight",
            "Hardware Display",
            "Height of hinge hardware visualization"
        ).HingeHeight = 90  # mm

        # Calculated properties (read-only)
        obj.addProperty(
            "App::PropertyInteger",
            "RecommendedHingeCount",
            "Calculated",
            "Recommended hinge count based on door weight"
        )
        obj.setEditorMode("RecommendedHingeCount", 1)  # Make read-only

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
            App.Console.PrintError("Invalid door dimensions\n")
            return

        # Create the glass panel shape
        panel = Part.makeBox(width, thickness, height)
        shapes = [panel]

        # Add hardware if enabled
        if obj.ShowHardware:
            # Add hinges
            hinges = self._createHinges(obj)
            shapes.extend(hinges)

            # Add handle
            handle = self._createHandle(obj)
            if handle:
                shapes.append(handle)

        # Add swing arc if enabled
        if obj.ShowSwingArc:
            arc = self._createSwingArc(obj)
            if arc:
                shapes.append(arc)

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
        self._updateRecommendedHingeCount(obj)

    def _calculateHingePositions(self, obj):
        """
        Calculate evenly-spaced hinge positions along the door height.

        Industry standard placement:
        - Top hinge: HingeOffsetTop from top edge
        - Bottom hinge: HingeOffsetBottom from bottom edge
        - Third hinge (if used): centered between top and bottom

        Args:
            obj: FreeCAD document object

        Returns:
            List of Z positions in mm (from bottom of panel)
        """
        height = obj.Height.Value
        offset_top = obj.HingeOffsetTop.Value
        offset_bottom = obj.HingeOffsetBottom.Value
        hinge_count = max(2, min(3, obj.HingeCount))

        positions = []

        # Bottom hinge position
        positions.append(offset_bottom)

        # Top hinge position
        positions.append(height - offset_top)

        # Middle hinge if count is 3
        if hinge_count >= 3:
            middle_z = (offset_bottom + (height - offset_top)) / 2
            positions.insert(1, middle_z)

        return sorted(positions)

    def _createHinges(self, obj):
        """
        Create hinge hardware visualization.

        Args:
            obj: FreeCAD document object

        Returns:
            List of Part shapes for hinges
        """
        hinges = []

        try:
            width = obj.Width.Value
            height = obj.Height.Value
            thickness = obj.Thickness.Value
            hinge_side = obj.HingeSide
            hinge_w = obj.HingeWidth.Value
            hinge_d = obj.HingeDepth.Value
            hinge_h = obj.HingeHeight.Value

            # Calculate hinge positions
            positions = self._calculateHingePositions(obj)

            for z_pos in positions:
                # Create box hinge
                hinge = Part.makeBox(hinge_w, hinge_d, hinge_h)

                # Position based on hinge side
                if hinge_side == "Left":
                    x_pos = -10  # 10 mm from left edge
                else:  # Right
                    x_pos = width - hinge_w + 10  # 10mm from right edge

                y_pos = thickness / 2 - hinge_d / 2
                z_offset = z_pos - hinge_h / 2

                hinge.translate(App.Vector(x_pos, y_pos, z_offset))
                hinges.append(hinge)

        except Exception as e:
            App.Console.PrintWarning(f"Error creating hinges: {e}\n")

        return hinges

    def _calculateHandlePosition(self, obj):
        """
        Calculate handle position based on configuration.

        Handle is always on opposite side from hinges.

        Args:
            obj: FreeCAD document object

        Returns:
            App.Vector for handle center position
        """
        width = obj.Width.Value
        height = obj.Height.Value
        thickness = obj.Thickness.Value
        handle_height = min(obj.HandleHeight.Value, height - 100)
        handle_offset = obj.HandleOffset.Value
        hinge_side = obj.HingeSide

        # X position depends on hinge side (handle is opposite)
        if hinge_side == "Left":
            x_pos = width - handle_offset
        else:  # Right
            x_pos = handle_offset

        # Y position at center of glass thickness
        y_pos = thickness / 2

        # Z position is handle height
        z_pos = handle_height

        return App.Vector(x_pos, y_pos, z_pos)

    def _createHandle(self, obj):
        """
        Create handle hardware visualization.

        Args:
            obj: FreeCAD document object

        Returns:
            Part.Shape or None if HandleType is "None"
        """
        if obj.HandleType == "None":
            return None

        try:
            handle_pos = self._calculateHandlePosition(obj)

            if obj.HandleType == "Knob":
                # Simple cylinder for knob (40mm diameter, 15mm depth)
                handle = Part.makeCylinder(
                    20, 15,
                    App.Vector(handle_pos.x, handle_pos.y, handle_pos.z),
                    App.Vector(0, 1, 0)
                )

            elif obj.HandleType == "Bar":
                # Vertical bar handle
                length = obj.HandleLength.Value
                radius = 12  # Typical bar radius
                start = App.Vector(
                    handle_pos.x,
                    handle_pos.y,
                    handle_pos.z - length / 2
                )
                handle = Part.makeCylinder(radius, length, start, App.Vector(0, 0, 1))

            elif obj.HandleType == "Pull":
                # Vertical pull handle (200mm length)
                length = 200
                radius = 10
                start = App.Vector(
                    handle_pos.x,
                    handle_pos.y,
                    handle_pos.z - length / 2
                )
                handle = Part.makeCylinder(radius, length, start, App.Vector(0, 0, 1))

            else:
                return None

            return handle

        except Exception as e:
            App.Console.PrintWarning(f"Error creating handle: {e}\n")
            return None

    def _createSwingArc(self, obj):
        """
        Create a 2D arc showing the door swing clearance on the floor plane.

        Args:
            obj: FreeCAD document object

        Returns:
            Part.Shape representing the swing arc, or None
        """
        try:
            width = obj.Width.Value
            thickness = obj.Thickness.Value
            opening_angle = obj.OpeningAngle.Value
            hinge_side = obj.HingeSide
            swing_direction = obj.SwingDirection

            # Arc radius is the door width
            radius = width

            # Determine arc center and angles based on configuration
            if hinge_side == "Left":
                center = App.Vector(0, thickness / 2, 0)
                if swing_direction == "Inward":
                    start_angle = 0
                    end_angle = 0 + opening_angle
                else:  # Outward
                    start_angle = 0 - opening_angle
                    end_angle = 0
            else:  # Right
                center = App.Vector(width, thickness / 2, 0)
                if swing_direction == "Inward":
                    start_angle = 180 - opening_angle
                    end_angle = 180
                else:  # Outward
                    start_angle = 180
                    end_angle = 180 + opening_angle

            # Create arc at floor level (Z=0)
            arc = Part.makeCircle(
                radius,
                center,
                App.Vector(0, 0, 1),  # Normal pointing up
                start_angle,
                end_angle
            )

            return arc

        except Exception as e:
            App.Console.PrintWarning(f"Error creating swing arc: {e}\n")
            return None

    def _updateRecommendedHingeCount(self, obj):
        """
        Calculate recommended hinge count based on door weight.

        Industry guidelines:
        - Up to 45kg: 2 hinges sufficient
        - Over 45kg: 3 hinges recommended
        """
        if not hasattr(obj, "Weight") or not hasattr(obj, "RecommendedHingeCount"):
            return

        try:
            weight = obj.Weight
            if weight <= 45:
                obj.RecommendedHingeCount = 2
            else:
                obj.RecommendedHingeCount = 3
        except Exception:
            pass

    def onChanged(self, obj, prop):
        """
        Called when a property changes.

        Args:
            obj: FreeCAD document object
            prop: Name of the property that changed
        """
        # Call parent onChanged
        super().onChanged(obj, prop)

        # Validate hinge count (2-3)
        if prop == "HingeCount":
            if hasattr(obj, "HingeCount"):
                if obj.HingeCount < 2:
                    obj.HingeCount = 2
                elif obj.HingeCount > 3:
                    obj.HingeCount = 3

        # Validate opening angle (max 110)
        if prop == "OpeningAngle":
            if hasattr(obj, "OpeningAngle"):
                if obj.OpeningAngle > 110:
                    obj.OpeningAngle = 110
                elif obj.OpeningAngle < 0:
                    obj.OpeningAngle = 0

        # Validate handle height (reasonable range)
        if prop == "HandleHeight":
            if hasattr(obj, "HandleHeight"):
                if obj.HandleHeight.Value < 300:
                    obj.HandleHeight = 300
                elif obj.HandleHeight.Value > 1800:
                    obj.HandleHeight = 1800


def createHingedDoor(name="HingedDoor"):
    """
    Create a new hinged door in the active document.

    Args:
        name: Name for the door object (default: "HingedDoor")

    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    obj = doc.addObject("Part::FeaturePython", name)
    HingedDoor(obj)

    if App.GuiUp:
        # Use custom view provider if available
        try:
            from freecad.ShowerDesigner.Models.GlassPanelViewProvider import setupViewProvider
            setupViewProvider(obj)
        except Exception:
            # Fallback to simple view provider
            obj.ViewObject.Proxy = 0
            obj.ViewObject.Transparency = 70

    doc.recompute()

    App.Console.PrintMessage(f"Hinged door '{name}' created\n")
    return obj
