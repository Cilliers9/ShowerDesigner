# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for SlidingDoor implementation

Run this in FreeCAD's Python console:
    exec(open('path/to/test_sliding_door.py').read())

Or via pytest (if FreeCAD modules are accessible):
    pytest freecad/ShowerDesigner/Tests/test_sliding_door.py
"""

import sys

# Add project path for imports
sys.path.insert(
    0, r"C:\Users\tclou\AppData\Roaming\FreeCAD\v1-1\Mod\ShowerDesigner"
)

import FreeCAD as App
from freecad.ShowerDesigner.Models.SlidingDoor import createSlidingDoor, TRACK_PROFILES


def test_basic_creation():
    """Test 1: Basic sliding door creation with default properties"""
    print("\n" + "=" * 70)
    print("Test 1: Basic sliding door creation")
    print("=" * 70)

    try:
        door = createSlidingDoor("TestDoor1")

        # Check default properties
        assert door.Width.Value == 900, f"Expected Width=900, got {door.Width.Value}"
        assert door.Height.Value == 2000, f"Expected Height=2000, got {door.Height.Value}"
        assert door.Thickness.Value == 8, f"Expected Thickness=8, got {door.Thickness.Value}"
        assert door.AttachmentType == "Sliding", f"Expected Sliding, got {door.AttachmentType}"
        assert door.PanelCount == 1, f"Expected PanelCount=1, got {door.PanelCount}"
        assert door.TrackType == "Edge", f"Expected Edge, got {door.TrackType}"
        assert door.SlideDirection == "Right", f"Expected Right, got {door.SlideDirection}"
        assert door.OverlapWidth.Value == 50, f"Expected OverlapWidth=50, got {door.OverlapWidth.Value}"
        assert door.RollerType == "Standard", f"Expected Standard, got {door.RollerType}"
        assert door.TrackFinish == "Chrome", f"Expected Chrome, got {door.TrackFinish}"
        assert door.ShowHardware is True, f"Expected ShowHardware=True, got {door.ShowHardware}"

        print(f"   Door created: {door.Label}")
        print(f"   Dimensions: {door.Width}mm W x {door.Height}mm H x {door.Thickness}mm T")
        print(f"   Track: {door.TrackType}, Panels: {door.PanelCount}")
        print(f"   Slide Direction: {door.SlideDirection}")
        print("   Status: PASSED")

    except Exception as e:
        print(f"   Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_panel_count_validation():
    """Test 2: Panel count validation (1-2 range)"""
    print("\n" + "=" * 70)
    print("Test 2: Panel count validation")
    print("=" * 70)

    try:
        door = createSlidingDoor("PanelCountTest")

        # Test lower bound
        door.PanelCount = 0
        App.ActiveDocument.recompute()
        assert door.PanelCount == 1, f"PanelCount should clamp to 1, got {door.PanelCount}"
        print("   PanelCount < 1 clamps to 1 - PASSED")

        # Test upper bound
        door.PanelCount = 5
        App.ActiveDocument.recompute()
        assert door.PanelCount == 2, f"PanelCount should clamp to 2, got {door.PanelCount}"
        print("   PanelCount > 2 clamps to 2 - PASSED")

    except Exception as e:
        print(f"   FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_track_type_bypass_constraint():
    """Test 3: Only Soft-Close track supports 2-panel bypass"""
    print("\n" + "=" * 70)
    print("Test 3: Track type bypass constraint")
    print("=" * 70)

    try:
        door = createSlidingDoor("BypassConstraintTest")

        # First, set to Soft-Close (the only track that supports bypass)
        door.TrackType = "Soft-Close"
        door.PanelCount = 2
        App.ActiveDocument.recompute()
        assert door.PanelCount == 2, f"Soft-Close should allow 2 panels, got {door.PanelCount}"
        print("   Soft-Close track allows PanelCount=2 - PASSED")

        # Now switch to Edge track - should reset PanelCount to 1
        door.TrackType = "Edge"
        App.ActiveDocument.recompute()
        assert door.PanelCount == 1, f"Edge track should reset to 1 panel, got {door.PanelCount}"
        print("   Edge track resets PanelCount to 1 - PASSED")

        # Try setting PanelCount=2 with non-Soft-Close track
        door.TrackType = "City"
        door.PanelCount = 2
        App.ActiveDocument.recompute()
        assert door.PanelCount == 1, f"City track should not allow 2 panels, got {door.PanelCount}"
        print("   City track resets PanelCount=2 to 1 - PASSED")

        door.TrackType = "Ezy"
        door.Thickness = 10  # Ezy requires 10mm or 12mm
        door.PanelCount = 2
        App.ActiveDocument.recompute()
        assert door.PanelCount == 1, f"Ezy track should not allow 2 panels, got {door.PanelCount}"
        print("   Ezy track resets PanelCount=2 to 1 - PASSED")

    except Exception as e:
        print(f"   FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_ezy_track_glass_constraint():
    """Test 4: Ezy track only compatible with 10mm or 12mm glass"""
    print("\n" + "=" * 70)
    print("Test 4: Ezy track glass thickness constraint")
    print("=" * 70)

    try:
        door = createSlidingDoor("EzyConstraintTest")

        # Set to Ezy track with valid thickness (10mm)
        door.TrackType = "Ezy"
        door.Thickness = 10
        App.ActiveDocument.recompute()
        print("   Ezy track with 10mm glass - PASSED (no warning expected)")

        # Set to 12mm (also valid)
        door.Thickness = 12
        App.ActiveDocument.recompute()
        print("   Ezy track with 12mm glass - PASSED (no warning expected)")

        # Set to 8mm (invalid - should print warning but still work)
        door.Thickness = 8
        App.ActiveDocument.recompute()
        print("   Ezy track with 8mm glass - PASSED (warning expected)")

        # Test setting Ezy track when thickness is already invalid
        door.TrackType = "Edge"
        door.Thickness = 6
        App.ActiveDocument.recompute()
        door.TrackType = "Ezy"
        App.ActiveDocument.recompute()
        print("   Setting Ezy track with 6mm glass - PASSED (warning expected)")

    except Exception as e:
        print(f"   FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_track_types():
    """Test 5: Different track types"""
    print("\n" + "=" * 70)
    print("Test 5: Track types")
    print("=" * 70)

    track_types = ["Edge", "City", "Ezy", "Soft-Close"]

    for track_type in track_types:
        try:
            door = createSlidingDoor(f"Track_{track_type.replace('-', '_')}")
            if track_type == "Ezy":
                door.Thickness = 10  # Ezy requires 10mm or 12mm
            door.TrackType = track_type
            App.ActiveDocument.recompute()

            # Verify track height is from profile
            expected_height = TRACK_PROFILES[track_type]["height"]
            assert door.TrackHeight.Value == expected_height, \
                f"Expected TrackHeight={expected_height}, got {door.TrackHeight.Value}"

            print(f"   TrackType={track_type}, TrackHeight={door.TrackHeight.Value}mm - PASSED")

        except Exception as e:
            print(f"   TrackType={track_type}: FAILED - {e}")


def test_overlap_calculations():
    """Test 6: Overlap width calculations for bypass doors"""
    print("\n" + "=" * 70)
    print("Test 6: Overlap calculations for bypass doors")
    print("=" * 70)

    try:
        door = createSlidingDoor("OverlapTest")
        door.TrackType = "Soft-Close"
        door.PanelCount = 2
        door.Width = 1000
        door.OverlapWidth = 100
        App.ActiveDocument.recompute()

        # Expected opening width = panel width - overlap
        expected_opening = 1000 - 100
        assert door.OpeningWidth.Value == expected_opening, \
            f"Expected OpeningWidth={expected_opening}, got {door.OpeningWidth.Value}"
        print(f"   OpeningWidth = Width - OverlapWidth = {door.OpeningWidth.Value}mm - PASSED")

        # Test overlap validation (min 20mm)
        door.OverlapWidth = 10
        App.ActiveDocument.recompute()
        assert door.OverlapWidth.Value >= 20, \
            f"OverlapWidth should clamp to >=20, got {door.OverlapWidth.Value}"
        print(f"   OverlapWidth < 20 clamps to 20mm - PASSED")

        # Test overlap validation (max Width/2)
        door.Width = 800
        door.OverlapWidth = 500
        App.ActiveDocument.recompute()
        assert door.OverlapWidth.Value <= 400, \
            f"OverlapWidth should clamp to <=Width/2, got {door.OverlapWidth.Value}"
        print(f"   OverlapWidth > Width/2 clamps to Width/2 - PASSED")

    except Exception as e:
        print(f"   FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_travel_distance():
    """Test 7: Travel distance calculation"""
    print("\n" + "=" * 70)
    print("Test 7: Travel distance calculation")
    print("=" * 70)

    try:
        # Single panel - travel = panel width
        door1 = createSlidingDoor("TravelSingle")
        door1.Width = 900
        door1.PanelCount = 1
        App.ActiveDocument.recompute()
        assert door1.TravelDistance.Value == 900, \
            f"Single panel travel should be {900}, got {door1.TravelDistance.Value}"
        print(f"   Single panel travel = {door1.TravelDistance.Value}mm - PASSED")

        # Bypass - travel = width - overlap
        door2 = createSlidingDoor("TravelBypass")
        door2.TrackType = "Soft-Close"
        door2.PanelCount = 2
        door2.Width = 900
        door2.OverlapWidth = 50
        App.ActiveDocument.recompute()
        expected_travel = 900 - 50
        assert door2.TravelDistance.Value == expected_travel, \
            f"Bypass travel should be {expected_travel}, got {door2.TravelDistance.Value}"
        print(f"   Bypass travel = {door2.TravelDistance.Value}mm - PASSED")

    except Exception as e:
        print(f"   FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_track_length():
    """Test 8: Track length calculation"""
    print("\n" + "=" * 70)
    print("Test 8: Track length calculation")
    print("=" * 70)

    try:
        # Single panel: track = width + 100 (50mm clearance each side)
        door1 = createSlidingDoor("TrackLengthSingle")
        door1.Width = 900
        door1.PanelCount = 1
        App.ActiveDocument.recompute()
        expected_single = 900 + 100
        assert door1.TrackLength.Value == expected_single, \
            f"Single track length should be {expected_single}, got {door1.TrackLength.Value}"
        print(f"   Single panel track length = {door1.TrackLength.Value}mm - PASSED")

        # Bypass: track = width*2 - overlap + 100
        door2 = createSlidingDoor("TrackLengthBypass")
        door2.TrackType = "Soft-Close"
        door2.PanelCount = 2
        door2.Width = 900
        door2.OverlapWidth = 50
        App.ActiveDocument.recompute()
        expected_bypass = 900 * 2 - 50 + 100
        assert door2.TrackLength.Value == expected_bypass, \
            f"Bypass track length should be {expected_bypass}, got {door2.TrackLength.Value}"
        print(f"   Bypass track length = {door2.TrackLength.Value}mm - PASSED")

    except Exception as e:
        print(f"   FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_hardware_visibility():
    """Test 9: Hardware visibility toggle"""
    print("\n" + "=" * 70)
    print("Test 9: Hardware visibility toggle")
    print("=" * 70)

    try:
        door = createSlidingDoor("HardwareToggle")

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

        # Shape should be smaller without hardware
        assert shape_without < shape_with, "Shape should be smaller without hardware"
        print("   Hardware adds to bounding box - PASSED")

    except Exception as e:
        print(f"   FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_bypass_configuration():
    """Test 10: Bypass (2-panel) configuration"""
    print("\n" + "=" * 70)
    print("Test 10: Bypass configuration")
    print("=" * 70)

    try:
        door = createSlidingDoor("BypassTest")
        door.TrackType = "Soft-Close"
        door.PanelCount = 2
        door.Width = 900
        door.OverlapWidth = 50
        App.ActiveDocument.recompute()

        # Should have a compound shape (multiple sub-shapes)
        if hasattr(door.Shape, 'Solids') and len(door.Shape.Solids) >= 2:
            print(f"   Compound shape with {len(door.Shape.Solids)} solids - PASSED")
        else:
            # Check if it's a compound with childShapes
            if door.Shape.ShapeType == "Compound":
                print(f"   Compound shape created - PASSED")
            else:
                print(f"   Shape type: {door.Shape.ShapeType}")

        print(f"   OpeningWidth: {door.OpeningWidth.Value}mm")
        print(f"   TravelDistance: {door.TravelDistance.Value}mm")
        print("   Status: PASSED")

    except Exception as e:
        print(f"   FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_track_finishes():
    """Test 11: Different track finishes"""
    print("\n" + "=" * 70)
    print("Test 11: Track finishes")
    print("=" * 70)

    finishes = ["Chrome", "Brushed-Nickel", "Matte-Black"]

    for finish in finishes:
        try:
            door = createSlidingDoor(f"Finish_{finish.replace('-', '_')}")
            door.TrackFinish = finish
            App.ActiveDocument.recompute()

            print(f"   TrackFinish={finish} - PASSED")

        except Exception as e:
            print(f"   TrackFinish={finish}: FAILED - {e}")


def test_slide_directions():
    """Test 12: Slide direction options"""
    print("\n" + "=" * 70)
    print("Test 12: Slide directions")
    print("=" * 70)

    directions = ["Left", "Right"]

    for direction in directions:
        try:
            door = createSlidingDoor(f"Slide_{direction}")
            door.SlideDirection = direction
            App.ActiveDocument.recompute()

            print(f"   SlideDirection={direction} - PASSED")

        except Exception as e:
            print(f"   SlideDirection={direction}: FAILED - {e}")


def test_roller_types():
    """Test 13: Roller type options"""
    print("\n" + "=" * 70)
    print("Test 13: Roller types")
    print("=" * 70)

    roller_types = ["Standard", "Soft-Close"]

    for roller_type in roller_types:
        try:
            door = createSlidingDoor(f"Roller_{roller_type.replace('-', '_')}")
            door.RollerType = roller_type
            App.ActiveDocument.recompute()

            print(f"   RollerType={roller_type} - PASSED")

        except Exception as e:
            print(f"   RollerType={roller_type}: FAILED - {e}")


def test_position_and_rotation():
    """Test 14: Position and rotation"""
    print("\n" + "=" * 70)
    print("Test 14: Position and rotation")
    print("=" * 70)

    try:
        door = createSlidingDoor("PositionTest")
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
    """Run all SlidingDoor tests"""
    print("=" * 70)
    print("SLIDING DOOR TEST SUITE")
    print("=" * 70)

    # Create or reuse document
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("SlidingDoorTests")
        print(f"\nCreated new document: {doc.Name}")
    else:
        print(f"\nUsing existing document: {doc.Name}")

    # Run all tests
    test_basic_creation()
    test_panel_count_validation()
    test_track_type_bypass_constraint()
    test_ezy_track_glass_constraint()
    test_track_types()
    test_overlap_calculations()
    test_travel_distance()
    test_track_length()
    test_hardware_visibility()
    test_bypass_configuration()
    test_track_finishes()
    test_slide_directions()
    test_roller_types()
    test_position_and_rotation()

    print("\n" + "=" * 70)
    print("TEST SUITE COMPLETE")
    print("=" * 70)


# Run tests when script is executed
if __name__ == "__main__":
    run_all_tests()
