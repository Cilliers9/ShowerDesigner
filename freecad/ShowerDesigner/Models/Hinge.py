# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Standalone hinge hardware model for shower enclosures.

Provides a Hinge Part::FeaturePython object and a shared
createHingeShape() function used by HingedDoor, BiFoldDoor, etc.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    HINGE_SPECS,
    HARDWARE_FINISHES,
)


def createHingeShape(width, depth, height):
    """
    Create a hinge box shape with the given dimensions.

    This is the shared geometry function imported by door models.

    Args:
        width: Hinge width in mm
        depth: Hinge depth in mm
        height: Hinge height in mm

    Returns:
        Part.Shape: Box shape representing the hinge
    """
    return Part.makeBox(width, depth, height)


class Hinge:
    """
    Parametric standalone hinge hardware object.

    Properties:
        HingeType: Enum from HINGE_SPECS keys
        Position: Placement vector
        Rotation: Z-axis rotation angle
        LoadCapacity: Read-only capacity from specs
        Finish: Hardware finish
    """

    def __init__(self, obj):
        obj.Proxy = self

        obj.addProperty(
            "App::PropertyEnumeration",
            "HingeType",
            "Hinge",
            "Type of hinge hardware"
        )
        obj.HingeType = list(HINGE_SPECS.keys())
        obj.HingeType = "standard_wall_mount"

        obj.addProperty(
            "App::PropertyVector",
            "Position",
            "Placement",
            "Position of the hinge"
        ).Position = App.Vector(0, 0, 0)

        obj.addProperty(
            "App::PropertyAngle",
            "Rotation",
            "Placement",
            "Rotation angle around Z-axis"
        ).Rotation = 0

        obj.addProperty(
            "App::PropertyFloat",
            "LoadCapacity",
            "Calculated",
            "Load capacity in kg (read-only)"
        )
        obj.setEditorMode("LoadCapacity", 1)

        obj.addProperty(
            "App::PropertyEnumeration",
            "Finish",
            "Hinge",
            "Hardware finish"
        )
        obj.Finish = HARDWARE_FINISHES[:]
        obj.Finish = "Chrome"

    def execute(self, obj):
        spec = HINGE_SPECS.get(obj.HingeType)
        if spec is None:
            App.Console.PrintError(f"Unknown hinge type: {obj.HingeType}\n")
            return

        dims = spec["dimensions"]
        shape = createHingeShape(dims["width"], dims["depth"], dims["height"])
        obj.Shape = shape

        obj.Placement.Base = obj.Position
        obj.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), obj.Rotation)

        if hasattr(obj, "LoadCapacity"):
            obj.LoadCapacity = float(spec["load_capacity_kg"])

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


def createHinge(name="Hinge"):
    """
    Create a standalone hinge object in the active document.

    Args:
        name: Name for the object

    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    obj = doc.addObject("Part::FeaturePython", name)
    Hinge(obj)

    if App.GuiUp:
        obj.ViewObject.Proxy = 0

    doc.recompute()
    App.Console.PrintMessage(f"Hinge '{name}' created\n")
    return obj
