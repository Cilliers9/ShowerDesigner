# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for SlidingDoor assembly implementation.

Run this in FreeCAD's Python console:
    exec(open('path/to/test_sliding_door.py').read())
"""

import sys
sys.path.insert(
    0, r"C:\Users\tclou\AppData\Roaming\FreeCAD\v1-1\Mod\ShowerDesigner"
)

import FreeCAD as App
from freecad.ShowerDesigner.Models.SlidingDoor import createSlidingDoor


def _get_varset(part_obj):
    for child in part_obj.Group:
        if child.TypeId == "App::VarSet":
            return child
    return None


def _get_children_by_prefix(part_obj, prefix):
    return [c for c in part_obj.Group if c.Label.startswith(prefix)]


def test_basic_creation():
    """Test 1: Basic sliding door assembly creation."""
    print("\n" + "=" * 70)
    print("Test 1: Basic sliding door creation")
    print("=" * 70)

    try:
        door = createSlidingDoor("TestSliding1")
        assert door.TypeId == "App::Part", f"Expected App::Part, got {door.TypeId}"
        print("  OK: Object is App::Part")

        vs = _get_varset(door)
        assert vs is not None, "VarSet not found"
        print("  OK: VarSet found")

        panels = _get_children_by_prefix(door, "Panel")
        assert len(panels) == 1, f"Expected 1 Panel, got {len(panels)}"
        print("  OK: Panel1 child found")

        assert vs.Width.Value == 900
        assert vs.Height.Value == 2000
        assert vs.Thickness.Value == 8
        assert vs.PanelCount == 1
        assert vs.TrackType == "Edge"
        assert vs.SlideDirection == "Right"
        assert vs.OverlapWidth.Value == 50
        assert vs.RollerType == "Standard"
        assert vs.HandleType == "flush_handle_with_plate"
        assert vs.HardwareFinish == "Chrome"
        assert vs.ShowHardware is True
        print("  OK: VarSet default properties correct")

        tracks = _get_children_by_prefix(door, "TopTrack")
        assert len(tracks) == 1, f"Expected 1 TopTrack, got {len(tracks)}"
        print("  OK: TopTrack child created")

        guides = _get_children_by_prefix(door, "BottomGuide")
        assert len(guides) == 1, f"Expected 1 BottomGuide, got {len(guides)}"
        print("  OK: BottomGuide child created")

        rollers = _get_children_by_prefix(door, "Roller")
        assert len(rollers) == 2, f"Expected 2 Rollers, got {len(rollers)}"
        print("  OK: 2 roller children created")

        handles = _get_children_by_prefix(door, "Handle")
        assert len(handles) == 1, f"Expected 1 Handle, got {len(handles)}"
        print("  OK: Handle child created")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_bypass_configuration():
    """Test 2: Bypass (2-panel) configuration."""
    print("\n" + "=" * 70)
    print("Test 2: Bypass configuration")
    print("=" * 70)

    try:
        door = createSlidingDoor("BypassTest")
        vs = _get_varset(door)
        vs.PanelCount = 2
        vs.Width = 900
        vs.OverlapWidth = 50
        App.ActiveDocument.recompute()

        panels = _get_children_by_prefix(door, "Panel")
        assert len(panels) == 2, f"Expected 2 Panels for bypass, got {len(panels)}"
        print("  OK: 2 panel children for bypass")

        rollers = _get_children_by_prefix(door, "Roller")
        assert len(rollers) == 4, f"Expected 4 Rollers for bypass, got {len(rollers)}"
        print("  OK: 4 roller children for bypass")

        # Switch back to single
        vs.PanelCount = 1
        App.ActiveDocument.recompute()
        panels = _get_children_by_prefix(door, "Panel")
        assert len(panels) == 1, f"Expected 1 Panel after switch, got {len(panels)}"
        print("  OK: Panel2 removed when switching back to single")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_track_types():
    """Test 3: Different track types."""
    print("\n" + "=" * 70)
    print("Test 3: Track types")
    print("=" * 70)

    from freecad.ShowerDesigner.Data.HardwareSpecs import TRACK_PROFILES

    for track_type in ["Edge", "City", "Ezy", "Soft-Close"]:
        try:
            door = createSlidingDoor(f"Track_{track_type.replace('-', '_')}")
            vs = _get_varset(door)
            vs.TrackType = track_type
            App.ActiveDocument.recompute()

            expected_height = TRACK_PROFILES[track_type]["height"]
            assert vs.TrackHeight.Value == expected_height, (
                f"Expected TrackHeight={expected_height}, got {vs.TrackHeight.Value}"
            )
            print(f"  TrackType={track_type}, TrackHeight={vs.TrackHeight.Value}mm - PASSED")

        except Exception as e:
            print(f"  TrackType={track_type}: FAILED - {e}")


def test_handle_types():
    """Test 4: Different handle types."""
    print("\n" + "=" * 70)
    print("Test 4: Handle types")
    print("=" * 70)

    for handle_type in ["None", "mushroom_knob_b2b", "pull_handle_round", "flush_handle_with_plate"]:
        try:
            safe_name = handle_type.replace("_", "")
            door = createSlidingDoor(f"Handle_{safe_name}")
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


def test_slide_directions():
    """Test 5: Slide direction options."""
    print("\n" + "=" * 70)
    print("Test 5: Slide directions")
    print("=" * 70)

    for direction in ["Left", "Right"]:
        try:
            door = createSlidingDoor(f"Slide_{direction}")
            vs = _get_varset(door)
            vs.SlideDirection = direction
            App.ActiveDocument.recompute()

            assert vs.SlideDirection == direction
            print(f"  SlideDirection={direction} - PASSED")

        except Exception as e:
            print(f"  SlideDirection={direction}: FAILED - {e}")


def test_show_hardware_toggle():
    """Test 6: Hardware visibility toggle."""
    print("\n" + "=" * 70)
    print("Test 6: Hardware visibility toggle")
    print("=" * 70)

    try:
        door = createSlidingDoor("HardwareToggle")
        vs = _get_varset(door)
        vs.ShowHardware = True
        App.ActiveDocument.recompute()

        hw = [c for c in door.Group
              if c.TypeId != "App::VarSet"
              and not c.Label.startswith("Panel")]
        assert len(hw) > 0, "Expected hardware children when ShowHardware=True"
        print(f"  ShowHardware=True: {len(hw)} hardware children - OK")

        vs.ShowHardware = False
        App.ActiveDocument.recompute()
        hw = [c for c in door.Group
              if c.TypeId != "App::VarSet"
              and not c.Label.startswith("Panel")]
        assert len(hw) == 0, f"Expected 0 hardware children, got {len(hw)}"
        print("  ShowHardware=False: 0 hardware children - OK")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_calculated_properties():
    """Test 7: Calculated properties."""
    print("\n" + "=" * 70)
    print("Test 7: Calculated properties")
    print("=" * 70)

    try:
        door = createSlidingDoor("CalcTest")
        vs = _get_varset(door)
        vs.Width = 1200
        vs.Height = 2200
        vs.Thickness = 12
        App.ActiveDocument.recompute()

        assert vs.Weight > 0, f"Expected positive weight, got {vs.Weight}"
        assert vs.Area > 0, f"Expected positive area, got {vs.Area}"
        assert vs.TrackLength.Value > 0, f"Expected positive track length"
        assert vs.TravelDistance.Value > 0, f"Expected positive travel distance"
        print(f"  Weight: {vs.Weight:.2f} kg, Area: {vs.Area:.3f} m2")
        print(f"  TrackLength: {vs.TrackLength.Value}mm")
        print(f"  TravelDistance: {vs.TravelDistance.Value}mm")
        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


def test_track_length_calculation():
    """Test 8: Track length calculation."""
    print("\n" + "=" * 70)
    print("Test 8: Track length calculation")
    print("=" * 70)

    try:
        # Single panel: track = width*2 + clearance*2
        door1 = createSlidingDoor("TrackLenSingle")
        vs1 = _get_varset(door1)
        vs1.Width = 900
        vs1.PanelCount = 1
        App.ActiveDocument.recompute()
        expected_single = 900 * 2 + 50 * 2  # 1900
        assert vs1.TrackLength.Value == expected_single, (
            f"Expected {expected_single}, got {vs1.TrackLength.Value}"
        )
        print(f"  Single panel track length = {vs1.TrackLength.Value}mm - PASSED")

        # Bypass: track = width*3 - overlap + clearance*2
        door2 = createSlidingDoor("TrackLenBypass")
        vs2 = _get_varset(door2)
        vs2.PanelCount = 2
        vs2.Width = 900
        vs2.OverlapWidth = 50
        App.ActiveDocument.recompute()
        expected_bypass = 900 * 3 - 50 + 50 * 2  # 2750
        assert vs2.TrackLength.Value == expected_bypass, (
            f"Expected {expected_bypass}, got {vs2.TrackLength.Value}"
        )
        print(f"  Bypass track length = {vs2.TrackLength.Value}mm - PASSED")

    except Exception as e:
        print(f"  FAILED - {e}")
        import traceback
        traceback.print_exc()


def run_all_tests():
    print("=" * 70)
    print("SLIDING DOOR ASSEMBLY TEST SUITE")
    print("=" * 70)

    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("SlidingDoorTests")
        print(f"\nCreated new document: {doc.Name}")
    else:
        print(f"\nUsing existing document: {doc.Name}")

    test_basic_creation()
    test_bypass_configuration()
    test_track_types()
    test_handle_types()
    test_slide_directions()
    test_show_hardware_toggle()
    test_calculated_properties()
    test_track_length_calculation()

    print("\n" + "=" * 70)
    print("TEST SUITE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
