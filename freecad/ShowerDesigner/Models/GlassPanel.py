# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Glass panel parametric object for shower enclosures
"""

import FreeCAD as App
import Part


class GlassPanel:
    """
    Parametric glass panel object for shower enclosures.

    This is the base class for all glass panel types including fixed panels,
    hinged doors, and sliding doors.
    """

    def __init__(self, obj):
        """
        Initialize the glass panel object.

        Args:
            obj: FreeCAD document object
        """
        obj.Proxy = self

        # Dimensions group
        obj.addProperty(
            "App::PropertyLength",
            "Width",
            "Dimensions",
            "Width of the glass panel"
        ).Width = 900

        obj.addProperty(
            "App::PropertyLength",
            "Height",
            "Dimensions",
            "Height of the glass panel"
        ).Height = 2000

        obj.addProperty(
            "App::PropertyLength",
            "Thickness",
            "Dimensions",
            "Thickness of the glass panel"
        ).Thickness = 8

        # Glass properties group
        obj.addProperty(
            "App::PropertyEnumeration",
            "GlassType",
            "Glass",
            "Type of glass"
        )
        obj.GlassType = ["Clear", "Frosted", "Bronze", "Grey", "Reeded", "Low-Iron"]
        obj.GlassType = "Clear"

        obj.addProperty(
            "App::PropertyEnumeration",
            "EdgeFinish",
            "Glass",
            "Edge finish type"
        )
        obj.EdgeFinish = ["Bright_Polish", "Dull_Polish"]
        obj.EdgeFinish = "Bright_Polish"

        obj.addProperty(
            "App::PropertyEnumeration",
            "TemperType",
            "Glass",
            "Tempering type"
        )
        obj.TemperType = ["Tempered", "Laminated", "None"]
        obj.TemperType = "Tempered"

        # Position and orientation group
        obj.addProperty(
            "App::PropertyVector",
            "Position",
            "Placement",
            "Position of the panel"
        ).Position = App.Vector(0, 0, 0)

        obj.addProperty(
            "App::PropertyAngle",
            "Rotation",
            "Placement",
            "Rotation angle around Z-axis"
        ).Rotation = 0

        # Attachment type
        obj.addProperty(
            "App::PropertyEnumeration",
            "AttachmentType",
            "Configuration",
            "How the panel is attached"
        )
        obj.AttachmentType = ["Fixed", "Hinged", "Sliding"]
        obj.AttachmentType = "Fixed"

        # Calculated properties (read-only)
        obj.addProperty(
            "App::PropertyFloat",
            "Weight",
            "Calculated",
            "Weight of the panel in kg (read-only)"
        )
        obj.setEditorMode("Weight", 1)  # Make read-only

        obj.addProperty(
            "App::PropertyFloat",
            "Area",
            "Calculated",
            "Area of the panel in m² (read-only)"
        )
        obj.setEditorMode("Area", 1)  # Make read-only

    def execute(self, obj):
        """
        Rebuild the geometry when properties change.

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

        # Set the shape
        obj.Shape = panel

        # Apply position
        obj.Placement.Base = obj.Position

        # Apply Rotation
        new_rotation= App.Rotation(App.Vector(0, 0, 1), obj.Rotation)
        obj.Placement.Rotation = new_rotation

        # Calculate weight and area
        self._updateCalculatedProperties(obj)

    def _updateCalculatedProperties(self, obj):
        """
        Update calculated properties like weight and area.

        Args:
            obj: FreeCAD document object
        """
        from freecad.ShowerDesigner.Data.GlassSpecs import GLASS_SPECS

        try:
            # Calculate area in m²
            width_m = obj.Width.Value / 1000.0
            height_m = obj.Height.Value / 1000.0
            area = width_m * height_m
            if hasattr(obj, "Area"):
                obj.Area = area

            # Calculate weight based on thickness
            thickness_key = f"{int(obj.Thickness.Value)}mm"
            if thickness_key in GLASS_SPECS:
                weight_per_m2 = GLASS_SPECS[thickness_key]["weight_kg_m2"]
                weight = area * weight_per_m2
            else:
                # Approximate weight if thickness not in database
                weight = area * 2.5 * obj.Thickness.Value  # Glass density ~2.5 kg/mm/m²
            if hasattr(obj, "Weight"):
                obj.Weight = weight

        except Exception as e:
            App.Console.PrintWarning(f"Error updating calculated properties: {e}\n")

    def onChanged(self, obj, prop):
        """
        Called when a property changes.

        Args:
            obj: FreeCAD document object
            prop: Name of the property that changed
        """
        # Recalculate when dimensions or glass type change
        if prop in ["Width", "Height", "Thickness", "GlassType"]:
            if (hasattr(obj, "Width") and hasattr(obj, "Height") and
                hasattr(obj, "Thickness") and hasattr(obj, "Weight") and
                hasattr(obj, "Area")):
                self._updateCalculatedProperties(obj)

    def __getstate__(self):
        """Return state for serialization"""
        return None

    def __setstate__(self, state):
        """Restore state from serialization"""
        return None


def createGlassPanel(name="GlassPanel"):
    """
    Create a new glass panel in the active document.

    Args:
        name: Name for the panel object (default: "GlassPanel")

    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    obj = doc.addObject("Part::FeaturePython", name)
    GlassPanel(obj)

    if App.GuiUp:
        # Set up view provider
        obj.ViewObject.Proxy = 0
        # Set transparency based on glass type
        obj.ViewObject.Transparency = 70

    doc.recompute()

    App.Console.PrintMessage(f"Glass panel '{name}' created\n")
    return obj
