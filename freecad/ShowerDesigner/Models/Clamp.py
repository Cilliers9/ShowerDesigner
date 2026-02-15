# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Standalone clamp hardware model for shower enclosures.

Provides a Clamp Part::FeaturePython object and a shared
createClampShape() function used by FixedPanel, etc.

Supported clamp shapes:
    U_Clamp         — U-bracket on base plate (default floor clamp)
    L_Clamp         — L-bracket with pressure plate (default wall clamp)
    180DEG_Clamp    — Connects Glass to inline wall or floor at 180 deg angle
    90DEG_G2G_Clamp — Glass-to-glass corner clamp (90 deg)
    180DEG_G2G_Clamp — Glass-to-glass inline clamp (180 deg)
    135DEG_G2G_Clamp    — Connects Glass to glass at 135 deg angle
    90DEG_Tee_Clamp — Glass-to-glass T-junction clamp (3 panels)
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

def _buildGlassClamp(dims):
    bs = dims["base_size"]
    bt = dims["base_thickness"]
    gg = dims["glass_gap"]
    cd = dims["cutout_depth"]
    cr = dims["cutout_radius"]
    cs = dims["chamfer_size"]
    #Make Slot
    slot = Part.makeCylinder(
        cr, gg,
        App.Vector(0, 0, 0),
        App.Vector(0, 1, 0)
    )
    #Make beveled front plate
    front_plate = Part.makeBox(
        bs, bt, bs,
        App.Vector(-bs/2, -bt, -cd)
    )
    front_edges = []
    for edge in front_plate.Edges:
            # We check the midpoint of the edge to see if it lies on the front plane
            midpoint = edge.valueAt(edge.FirstParameter + (edge.LastParameter - edge.FirstParameter) / 2)
            if midpoint.y == -bt:
                front_edges.append(edge)
    beveled_front_edge = front_plate.makeChamfer(cs, front_edges)
    front_slot = slot.fuse(beveled_front_edge)
    #Make back plate
    back_plate = Part.makeBox(
        bs, bt, bs,
        App.Vector(-bs/2, gg, -cd)
    )
    clamp = front_slot.fuse(back_plate)
    return clamp

def _buildUClamp(dims):

    bs = dims["base_size"]
    bt = dims["base_thickness"]
    gg = dims["glass_gap"]
    cd = dims["cutout_depth"]
    cr = dims["cutout_radius"]
    cs = dims["chamfer_size"]

    glass_clamp = _buildGlassClamp(dims)
    #Make Slot
    slot_base = Part.makeBox(
        cr * 2, gg, cd,
        App.Vector(-gg, 0, -cd)
    )
    clamp = glass_clamp.fuse(slot_base)
    shape = clamp.removeSplitter()
    return shape


def _buildLClamp(dims):
    """
    Build an L-Clamp shape: U-Clamp + WallPlate
    """
    bs = dims["base_size"]
    bt = dims["base_thickness"]
    gg = dims["glass_gap"]
    cd = dims["cutout_depth"]

    u_clamp = _buildUClamp(dims)
    # Wall plate
    wall_plate = Part.makeBox(
        bs, bs, bt,
        App.Vector(-bs/2, gg, -cd))

    l_clamp = u_clamp.fuse(wall_plate)
    shape = l_clamp.removeSplitter()
    return shape

def _build180degClamp(dims):
    """
    Build an 180deg_Clamp shape: U-Clamp + WallPlate
    """
    bs = dims["base_size"]
    bt = dims["base_thickness"]
    gg = dims["glass_gap"]
    cd = dims["cutout_depth"]

    u_clamp = _buildUClamp(dims)
    # Wall plate
    wall_plate = Part.makeBox(
        bs, bt, bs,
        App.Vector(-bs/2, gg, -cd-bs)
    )                                                   # Extend back plate down by base size

    l_clamp = u_clamp.fuse(wall_plate)
    shape = l_clamp.removeSplitter()
    return shape

def _build135degClamp(dims):
    """
    Build an 135deg_Clamp shape: U-Clamp + WallPlate
    """
    bs = dims["base_size"]
    bt = dims["base_thickness"]
    gg = dims["glass_gap"]
    cd = dims["cutout_depth"]

    u_clamp = _buildGlassClamp(dims)
    # Wall plate
    wall_plate = Part.makeBox(
        bs, bs, bt,
        App.Vector(0, 0, 0))            # Extend back plate down by base size
    rotation = App.Rotation(App.Vector(1, 0, 0), -45)
    wall_plate.Placement.Rotation = rotation
    wall_plate.translate(App.Vector(-bs/2, gg, -cd))
    l_clamp = u_clamp.fuse(wall_plate)
    shape = l_clamp.removeSplitter()
    return shape

