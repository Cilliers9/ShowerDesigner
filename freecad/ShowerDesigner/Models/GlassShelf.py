# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Corner glass shelf — pentagonal glass shelf for 90-degree corners.

The shelf has a pentagon profile: two straight edges at 90 degrees
(against wall/glass), a diagonal front edge with step notches at each end,
and a rounded fillet at the inner corner. It is horizontal (XY plane,
extruded along Z by thickness).

Provides:
  - createGlassShelfShape() — reusable shape builder
  - GlassShelf — standalone Part::FeaturePython model
  - createGlassShelf() — factory function
"""

import FreeCAD as App
import Part

from freecad.ShowerDesigner.Data.HardwareSpecs import GLASS_SHELF_SPECS


def createGlassShelfShape(width, depth, thickness, step=None,
                          clearance_edge1=0, clearance_edge2=0):
    """
    Build a pentagonal glass shelf shape in the XY plane, extruded along Z.

    Profile (top-down, before extrusion), with clearances c1/c2::

        P4 (c2, depth) ---- P3 (c2+step, depth)
        |                         \\
        |                          \\  diagonal
        |                           \\
        P0 (c2, c1) ------------- P5 (width, c1) ---- P2 (width, c1+step)

    Args:
        width: Shelf extent along X (wall/glass edge 1)
        depth: Shelf extent along Y (wall/glass edge 2)
        thickness: Extrusion height along Z
        step: Size of the step notches at each end of the diagonal (default from specs)
        clearance_edge1: Gap from surface along edge 1 / X axis (mm)
        clearance_edge2: Gap from surface along edge 2 / Y axis (mm)

    Returns:
        Part.Shape — the extruded shelf solid
    """
    if step is None:
        step = GLASS_SHELF_SPECS["step"]

    c1 = clearance_edge1
    c2 = clearance_edge2

    edges = []

    # Edge 2 (along Y): from P0 to P4
    edges.append(Part.makeLine(
        App.Vector(c2, c1, 0),
        App.Vector(c2, depth, 0),
    ))

    # P4 to P3: top step notch
    edges.append(Part.makeLine(
        App.Vector(c2, depth, 0),
        App.Vector(c2 + step, depth, 0),
    ))

    # P3 to P2: diagonal
    edges.append(Part.makeLine(
        App.Vector(c2 + step, depth, 0),
        App.Vector(width, c1 + step, 0),
    ))

    # P2 to P5: right step notch
    edges.append(Part.makeLine(
        App.Vector(width, c1 + step, 0),
        App.Vector(width, c1, 0),
    ))

    # Edge 1 (along X): from P5 back to P0
    edges.append(Part.makeLine(
        App.Vector(width, c1, 0),
        App.Vector(c2, c1, 0),
    ))

    wire = Part.Wire(edges)
    face = Part.Face(wire)
    shape = face.extrude(App.Vector(0, 0, thickness))
    return shape.removeSplitter()


class GlassShelf:
    """Standalone parametric glass shelf Part::FeaturePython model."""

    EDGE_TYPES = ["Wall", "Glass"]

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyLength", "Width", "Dimensions", "Shelf extent along edge 1"
        ).Width = GLASS_SHELF_SPECS["default_width"]
        obj.addProperty(
            "App::PropertyLength", "Depth", "Dimensions", "Shelf extent along edge 2"
        ).Depth = GLASS_SHELF_SPECS["default_depth"]
        obj.addProperty(
            "App::PropertyLength", "Thickness", "Dimensions", "Glass thickness"
        ).Thickness = GLASS_SHELF_SPECS["default_thickness"]
        obj.addProperty(
            "App::PropertyLength", "HeightFromFloor", "Dimensions",
            "Height of shelf from floor"
        ).HeightFromFloor = GLASS_SHELF_SPECS["default_height_from_floor"]
        obj.addProperty(
            "App::PropertyEnumeration", "Edge1Type", "Clearance",
            "Surface type along edge 1 (X axis)"
        )
        obj.Edge1Type = self.EDGE_TYPES
        obj.Edge1Type = "Wall"
        obj.addProperty(
            "App::PropertyEnumeration", "Edge2Type", "Clearance",
            "Surface type along edge 2 (Y axis)"
        )
        obj.Edge2Type = self.EDGE_TYPES
        obj.Edge2Type = "Wall"
        obj.addProperty(
            "App::PropertyLength", "PanelThickness", "Clearance",
            "Thickness of adjacent glass panel(s)"
        ).PanelThickness = GLASS_SHELF_SPECS["default_thickness"]
        obj.addProperty(
            "App::PropertyEnumeration", "GlassType", "Glass", "Glass type"
        )
        obj.GlassType = ["Clear", "Frosted", "Bronze", "Grey", "Reeded", "Low-Iron"]
        obj.GlassType = "Clear"

    def _clearanceForEdge(self, edgeType, panelThickness):
        if edgeType == "Glass":
            return panelThickness + GLASS_SHELF_SPECS["glass_clearance"]
        return GLASS_SHELF_SPECS["wall_clearance"]

    def execute(self, obj):
        w = obj.Width.Value
        d = obj.Depth.Value
        t = obj.Thickness.Value
        if w <= 0 or d <= 0 or t <= 0:
            return
        pt = obj.PanelThickness.Value
        c1 = self._clearanceForEdge(obj.Edge1Type, pt)
        c2 = self._clearanceForEdge(obj.Edge2Type, pt)
        obj.Shape = createGlassShelfShape(w, d, t, clearance_edge1=c1, clearance_edge2=c2)
        obj.Placement.Base.z = obj.HeightFromFloor.Value

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


def createGlassShelf(name="GlassShelf"):
    """
    Create a new standalone glass shelf in the active document.

    Args:
        name: Name for the object (default: "GlassShelf")

    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    obj = doc.addObject("Part::FeaturePython", name)
    GlassShelf(obj)

    from freecad.ShowerDesigner.Models.GlassPanelViewProvider import setupViewProvider
    setupViewProvider(obj)

    doc.recompute()
    App.Console.PrintMessage(f"Glass shelf '{name}' created\n")
    return obj
