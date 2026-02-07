# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Standalone clamp hardware model for shower enclosures.

Provides a Clamp Part::FeaturePython object and a shared
createClampShape() function used by FixedPanel, etc.

Supported clamp shapes:
    U_Clamp     — U-channel on base plate (default floor clamp)
    L_Clamp     — L-bracket with pressure plate (default wall clamp)
    180DEG_Clamp — placeholder box (two-panel inline joint)
    135DEG_Clamp — placeholder box (two-panel corner joint)
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    CLAMP_SPECS,
    HARDWARE_FINISHES,
)


# ---------------------------------------------------------------------------
# Shape builder helpers
# ---------------------------------------------------------------------------

def _buildUClamp(dims):

    bs = dims["base_size"]                    # 45 mm (overall W and H)
    bt = dims["base_thickness"]               # 4.5 mm
    gg = dims["glass_gap"]                    # 10 mm
    cd = dims["cutout_depth"]                 # 20 mm
    cr = dims["cutout_radius"]                # 10 mm
    slot_center = Part.makeCylinder(
        cr, gg,
        App.Vector(0, 0, 0),
        App.Vector(0, 1, 0)
    )
    slot_base = Part.makeBox(
        cr * 2, gg, cd,
        App.Vector(-gg, 0, -cd)
    )
    slot = slot_center.fuse(slot_base)
    front_plate = Part.makeBox(
        bs, bt, bs,
        App.Vector(-bs/2, -bt, -cd)
    )
    front_slot = slot.fuse(front_plate)
    back_plate = Part.makeBox(
        bs, bt, bs,
        App.Vector(-bs/2, gg, -cd)
    )
    clamp = front_slot.fuse(back_plate)
    shape = clamp.removeSplitter()
    return shape


def _buildLClamp(dims):
    """
    Build an L-Clamp shape: U-Clamp + WallPlate
    """
    bs = dims["base_size"]                    # 45 mm (overall W and H)
    bt = dims["base_thickness"]               # 4.5 mm
    gg = dims["glass_gap"]                    # 10 mm

    u_clamp = _buildUClamp(dims)
    # Wall plate
    wall_plate = Part.makeBox(
        bs, bs, bt,
        App.Vector(-bs/2, gg, -bs/2+2.5))

    l_clamp = u_clamp.fuse(wall_plate)
    shape = l_clamp.removeSplitter()
    return shape


def _buildPlaceholderBox(spec):
    """Build a simple box from the bounding_box spec (placeholder shape)."""
    bb = spec["bounding_box"]
    return Part.makeBox(bb["width"], bb["depth"], bb["height"])


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def createClampShape(clamp_type="L_Clamp"):
    """
    Create a clamp shape from specs.

    This is the shared geometry function imported by FixedPanel and others.

    Args:
        clamp_type: Key into CLAMP_SPECS (U_Clamp, L_Clamp,
                    180DEG_Clamp, 135DEG_Clamp)

    Returns:
        Part.Shape representing the clamp
    """
    spec = CLAMP_SPECS.get(clamp_type)
    if spec is None:
        spec = CLAMP_SPECS["L_Clamp"]

    builder = _SHAPE_BUILDERS.get(clamp_type)
    if builder is not None:
        return builder(spec["dimensions"])

    # Placeholder box for types without custom geometry
    return _buildPlaceholderBox(spec)


_SHAPE_BUILDERS = {
    "U_Clamp": _buildUClamp,
    "L_Clamp": _buildLClamp,
}


class Clamp:
    """
    Parametric standalone clamp hardware object.

    Properties:
        ClampType: Enum from CLAMP_SPECS keys
        MountingType: Wall or Floor
        Position: Placement vector
        Rotation: Z-axis rotation angle
        LoadCapacity: Read-only capacity from specs
        Finish: Hardware finish
    """

    def __init__(self, obj):
        obj.Proxy = self

        obj.addProperty(
            "App::PropertyEnumeration",
            "ClampType",
            "Clamp",
            "Type of clamp hardware"
        )
        obj.ClampType = list(CLAMP_SPECS.keys())
        obj.ClampType = "L_Clamp"

        obj.addProperty(
            "App::PropertyEnumeration",
            "MountingType",
            "Clamp",
            "Mounting location"
        )
        obj.MountingType = ["Wall", "Floor"]
        obj.MountingType = "Wall"

        obj.addProperty(
            "App::PropertyVector",
            "Position",
            "Placement",
            "Position of the clamp"
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
            "Clamp",
            "Hardware finish"
        )
        obj.Finish = HARDWARE_FINISHES[:]
        obj.Finish = "Chrome"

    def execute(self, obj):
        shape = createClampShape(obj.ClampType)
        obj.Shape = shape

        obj.Placement.Base = obj.Position
        obj.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), obj.Rotation)

        spec = CLAMP_SPECS.get(obj.ClampType)
        if spec and hasattr(obj, "LoadCapacity"):
            obj.LoadCapacity = float(spec["load_capacity_kg"])

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


def createClamp(name="Clamp"):
    """
    Create a standalone clamp object in the active document.

    Args:
        name: Name for the object

    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    obj = doc.addObject("Part::FeaturePython", name)
    Clamp(obj)

    if App.GuiUp:
        obj.ViewObject.Proxy = 0

    doc.recompute()
    App.Console.PrintMessage(f"Clamp '{name}' created\n")
    return obj
