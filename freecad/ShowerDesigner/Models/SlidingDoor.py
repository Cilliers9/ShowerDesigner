# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Sliding shower door with track-based mechanism.

This module provides a SlidingDoor class that extends GlassPanel with
track hardware, roller placement, and support for single and bypass configurations.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.GlassPanel import GlassPanel
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    TRACK_PROFILES,
    ROLLER_SPECS,
    BOTTOM_GUIDE_SPECS,
)
from freecad.ShowerDesigner.Models.Handle import createHandleShape


class SlidingDoor(GlassPanel):
    """
    Parametric sliding shower door with track and roller hardware.

    Extends the base GlassPanel with sliding door-specific properties including
    track type, panel count (for bypass configuration), roller visualization,
    and calculated travel/opening widths.
    """

    def __init__(self, obj):
        """
        Initialize the sliding door with track and hardware properties.

        Args:
            obj: FreeCAD document object
        """
        # Initialize base GlassPanel
        super().__init__(obj)

        # Override attachment type to Sliding
        obj.AttachmentType = "Sliding"

        # Door configuration properties
        obj.addProperty(
            "App::PropertyInteger",
            "PanelCount",
            "Door Configuration",
            "Number of panels (1=single, 2=bypass)"
        )
        obj.PanelCount = 1

        obj.addProperty(
            "App::PropertyEnumeration",
            "TrackType",
            "Door Configuration",
            "Type of sliding track system"
        )
        obj.TrackType = ["Edge", "City", "Ezy", "Soft-Close"]
        obj.TrackType = "Edge"

        obj.addProperty(
            "App::PropertyEnumeration",
            "SlideDirection",
            "Door Configuration",
            "Direction the door slides when opening"
        )
        obj.SlideDirection = ["Left", "Right"]
        obj.SlideDirection = "Right"

        obj.addProperty(
            "App::PropertyLength",
            "OverlapWidth",
            "Door Configuration",
            "Overlap width for bypass doors (mm)"
        ).OverlapWidth = 50

        # Track hardware properties
        obj.addProperty(
            "App::PropertyEnumeration",
            "RollerType",
            "Track Hardware",
            "Type of roller mechanism"
        )
        obj.RollerType = ["Standard", "Soft-Close"]
        obj.RollerType = "Standard"

        obj.addProperty(
            "App::PropertyEnumeration",
            "TrackFinish",
            "Track Hardware",
            "Finish/color of track hardware"
        )
        obj.TrackFinish = ["Chrome", "Brushed-Nickel", "Matte-Black"]
        obj.TrackFinish = "Chrome"

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
            "Show track and roller hardware in 3D view"
        ).ShowHardware = True

        # Calculated properties (read-only)
        obj.addProperty(
            "App::PropertyLength",
            "TrackLength",
            "Calculated",
            "Total length of the top track (read-only)"
        )
        obj.setEditorMode("TrackLength", 1)  # Make read-only

        obj.addProperty(
            "App::PropertyLength",
            "TrackHeight",
            "Calculated",
            "Height of the top track profile (read-only)"
        )
        obj.setEditorMode("TrackHeight", 1)  # Make read-only

        obj.addProperty(
            "App::PropertyLength",
            "TravelDistance",
            "Calculated",
            "How far the door can slide (read-only)"
        )
        obj.setEditorMode("TravelDistance", 1)  # Make read-only

        obj.addProperty(
            "App::PropertyLength",
            "OpeningWidth",
            "Calculated",
            "Clear opening when fully open (read-only)"
        )
        obj.setEditorMode("OpeningWidth", 1)  # Make read-only

    def execute(self, obj):
        """
        Rebuild the geometry when properties change.

        Creates the glass panel(s) and adds track/roller visualization if enabled.

        Args:
            obj: FreeCAD document object
        """
        # Get dimensions
        width = obj.Width.Value
        height = obj.Height.Value
        thickness = obj.Thickness.Value
        panel_count = max(1, min(2, obj.PanelCount))

        # Validate dimensions
        if width <= 0 or height <= 0 or thickness <= 0:
            App.Console.PrintError("Invalid door dimensions\n")
            return

        shapes = []

        # Create glass panel(s)
        if panel_count == 1:
            # Single panel
            panel = Part.makeBox(width, thickness, height)
            shapes.append(panel)
        else:
            # Bypass (2 panels)
            overlap = obj.OverlapWidth.Value
            panel1 = Part.makeBox(width, thickness, height)
            shapes.append(panel1)

            # Second panel offset by overlap
            panel2 = Part.makeBox(width, thickness, height)
            panel2.translate(App.Vector(width - overlap, thickness + 25, 0))
            shapes.append(panel2)

        # Add hardware if enabled
        if obj.ShowHardware:
            # Add top track
            track = self._createTopTrack(obj)
            if track:
                shapes.append(track)

            # Add bottom guide
            guide = self._createBottomGuide(obj)
            if guide:
                shapes.append(guide)

            # Add rollers
            rollers = self._createRollers(obj)
            shapes.extend(rollers)

            # Add handle
            handle = self._createHandle(obj)
            if handle:
                shapes.append(handle)

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
        self._updateSlidingProperties(obj)

    def _calculateTrackLength(self, obj):
        """
        Calculate total track length based on panel configuration.

        Single panel: Panel width + 50mm clearance each side
        Bypass: Panel width * 2 - OverlapWidth + clearances

        Args:
            obj: FreeCAD document object

        Returns:
            Track length in mm
        """
        width = obj.Width.Value
        panel_count = max(1, min(2, obj.PanelCount))
        clearance = 50  # 50mm clearance on each side

        if panel_count == 1:
            return width * 2 + clearance * 2
        else:
            overlap = obj.OverlapWidth.Value
            return width * 3 - overlap + clearance * 2

    def _createTopTrack(self, obj):
        """
        Create top track profile shape.

        Args:
            obj: FreeCAD document object

        Returns:
            Part.Shape for the track, or None
        """
        try:
            track_type = obj.TrackType
            track_spec = TRACK_PROFILES.get(track_type, TRACK_PROFILES["Edge"])
            track_width = track_spec["width"]
            track_height = track_spec["height"]
            sliding_direction = obj.SlideDirection

            track_length = self._calculateTrackLength(obj)
            height = obj.Height.Value
            thickness = obj.Thickness.Value

            # Create track as extruded box (U-channel profile simplified to box)
            track = Part.makeBox(track_length, track_width, track_height)

            # Position at top of panel, Centered based on sliding direction
            if sliding_direction == "Right":
                x_offset = -50  # Start 50mm before panel
            else: #Left
                x_offset = -track_length / 2
            y_offset = thickness / 2 - track_width / 2
            z_offset = height + 5  # 5mm above glass

            track.translate(App.Vector(x_offset, y_offset, z_offset))
            return track

        except Exception as e:
            App.Console.PrintWarning(f"Error creating track: {e}\n")
            return None

    def _createBottomGuide(self, obj):
        """
        Create bottom floor guide channel.

        Args:
            obj: FreeCAD document object

        Returns:
            Part.Shape for the guide, or None
        """
        try:
            track_length = self._calculateTrackLength(obj)
            thickness = obj.Thickness.Value
            sliding_direction = obj.SlideDirection

            guide_width = BOTTOM_GUIDE_SPECS["width"]
            guide_height = BOTTOM_GUIDE_SPECS["height"]

            guide = Part.makeBox(track_length, guide_width, guide_height)

            # Position at floor level, Centered based on sliding direction
            if sliding_direction == "Right":
                x_offset = -50  # Start 50mm before panel
            else: #Left
                x_offset = -track_length / 2
            y_offset = thickness / 2 - guide_width / 2
            z_offset = -guide_height  # Below floor level

            guide.translate(App.Vector(x_offset, y_offset, z_offset))
            return guide

        except Exception as e:
            App.Console.PrintWarning(f"Error creating bottom guide: {e}\n")
            return None

    def _createRollers(self, obj):
        """
        Create roller hardware visualization.

        Args:
            obj: FreeCAD document object

        Returns:
            List of Part shapes for rollers
        """
        rollers = []

        try:
            width = obj.Width.Value
            height = obj.Height.Value
            thickness = obj.Thickness.Value
            panel_count = max(1, min(2, obj.PanelCount))

            roller_type = obj.RollerType if hasattr(obj, "RollerType") else "Standard"
            roller_spec = ROLLER_SPECS.get(roller_type, ROLLER_SPECS["Standard"])
            roller_radius = roller_spec["radius"]
            roller_height = roller_spec["height"]

            # Rollers at panel edges (top)
            for panel_idx in range(panel_count):
                if panel_idx == 0:
                    # First panel
                    x_positions = [20, width - 20]  # 20mm from edges
                    y_offset = thickness / 2
                else:
                    # Second panel (offset for bypass)
                    overlap = obj.OverlapWidth.Value
                    base_x = width - overlap
                    x_positions = [base_x + 20, base_x + width - 20]
                    y_offset = thickness / 2 + thickness + 5

                z_pos = height + 5 + 15  # Above track

                for x_pos in x_positions:
                    roller = Part.makeCylinder(
                        roller_radius,
                        roller_height,
                        App.Vector(x_pos, y_offset, z_pos),
                        App.Vector(0, 0, 1)
                    )
                    rollers.append(roller)

        except Exception as e:
            App.Console.PrintWarning(f"Error creating rollers: {e}\n")

        return rollers

    def _calculateHandlePosition(self, obj):
        """
        Calculate handle position based on slide direction.

        Handle is placed on the leading edge (the edge the user grabs to slide).

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
        slide_direction = obj.SlideDirection

        # Handle on the leading edge (opposite to slide direction)
        if slide_direction == "Right":
            x_pos = handle_offset
        else:  # Left
            x_pos = width - handle_offset

        y_pos = thickness / 2
        z_pos = handle_height

        return App.Vector(x_pos, y_pos, z_pos)

    def _createHandle(self, obj):
        """
        Create handle hardware visualization using shared shape function.

        Args:
            obj: FreeCAD document object

        Returns:
            Part.Shape or None if HandleType is "None"
        """
        if obj.HandleType == "None":
            return None

        try:
            handle_pos = self._calculateHandlePosition(obj)
            length = obj.HandleLength.Value if obj.HandleType == "Bar" else None
            return createHandleShape(obj.HandleType, length, handle_pos)
        except Exception as e:
            App.Console.PrintWarning(f"Error creating handle: {e}\n")
            return None

    def _updateSlidingProperties(self, obj):
        """
        Update sliding-specific calculated properties.

        Args:
            obj: FreeCAD document object
        """
        try:
            width = obj.Width.Value
            panel_count = max(1, min(2, obj.PanelCount))
            overlap = obj.OverlapWidth.Value

            # Track length
            track_length = self._calculateTrackLength(obj)
            if hasattr(obj, "TrackLength"):
                obj.TrackLength = track_length

            # Track height from profile
            track_type = obj.TrackType
            track_spec = TRACK_PROFILES.get(track_type, TRACK_PROFILES["Edge"])
            if hasattr(obj, "TrackHeight"):
                obj.TrackHeight = track_spec["height"]

            # Travel distance
            if panel_count == 1:
                travel = width
            else:
                travel = width - overlap
            if hasattr(obj, "TravelDistance"):
                obj.TravelDistance = travel

            # Opening width
            if panel_count == 1:
                opening = width
            else:
                opening = width - overlap
            if hasattr(obj, "OpeningWidth"):
                obj.OpeningWidth = opening

        except Exception as e:
            App.Console.PrintWarning(f"Error updating sliding properties: {e}\n")

    def onChanged(self, obj, prop):
        """
        Called when a property changes.

        Enforces constraints:
        - PanelCount=2 only allowed with Soft-Close track type
        - Ezy track type only compatible with 10mm or 12mm glass

        Args:
            obj: FreeCAD document object
            prop: Name of the property that changed
        """
        # Call parent onChanged
        super().onChanged(obj, prop)

        # Validate PanelCount (1-2)
        if prop == "PanelCount":
            if hasattr(obj, "PanelCount"):
                if obj.PanelCount < 1:
                    obj.PanelCount = 1
                elif obj.PanelCount > 2:
                    obj.PanelCount = 2

                # Enforce: Only Soft-Close supports 2-panel bypass
                if hasattr(obj, "TrackType"):
                    if obj.PanelCount == 2 and obj.TrackType != "Soft-Close":
                        App.Console.PrintWarning(
                            "Bypass (2-panel) configuration requires Soft-Close track. "
                            "Resetting PanelCount to 1.\n"
                        )
                        obj.PanelCount = 1

        # Validate TrackType changes
        if prop == "TrackType":
            if hasattr(obj, "TrackType") and hasattr(obj, "PanelCount"):
                # If switching away from Soft-Close with 2 panels, reset to 1
                if obj.TrackType != "Soft-Close" and obj.PanelCount == 2:
                    App.Console.PrintWarning(
                        f"{obj.TrackType} track only supports single panel. "
                        "Resetting PanelCount to 1.\n"
                    )
                    obj.PanelCount = 1

            # Ezy track only compatible with 10mm or 12mm glass
            if hasattr(obj, "TrackType") and hasattr(obj, "Thickness"):
                if obj.TrackType == "Ezy":
                    thickness_mm = int(obj.Thickness.Value)
                    if thickness_mm not in [10, 12]:
                        App.Console.PrintWarning(
                            f"Ezy track only compatible with 10mm or 12mm glass "
                            f"(current: {thickness_mm}mm). Consider changing glass "
                            "thickness or track type.\n"
                        )

        # Validate thickness for Ezy track
        if prop == "Thickness":
            if hasattr(obj, "TrackType") and hasattr(obj, "Thickness"):
                if obj.TrackType == "Ezy":
                    thickness_mm = int(obj.Thickness.Value)
                    if thickness_mm not in [10, 12]:
                        App.Console.PrintWarning(
                            f"Ezy track only compatible with 10mm or 12mm glass "
                            f"(current: {thickness_mm}mm). Consider changing glass "
                            "thickness or track type.\n"
                        )

        # Validate handle height (reasonable range)
        if prop == "HandleHeight":
            if hasattr(obj, "HandleHeight"):
                if obj.HandleHeight.Value < 300:
                    obj.HandleHeight = 300
                elif obj.HandleHeight.Value > 1800:
                    obj.HandleHeight = 1800

        # Validate overlap width
        if prop == "OverlapWidth":
            if hasattr(obj, "OverlapWidth") and hasattr(obj, "Width"):
                if obj.OverlapWidth.Value < 20:
                    obj.OverlapWidth = 20
                elif obj.OverlapWidth.Value > obj.Width.Value / 2:
                    obj.OverlapWidth = obj.Width.Value / 2


def createSlidingDoor(name="SlidingDoor"):
    """
    Create a new sliding door in the active document.

    Args:
        name: Name for the door object (default: "SlidingDoor")

    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    obj = doc.addObject("Part::FeaturePython", name)
    SlidingDoor(obj)

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

    App.Console.PrintMessage(f"Sliding door '{name}' created\n")
    return obj