def _build90degG2GClamp(dims):
    """
    Build a 90° glass-to-glass clamp: two glass slots at right angles.

    Uses two _buildGlassClamp instances fused at 90°. The front (beveled)
    faces point outward on two perpendicular sides, forming a corner piece.
    """
    bt = dims["base_thickness"]
    gg = dims["glass_gap"]
    cd = dims["cutout_depth"]

    clamp1 = _buildGlassClamp(dims)
    clamp2 = _buildGlassClamp(dims)
    clamp2.rotate(App.Vector(0, 0, -cd), App.Vector(0, 1, 0), 180)
    clamp2.rotate(App.Vector(0, gg, -cd), App.Vector(1, 0, 0), 90)
    shape = clamp1.fuse(clamp2)
    return shape.removeSplitter()


def _build180degG2GClamp(dims):
    """
    Build a 180° glass-to-glass clamp: two inline glass slots back to back.

    The top slot opens upward and the bottom slot opens downward, connecting
    two inline glass panels. Rotated around Y-axis to keep both front
    (beveled) plates facing the same direction.
    """
    cd = dims["cutout_depth"]

    top = _buildGlassClamp(dims)
    bottom = _buildGlassClamp(dims)
    bottom.rotate(App.Vector(0, 0, -cd), App.Vector(0, 1, 0), 180)

    shape = top.fuse(bottom)
    return shape.removeSplitter()


def _build135degG2GClamp(dims):
    """
    Build an 135deg_Clamp shape: U-Clamp + WallPlate
    """
    bt = dims["base_thickness"]
    gg = dims["glass_gap"]
    cd = dims["cutout_depth"]

    clamp1 = _buildGlassClamp(dims)
    clamp2 = _buildGlassClamp(dims)
    clamp2.rotate(App.Vector(0, 0, -cd), App.Vector(0, 1, 0), 180)
    clamp2.rotate(App.Vector(0, gg, -cd), App.Vector(1, 0, 0), 45)
    shape = clamp1.fuse(clamp2)
    return shape.removeSplitter()

def _build90degTeeClamp(dims):
    """
    Build a 90° glass-to-glass tee clamp: T-junction with 3 glass slots.

    Two inline slots form the bar of the T (shifted ±bs/2 along X),
    and one perpendicular slot forms the stem (rotated 90° around Z).
    """
    bs = dims["base_size"]
    ip = dims["inline_plate"]
    bt = dims["base_thickness"]
    gg = dims["glass_gap"]
    cd = dims["cutout_depth"]
    cr = dims["cutout_radius"]
    ci = dims["inline_cutout"]
    cs = dims["chamfer_size"]

    front_plate = Part.makeBox(
        bs, bt, ip,
        App.Vector(-bs/2, -bt, -ip/2)
        )
    front_edges = []
    for edge in front_plate.Edges:
            # We check the midpoint of the edge to see if it lies on the front plane
            midpoint = edge.valueAt(edge.FirstParameter + (edge.LastParameter - edge.FirstParameter) / 2)
            if midpoint.y == -bt:
                front_edges.append(edge)
    beveled_front_plate = front_plate.makeChamfer(cs, front_edges)
    bottom_cutout = Part.makeCylinder(
        cr, gg,
        App.Vector(0, 0, -ci/2),
        App.Vector(0, 1, 0)
    )
    top_cutout = Part.makeCylinder(
        cr, gg,
        App.Vector(0, 0, ci/2),
        App.Vector(0, 1, 0)
    )
    front_plate = beveled_front_plate.fuse(bottom_cutout).fuse(top_cutout)
    bottom_back_plate = Part.makeBox(
        bs, bt, bs,
        App.Vector(-bs/2, gg, -ip/2)
        )
    bottom_div_plate = Part.makeBox(
        bs, bs, bt,
        App.Vector(-bs/2, gg, -ip/2+bs-bt)
        )
    bottom_plate = bottom_back_plate.fuse(bottom_div_plate)
    top_back_plate = Part.makeBox(
        bs, bt, bs,
        App.Vector(-bs/2, gg, ip/2 - bs)
        )
    top_div_plate = Part.makeBox(
        bs, bs, bt,
        App.Vector(-bs/2, gg, ip/2-bs)
        )
    top_plate = top_back_plate.fuse(top_div_plate)
    div_cutout = Part.makeCylinder(
        cr, ip-bs*2,
        App.Vector(0, gg+cd, -ip/2+bs),
        App.Vector(0, 0, 1)
    )
    t_clamp = front_plate.fuse(bottom_plate).fuse(top_plate).fuse(div_cutout)
    return t_clamp.removeSplitter()

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
    "180DEG_Clamp": _build180degClamp,
    "135DEG_G2G_Clamp": _build135degG2GClamp,
    "90DEG_G2G_Clamp": _build90degG2GClamp,
    "180DEG_G2G_Clamp": _build180degG2GClamp,
    "90DEG_Tee_Clamp": _build90degTeeClamp,
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
