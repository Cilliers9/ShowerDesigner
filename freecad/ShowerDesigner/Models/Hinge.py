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
    BEVEL_HINGE_SPECS,
    BEVEL_FINISHES,
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


# ======================================================================
# Bevel hinge shape builders
# ======================================================================

def _makeGlassClamp(plate_w, plate_t, height, glass_t, cutout_depth):
    """
    Create a C-channel glass clamp: outer box with a glass slot cut out.

    The clamp extends in +Y. The slot is centered in X, runs full height,
    and is sized to accept the glass panel.

    Args:
        plate_w: Plate width (X)
        plate_t: Plate total depth (Y) — includes cutout
        height: Body height (Z)
        glass_t: Glass thickness for the slot
        cutout_depth: Depth of the glass slot

    Returns:
        Part.Shape
    """
    outer = Part.makeBox(plate_w, plate_t, height)
    slot_x = (plate_w - glass_t) / 2
    slot = Part.makeBox(glass_t, cutout_depth, height)
    slot.translate(App.Vector(slot_x, 0, 0))
    return outer.cut(slot)


def _buildWallToGlass(dims, glass_t):
    """
    Build a Wall-to-Glass Bevel hinge shape (L-profile from top view).

    - Wall plate extends in -Y (toward wall)
    - Glass clamp extends in +Y (toward room)
    - Knuckle cylinder centered on Z axis at the join

    Origin: bottom-center of knuckle barrel.
    """
    body_h = dims["body_height"]                # 90 mm
    wall_pw = dims["wall_plate_width"]          # 50 mm
    glass_pw = dims["glass_plate_width"]        # 55 mm
    cutout_depth = dims["glass_cutout_depth"]   # 41 mm
    cutout_width =dims["glass_cutout_width"]    # 63 mm
    knuckle_dia = dims["knuckle_diameter"]      # 16 mm
    knuckle_dep = dims["knuckle_depth"]         # 37 mm
    knuckle_w = dims["knuckle_width"]           # 58 mm
    plate_t = 5  # plate thickness

    # Glass Cutout
    cutout_base = Part.makeBox(
        cutout_depth,  glass_t, cutout_width,
        App.Vector(0, 0, -cutout_width / 2))
    knuckle_b = Part.makeCylinder(
        knuckle_dia/2, glass_t,
        App.Vector(knuckle_dep, 0, knuckle_w/2),
        App.Vector(0, 1, 0),
        360
    )
    knuckle_t = Part.makeCylinder(
        knuckle_dia/2, glass_t,
        App.Vector(knuckle_dep, 0, -knuckle_w/2),
        App.Vector(0, 1, 0),
        360
    )
    cutout = cutout_base.fuse(knuckle_b).fuse(knuckle_t)
    #Make beveled front plate
    front_plate = Part.makeBox(
        glass_pw, plate_t, body_h,
        App.Vector(0, -plate_t, -body_h/2)
    )
    front_edges = []
    for edge in front_plate.Edges:
            # We check the midpoint of the edge to see if it lies on the front plane
            midpoint = edge.valueAt(edge.FirstParameter + (edge.LastParameter - edge.FirstParameter) / 2)
            if midpoint.y == -plate_t:
                front_edges.append(edge)
    beveled_plate = front_plate.makeChamfer(3, front_edges)
    front_cutout = cutout.fuse(beveled_plate)
    #Make beveled back plate
    rotation = App.Rotation(App.Vector(1, 0, 0), 180)
    beveled_plate.Placement.Rotation = rotation
    beveled_plate.translate(App.Vector(0, glass_t, 0))
    glass_clamp = front_cutout.fuse(beveled_plate)
    #Hinge cut
    hinge_cut = Part.makeBox(
        27, glass_t + plate_t*2, 45,
        App.Vector(0, -plate_t, -45/2)
    )

    return glass_clamp.cut(hinge_cut)


