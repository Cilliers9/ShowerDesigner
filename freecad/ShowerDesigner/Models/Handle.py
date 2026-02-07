# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Standalone handle hardware model for shower enclosures.

Provides a Handle Part::FeaturePython object and a shared
createHandleShape() function that replaces the 3× copy-pasted
handle branching logic in HingedDoor, BiFoldDoor, and SlidingDoor.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    HANDLE_SPECS,
    HANDLE_PLACEMENT_DEFAULTS,
    HARDWARE_FINISHES,
)


def createHandleShape(handle_type, length=None, position=None):
    """
    Create a handle shape at the given position.

    This is the shared geometry function imported by door models.
    Each model computes its own position and passes it here.

    Args:
        handle_type: "Knob", "Bar", or "Pull"
        length: Length for Bar/Pull types (mm). Uses first spec length if None.
        position: App.Vector for handle center. Defaults to origin.

    Returns:
        Part.Shape or None if handle_type is "None" or unknown
    """
    if handle_type == "None" or handle_type not in HANDLE_SPECS:
        return None

    if position is None:
        position = App.Vector(0, 0, 0)

    spec = HANDLE_SPECS[handle_type]

    if handle_type == "Knob":
        radius = spec["diameter"] / 2  # 20mm
        depth = spec["depth"]          # 15mm
        return Part.makeCylinder(
            radius, depth,
            App.Vector(position.x, position.y, position.z),
            App.Vector(0, 1, 0)
        )

    elif handle_type == "Bar":
        if length is None:
            length = spec["lengths"][0]
        radius = spec["diameter"] / 2  # 12mm
        start = App.Vector(
            position.x,
            position.y,
            position.z - length / 2
        )
        return Part.makeCylinder(radius, length, start, App.Vector(0, 0, 1))

    elif handle_type == "Pull":
        if length is None:
            length = spec["lengths"][0]
        radius = spec["diameter"] / 2  # 10mm
        start = App.Vector(
            position.x,
            position.y,
            position.z - length / 2
        )
        return Part.makeCylinder(radius, length, start, App.Vector(0, 0, 1))

    return None


class Handle:
    """
    Parametric standalone handle hardware object.

    Properties:
        HandleType: Enum — Knob, Bar, Pull, Towel_Bar
        HandleLength: Length for bar-type handles
        Finish: Hardware finish
    """

    def __init__(self, obj):
        obj.Proxy = self

        obj.addProperty(
            "App::PropertyEnumeration",
            "HandleType",
            "Handle",
            "Type of handle"
        )
        obj.HandleType = [k for k in HANDLE_SPECS.keys()]
        obj.HandleType = "Bar"

        obj.addProperty(
            "App::PropertyLength",
            "HandleLength",
            "Handle",
            "Length of bar/pull handle"
        ).HandleLength = 300

        obj.addProperty(
            "App::PropertyEnumeration",
            "Finish",
            "Handle",
            "Hardware finish"
        )
        obj.Finish = HARDWARE_FINISHES[:]
        obj.Finish = "Chrome"

        obj.addProperty(
            "App::PropertyVector",
            "Position",
            "Placement",
            "Position of the handle"
        ).Position = App.Vector(0, 0, 0)

        obj.addProperty(
            "App::PropertyAngle",
            "Rotation",
            "Placement",
            "Rotation angle around Z-axis"
        ).Rotation = 0

    def execute(self, obj):
        handle_type = obj.HandleType
        length = obj.HandleLength.Value

        shape = createHandleShape(handle_type, length, obj.Position)
        if shape is None:
            # Fallback to a small marker shape
            shape = Part.makeSphere(5, obj.Position)

        obj.Shape = shape
        obj.Placement.Base = obj.Position
        obj.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), obj.Rotation)

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


def createHandle(name="Handle"):
    """
    Create a standalone handle object in the active document.

    Args:
        name: Name for the object

    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    obj = doc.addObject("Part::FeaturePython", name)
    Handle(obj)

    if App.GuiUp:
        obj.ViewObject.Proxy = 0

    doc.recompute()
    App.Console.PrintMessage(f"Handle '{name}' created\n")
    return obj
