# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for HingedDoor assembly implementation.

Run this in FreeCAD's Python console:
    exec(open('path/to/test_hinged_door.py').read())
"""

import sys
sys.path.insert(
    0, r"C:\Users\tclou\AppData\Roaming\FreeCAD\v1-1\Mod\ShowerDesigner"
)

import FreeCAD as App
from freecad.ShowerDesigner.Models.HingedDoor import createHingedDoor


def _get_varset(part_obj):
    for child in part_obj.Group:
        if child.TypeId == "App::VarSet":
            return child
    return None


def _get_children_by_prefix(part_obj, prefix):
    return [c for c in part_obj.Group if c.Label.startswith(prefix)]


def test_basic_creation():
    """Test 1: Basic hinged door assembly creation."""
    print("\n" + "=" * 70)
    print("Test 1: Basic hinged door creation")
    print("=" * 70)

    try:
        door = createHingedDoor("TestDoor1")
        assert door.TypeId == "App::Part", f"Expected App::Part, got {door.TypeId}"
        print("  OK: Object is App::Part")

        vs = _get_varset(door)
        assert vs is not None, "VarSet not found"
        print("  OK: VarSet found")

        glass = _get_children_by_prefix(door, "Glass")
        assert len(glass) == 1, f"Expected 1 Glass child, got {len(glass)}"
        print("  OK: Glass child found")

        assert vs.Width.Value == 900
        assert vs.Height.Value == 2000
        assert vs.SwingDirection == "Inward"
        assert vs.HingeSide == "Left"
        assert vs.HingeCount == 2
        assert vs.HandleType == "mushroom_knob_b2b"
        print("  OK: VarSet default properties correct")

        hinges = _get_children_by_prefix(door, "Hinge")
        assert len(hinges) == 2, f"Expected 2 Hinge children, got {len(hinges)}"
        print("  OK: 2 hinge children created")

        handles = _get_children_by_prefix(door, "Handle")
        assert len(handles) == 1, f"Expected 1 Handle child, got {len(handles)}"
        print("  OK: Handle child created")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_hinge_configurations():
    """Test 2: Different hinge configurations."""
    print("\n" + "=" * 70)
    print("Test 2: Hinge configurations")
    print("=" * 70)

    configs = [
        ("LeftInward", "Left", "Inward", 2),
        ("RightInward", "Right", "Inward", 2),
        ("LeftOutward3", "Left", "Outward", 3),
        ("RightOutward3", "Right", "Outward", 3),
    ]

    for name, side, direction, count in configs:
        try:
            door = createHingedDoor(name)
            vs = _get_varset(door)
            vs.HingeSide = side
            vs.SwingDirection = direction
            vs.HingeCount = count
            App.ActiveDocument.recompute()

            hinges = _get_children_by_prefix(door, "Hinge")
            assert len(hinges) == count, f"Expected {count} hinges, got {len(hinges)}"
            print(f"  {name}: {side} hinges, {direction} swing, {count} hinges - PASSED")
        except Exception as e:
            print(f"  {name}: FAILED - {e}")


def test_handle_types():
    """Test 3: Different handle types."""
    print("\n" + "=" * 70)
    print("Test 3: Handle types")
    print("=" * 70)

    for handle_type in ["None", "mushroom_knob_b2b", "pull_handle_round", "flush_handle_with_plate"]:
        try:
            safe_name = handle_type.replace("_", "")
            door = createHingedDoor(f"Handle_{safe_name}")
            vs = _get_varset(door)
            vs.HandleType = handle_type
            App.ActiveDocument.recompute()

            handles = _get_children_by_prefix(door, "Handle")
            if handle_type == "None":
                assert len(handles) == 0, f"Expected 0 handles for None, got {len(handles)}"
            else:
                assert len(handles) == 1, f"Expected 1 handle for {handle_type}, got {len(handles)}"
            print(f"  HandleType={handle_type} - PASSED")
        except Exception as e:
            print(f"  HandleType={handle_type}: FAILED - {e}")


def test_swing_arc():
    """Test 4: Swing arc visualization."""
    print("\n" + "=" * 70)
    print("Test 4: Swing arc visualization")
    print("=" * 70)

    try:
        door = createHingedDoor("SwingArcTest")
        vs = _get_varset(door)
        vs.ShowSwingArc = True
        App.ActiveDocument.recompute()

        arcs = _get_children_by_prefix(door, "SwingArc")
        assert len(arcs) == 1, f"Expected 1 SwingArc, got {len(arcs)}"
        print("  ShowSwingArc=True: arc created - PASSED")

        vs.ShowSwingArc = False
        App.ActiveDocument.recompute()
        arcs = _get_children_by_prefix(door, "SwingArc")
        assert len(arcs) == 0, f"Expected 0 SwingArc when off, got {len(arcs)}"
        print("  ShowSwingArc=False: arc removed - PASSED")
    except Exception as e:
        print(f"  FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_show_hardware_toggle():
    """Test 5: Hardware visibility toggle."""
    print("\n" + "=" * 70)
    print("Test 5: Hardware visibility toggle")
    print("=" * 70)

    try:
        door = createHingedDoor("HardwareToggle")
        vs = _get_varset(door)
        vs.ShowHardware = True
        App.ActiveDocument.recompute()

        hw = [c for c in door.Group
              if c.TypeId != "App::VarSet" and c.Label != "Glass"]
        assert len(hw) > 0, "Expected hardware children when ShowHardware=True"
        print(f"  ShowHardware=True: {len(hw)} hardware children - OK")

        vs.ShowHardware = False
        App.ActiveDocument.recompute()
        hw = [c for c in door.Group
              if c.TypeId != "App::VarSet" and c.Label != "Glass"]
        # Hinges and handle removed, but SwingArc is separate (controlled by ShowSwingArc)
        assert len(hw) == 0, f"Expected 0 hardware children, got {len(hw)}"
        print("  ShowHardware=False: 0 hardware children - OK")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_calculated_properties():
    """Test 6: Weight and recommended hinge count."""
    print("\n" + "=" * 70)
    print("Test 6: Calculated properties")
    print("=" * 70)

    try:
        door = createHingedDoor("CalcTest")
        vs = _get_varset(door)
        vs.Width = 1200
        vs.Height = 2200
        vs.Thickness = 12
        App.ActiveDocument.recompute()

        assert vs.Weight > 0, f"Expected positive weight, got {vs.Weight}"
        assert vs.Area > 0, f"Expected positive area, got {vs.Area}"
        assert vs.RecommendedHingeCount in [2, 3]
        print(f"  Weight: {vs.Weight:.2f} kg, Area: {vs.Area:.3f} m2")
        print(f"  RecommendedHingeCount: {vs.RecommendedHingeCount}")
        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def run_all_tests():
    print("=" * 70)
    print("HINGED DOOR ASSEMBLY TEST SUITE")
    print("=" * 70)

    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("HingedDoorTests")
        print(f"\nCreated new document: {doc.Name}")
    else:
        print(f"\nUsing existing document: {doc.Name}")

    test_basic_creation()
    test_hinge_configurations()
    test_handle_types()
    test_swing_arc()
    test_show_hardware_toggle()
    test_calculated_properties()

    print("\n" + "=" * 70)
    print("TEST SUITE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
