# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Bi-fold shower door with two-panel folding mechanism.

This module provides a BiFoldDoor class that extends GlassPanel with
bi-fold hinge hardware, handle placement, and folded position visualization.
Bi-fold hinges open 180 degrees in the primary direction and 45 degrees
in the secondary direction. Left/Right hinge configuration determines
whether the door folds inward or outward.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.GlassPanel import GlassPanel


# Bi-fold hinge specifications
# Left/Right configuration determines fold direction (inward/outward)
# Primary direction: 180 deg, secondary direction: 45 deg
BIFOLD_HINGE_SPECS = {
    "Left": {
        "primary_angle": 180,
        "secondary_angle": 45,
        "fold_direction": "Inward",
    },
    "Right": {
        "primary_angle": 180,
        "secondary_angle": 45,
        "fold_direction": "Outward",
    },
}


class BiFoldDoor(GlassPanel):
    """
    Parametric bi-fold shower door with bi-fold hinge hardware.

    Extends the base GlassPanel with bi-fold door-specific properties including
    hinge configuration (Left/Right), handle positioning, and optional folded
    position ghost for clearance checking. Bi-fold hinges allow 180 degrees
    opening in the primary direction and 45 degrees in the secondary direction.
    """

    def __init__(self, obj):
        # Initialize base GlassPanel
        super().__init__(obj)

        # Override attachment type to Hinged
        obj.AttachmentType = "Hinged"

        # Door configuration properties
        obj.addProperty(
            "App::PropertyEnumeration",
            "HingeConfiguration",
            "Door Configuration",
            "Bi-fold hinge hand (Left=Inward, Right=Outward)"
        )
        obj.HingeConfiguration = ["Left", "Right"]
        obj.HingeConfiguration = "Left"

        obj.addProperty(
            "App::PropertyEnumeration",
            "FoldDirection",
            "Door Configuration",
            "Direction the door folds (derived from hinge configuration)"
        )
        obj.FoldDirection = ["Inward", "Outward"]
        obj.FoldDirection = "Inward"
        obj.setEditorMode("FoldDirection", 1)  # Read-only

        obj.addProperty(
            "App::PropertyEnumeration",
            "HingeSide",
            "Door Configuration",
            "Which side is attached to the wall"
        )
        obj.HingeSide = ["Left", "Right"]
        obj.HingeSide = "Left"

        obj.addProperty(
            "App::PropertyAngle",
            "FoldAngle",
            "Door Configuration",
            "Current fold angle (0=closed, positive=primary, negative=secondary)"
        ).FoldAngle = 0

        # Hinge hardware properties
        obj.addProperty(
            "App::PropertyEnumeration",
            "HingeFinish",
            "Hinge Hardware",
            "Finish/color of bi-fold hinge hardware"
        )
        obj.HingeFinish = ["Chrome", "Brushed-Nickel", "Matte-Black", "Gold"]
        obj.HingeFinish = "Chrome"

        obj.addProperty(
            "App::PropertyInteger",
            "HingeCount",
            "Hinge Hardware",
            "Number of bi-fold hinges at fold joint (2-3)"
        ).HingeCount = 2

        obj.addProperty(
            "App::PropertyLength",
            "HingeWidth",
            "Hinge Hardware",
            "Width of hinge hardware visualization"
        ).HingeWidth = 65  # mm

        obj.addProperty(
            "App::PropertyLength",
            "HingeDepth",
            "Hinge Hardware",
            "Depth of hinge hardware visualization"
        ).HingeDepth = 20  # mm

        obj.addProperty(
            "App::PropertyLength",
            "HingeHeight",
            "Hinge Hardware",
            "Height of hinge hardware visualization"
        ).HingeHeight = 90  # mm

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
            "ShowFoldedPosition",
            "Hardware Display",
            "Show folded position ghost"
        ).ShowFoldedPosition = False

        # Calculated properties (read-only)
        obj.addProperty(
            "App::PropertyLength",
            "PanelWidth",
            "Calculated",
            "Width of each panel (half total width, read-only)"
        )
        obj.setEditorMode("PanelWidth", 1)

        obj.addProperty(
            "App::PropertyLength",
            "FoldedWidth",
            "Calculated",
            "Width of folded stack (read-only)"
        )
        obj.setEditorMode("FoldedWidth", 1)

        obj.addProperty(
            "App::PropertyLength",
            "OpeningWidth",
            "Calculated",
            "Clear opening when fully folded (read-only)"
        )
        obj.setEditorMode("OpeningWidth", 1)

        obj.addProperty(
            "App::PropertyLength",
            "ClearanceDepth",
            "Calculated",
            "Depth clearance needed for folding (read-only)"
        )
        obj.setEditorMode("ClearanceDepth", 1)

        obj.addProperty(
            "App::PropertyAngle",
            "MaxFoldAngle",
            "Calculated",
            "Maximum fold angle in primary direction (read-only)"
        )
        obj.setEditorMode("MaxFoldAngle", 1)

    def execute(self, obj):
        """Rebuild the geometry when properties change."""
        width = obj.Width.Value
        height = obj.Height.Value
        thickness = obj.Thickness.Value

        if width < 400 or height <= 0 or thickness <= 0:
            App.Console.PrintError("Invalid bi-fold door dimensions (min width: 400mm)\n")
            return

        shapes = []

        # Create the two glass panels
        panels = self._createPanels(obj)
        shapes.extend(panels)

        # Add hardware if enabled
        if obj.ShowHardware:
            # Wall-side hinges (attach wall panel to wall/fixed panel)
            wall_hinges = self._createWallHinges(obj)
            shapes.extend(wall_hinges)

            # Bi-fold hinges at the center fold joint
            fold_hinges = self._createBiFoldHinges(obj)
            shapes.extend(fold_hinges)

            handle = self._createHandle(obj)
            if handle:
                shapes.append(handle)

        # Add folded position ghost if enabled
        if obj.ShowFoldedPosition:
            ghost = self._createFoldedGhost(obj)
            if ghost:
                shapes.append(ghost)

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
        self._updateBifoldProperties(obj)

    def _createPanels(self, obj):
        """Create two glass panels side by side."""
        width = obj.Width.Value
        height = obj.Height.Value
        thickness = obj.Thickness.Value
        panel_width = width / 2

        panels = []

        # Panel 1 (wall-side)
        panel1 = Part.makeBox(panel_width, thickness, height)
        panels.append(panel1)

        # Panel 2 (free-side)
        panel2 = Part.makeBox(panel_width, thickness, height)
        panel2.translate(App.Vector(panel_width, 0, 0))
        panels.append(panel2)

        return panels

    def _calculateHingePositions(self, obj):
        """
        Calculate evenly-spaced hinge positions along the door height.

        Returns:
            List of Z positions in mm (from bottom of panel)
        """
        height = obj.Height.Value
        hinge_count = max(2, min(3, obj.HingeCount))
        offset_top = 300  # mm from top
        offset_bottom = 300  # mm from bottom

        positions = [offset_bottom, height - offset_top]

        if hinge_count >= 3:
            middle_z = (offset_bottom + (height - offset_top)) / 2
            positions.insert(1, middle_z)

        return sorted(positions)

    def _createWallHinges(self, obj):
        """
        Create wall-side hinges that attach the wall panel to the wall or fixed panel.

        Two hinges (top and bottom) on the hinge side edge of the wall panel.
        """
        hinges = []

        try:
            width = obj.Width.Value
            thickness = obj.Thickness.Value
            hinge_side = obj.HingeSide
            hinge_w = obj.HingeWidth.Value
            hinge_d = obj.HingeDepth.Value
            hinge_h = obj.HingeHeight.Value

            # Wall hinges always at top and bottom (2 hinges)
            z_positions = self._calculateHingePositions(obj)
            # Use only top and bottom positions for wall hinges
            wall_z = [z_positions[0], z_positions[-1]]

            y_pos = thickness / 2 - hinge_d / 2

            for z_pos in wall_z:
                hinge = Part.makeBox(hinge_w, hinge_d, hinge_h)
                z_offset = z_pos - hinge_h / 2

                if hinge_side == "Left":
                    x_pos = -hinge_w / 2
                else:
                    x_pos = width - hinge_w / 2

                hinge.translate(App.Vector(x_pos, y_pos, z_offset))
                hinges.append(hinge)

        except Exception as e:
            App.Console.PrintWarning(f"Error creating wall hinges: {e}\n")

        return hinges

    def _createBiFoldHinges(self, obj):
        """
        Create bi-fold hinge hardware at the center fold joint.

        Bi-fold hinges are box-shaped and mounted at the fold point
        between the two panels.
        """
        hinges = []

        try:
            width = obj.Width.Value
            thickness = obj.Thickness.Value
            panel_width = width / 2
            hinge_w = obj.HingeWidth.Value
            hinge_d = obj.HingeDepth.Value
            hinge_h = obj.HingeHeight.Value

            z_positions = self._calculateHingePositions(obj)

            # Center hinge at the fold joint between the two panels
            center_x = panel_width - hinge_w / 2
            y_pos = thickness / 2 - hinge_d / 2

            for z_pos in z_positions:
                hinge = Part.makeBox(hinge_w, hinge_d, hinge_h)
                z_offset = z_pos - hinge_h / 2
                hinge.translate(App.Vector(center_x, y_pos, z_offset))
                hinges.append(hinge)

        except Exception as e:
            App.Console.PrintWarning(f"Error creating bi-fold hinges: {e}\n")

        return hinges

    def _calculateHandlePosition(self, obj):
        """Calculate handle position on the free edge (opposite HingeSide)."""
        width = obj.Width.Value
        height = obj.Height.Value
        thickness = obj.Thickness.Value
        handle_height = min(obj.HandleHeight.Value, height - 100)
        handle_offset = obj.HandleOffset.Value
        hinge_side = obj.HingeSide

        if hinge_side == "Left":
            x_pos = width - handle_offset
        else:
            x_pos = handle_offset

        y_pos = thickness / 2
        z_pos = handle_height

        return App.Vector(x_pos, y_pos, z_pos)

    def _createHandle(self, obj):
        """Create handle hardware visualization."""
        if obj.HandleType == "None":
            return None

        try:
            handle_pos = self._calculateHandlePosition(obj)

            if obj.HandleType == "Knob":
                handle = Part.makeCylinder(
                    20, 15,
                    App.Vector(handle_pos.x, handle_pos.y, handle_pos.z),
                    App.Vector(0, 1, 0)
                )

            elif obj.HandleType == "Bar":
                length = obj.HandleLength.Value
                radius = 12
                start = App.Vector(
                    handle_pos.x,
                    handle_pos.y,
                    handle_pos.z - length / 2
                )
                handle = Part.makeCylinder(radius, length, start, App.Vector(0, 0, 1))

            elif obj.HandleType == "Pull":
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

    def _createFoldedGhost(self, obj):
        """Create a thin box showing the folded stack position."""
        try:
            width = obj.Width.Value
            height = obj.Height.Value
            thickness = obj.Thickness.Value
            panel_width = width / 2
            hinge_side = obj.HingeSide

            # Folded width: two panels stacked
            folded_width = panel_width + thickness

            ghost = Part.makeBox(folded_width, thickness * 2 + 5, height)

            if hinge_side == "Left":
                x_pos = 0
            else:
                x_pos = width - folded_width

            ghost.translate(App.Vector(x_pos, -thickness - 5, 0))
            return ghost

        except Exception as e:
            App.Console.PrintWarning(f"Error creating folded ghost: {e}\n")
            return None

    def _updateBifoldProperties(self, obj):
        """Update bi-fold-specific calculated properties."""
        try:
            width = obj.Width.Value
            thickness = obj.Thickness.Value
            panel_width = width / 2
            spec = BIFOLD_HINGE_SPECS[obj.HingeConfiguration]

            if hasattr(obj, "PanelWidth"):
                obj.PanelWidth = panel_width

            # Folded width: panel width + glass thickness
            folded_width = panel_width + thickness
            if hasattr(obj, "FoldedWidth"):
                obj.FoldedWidth = folded_width

            if hasattr(obj, "OpeningWidth"):
                obj.OpeningWidth = width - folded_width

            if hasattr(obj, "ClearanceDepth"):
                obj.ClearanceDepth = panel_width

            if hasattr(obj, "MaxFoldAngle"):
                obj.MaxFoldAngle = spec["primary_angle"]

        except Exception as e:
            App.Console.PrintWarning(f"Error updating bifold properties: {e}\n")

    def onChanged(self, obj, prop):
        """Called when a property changes."""
        super().onChanged(obj, prop)

        # HingeConfiguration drives FoldDirection
        if prop == "HingeConfiguration":
            if hasattr(obj, "HingeConfiguration") and hasattr(obj, "FoldDirection"):
                spec = BIFOLD_HINGE_SPECS[obj.HingeConfiguration]
                obj.FoldDirection = spec["fold_direction"]

        # Validate FoldAngle: -45 (secondary) to +180 (primary)
        if prop == "FoldAngle":
            if hasattr(obj, "FoldAngle") and hasattr(obj, "HingeConfiguration"):
                spec = BIFOLD_HINGE_SPECS[obj.HingeConfiguration]
                max_angle = spec["primary_angle"]
                min_angle = -spec["secondary_angle"]
                if obj.FoldAngle > max_angle:
                    obj.FoldAngle = max_angle
                elif obj.FoldAngle < min_angle:
                    obj.FoldAngle = min_angle

        # Validate HingeCount (2-3)
        if prop == "HingeCount":
            if hasattr(obj, "HingeCount"):
                if obj.HingeCount < 2:
                    obj.HingeCount = 2
                elif obj.HingeCount > 3:
                    obj.HingeCount = 3

        # Validate HandleHeight (300-1800)
        if prop == "HandleHeight":
            if hasattr(obj, "HandleHeight"):
                if obj.HandleHeight.Value < 300:
                    obj.HandleHeight = 300
                elif obj.HandleHeight.Value > 1800:
                    obj.HandleHeight = 1800

        # Validate minimum width (>= 400)
        if prop == "Width":
            if hasattr(obj, "Width"):
                if obj.Width.Value < 400:
                    obj.Width = 400


def createBiFoldDoor(name="BiFoldDoor"):
    """
    Create a new bi-fold door in the active document.

    Args:
        name: Name for the door object (default: "BiFoldDoor")

    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    obj = doc.addObject("Part::FeaturePython", name)
    BiFoldDoor(obj)

    if App.GuiUp:
        try:
            from freecad.ShowerDesigner.Models.GlassPanelViewProvider import setupViewProvider
            setupViewProvider(obj)
        except Exception:
            obj.ViewObject.Proxy = 0
            obj.ViewObject.Transparency = 70

    doc.recompute()

    App.Console.PrintMessage(f"Bi-fold door '{name}' created\n")
    return obj