def _buildGlassToGlass(dims, glass_t):
    """
    Build a Glass-to-Glass Bevel hinge shape (two clamps mirrored about knuckle).

    Handles both equal and unequal cutout variants by checking for
    `_door` / `_fix` suffixed dimension keys.

    Origin: bottom-center of knuckle barrel.
    """
    body_h = dims["body_height"]
    knuckle_d = dims["knuckle_diameter"]
    knuckle_w = dims["knuckle_width"]
    plate_t = 5

    # Determine clamp dimensions — unequal variants have _door/_fix suffixes
    pw_pos = dims.get("glass_plate_width", dims.get("glass_plate_width_door", 55))
    pw_neg = dims.get("glass_plate_width", dims.get("glass_plate_width_fix", 55))
    cd_pos = dims.get("glass_cutout_depth", dims.get("glass_cutout_depth_door", 41))
    cd_neg = dims.get("glass_cutout_depth", dims.get("glass_cutout_depth_fix", 35))

    # Positive-Y clamp (door side)
    depth_pos = plate_t + cd_pos
    clamp_pos = _makeGlassClamp(pw_pos, depth_pos, body_h, glass_t, cd_pos)
    clamp_pos.translate(App.Vector(-pw_pos / 2, 0, 0))

    # Negative-Y clamp (fixed side) — mirror by building in +Y then flipping
    depth_neg = plate_t + cd_neg
    clamp_neg = _makeGlassClamp(pw_neg, depth_neg, body_h, glass_t, cd_neg)
    clamp_neg.translate(App.Vector(-pw_neg / 2, 0, 0))
    # Mirror about XZ plane: reflect Y
    mirror_mat = App.Matrix()
    mirror_mat.A22 = -1
    clamp_neg = clamp_neg.transformGeometry(mirror_mat)

    # Knuckle
    knuckle = Part.makeCylinder(
        knuckle_d / 2, knuckle_w,
        App.Vector(0, 0, (body_h - knuckle_w) / 2),
        App.Vector(0, 0, 1)
    )

    return clamp_pos.fuse(clamp_neg).fuse(knuckle)


def _buildPivotHinge(dims, glass_t):
    """
    Build a Pivot Bevel hinge shape (glass clamp + pivot body + knuckle).

    Origin: bottom-center of knuckle barrel.
    """
    body_h = dims["body_height"]
    knuckle_d = dims["knuckle_diameter"]
    knuckle_w = dims["knuckle_width"]
    glass_ph = dims.get("glass_plate_height", 55)
    cutout_depth = dims.get("glass_cutout_depth", 41)
    plate_t = 5

    # Glass clamp (extends in +Y)
    clamp_depth = plate_t + cutout_depth
    clamp = _makeGlassClamp(glass_ph, clamp_depth, body_h, glass_t, cutout_depth)
    clamp.translate(App.Vector(-glass_ph / 2, 0, 0))

    # Pivot body (extends in -Y)
    pivot_depth = dims.get("pivot_plate_depth", 20)
    pivot_h = dims.get("pivot_plate_height", body_h)
    pivot = Part.makeBox(glass_ph, pivot_depth, pivot_h)
    pivot.translate(App.Vector(-glass_ph / 2, -pivot_depth, 0))

    # Knuckle
    knuckle = Part.makeCylinder(
        knuckle_d / 2, knuckle_w,
        App.Vector(0, 0, (body_h - knuckle_w) / 2),
        App.Vector(0, 0, 1)
    )

    return clamp.fuse(pivot).fuse(knuckle)


def _buildTeeHinge(dims, glass_t):
    """
    Build a Tee Bevel hinge shape.

    Two inline glass clamps (like Glass-to-Glass) plus a perpendicular
    fixed arm extending in -X with a mounting hole.

    Origin: bottom-center of knuckle barrel.
    """
    body_h = dims["body_height"]
    knuckle_d = dims["knuckle_diameter"]
    knuckle_w = dims["knuckle_width"]
    plate_t = 5

    # Two inline clamps (reuse Glass-to-Glass builder for the two clamps)
    pw = dims.get("glass_plate_width", 55)
    cd = dims.get("glass_cutout_depth", 41)
    depth = plate_t + cd

    clamp_pos = _makeGlassClamp(pw, depth, body_h, glass_t, cd)
    clamp_pos.translate(App.Vector(-pw / 2, 0, 0))

    # Fixed panel clamp (negative Y)
    fp_w = dims.get("fixed_plate_width", 60)
    clamp_neg = _makeGlassClamp(fp_w, depth, body_h, glass_t, cd)
    clamp_neg.translate(App.Vector(-fp_w / 2, 0, 0))
    mirror_mat = App.Matrix()
    mirror_mat.A22 = -1
    clamp_neg = clamp_neg.transformGeometry(mirror_mat)

    # Perpendicular fixed arm extending in -X
    arm_length = dims.get("fixed_hole_depth", 37)
    arm_height = dims.get("fixed_hole_height", 58)
    arm = Part.makeBox(arm_length, plate_t, arm_height)
    arm_z_offset = (body_h - arm_height) / 2
    arm.translate(App.Vector(-pw / 2 - arm_length, -plate_t / 2, arm_z_offset))

    # Mounting hole in the arm
    hole_d = dims.get("fixed_hole_diameter", 16)
    hole_cyl = Part.makeCylinder(
        hole_d / 2, plate_t + 2,
        App.Vector(
            -pw / 2 - arm_length / 2,
            -plate_t / 2 - 1,
            body_h / 2
        ),
        App.Vector(0, 1, 0)
    )

    # Knuckle
    knuckle = Part.makeCylinder(
        knuckle_d / 2, knuckle_w,
        App.Vector(0, 0, (body_h - knuckle_w) / 2),
        App.Vector(0, 0, 1)
    )

    shape = clamp_pos.fuse(clamp_neg).fuse(arm).fuse(knuckle)
    return shape.cut(hole_cyl)


