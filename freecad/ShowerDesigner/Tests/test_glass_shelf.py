# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for the GlassShelf model and enclosure integration.

Requires FreeCAD accessible. Run in FreeCAD console:
    exec(open('path/to/test_glass_shelf.py').read())

Or via pytest (if FreeCAD modules are accessible):
    pytest freecad/ShowerDesigner/Tests/test_glass_shelf.py
"""

import sys
sys.path.insert(
    0, r"C:\Users\tclou\AppData\Roaming\FreeCAD\v1-1\Mod\ShowerDesigner"
)

import FreeCAD as App
from freecad.ShowerDesigner.Models.GlassShelf import (
    createGlassShelfShape,
    createGlassShelf,
)
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    GLASS_SHELF_SPECS,
    SHELF_CLAMP_MAPPING,
)


# -----------------------------------------------------------------------
# Shape builder tests
# -----------------------------------------------------------------------

def test_createGlassShelfShape_basic():
    """Test basic shelf shape creation with default parameters."""
    print("\n" + "=" * 70)
    print("Test: createGlassShelfShape - basic")
    print("=" * 70)

    shape = createGlassShelfShape(400, 200, 8)
    assert shape is not None, "Shape should not be None"
    assert shape.isValid(), "Shape should be valid"

    bb = shape.BoundBox
    assert abs(bb.XLength - 400) < 0.1, f"XLength should be 400, got {bb.XLength}"
    assert abs(bb.YLength - 200) < 0.1, f"YLength should be 200, got {bb.YLength}"
    assert abs(bb.ZLength - 8) < 0.1, f"ZLength should be 8, got {bb.ZLength}"
    print("  createGlassShelfShape(400, 200, 8) - PASSED")


def test_createGlassShelfShape_with_clearances():
    """Test shelf shape with wall and glass clearances (glass = panel_thickness + gap)."""
    print("\n" + "=" * 70)
    print("Test: createGlassShelfShape - with clearances")
    print("=" * 70)

    wall_c = GLASS_SHELF_SPECS["wall_clearance"]       # 5mm from wall
    glass_c = 8 + GLASS_SHELF_SPECS["glass_clearance"]  # 8mm panel + 2mm gap = 10mm
    shape = createGlassShelfShape(400, 200, 8, clearance_edge1=glass_c, clearance_edge2=wall_c)
    assert shape is not None, "Shape should not be None"
    assert shape.isValid(), "Shape should be valid"
    bb = shape.BoundBox
    assert abs(bb.XLength - (400 - wall_c)) < 0.1, (
        f"XLength should be {400 - wall_c}, got {bb.XLength}"
    )
    assert abs(bb.YLength - (200 - glass_c)) < 0.1, (
        f"YLength should be {200 - glass_c}, got {bb.YLength}"
    )
    assert abs(bb.ZLength - 8) < 0.1
    print("  createGlassShelfShape with clearances - PASSED")


def test_createGlassShelfShape_custom_step():
    """Test shelf shape with custom step size."""
    print("\n" + "=" * 70)
    print("Test: createGlassShelfShape - custom step")
    print("=" * 70)

    shape = createGlassShelfShape(500, 250, 8, step=80)
    assert shape is not None, "Shape should not be None"
    assert shape.isValid(), "Shape should be valid"
    bb = shape.BoundBox
    assert abs(bb.XLength - 500) < 0.1
    assert abs(bb.YLength - 250) < 0.1
    print("  createGlassShelfShape(500, 250, 8, step=80) - PASSED")


# -----------------------------------------------------------------------
# Standalone model tests
# -----------------------------------------------------------------------

def test_createGlassShelf_standalone():
    """Test standalone glass shelf creation."""
    print("\n" + "=" * 70)
    print("Test: createGlassShelf - standalone")
    print("=" * 70)

    doc = App.newDocument("TestGlassShelf")
    try:
        obj = createGlassShelf("TestShelf")
        assert obj is not None, "Object should not be None"
        assert obj.Shape.isValid(), "Shape should be valid"
        assert obj.Width.Value == GLASS_SHELF_SPECS["default_width"]
        assert obj.Depth.Value == GLASS_SHELF_SPECS["default_depth"]
        assert obj.Thickness.Value == GLASS_SHELF_SPECS["default_thickness"]
        assert obj.HeightFromFloor.Value == GLASS_SHELF_SPECS["default_height_from_floor"]
        print("  createGlassShelf standalone - PASSED")
    finally:
        App.closeDocument(doc.Name)


def test_glassShelf_property_changes():
    """Test that changing properties updates the shape."""
    print("\n" + "=" * 70)
    print("Test: GlassShelf - property changes")
    print("=" * 70)

    doc = App.newDocument("TestGlassShelfProps")
    try:
        obj = createGlassShelf("TestShelf")

        obj.Width = 500
        obj.Depth = 300
        obj.Thickness = 10
        doc.recompute()

        wc = GLASS_SHELF_SPECS["wall_clearance"]
        bb = obj.Shape.BoundBox
        assert abs(bb.XLength - (500 - wc)) < 0.1, (
            f"Width should be {500 - wc}, got {bb.XLength}"
        )
        assert abs(bb.YLength - (300 - wc)) < 0.1, (
            f"Depth should be {300 - wc}, got {bb.YLength}"
        )
        assert abs(bb.ZLength - 10) < 0.1, f"Thickness should update to 10, got {bb.ZLength}"
        print("  GlassShelf property changes - PASSED")
    finally:
        App.closeDocument(doc.Name)


# -----------------------------------------------------------------------
# Data specs tests
# -----------------------------------------------------------------------

def test_glass_shelf_specs():
    """Test that GLASS_SHELF_SPECS has required keys."""
    print("\n" + "=" * 70)
    print("Test: GLASS_SHELF_SPECS")
    print("=" * 70)

    required = [
        "default_height_from_floor", "default_width", "default_depth",
        "default_thickness", "step", "clamp_inset",
        "wall_clearance", "glass_clearance",
    ]
    for key in required:
        assert key in GLASS_SHELF_SPECS, f"Missing key: {key}"
    print("  GLASS_SHELF_SPECS keys - PASSED")


def test_shelf_clamp_mapping():
    """Test that SHELF_CLAMP_MAPPING has wall and glass entries."""
    print("\n" + "=" * 70)
    print("Test: SHELF_CLAMP_MAPPING")
    print("=" * 70)

    assert "wall" in SHELF_CLAMP_MAPPING
    assert "glass" in SHELF_CLAMP_MAPPING
    assert SHELF_CLAMP_MAPPING["wall"] == "L_Clamp"
    assert SHELF_CLAMP_MAPPING["glass"] == "90DEG_G2G_Clamp"
    print("  SHELF_CLAMP_MAPPING - PASSED")


# -----------------------------------------------------------------------
# Enclosure integration tests
# -----------------------------------------------------------------------

def test_corner_enclosure_shelf():
    """Test glass shelf integration in CornerEnclosure."""
    print("\n" + "=" * 70)
    print("Test: CornerEnclosure - glass shelf integration")
    print("=" * 70)

    from freecad.ShowerDesigner.Models.CornerEnclosure import createCornerEnclosure

    doc = App.newDocument("TestCornerShelf")
    try:
        createCornerEnclosure("TestCorner")
        doc.recompute()

        part = doc.getObject("TestCorner")
        assert part is not None, "CornerEnclosure should exist"

        # Find VarSet
        vs = None
        for child in part.Group:
            if child.TypeId == "App::VarSet":
                vs = child
                break
        assert vs is not None, "VarSet should exist"

        # Enable shelf
        vs.ShowGlassShelf = True
        doc.recompute()

        # Check shelf child exists
        shelf = None
        for child in part.Group:
            if child.Label == "GlassShelf":
                shelf = child
                break
        assert shelf is not None, "GlassShelf child should exist after enabling"
        assert shelf.Shape.isValid(), "Shelf shape should be valid"

        # Check clamp children exist
        clamp_labels = [c.Label for c in part.Group if "ShelfClamp" in c.Label]
        assert len(clamp_labels) >= 2, f"Should have 2 shelf clamps, got {clamp_labels}"

        # Test position change
        vs.ShelfPosition = "Position 2"
        doc.recompute()
        assert shelf.Shape.isValid(), "Shelf shape should remain valid after position change"

        # Disable shelf
        vs.ShowGlassShelf = False
        doc.recompute()

        shelf_after = None
        for child in part.Group:
            if child.Label == "GlassShelf":
                shelf_after = child
                break
        assert shelf_after is None, "GlassShelf should be removed when disabled"

        print("  CornerEnclosure shelf integration - PASSED")
    finally:
        App.closeDocument(doc.Name)


def test_alcove_enclosure_shelf():
    """Test glass shelf integration in AlcoveEnclosure."""
    print("\n" + "=" * 70)
    print("Test: AlcoveEnclosure - glass shelf integration")
    print("=" * 70)

    from freecad.ShowerDesigner.Models.AlcoveEnclosure import createAlcoveEnclosure

    doc = App.newDocument("TestAlcoveShelf")
    try:
        createAlcoveEnclosure("TestAlcove")
        doc.recompute()

        part = doc.getObject("TestAlcove")
        assert part is not None, "AlcoveEnclosure should exist"

        # Find VarSet
        vs = None
        for child in part.Group:
            if child.TypeId == "App::VarSet":
                vs = child
                break
        assert vs is not None, "VarSet should exist"

        # Enable shelf
        vs.ShowGlassShelf = True
        doc.recompute()

        # Check shelf child exists
        shelf = None
        for child in part.Group:
            if child.Label == "GlassShelf":
                shelf = child
                break
        assert shelf is not None, "GlassShelf child should exist after enabling"

        # Disable shelf
        vs.ShowGlassShelf = False
        doc.recompute()

        shelf_after = None
        for child in part.Group:
            if child.Label == "GlassShelf":
                shelf_after = child
                break
        assert shelf_after is None, "GlassShelf should be removed when disabled"

        print("  AlcoveEnclosure shelf integration - PASSED")
    finally:
        App.closeDocument(doc.Name)


# -----------------------------------------------------------------------
# Runner
# -----------------------------------------------------------------------

def run_all_tests():
    """Run all glass shelf tests."""
    print("\n" + "#" * 70)
    print("# Glass Shelf Tests")
    print("#" * 70)

    tests = [
        test_createGlassShelfShape_basic,
        test_createGlassShelfShape_with_clearances,
        test_createGlassShelfShape_custom_step,
        test_createGlassShelf_standalone,
        test_glassShelf_property_changes,
        test_glass_shelf_specs,
        test_shelf_clamp_mapping,
        test_corner_enclosure_shelf,
        test_alcove_enclosure_shelf,
    ]

    passed = 0
    failed = 0
    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  FAILED: {e}")

    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)}")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
