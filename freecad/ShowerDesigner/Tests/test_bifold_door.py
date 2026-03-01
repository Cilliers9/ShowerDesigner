# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for BiFoldDoor assembly implementation.

Run this in FreeCAD's Python console:
    exec(open('path/to/test_bifold_door.py').read())
"""

import sys
sys.path.insert(
    0, r"C:\Users\tclou\AppData\Roaming\FreeCAD\v1-1\Mod\ShowerDesigner"
)

import FreeCAD as App
from freecad.ShowerDesigner.Models.BiFoldDoor import createBiFoldDoor


def _get_varset(part_obj):
    for child in part_obj.Group:
        if child.TypeId == "App::VarSet":
            return child
    return None


def _get_children_by_prefix(part_obj, prefix):
    return [c for c in part_obj.Group if c.Label.startswith(prefix)]


def test_basic_creation():
    """Test 1: Basic bi-fold door assembly creation."""
    print("\n" + "=" * 70)
    print("Test 1: Basic bi-fold door creation")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestBiFold1")
        assert door.TypeId == "App::Part", f"Expected App::Part, got {door.TypeId}"
        print("  OK: Object is App::Part")

        vs = _get_varset(door)
        assert vs is not None, "VarSet not found"
        print("  OK: VarSet found")

        wall_panels = _get_children_by_prefix(door, "WallPanel")
        assert len(wall_panels) == 1, f"Expected 1 WallPanel, got {len(wall_panels)}"
        print("  OK: WallPanel child found")

        free_panels = _get_children_by_prefix(door, "FreePanel")
        assert len(free_panels) == 1, f"Expected 1 FreePanel, got {len(free_panels)}"
        print("  OK: FreePanel child found")

        assert vs.Width.Value == 900
        assert vs.Height.Value == 2000
        assert vs.Thickness.Value == 8
        assert vs.FoldDirection == "Inward"
        assert vs.HingeSide == "Left"
        assert vs.FoldAngle.Value == 0
        assert vs.HandleType == "mushroom_knob_b2b"
        assert vs.ShowHardware is True
        assert vs.ShowFoldedPosition is False
        assert vs.HingeCount == 2
        print("  OK: VarSet default properties correct")

        wall_hinges = _get_children_by_prefix(door, "WallHinge")
        assert len(wall_hinges) == 2, f"Expected 2 WallHinge, got {len(wall_hinges)}"
        print("  OK: 2 wall hinge children created")

        fold_hinges = _get_children_by_prefix(door, "FoldHinge")
        assert len(fold_hinges) == 2, f"Expected 2 FoldHinge, got {len(fold_hinges)}"
        print("  OK: 2 fold hinge children created")

        handles = _get_children_by_prefix(door, "Handle")
        assert len(handles) == 1, f"Expected 1 Handle, got {len(handles)}"
        print("  OK: Handle child created")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_panel_width_calculation():
    """Test 2: Panel width is half of total width."""
    print("\n" + "=" * 70)
    print("Test 2: Panel width calculation")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestPanelWidth")
        vs = _get_varset(door)
        vs.Width = 1000
        App.ActiveDocument.recompute()

        expected = 500
        actual = vs.PanelWidth.Value
        assert abs(actual - expected) < 0.01, (
            f"Expected PanelWidth={expected}, got {actual}"
        )
        print(f"  Width=1000 -> PanelWidth={actual} - PASSED")

        vs.Width = 800
        App.ActiveDocument.recompute()
        expected = 400
        actual = vs.PanelWidth.Value
        assert abs(actual - expected) < 0.01, (
            f"Expected PanelWidth={expected}, got {actual}"
        )
        print(f"  Width=800 -> PanelWidth={actual} - PASSED")

    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_folded_width():
    """Test 3: Folded width = PanelWidth + Thickness."""
    print("\n" + "=" * 70)
    print("Test 3: Folded width")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestFolded")
        vs = _get_varset(door)
        vs.Width = 900
        vs.Thickness = 8
        App.ActiveDocument.recompute()

        panel_width = 450
        expected = panel_width + 8
        actual = vs.FoldedWidth.Value
        assert abs(actual - expected) < 0.01, (
            f"Expected FoldedWidth={expected}, got {actual}"
        )
        print(f"  FoldedWidth={actual} (expected {expected}) - PASSED")

    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_opening_width():
    """Test 4: Opening width = Width - FoldedWidth."""
    print("\n" + "=" * 70)
    print("Test 4: Opening width")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestOpening")
        vs = _get_varset(door)
        vs.Width = 900
        vs.Thickness = 8
        App.ActiveDocument.recompute()

        folded_width = 450 + 8
        expected = 900 - folded_width
        actual = vs.OpeningWidth.Value
        assert abs(actual - expected) < 0.01, (
            f"Expected OpeningWidth={expected}, got {actual}"
        )
        print(f"  OpeningWidth={actual} (expected {expected}) - PASSED")

    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_clearance_depth():
    """Test 5: Clearance depth = PanelWidth."""
    print("\n" + "=" * 70)
    print("Test 5: Clearance depth")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestClearance")
        vs = _get_varset(door)
        vs.Width = 900
        App.ActiveDocument.recompute()

        expected = 450
        actual = vs.ClearanceDepth.Value
        assert abs(actual - expected) < 0.01, (
            f"Expected ClearanceDepth={expected}, got {actual}"
        )
        print(f"  ClearanceDepth={actual} (expected {expected}) - PASSED")

    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_hinge_configurations():
    """Test 6: Different hinge/fold configurations."""
    print("\n" + "=" * 70)
    print("Test 6: Hinge configurations")
    print("=" * 70)

    configs = [
        ("LeftHinge2", "Left", "Inward", 2),
        ("RightHinge2", "Right", "Outward", 2),
        ("LeftHinge3", "Left", "Inward", 3),
    ]

    for name, hinge_side, fold_direction, hinge_count in configs:
        try:
            door = createBiFoldDoor(name)
            vs = _get_varset(door)
            vs.HingeSide = hinge_side
            vs.FoldDirection = fold_direction
            vs.HingeCount = hinge_count
            App.ActiveDocument.recompute()

            fold_hinges = _get_children_by_prefix(door, "FoldHinge")
            assert len(fold_hinges) == hinge_count, (
                f"Expected {hinge_count} fold hinges, got {len(fold_hinges)}"
            )

            wall_hinges = _get_children_by_prefix(door, "WallHinge")
            assert len(wall_hinges) == 2, (
                f"Expected 2 wall hinges, got {len(wall_hinges)}"
            )

            print(f"  {name}: side={hinge_side}, fold hinges={hinge_count} - PASSED")
        except Exception as e:
            print(f"  {name}: FAILED - {e}")


def test_handle_types():
    """Test 7: Different handle types."""
    print("\n" + "=" * 70)
    print("Test 7: Handle types")
    print("=" * 70)

    for handle_type in ["None", "mushroom_knob_b2b", "pull_handle_round", "flush_handle_with_plate"]:
        try:
            safe_name = handle_type.replace("_", "")
            door = createBiFoldDoor(f"Handle_{safe_name}")
            vs = _get_varset(door)
            vs.HandleType = handle_type
            App.ActiveDocument.recompute()

            handles = _get_children_by_prefix(door, "Handle")
            if handle_type == "None":
                assert len(handles) == 0, (
                    f"Expected 0 handles for None, got {len(handles)}"
                )
            else:
                assert len(handles) == 1, (
                    f"Expected 1 handle for {handle_type}, got {len(handles)}"
                )
            print(f"  HandleType={handle_type} - PASSED")
        except Exception as e:
            print(f"  HandleType={handle_type}: FAILED - {e}")


def test_ghost_toggle():
    """Test 8: Folded position ghost toggle."""
    print("\n" + "=" * 70)
    print("Test 8: Folded position ghost")
    print("=" * 70)

    try:
        door = createBiFoldDoor("GhostTest")
        vs = _get_varset(door)
        vs.ShowFoldedPosition = True
        App.ActiveDocument.recompute()

        ghosts = _get_children_by_prefix(door, "Ghost")
        assert len(ghosts) == 1, f"Expected 1 Ghost, got {len(ghosts)}"
        print("  ShowFoldedPosition=True: ghost created - PASSED")

        vs.ShowFoldedPosition = False
        App.ActiveDocument.recompute()
        ghosts = _get_children_by_prefix(door, "Ghost")
        assert len(ghosts) == 0, f"Expected 0 Ghost when off, got {len(ghosts)}"
        print("  ShowFoldedPosition=False: ghost removed - PASSED")
    except Exception as e:
        print(f"  FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_show_hardware_toggle():
    """Test 9: Hardware visibility toggle."""
    print("\n" + "=" * 70)
    print("Test 9: Hardware visibility toggle")
    print("=" * 70)

    try:
        door = createBiFoldDoor("HardwareToggle")
        vs = _get_varset(door)
        vs.ShowHardware = True
        App.ActiveDocument.recompute()

        hw = [c for c in door.Group
              if c.TypeId != "App::VarSet"
              and not c.Label.startswith("WallPanel")
              and not c.Label.startswith("FreePanel")]
        assert len(hw) > 0, "Expected hardware children when ShowHardware=True"
        print(f"  ShowHardware=True: {len(hw)} hardware children - OK")

        vs.ShowHardware = False
        App.ActiveDocument.recompute()
        hw = [c for c in door.Group
              if c.TypeId != "App::VarSet"
              and not c.Label.startswith("WallPanel")
              and not c.Label.startswith("FreePanel")]
        assert len(hw) == 0, f"Expected 0 hardware children, got {len(hw)}"
        print("  ShowHardware=False: 0 hardware children - OK")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_calculated_properties():
    """Test 10: Weight and area calculation."""
    print("\n" + "=" * 70)
    print("Test 10: Calculated properties")
    print("=" * 70)

    try:
        door = createBiFoldDoor("CalcTest")
        vs = _get_varset(door)
        vs.Width = 1200
        vs.Height = 2200
        vs.Thickness = 12
        App.ActiveDocument.recompute()

        assert vs.Weight > 0, f"Expected positive weight, got {vs.Weight}"
        assert vs.Area > 0, f"Expected positive area, got {vs.Area}"
        print(f"  Weight: {vs.Weight:.2f} kg, Area: {vs.Area:.3f} m2")
        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def run_all_tests():
    print("=" * 70)
    print("BI-FOLD DOOR ASSEMBLY TEST SUITE")
    print("=" * 70)

    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("BiFoldDoorTests")
        print(f"\nCreated new document: {doc.Name}")
    else:
        print(f"\nUsing existing document: {doc.Name}")

    test_basic_creation()
    test_panel_width_calculation()
    test_folded_width()
    test_opening_width()
    test_clearance_depth()
    test_hinge_configurations()
    test_handle_types()
    test_ghost_toggle()
    test_show_hardware_toggle()
    test_calculated_properties()

    print("\n" + "=" * 70)
    print("TEST SUITE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
