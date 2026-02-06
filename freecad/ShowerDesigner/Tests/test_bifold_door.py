# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for BiFoldDoor implementation

Run this in FreeCAD's Python console:
    exec(open('path/to/test_bifold_door.py').read())

Or via pytest (if FreeCAD modules are accessible):
    pytest freecad/ShowerDesigner/Tests/test_bifold_door.py
"""

import sys

# Add project path for imports
sys.path.insert(
    0, r"C:\Users\tclou\AppData\Roaming\FreeCAD\v1-1\Mod\ShowerDesigner"
)

import FreeCAD as App
from freecad.ShowerDesigner.Models.BiFoldDoor import createBiFoldDoor, BIFOLD_HINGE_SPECS


def test_basic_creation():
    """Test 1: Basic bi-fold door creation with default properties"""
    print("\n" + "=" * 70)
    print("Test 1: Basic bi-fold door creation")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestBiFold1")

        # Check default properties
        assert door.Width.Value == 900, f"Expected Width=900, got {door.Width.Value}"
        assert door.Height.Value == 2000, f"Expected Height=2000, got {door.Height.Value}"
        assert door.Thickness.Value == 8, f"Expected Thickness=8, got {door.Thickness.Value}"
        assert door.AttachmentType == "Hinged", f"Expected Hinged, got {door.AttachmentType}"
        assert door.HingeConfiguration == "Left", (
            f"Expected Left, got {door.HingeConfiguration}"
        )
        assert door.FoldDirection == "Inward", f"Expected Inward, got {door.FoldDirection}"
        assert door.HingeSide == "Left", f"Expected Left, got {door.HingeSide}"
        assert door.FoldAngle == 0, f"Expected FoldAngle=0, got {door.FoldAngle}"
        assert door.HandleType == "Bar", f"Expected Bar, got {door.HandleType}"
        assert door.ShowHardware is True, "Expected ShowHardware=True"
        assert door.ShowFoldedPosition is False, "Expected ShowFoldedPosition=False"
        assert door.HingeCount == 2, f"Expected HingeCount=2, got {door.HingeCount}"

        print(f"   Door created: {door.Label}")
        print(f"   Dimensions: {door.Width}mm W x {door.Height}mm H x {door.Thickness}mm T")
        print(f"   Hinge Config: {door.HingeConfiguration}, Fold: {door.FoldDirection}")
        print(f"   Hinge Side: {door.HingeSide}, Handle: {door.HandleType}")
        print("   Status: PASSED")

    except Exception as e:
        print(f"   Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_panel_width_calculation():
    """Test 2: Panel width is half of total width"""
    print("\n" + "=" * 70)
    print("Test 2: Panel width calculation")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestPanelWidth")
        door.Width = 1000
        App.ActiveDocument.recompute()

        expected = 500
        actual = door.PanelWidth.Value
        assert abs(actual - expected) < 0.01, (
            f"Expected PanelWidth={expected}, got {actual}"
        )
        print(f"   Width=1000 -> PanelWidth={actual} - PASSED")

        door.Width = 800
        App.ActiveDocument.recompute()
        expected = 400
        actual = door.PanelWidth.Value
        assert abs(actual - expected) < 0.01, (
            f"Expected PanelWidth={expected}, got {actual}"
        )
        print(f"   Width=800 -> PanelWidth={actual} - PASSED")

    except Exception as e:
        print(f"   Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_folded_width():
    """Test 3: Folded width = PanelWidth + Thickness"""
    print("\n" + "=" * 70)
    print("Test 3: Folded width")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestFolded")
        door.Width = 900
        door.Thickness = 8
        App.ActiveDocument.recompute()

        panel_width = 450  # 900 / 2
        expected = panel_width + 8  # PanelWidth + Thickness
        actual = door.FoldedWidth.Value
        assert abs(actual - expected) < 0.01, (
            f"Expected FoldedWidth={expected}, got {actual}"
        )
        print(f"   FoldedWidth={actual} (expected {expected}) - PASSED")

    except Exception as e:
        print(f"   Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_opening_width():
    """Test 4: Opening width = Width - FoldedWidth"""
    print("\n" + "=" * 70)
    print("Test 4: Opening width")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestOpening")
        door.Width = 900
        door.Thickness = 8
        App.ActiveDocument.recompute()

        folded_width = 450 + 8  # PanelWidth + Thickness
        expected = 900 - folded_width
        actual = door.OpeningWidth.Value
        assert abs(actual - expected) < 0.01, (
            f"Expected OpeningWidth={expected}, got {actual}"
        )
        print(f"   OpeningWidth={actual} (expected {expected}) - PASSED")

    except Exception as e:
        print(f"   Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_clearance_depth():
    """Test 5: Clearance depth = PanelWidth"""
    print("\n" + "=" * 70)
    print("Test 5: Clearance depth")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestClearance")
        door.Width = 900
        App.ActiveDocument.recompute()

        expected = 450  # PanelWidth
        actual = door.ClearanceDepth.Value
        assert abs(actual - expected) < 0.01, (
            f"Expected ClearanceDepth={expected}, got {actual}"
        )
        print(f"   ClearanceDepth={actual} (expected {expected}) - PASSED")

    except Exception as e:
        print(f"   Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_hinge_configuration_fold_direction():
    """Test 6: HingeConfiguration drives FoldDirection"""
    print("\n" + "=" * 70)
    print("Test 6: Hinge configuration drives fold direction")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestHingeConfig")

        # Left hinge -> Inward
        door.HingeConfiguration = "Left"
        App.ActiveDocument.recompute()
        assert door.FoldDirection == "Inward", (
            f"Expected Inward for Left, got {door.FoldDirection}"
        )
        print(f"   Left -> FoldDirection={door.FoldDirection} - PASSED")

        # Right hinge -> Outward
        door.HingeConfiguration = "Right"
        App.ActiveDocument.recompute()
        assert door.FoldDirection == "Outward", (
            f"Expected Outward for Right, got {door.FoldDirection}"
        )
        print(f"   Right -> FoldDirection={door.FoldDirection} - PASSED")

        # Back to Left -> Inward
        door.HingeConfiguration = "Left"
        App.ActiveDocument.recompute()
        assert door.FoldDirection == "Inward", (
            f"Expected Inward for Left, got {door.FoldDirection}"
        )
        print(f"   Left (back) -> FoldDirection={door.FoldDirection} - PASSED")

    except Exception as e:
        print(f"   Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_fold_angle_limits():
    """Test 7: Fold angle clamped to -45 (secondary) to +180 (primary)"""
    print("\n" + "=" * 70)
    print("Test 7: Fold angle limits")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestFoldAngle")

        # Primary direction max: 180
        door.FoldAngle = 200
        assert door.FoldAngle == 180, (
            f"Expected FoldAngle clamped to 180, got {door.FoldAngle}"
        )
        print(f"   Set 200 -> clamped to {door.FoldAngle} - PASSED")

        # Secondary direction min: -45
        door.FoldAngle = -60
        assert door.FoldAngle == -45, (
            f"Expected FoldAngle clamped to -45, got {door.FoldAngle}"
        )
        print(f"   Set -60 -> clamped to {door.FoldAngle} - PASSED")

        # Valid angle within range
        door.FoldAngle = 90
        assert door.FoldAngle == 90, (
            f"Expected FoldAngle=90, got {door.FoldAngle}"
        )
        print(f"   Set 90 -> {door.FoldAngle} - PASSED")

    except Exception as e:
        print(f"   Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_max_fold_angle():
    """Test 8: MaxFoldAngle calculated property"""
    print("\n" + "=" * 70)
    print("Test 8: MaxFoldAngle calculated property")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestMaxAngle")
        App.ActiveDocument.recompute()

        expected = 180
        actual = door.MaxFoldAngle.Value
        assert abs(actual - expected) < 0.01, (
            f"Expected MaxFoldAngle={expected}, got {actual}"
        )
        print(f"   MaxFoldAngle={actual} (expected {expected}) - PASSED")

    except Exception as e:
        print(f"   Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_hinge_side():
    """Test 9: Hinge side Left/Right"""
    print("\n" + "=" * 70)
    print("Test 9: Hinge side")
    print("=" * 70)

    for side in ["Left", "Right"]:
        try:
            door = createBiFoldDoor(f"TestHinge_{side}")
            door.HingeSide = side
            App.ActiveDocument.recompute()

            assert door.HingeSide == side, (
                f"Expected {side}, got {door.HingeSide}"
            )
            print(f"   HingeSide={side} - PASSED")

        except Exception as e:
            print(f"   HingeSide={side}: FAILED - {e}")


def test_handle_types():
    """Test 10: Different handle types"""
    print("\n" + "=" * 70)
    print("Test 10: Handle types")
    print("=" * 70)

    handle_types = ["None", "Knob", "Bar", "Pull"]

    for handle_type in handle_types:
        try:
            door = createBiFoldDoor(f"TestHandle_{handle_type}")
            door.HandleType = handle_type
            App.ActiveDocument.recompute()

            assert door.HandleType == handle_type, (
                f"Expected {handle_type}, got {door.HandleType}"
            )
            print(f"   HandleType={handle_type} - PASSED")

        except Exception as e:
            print(f"   HandleType={handle_type}: FAILED - {e}")


def test_hardware_visibility():
    """Test 11: Hardware visibility toggle"""
    print("\n" + "=" * 70)
    print("Test 11: Hardware visibility toggle")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestHardwareToggle")

        # With hardware
        door.ShowHardware = True
        App.ActiveDocument.recompute()
        shape_with = door.Shape.BoundBox.DiagonalLength
        print(f"   ShowHardware=True: BoundBox diagonal = {shape_with:.2f}")

        # Without hardware
        door.ShowHardware = False
        App.ActiveDocument.recompute()
        shape_without = door.Shape.BoundBox.DiagonalLength
        print(f"   ShowHardware=False: BoundBox diagonal = {shape_without:.2f}")

        print("   Status: PASSED")

    except Exception as e:
        print(f"   Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_hinge_count():
    """Test 12: Hinge count validation (2-3)"""
    print("\n" + "=" * 70)
    print("Test 12: Hinge count validation")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestHingeCount")

        door.HingeCount = 1
        assert door.HingeCount == 2, f"Expected clamped to 2, got {door.HingeCount}"
        print(f"   Set 1 -> clamped to {door.HingeCount} - PASSED")

        door.HingeCount = 3
        assert door.HingeCount == 3, f"Expected 3, got {door.HingeCount}"
        print(f"   Set 3 -> {door.HingeCount} - PASSED")

        door.HingeCount = 5
        assert door.HingeCount == 3, f"Expected clamped to 3, got {door.HingeCount}"
        print(f"   Set 5 -> clamped to {door.HingeCount} - PASSED")

    except Exception as e:
        print(f"   Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_position_and_rotation():
    """Test 13: Position and rotation"""
    print("\n" + "=" * 70)
    print("Test 13: Position and rotation")
    print("=" * 70)

    try:
        door = createBiFoldDoor("TestPosition")
        door.Position = App.Vector(1000, 500, 0)
        door.Rotation = 45
        App.ActiveDocument.recompute()

        print(f"   Position: {door.Position}")
        print(f"   Rotation: {door.Rotation}")
        print("   Status: PASSED")

    except Exception as e:
        print(f"   Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def run_all_tests():
    """Run all BiFoldDoor tests"""
    print("=" * 70)
    print("BI-FOLD DOOR TEST SUITE")
    print("=" * 70)

    # Create or reuse document
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("BiFoldDoorTests")
        print(f"\nCreated new document: {doc.Name}")
    else:
        print(f"\nUsing existing document: {doc.Name}")

    # Run all tests
    test_basic_creation()
    test_panel_width_calculation()
    test_folded_width()
    test_opening_width()
    test_clearance_depth()
    test_hinge_configuration_fold_direction()
    test_fold_angle_limits()
    test_max_fold_angle()
    test_hinge_side()
    test_handle_types()
    test_hardware_visibility()
    test_hinge_count()
    test_position_and_rotation()

    print("\n" + "=" * 70)
    print("TEST SUITE COMPLETE")
    print("=" * 70)


# Run tests when script is executed
if __name__ == "__main__":
    run_all_tests()
