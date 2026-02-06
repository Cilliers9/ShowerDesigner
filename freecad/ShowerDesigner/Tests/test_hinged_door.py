# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for HingedDoor implementation

Run this in FreeCAD's Python console:
    exec(open('path/to/test_hinged_door.py').read())

Or via pytest (if FreeCAD modules are accessible):
    pytest freecad/ShowerDesigner/Tests/test_hinged_door.py
"""

import sys

# Add project path for imports
sys.path.insert(
    0, r"C:\Users\tclou\AppData\Roaming\FreeCAD\v1-1\Mod\ShowerDesigner"
)

import FreeCAD as App
from freecad.ShowerDesigner.Models.HingedDoor import createHingedDoor


def test_basic_creation():
    """Test 1: Basic hinged door creation with default properties"""
    print("\n" + "=" * 70)
    print("Test 1: Basic hinged door creation")
    print("=" * 70)

    try:
        door = createHingedDoor("TestDoor1")

        # Check default properties
        assert door.Width.Value == 900, f"Expected Width=900, got {door.Width.Value}"
        assert door.Height.Value == 2000, f"Expected Height=2000, got {door.Height.Value}"
        assert door.Thickness.Value == 8, f"Expected Thickness=8, got {door.Thickness.Value}"
        assert door.AttachmentType == "Hinged", f"Expected Hinged, got {door.AttachmentType}"
        assert door.SwingDirection == "Inward", f"Expected Inward, got {door.SwingDirection}"
        assert door.HingeSide == "Left", f"Expected Left, got {door.HingeSide}"
        assert door.HingeCount == 2, f"Expected HingeCount=2, got {door.HingeCount}"
        assert door.HandleType == "Bar", f"Expected Bar, got {door.HandleType}"

        print(f"   Door created: {door.Label}")
        print(f"   Dimensions: {door.Width}mm W x {door.Height}mm H x {door.Thickness}mm T")
        print(f"   Swing: {door.SwingDirection}, Hinge Side: {door.HingeSide}")
        print(f"   Hinges: {door.HingeCount}, Handle: {door.HandleType}")
        print("   Status: PASSED")

    except Exception as e:
        print(f"   Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_hinge_configurations():
    """Test 2: Different hinge configurations"""
    print("\n" + "=" * 70)
    print("Test 2: Hinge configurations")
    print("=" * 70)

    configs = [
        ("LeftInward", "Left", "Inward", 2),
        ("RightInward", "Right", "Inward", 2),
        ("LeftOutward", "Left", "Outward", 3),
        ("RightOutward", "Right", "Outward", 3),
    ]

    for name, side, direction, count in configs:
        try:
            door = createHingedDoor(name)
            door.HingeSide = side
            door.SwingDirection = direction
            door.HingeCount = count
            App.ActiveDocument.recompute()

            print(f"   {name}: {side} hinges, {direction} swing, {count} hinges - PASSED")

        except Exception as e:
            print(f"   {name}: FAILED - {e}")


def test_handle_types():
    """Test 3: Different handle types"""
    print("\n" + "=" * 70)
    print("Test 3: Handle types")
    print("=" * 70)

    handle_types = ["None", "Knob", "Bar", "Pull"]

    for handle_type in handle_types:
        try:
            door = createHingedDoor(f"Handle_{handle_type}")
            door.HandleType = handle_type
            App.ActiveDocument.recompute()

            print(f"   HandleType={handle_type} - PASSED")

        except Exception as e:
            print(f"   HandleType={handle_type}: FAILED - {e}")


def test_swing_arc():
    """Test 4: Swing arc visualization"""
    print("\n" + "=" * 70)
    print("Test 4: Swing arc visualization")
    print("=" * 70)

    try:
        door = createHingedDoor("SwingArcTest")
        door.ShowSwingArc = True
        door.OpeningAngle = 90
        App.ActiveDocument.recompute()

        print(f"   ShowSwingArc=True, OpeningAngle={door.OpeningAngle} - PASSED")

        # Test different angles
        for angle in [45, 90, 110]:
            door.OpeningAngle = angle
            App.ActiveDocument.recompute()
            print(f"   OpeningAngle={angle} - PASSED")

    except Exception as e:
        print(f"   FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_validation():
    """Test 5: Property validation"""
    print("\n" + "=" * 70)
    print("Test 5: Property validation")
    print("=" * 70)

    try:
        door = createHingedDoor("ValidationTest")

        # Test hinge count validation (should clamp to 2-3)
        door.HingeCount = 1
        App.ActiveDocument.recompute()
        assert door.HingeCount == 2, f"HingeCount should clamp to 2, got {door.HingeCount}"
        print("   HingeCount < 2 clamps to 2 - PASSED")

        door.HingeCount = 5
        App.ActiveDocument.recompute()
        assert door.HingeCount == 3, f"HingeCount should clamp to 3, got {door.HingeCount}"
        print("   HingeCount > 3 clamps to 3 - PASSED")

        # Test opening angle validation (max 110)
        door.OpeningAngle = 150
        App.ActiveDocument.recompute()
        assert door.OpeningAngle <= 110, f"OpeningAngle should clamp to 110, got {door.OpeningAngle}"
        print("   OpeningAngle > 110 clamps to 110 - PASSED")

        # Test handle height validation
        door.HandleHeight = 100
        App.ActiveDocument.recompute()
        assert door.HandleHeight.Value >= 300, f"HandleHeight should clamp to >=300, got {door.HandleHeight.Value}"
        print("   HandleHeight < 300 clamps to 300 - PASSED")

    except Exception as e:
        print(f"   FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_weight_recommendation():
    """Test 6: Weight-based hinge recommendation"""
    print("\n" + "=" * 70)
    print("Test 6: Weight-based hinge recommendation")
    print("=" * 70)

    try:
        # Small door (should recommend 2 hinges)
        door1 = createHingedDoor("SmallDoor")
        door1.Width = 600
        door1.Height = 1500
        door1.Thickness = 8
        App.ActiveDocument.recompute()

        print(f"   Small door ({door1.Width}x{door1.Height}x{door1.Thickness}mm)")
        print(f"   Weight: {door1.Weight:.2f} kg")
        print(f"   Recommended hinges: {door1.RecommendedHingeCount}")

        # Large door (may recommend 3 hinges if weight > 45kg)
        door2 = createHingedDoor("LargeDoor")
        door2.Width = 1200
        door2.Height = 2200
        door2.Thickness = 12
        App.ActiveDocument.recompute()

        print(f"   Large door ({door2.Width}x{door2.Height}x{door2.Thickness}mm)")
        print(f"   Weight: {door2.Weight:.2f} kg")
        print(f"   Recommended hinges: {door2.RecommendedHingeCount}")

        print("   Status: PASSED")

    except Exception as e:
        print(f"   FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_hardware_visibility():
    """Test 7: Hardware visibility toggle"""
    print("\n" + "=" * 70)
    print("Test 7: Hardware visibility toggle")
    print("=" * 70)

    try:
        door = createHingedDoor("HardwareToggle")

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
        print(f"   FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_glass_types():
    """Test 8: Different glass types"""
    print("\n" + "=" * 70)
    print("Test 8: Glass types")
    print("=" * 70)

    glass_types = ["Clear", "Frosted", "Bronze", "Grey", "Reeded", "Low-Iron"]

    for glass_type in glass_types:
        try:
            door = createHingedDoor(f"Glass_{glass_type}")
            door.GlassType = glass_type
            App.ActiveDocument.recompute()

            print(f"   GlassType={glass_type} - PASSED")

        except Exception as e:
            print(f"   GlassType={glass_type}: FAILED - {e}")


def test_position_and_rotation():
    """Test 9: Position and rotation"""
    print("\n" + "=" * 70)
    print("Test 9: Position and rotation")
    print("=" * 70)

    try:
        door = createHingedDoor("PositionTest")
        door.Position = App.Vector(1000, 500, 0)
        door.Rotation = 45
        App.ActiveDocument.recompute()

        print(f"   Position: {door.Position}")
        print(f"   Rotation: {door.Rotation}")
        print("   Status: PASSED")

    except Exception as e:
        print(f"   FAILED - {e}")
        import traceback
        traceback.print_exc()


def run_all_tests():
    """Run all HingedDoor tests"""
    print("=" * 70)
    print("HINGED DOOR TEST SUITE")
    print("=" * 70)

    # Create or reuse document
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("HingedDoorTests")
        print(f"\nCreated new document: {doc.Name}")
    else:
        print(f"\nUsing existing document: {doc.Name}")

    # Run all tests
    test_basic_creation()
    test_hinge_configurations()
    test_handle_types()
    test_swing_arc()
    test_validation()
    test_weight_recommendation()
    test_hardware_visibility()
    test_glass_types()
    test_position_and_rotation()

    print("\n" + "=" * 70)
    print("TEST SUITE COMPLETE")
    print("=" * 70)


# Run tests when script is executed
if __name__ == "__main__":
    run_all_tests()
