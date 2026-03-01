# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Standalone support bar hardware model for shower enclosures.

Provides a SupportBar Part::FeaturePython object and a shared
createSupportBarShape() function.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    SUPPORT_BAR_SPECS,
    HARDWARE_FINISHES,
)


def createSupportBarShape(bar_type, length, diameter):
    """
    Create a support bar cylinder shape.

    Args:
        bar_type: "Horizontal", "Vertical", "Diagonal", or "Ceiling"
        length: Bar length in mm
        diameter: Bar diameter in mm

    Returns:
        Part.Shape: Cylinder representing the bar
    """
    radius = diameter / 2

    if bar_type == "Vertical" or bar_type == "Ceiling":
        # Z-axis aligned
        return Part.makeCylinder(radius, length, App.Vector(0, 0, 0), App.Vector(0, 0, 1))
    elif bar_type == "Diagonal":
        # 45-degree from horizontal (X-Z plane)
        direction = App.Vector(1, 1, 0).normalize()
        return Part.makeCylinder(radius, length, App.Vector(0, 0, 0), direction)
    else:
        # Horizontal: X-axis aligned
        return Part.makeCylinder(radius, length, App.Vector(0, 0, 0), App.Vector(0, 1, 0))


class SupportBar:
    """
    Parametric standalone support bar hardware object.

    Properties:
        BarType: Horizontal, Vertical, Diagonal, Ceiling
        Length: Bar length in mm
        Diameter: Bar diameter in mm (12-25)
        Finish: Hardware finish
    """

    def __init__(self, obj):
        obj.Proxy = self

        obj.addProperty(
            "App::PropertyEnumeration",
            "BarType",
            "Support Bar",
            "Type of support bar"
        )
        obj.BarType = list(SUPPORT_BAR_SPECS.keys())
        obj.BarType = "Horizontal"

        obj.addProperty(
            "App::PropertyLength",
            "Length",
            "Support Bar",
            "Length of the bar"
        ).Length = 500

        obj.addProperty(
            "App::PropertyLength",
            "Diameter",
            "Support Bar",
            "Diameter of the bar (12-25mm)"
        ).Diameter = 19

        obj.addProperty(
            "App::PropertyEnumeration",
            "Finish",
            "Support Bar",
            "Hardware finish"
        )
        obj.Finish = HARDWARE_FINISHES[:]
        obj.Finish = "Chrome"

        obj.addProperty(
            "App::PropertyVector",
            "Position",
            "Placement",
            "Position of the bar"
        ).Position = App.Vector(0, 0, 0)

        obj.addProperty(
            "App::PropertyAngle",
            "Rotation",
            "Placement",
            "Rotation angle around Z-axis"
        ).Rotation = 0

    def execute(self, obj):
        length = obj.Length.Value
        diameter = obj.Diameter.Value

        if length <= 0 or diameter <= 0:
            App.Console.PrintError("Invalid support bar dimensions\n")
            return

        shape = createSupportBarShape(obj.BarType, length, diameter)
        obj.Shape = shape

        obj.Placement.Base = obj.Position
        obj.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), obj.Rotation)

    def onChanged(self, obj, prop):
        if prop == "Diameter":
            if hasattr(obj, "Diameter") and hasattr(obj, "BarType"):
                spec = SUPPORT_BAR_SPECS.get(obj.BarType)
                if spec:
                    min_d, max_d = spec["diameter_range"]
                    if obj.Diameter.Value < min_d:
                        obj.Diameter = min_d
                    elif obj.Diameter.Value > max_d:
                        obj.Diameter = max_d

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


def createSupportBar(name="SupportBar"):
    """
    Create a standalone support bar object in the active document.

    Args:
        name: Name for the object

    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    obj = doc.addObject("Part::FeaturePython", name)
    SupportBar(obj)

    if App.GuiUp:
        obj.ViewObject.Proxy = 0

    doc.recompute()
    App.Console.PrintMessage(f"Support bar '{name}' created\n")
    return obj