# Dispatch table: mounting_type → builder function
_BEVEL_BUILDERS = {
    "Wall-to-Glass": _buildWallToGlass,
    "Glass-to-Glass": _buildGlassToGlass,
    "Glass-to-Wall-Pivot": _buildPivotHinge,
    "Glass-to-Glass-Pivot": _buildPivotHinge,
    "Glass-to-Glass-Tee": _buildTeeHinge,
}


def createBevelHingeShape(hinge_type, glass_thickness=8):
    """
    Create a 3D shape for a Bevel-range hinge.

    Dispatches to the appropriate builder based on the hinge's mounting_type.
    Falls back to a simple box if CSG operations fail.

    Args:
        hinge_type: Key into BEVEL_HINGE_SPECS
        glass_thickness: Glass thickness in mm (default 8)

    Returns:
        Part.Shape
    """
    spec = BEVEL_HINGE_SPECS.get(hinge_type)
    if spec is None:
        App.Console.PrintError(f"Unknown Bevel hinge type: {hinge_type}\n")
        return Part.makeBox(65, 20, 90)

    dims = spec["dimensions"]
    mounting = spec["mounting_type"]
    builder = _BEVEL_BUILDERS.get(mounting)

    if builder is None:
        App.Console.PrintWarning(
            f"No builder for mounting type '{mounting}', using fallback box\n"
        )
        bw = dims.get("body_width", 65)
        bh = dims.get("body_height", 90)
        return Part.makeBox(bw, 20, bh)

    try:
        return builder(dims, glass_thickness)
    except Exception as e:
        App.Console.PrintError(
            f"Bevel hinge CSG failed for '{hinge_type}': {e} — using fallback box\n"
        )
        bw = dims.get("body_width", 65)
        bh = dims.get("body_height", 90)
        return Part.makeBox(bw, 20, bh)


class Hinge:
    """
    Parametric standalone hinge hardware object.

    Properties:
        HingeType: Enum from HINGE_SPECS + BEVEL_HINGE_SPECS keys
        GlassThickness: Glass thickness for Bevel slot sizing
        Position: Placement vector
        Rotation: Z-axis rotation angle
        LoadCapacity: Read-only capacity from specs
        Finish: Hardware finish (includes Bevel finishes)
    """

    def __init__(self, obj):
        obj.Proxy = self

        all_types = list(HINGE_SPECS.keys()) + list(BEVEL_HINGE_SPECS.keys())
        obj.addProperty(
            "App::PropertyEnumeration",
            "HingeType",
            "Hinge",
            "Type of hinge hardware"
        )
        obj.HingeType = all_types
        obj.HingeType = "standard_wall_mount"

        obj.addProperty(
            "App::PropertyLength",
            "GlassThickness",
            "Hinge",
            "Glass thickness for Bevel slot sizing"
        ).GlassThickness = 8

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

        all_finishes = HARDWARE_FINISHES[:] + [
            f for f in BEVEL_FINISHES if f not in HARDWARE_FINISHES
        ]
        obj.addProperty(
            "App::PropertyEnumeration",
            "Finish",
            "Hinge",
            "Hardware finish"
        )
        obj.Finish = all_finishes
        obj.Finish = "Chrome"

    def execute(self, obj):
        hinge_type = obj.HingeType
        glass_t = 8
        if hasattr(obj, "GlassThickness"):
            glass_t = obj.GlassThickness.Value or 8

        # Bevel hinge
        if hinge_type in BEVEL_HINGE_SPECS:
            obj.Shape = createBevelHingeShape(hinge_type, glass_t)
            obj.Placement.Base = obj.Position
            obj.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), obj.Rotation)
            return

        # Legacy hinge
        spec = HINGE_SPECS.get(hinge_type)
        if spec is None:
            App.Console.PrintError(f"Unknown hinge type: {hinge_type}\n")
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
