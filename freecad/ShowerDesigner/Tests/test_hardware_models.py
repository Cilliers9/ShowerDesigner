# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for standalone hardware model classes.

Requires FreeCAD accessible. Run in FreeCAD console:
    exec(open('path/to/test_hardware_models.py').read())

Or via pytest (if FreeCAD modules are accessible):
    pytest freecad/ShowerDesigner/Tests/test_hardware_models.py
"""

import sys
sys.path.insert(
    0, r"C:\Users\tclou\AppData\Roaming\FreeCAD\v1-1\Mod\ShowerDesigner"
)

import FreeCAD as App
from freecad.ShowerDesigner.Models.Hinge import createHinge, createHingeShape
from freecad.ShowerDesigner.Models.Handle import createHandle, createHandleShape
from freecad.ShowerDesigner.Models.Clamp import createClamp, createClampShape
from freecad.ShowerDesigner.Models.SupportBar import createSupportBar, createSupportBarShape
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    HINGE_SPECS,
    HANDLE_SPECS,
    CLAMP_SPECS,
    SUPPORT_BAR_SPECS,
)


# -----------------------------------------------------------------------
# Shape function tests
# -----------------------------------------------------------------------

def test_createHingeShape():
    """Test standalone hinge shape creation."""
    print("\n" + "=" * 70)
    print("Test: createHingeShape")
    print("=" * 70)

    shape = createHingeShape(65, 20, 90)
    assert shape is not None, "Shape should not be None"
    assert shape.BoundBox.XLength == 65
    assert shape.BoundBox.YLength == 20
    assert shape.BoundBox.ZLength == 90
    print("  createHingeShape(65, 20, 90) - PASSED")


def test_createHandleShape_knob():
    """Test mushroom knob handle shape (catalogue key: mushroom_knob_b2b)."""
    print("\n" + "=" * 70)
    print("Test: createHandleShape - mushroom_knob_b2b")
    print("=" * 70)

    shape = createHandleShape("mushroom_knob_b2b")
    assert shape is not None, "mushroom_knob_b2b shape should not be None"
    print("  createHandleShape('mushroom_knob_b2b') - PASSED")


def test_createHandleShape_bar():
    """Test pull handle (round) shape (catalogue key: pull_handle_round)."""
    print("\n" + "=" * 70)
    print("Test: createHandleShape - pull_handle_round")
    print("=" * 70)

    shape = createHandleShape("pull_handle_round")
    assert shape is not None, "pull_handle_round shape should not be None"
    print("  createHandleShape('pull_handle_round') - PASSED")


def test_createHandleShape_pull():
    """Test flush handle with plate shape (catalogue key: flush_handle_with_plate)."""
    print("\n" + "=" * 70)
    print("Test: createHandleShape - flush_handle_with_plate")
    print("=" * 70)

    shape = createHandleShape("flush_handle_with_plate")
    assert shape is not None, "flush_handle_with_plate shape should not be None"
    print("  createHandleShape('flush_handle_with_plate') - PASSED")


def test_createHandleShape_none():
    """Test that 'None' handle type returns None."""
    print("\n" + "=" * 70)
    print("Test: createHandleShape - None")
    print("=" * 70)

    shape = createHandleShape("None")
    assert shape is None, "None handle should return None"
    print("  createHandleShape('None') returns None - PASSED")


def test_createClampShape():
    """Test standalone clamp shape creation for all types."""
    print("\n" + "=" * 70)
    print("Test: createClampShape")
    print("=" * 70)

    for clamp_type in CLAMP_SPECS:
        shape = createClampShape(clamp_type)
        bb = CLAMP_SPECS[clamp_type]["bounding_box"]
        assert shape is not None
        # Tolerance for boolean/chamfer floating-point deviation
        assert abs(shape.BoundBox.XLength - bb["width"]) < 0.5, \
            f"{clamp_type} width: expected {bb['width']}, got {shape.BoundBox.XLength}"
        assert abs(shape.BoundBox.YLength - bb["depth"]) < 0.5, \
            f"{clamp_type} depth: expected {bb['depth']}, got {shape.BoundBox.YLength}"
        assert abs(shape.BoundBox.ZLength - bb["height"]) < 0.5, \
            f"{clamp_type} height: expected {bb['height']}, got {shape.BoundBox.ZLength}"
        print(f"  createClampShape('{clamp_type}') - PASSED")


def test_uclamp_topology():
    """U-Clamp should have more faces than a simple box (U-slot creates internal faces)."""
    print("\n" + "=" * 70)
    print("Test: U_Clamp topology")
    print("=" * 70)

    shape = createClampShape("U_Clamp")
    assert len(shape.Faces) > 6, f"U_Clamp should have >6 faces, got {len(shape.Faces)}"
    print(f"  U_Clamp faces: {len(shape.Faces)} - PASSED")


def test_lclamp_topology():
    """L-Clamp compound should have two solids (L-body + pressure plate)."""
    print("\n" + "=" * 70)
    print("Test: L_Clamp topology")
    print("=" * 70)

    shape = createClampShape("L_Clamp")
    assert len(shape.Solids) >= 2, \
        f"L_Clamp should have >=2 solids, got {len(shape.Solids)}"
    print(f"  L_Clamp solids: {len(shape.Solids)} - PASSED")


def test_createSupportBarShape():
    """Test standalone support bar shape creation."""
    print("\n" + "=" * 70)
    print("Test: createSupportBarShape")
    print("=" * 70)

    for bar_type in SUPPORT_BAR_SPECS:
        shape = createSupportBarShape(bar_type, 500, 16)
        assert shape is not None
        print(f"  createSupportBarShape('{bar_type}', 500, 16) - PASSED")


# -----------------------------------------------------------------------
# FreeCAD object creation tests
# -----------------------------------------------------------------------

def test_createHinge_object():
    """Test Hinge FreeCAD object creation."""
    print("\n" + "=" * 70)
    print("Test: createHinge (FreeCAD object)")
    print("=" * 70)

    obj = createHinge("TestHinge")
    assert obj is not None
    assert hasattr(obj, "HingeType")
    assert hasattr(obj, "LoadCapacity")
    assert hasattr(obj, "Finish")
    assert obj.HingeType == "standard_wall_mount"

    # Change type and recompute
    for hinge_type in HINGE_SPECS:
        obj.HingeType = hinge_type
        App.ActiveDocument.recompute()
        expected_cap = HINGE_SPECS[hinge_type]["load_capacity_kg"]
        assert obj.LoadCapacity == expected_cap, \
            f"Expected capacity {expected_cap}, got {obj.LoadCapacity}"
        print(f"  HingeType={hinge_type}, LoadCapacity={obj.LoadCapacity}kg - PASSED")


def test_createClamp_object():
    """Test Clamp FreeCAD object creation."""
    print("\n" + "=" * 70)
    print("Test: createClamp (FreeCAD object)")
    print("=" * 70)

    obj = createClamp("TestClamp")
    assert obj is not None
    assert hasattr(obj, "ClampType")
    assert hasattr(obj, "MountingType")
    assert hasattr(obj, "LoadCapacity")

    for clamp_type in CLAMP_SPECS:
        obj.ClampType = clamp_type
        App.ActiveDocument.recompute()
        expected_cap = CLAMP_SPECS[clamp_type]["load_capacity_kg"]
        assert obj.LoadCapacity == expected_cap
        print(f"  ClampType={clamp_type}, LoadCapacity={obj.LoadCapacity}kg - PASSED")


def test_createHandle_object():
    """Test Handle FreeCAD object creation."""
    print("\n" + "=" * 70)
    print("Test: createHandle (FreeCAD object)")
    print("=" * 70)

    obj = createHandle("TestHandle")
    assert obj is not None
    assert hasattr(obj, "HandleType")
    assert hasattr(obj, "HandleLength")
    assert hasattr(obj, "Finish")

    for handle_type in HANDLE_SPECS:
        obj.HandleType = handle_type
        App.ActiveDocument.recompute()
        print(f"  HandleType={handle_type} - PASSED")


def test_createSupportBar_object():
    """Test SupportBar FreeCAD object creation."""
    print("\n" + "=" * 70)
    print("Test: createSupportBar (FreeCAD object)")
    print("=" * 70)

    obj = createSupportBar("TestSupportBar")
    assert obj is not None
    assert hasattr(obj, "BarType")
    assert hasattr(obj, "Length")
    assert hasattr(obj, "Diameter")

    for bar_type in SUPPORT_BAR_SPECS:
        obj.BarType = bar_type
        App.ActiveDocument.recompute()
        print(f"  BarType={bar_type} - PASSED")

    # Test diameter clamping
    obj.BarType = "Horizontal"
    obj.Diameter = 5  # Below min (12)
    App.ActiveDocument.recompute()
    assert obj.Diameter.Value >= 12, f"Diameter should clamp to >=12, got {obj.Diameter.Value}"
    print("  Diameter clamp (min) - PASSED")

    obj.Diameter = 30  # Above max (25)
    App.ActiveDocument.recompute()
    assert obj.Diameter.Value <= 25, f"Diameter should clamp to <=25, got {obj.Diameter.Value}"
    print("  Diameter clamp (max) - PASSED")


# -----------------------------------------------------------------------
# Runner
# -----------------------------------------------------------------------

def run_all_tests():
    """Run all hardware model tests."""
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("HardwareModelTests")
        print(f"\nCreated document: {doc.Name}")
    else:
        print(f"\nUsing document: {doc.Name}")

    test_createHingeShape()
    test_createHandleShape_knob()
    test_createHandleShape_bar()
    test_createHandleShape_pull()
    test_createHandleShape_none()
    test_createClampShape()
    test_uclamp_topology()
    test_lclamp_topology()
    test_createSupportBarShape()
    test_createHinge_object()
    test_createClamp_object()
    test_createHandle_object()
    test_createSupportBar_object()

    print("\n" + "=" * 70)
    print("HARDWARE MODELS TEST SUITE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
