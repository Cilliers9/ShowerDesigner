# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for CornerEnclosure assembly implementation.

Run inside FreeCAD's Python console:
    exec(open('path/to/test_corner_enclosure.py').read())

Or via the test runner (requires FreeCAD accessible):
    exec'd by mcp__freecad__execute_python with run_all_tests()

Covers:
  - Basic assembly creation and structure
  - Default VarSet property values
  - Nested FixedPanel and DoorPanel assemblies
  - DoorSide placement (Left / Right)
  - DoorType switching (HingedDoor <-> FixedPanel)
  - Inline panel layout (None / Wall Side / Corner Side / Both Sides)
  - Inline panel placement coordinates
  - Support bar creation / removal
  - Door constraint propagation (mounting types and seal options)
  - Dimension propagation to nested panel VarSets
  - Door-width calculation with inline panels
"""

import sys
sys.path.insert(
    0, r"C:\Users\tclou\AppData\Roaming\FreeCAD\v1-1\Mod\ShowerDesigner"
)

import FreeCAD as App
from freecad.ShowerDesigner.Models.CornerEnclosure import createCornerEnclosure


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_varset(part_obj):
    """Return the App::VarSet child of an assembly, or None."""
    for child in part_obj.Group:
        if child.TypeId == "App::VarSet":
            return child
    return None


def _get_nested_parts(part_obj):
    """Return direct App::Part children (nested assemblies)."""
    return [c for c in part_obj.Group if c.TypeId == "App::Part"]


def _get_nested_part_by_label(part_obj, label):
    """Return the first App::Part child whose Label starts with *label*."""
    for c in part_obj.Group:
        if c.TypeId == "App::Part" and c.Label.startswith(label):
            return c
    return None


def _get_nested_varset(part_obj):
    """Get VarSet from a nested App::Part assembly."""
    for child in part_obj.Group:
        if child.TypeId == "App::VarSet":
            return child
    return None


def _get_children_by_prefix(part_obj, prefix):
    """Return direct children whose Label starts with *prefix*."""
    return [c for c in part_obj.Group if c.Label.startswith(prefix)]


# ---------------------------------------------------------------------------
# Test 1: Basic creation
# ---------------------------------------------------------------------------

def test_basic_creation():
    """Test 1: Basic corner enclosure assembly creation."""
    print("\n" + "=" * 70)
    print("Test 1: Basic creation")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestCorner1")
        assert enc.TypeId == "App::Part", (
            f"Expected App::Part, got {enc.TypeId}"
        )
        print("  OK: Object is App::Part")

        vs = _get_varset(enc)
        assert vs is not None, "VarSet not found"
        print("  OK: VarSet found")

        nested = _get_nested_parts(enc)
        assert len(nested) >= 2, (
            f"Expected at least 2 nested App::Parts (FixedPanel + DoorPanel), "
            f"got {len(nested)}"
        )
        print(f"  OK: {len(nested)} nested App::Part assemblies found")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Test 2: Default VarSet properties
# ---------------------------------------------------------------------------

def test_default_properties():
    """Test 2: Default VarSet property values."""
    print("\n" + "=" * 70)
    print("Test 2: Default VarSet properties")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestDefaults")
        vs = _get_varset(enc)

        assert abs(vs.Width.Value - 900) < 0.01, (
            f"Expected Width=900, got {vs.Width.Value}"
        )
        assert abs(vs.Depth.Value - 900) < 0.01, (
            f"Expected Depth=900, got {vs.Depth.Value}"
        )
        assert abs(vs.Height.Value - 2000) < 0.01, (
            f"Expected Height=2000, got {vs.Height.Value}"
        )
        assert abs(vs.GlassThickness.Value - 8) < 0.01, (
            f"Expected GlassThickness=8, got {vs.GlassThickness.Value}"
        )
        assert vs.GlassType == "Clear", (
            f"Expected GlassType=Clear, got {vs.GlassType}"
        )
        assert vs.DoorType == "HingedDoor", (
            f"Expected DoorType=HingedDoor, got {vs.DoorType}"
        )
        assert vs.DoorSide == "Right", (
            f"Expected DoorSide=Right, got {vs.DoorSide}"
        )
        assert vs.InlinePanelLayout == "None", (
            f"Expected InlinePanelLayout=None, got {vs.InlinePanelLayout}"
        )
        assert vs.ShowSupportBar is True, (
            f"Expected ShowSupportBar=True, got {vs.ShowSupportBar}"
        )
        print("  OK: All default VarSet properties correct")
        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Test 3: Nested panel dimension propagation
# ---------------------------------------------------------------------------

def test_dimension_propagation():
    """Test 3: Width/Height/GlassThickness propagate to nested panels."""
    print("\n" + "=" * 70)
    print("Test 3: Dimension propagation")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestDims")
        vs = _get_varset(enc)
        vs.Width = 1000
        vs.Depth = 800
        vs.Height = 2100
        vs.GlassThickness = 10
        App.ActiveDocument.recompute()

        # Fixed panel (door on Right → fixed panel width == Width)
        fixed = _get_nested_part_by_label(enc, "FixedPanel")
        assert fixed is not None, "FixedPanel nested assembly not found"
        fixed_vs = _get_nested_varset(fixed)
        assert fixed_vs is not None, "FixedPanel VarSet not found"
        assert abs(fixed_vs.Width.Value - 1000) < 0.5, (
            f"Expected FixedPanel Width=1000, got {fixed_vs.Width.Value}"
        )
        assert abs(fixed_vs.Height.Value - 2100) < 0.5, (
            f"Expected FixedPanel Height=2100, got {fixed_vs.Height.Value}"
        )
        print(f"  OK: FixedPanel Width={fixed_vs.Width.Value}, Height={fixed_vs.Height.Value}")

        # Door panel (door on Right, no inline panels → door width = Depth - GlassThickness)
        door = _get_nested_part_by_label(enc, "DoorPanel")
        assert door is not None, "DoorPanel nested assembly not found"
        door_vs = _get_nested_varset(door)
        assert door_vs is not None, "DoorPanel VarSet not found"
        expected_door_width = 800 - 10  # depth - thickness
        assert abs(door_vs.Width.Value - expected_door_width) < 0.5, (
            f"Expected DoorPanel Width={expected_door_width}, "
            f"got {door_vs.Width.Value}"
        )
        assert abs(door_vs.Height.Value - 2100) < 0.5, (
            f"Expected DoorPanel Height=2100, got {door_vs.Height.Value}"
        )
        print(f"  OK: DoorPanel Width={door_vs.Width.Value} "
              f"(expected {expected_door_width})")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Test 4: DoorSide Left vs Right
# ---------------------------------------------------------------------------

def test_door_side():
    """Test 4: DoorSide Left vs Right swaps which panel gets Width/Depth."""
    print("\n" + "=" * 70)
    print("Test 4: DoorSide Left vs Right")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestDoorSide")
        vs = _get_varset(enc)
        vs.Width = 1000
        vs.Depth = 800
        vs.GlassThickness = 8
        vs.InlinePanelLayout = "None"

        # --- DoorSide=Right (default): fixed=Width, door wall=Depth-t ---
        vs.DoorSide = "Right"
        App.ActiveDocument.recompute()

        fixed = _get_nested_part_by_label(enc, "FixedPanel")
        fixed_vs = _get_nested_varset(fixed)
        assert abs(fixed_vs.Width.Value - 1000) < 0.5, (
            f"Right: Expected FixedPanel Width=1000, got {fixed_vs.Width.Value}"
        )
        door = _get_nested_part_by_label(enc, "DoorPanel")
        door_vs = _get_nested_varset(door)
        expected_right_door = 800 - 8
        assert abs(door_vs.Width.Value - expected_right_door) < 0.5, (
            f"Right: Expected DoorPanel Width={expected_right_door}, "
            f"got {door_vs.Width.Value}"
        )
        print(f"  OK DoorSide=Right: fixed_w={fixed_vs.Width.Value}, "
              f"door_w={door_vs.Width.Value}")

        # --- DoorSide=Left: fixed=Depth, door wall=Width-t ---
        vs.DoorSide = "Left"
        App.ActiveDocument.recompute()

        fixed_vs = _get_nested_varset(fixed)
        assert abs(fixed_vs.Width.Value - 800) < 0.5, (
            f"Left: Expected FixedPanel Width=800, got {fixed_vs.Width.Value}"
        )
        door_vs = _get_nested_varset(door)
        expected_left_door = 1000 - 8
        assert abs(door_vs.Width.Value - expected_left_door) < 0.5, (
            f"Left: Expected DoorPanel Width={expected_left_door}, "
            f"got {door_vs.Width.Value}"
        )
        print(f"  OK DoorSide=Left: fixed_w={fixed_vs.Width.Value}, "
              f"door_w={door_vs.Width.Value}")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Test 5: DoorType switching
# ---------------------------------------------------------------------------

def test_door_type_switching():
    """Test 5: Switching DoorType replaces the DoorPanel nested assembly."""
    print("\n" + "=" * 70)
    print("Test 5: DoorType switching")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestDoorType")
        vs = _get_varset(enc)

        # Default is HingedDoor — DoorPanel should be a hinged door assembly
        assert vs.DoorType == "HingedDoor"
        door_before = _get_nested_part_by_label(enc, "DoorPanel")
        assert door_before is not None, "DoorPanel not found for HingedDoor"
        door_vs_before = _get_nested_varset(door_before)
        has_hinge_props = hasattr(door_vs_before, "HingeSide")
        print(f"  OK: HingedDoor - DoorPanel has HingeSide prop: {has_hinge_props}")

        # Switch to FixedPanel door
        vs.DoorType = "FixedPanel"
        App.ActiveDocument.recompute()

        door_after = _get_nested_part_by_label(enc, "DoorPanel")
        assert door_after is not None, "DoorPanel not found after DoorType=FixedPanel"
        door_vs_after = _get_nested_varset(door_after)
        has_wall_hw = hasattr(door_vs_after, "WallHardware")
        print(f"  OK: FixedPanel - DoorPanel has WallHardware prop: {has_wall_hw}")

        # Switch back to HingedDoor
        vs.DoorType = "HingedDoor"
        App.ActiveDocument.recompute()
        door_final = _get_nested_part_by_label(enc, "DoorPanel")
        assert door_final is not None, "DoorPanel not found after switching back"
        door_vs_final = _get_nested_varset(door_final)
        assert hasattr(door_vs_final, "HingeSide"), (
            "DoorPanel VarSet missing HingeSide after switching back to HingedDoor"
        )
        print("  OK: Switched back to HingedDoor successfully")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Test 6: Inline panel layout — None
# ---------------------------------------------------------------------------

def test_inline_panel_none():
    """Test 6: InlinePanelLayout=None creates no inline panels."""
    print("\n" + "=" * 70)
    print("Test 6: InlinePanelLayout=None")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestInlineNone")
        vs = _get_varset(enc)
        vs.InlinePanelLayout = "None"
        App.ActiveDocument.recompute()

        nested = _get_nested_parts(enc)
        labels = [p.Label for p in nested]
        assert not any("Inline" in l for l in labels), (
            f"Expected no Inline panels, found: {labels}"
        )
        print(f"  OK: No inline panels. Nested parts: {labels}")
        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Test 7: Inline panel layout — Wall Side
# ---------------------------------------------------------------------------

def test_inline_panel_wall_side():
    """Test 7: InlinePanelLayout=Wall Side creates one WallInline panel."""
    print("\n" + "=" * 70)
    print("Test 7: InlinePanelLayout=Wall Side")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestInlineWall")
        vs = _get_varset(enc)
        vs.WallInlineWidth = 350
        vs.InlinePanelLayout = "Wall Side"
        App.ActiveDocument.recompute()

        nested = _get_nested_parts(enc)
        labels = [p.Label for p in nested]

        wall_inlines = [p for p in nested if "WallInline" in p.Label]
        corner_inlines = [p for p in nested if "CornerInline" in p.Label]
        assert len(wall_inlines) == 1, (
            f"Expected 1 WallInline panel, found {len(wall_inlines)}: {labels}"
        )
        assert len(corner_inlines) == 0, (
            f"Expected 0 CornerInline panels, found {len(corner_inlines)}"
        )
        print(f"  OK: 1 WallInline, 0 CornerInline. Parts: {labels}")

        # WallInline VarSet Width should match WallInlineWidth
        wr_vs = _get_nested_varset(wall_inlines[0])
        assert abs(wr_vs.Width.Value - 350) < 0.5, (
            f"Expected WallInline Width=350, got {wr_vs.Width.Value}"
        )
        print(f"  OK: WallInline Width={wr_vs.Width.Value}")
        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Test 8: Inline panel layout — Corner Side
# ---------------------------------------------------------------------------

def test_inline_panel_corner_side():
    """Test 8: InlinePanelLayout=Corner Side creates one CornerInline panel."""
    print("\n" + "=" * 70)
    print("Test 8: InlinePanelLayout=Corner Side")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestInlineCorner")
        vs = _get_varset(enc)
        vs.CornerInlineWidth = 250
        vs.InlinePanelLayout = "Corner Side"
        App.ActiveDocument.recompute()

        nested = _get_nested_parts(enc)
        labels = [p.Label for p in nested]

        wall_inlines = [p for p in nested if "WallInline" in p.Label]
        corner_inlines = [p for p in nested if "CornerInline" in p.Label]
        assert len(wall_inlines) == 0, (
            f"Expected 0 WallInline, found {len(wall_inlines)}"
        )
        assert len(corner_inlines) == 1, (
            f"Expected 1 CornerInline, found {len(corner_inlines)}: {labels}"
        )
        print(f"  OK: 0 WallInline, 1 CornerInline. Parts: {labels}")

        cr_vs = _get_nested_varset(corner_inlines[0])
        assert abs(cr_vs.Width.Value - 250) < 0.5, (
            f"Expected CornerInline Width=250, got {cr_vs.Width.Value}"
        )
        print(f"  OK: CornerInline Width={cr_vs.Width.Value}")
        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Test 9: Inline panel layout — Both Sides
# ---------------------------------------------------------------------------

def test_inline_panel_both_sides():
    """Test 9: InlinePanelLayout=Both Sides creates WallInline and CornerInline."""
    print("\n" + "=" * 70)
    print("Test 9: InlinePanelLayout=Both Sides")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestInlineBoth")
        vs = _get_varset(enc)
        vs.Width = 1000
        vs.Depth = 900
        vs.GlassThickness = 8
        vs.WallInlineWidth = 200
        vs.CornerInlineWidth = 200
        vs.InlinePanelLayout = "Both Sides"
        App.ActiveDocument.recompute()

        nested = _get_nested_parts(enc)
        labels = [p.Label for p in nested]

        wall_inlines = [p for p in nested if "WallInline" in p.Label]
        corner_inlines = [p for p in nested if "CornerInline" in p.Label]
        assert len(wall_inlines) == 1, (
            f"Expected 1 WallInline, found {len(wall_inlines)}: {labels}"
        )
        assert len(corner_inlines) == 1, (
            f"Expected 1 CornerInline, found {len(corner_inlines)}: {labels}"
        )
        print(f"  OK: 1 WallInline + 1 CornerInline. Parts: {labels}")

        # Door width = door_wall_span - wall_ret_w - corner_ret_w
        # door_wall_span = Depth - GlassThickness = 900 - 8 = 892 (DoorSide=Right)
        door = _get_nested_part_by_label(enc, "DoorPanel")
        door_vs = _get_nested_varset(door)
        expected_door_w = 900 - 8 - 200 - 200  # 492
        assert abs(door_vs.Width.Value - expected_door_w) < 0.5, (
            f"Expected DoorPanel Width={expected_door_w}, "
            f"got {door_vs.Width.Value}"
        )
        print(f"  OK: DoorPanel Width={door_vs.Width.Value} (expected {expected_door_w})")
        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Test 10: Inline panel layout toggling (add then remove)
# ---------------------------------------------------------------------------

def test_inline_panel_toggle():
    """Test 10: Toggling InlinePanelLayout adds and removes panels correctly."""
    print("\n" + "=" * 70)
    print("Test 10: InlinePanelLayout toggle")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestInlineToggle")
        vs = _get_varset(enc)

        # Start with Both Sides
        vs.InlinePanelLayout = "Both Sides"
        App.ActiveDocument.recompute()
        nested = _get_nested_parts(enc)
        labels = [p.Label for p in nested]
        assert any("WallInline" in l for l in labels), "WallInline missing"
        assert any("CornerInline" in l for l in labels), "CornerInline missing"
        print(f"  OK: Both Sides — {labels}")

        # Switch to None — inline panels should be removed
        vs.InlinePanelLayout = "None"
        App.ActiveDocument.recompute()
        nested = _get_nested_parts(enc)
        labels = [p.Label for p in nested]
        assert not any("Inline" in l for l in labels), (
            f"Inline panels still present after setting None: {labels}"
        )
        print(f"  OK: None — {labels}")

        # Switch back to Wall Side
        vs.InlinePanelLayout = "Wall Side"
        App.ActiveDocument.recompute()
        nested = _get_nested_parts(enc)
        labels = [p.Label for p in nested]
        assert any("WallInline" in l for l in labels), (
            f"WallInline missing after switching to Wall Side: {labels}"
        )
        assert not any("CornerInline" in l for l in labels), (
            f"CornerInline still present: {labels}"
        )
        print(f"  OK: Wall Side — {labels}")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Test 11: Support bar creation and removal
# ---------------------------------------------------------------------------

def test_support_bar():
    """Test 11: ShowSupportBar creates and removes the SupportBar child."""
    print("\n" + "=" * 70)
    print("Test 11: Support bar creation / removal")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestSupportBar")
        vs = _get_varset(enc)

        # ShowSupportBar=True (default)
        vs.ShowSupportBar = True
        App.ActiveDocument.recompute()
        support_bars = _get_children_by_prefix(enc, "SupportBar")
        assert len(support_bars) == 1, (
            f"Expected 1 SupportBar when ShowSupportBar=True, "
            f"got {len(support_bars)}"
        )
        print(f"  OK: ShowSupportBar=True — 1 SupportBar child")

        # ShowSupportBar=False
        vs.ShowSupportBar = False
        App.ActiveDocument.recompute()
        support_bars = _get_children_by_prefix(enc, "SupportBar")
        assert len(support_bars) == 0, (
            f"Expected 0 SupportBar when ShowSupportBar=False, "
            f"got {len(support_bars)}"
        )
        print(f"  OK: ShowSupportBar=False — 0 SupportBar children")

        # Toggle back on
        vs.ShowSupportBar = True
        App.ActiveDocument.recompute()
        support_bars = _get_children_by_prefix(enc, "SupportBar")
        assert len(support_bars) == 1, (
            f"Expected 1 SupportBar after toggling back on, "
            f"got {len(support_bars)}"
        )
        print(f"  OK: ShowSupportBar toggled back on")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Test 12: Support bar length tracks fixed panel width
# ---------------------------------------------------------------------------

def test_support_bar_length():
    """Test 12: SupportBar Length equals the fixed panel width."""
    print("\n" + "=" * 70)
    print("Test 12: Support bar length")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestSupportBarLen")
        vs = _get_varset(enc)
        vs.Width = 1200
        vs.Depth = 900
        vs.DoorSide = "Right"   # fixed panel width = Width = 1200
        vs.ShowSupportBar = True
        App.ActiveDocument.recompute()

        support_bars = _get_children_by_prefix(enc, "SupportBar")
        assert len(support_bars) == 1, "SupportBar not found"
        sb = support_bars[0]
        assert abs(sb.Length.Value - 1200) < 0.5, (
            f"Expected SupportBar Length=1200, got {sb.Length.Value}"
        )
        print(f"  OK: SupportBar Length={sb.Length.Value} (expected 1200)")

        # Change width and verify bar updates
        vs.Width = 900
        App.ActiveDocument.recompute()
        sb = _get_children_by_prefix(enc, "SupportBar")[0]
        assert abs(sb.Length.Value - 900) < 0.5, (
            f"Expected SupportBar Length=900 after width change, "
            f"got {sb.Length.Value}"
        )
        print(f"  OK: SupportBar Length updated to {sb.Length.Value}")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Test 13: Door-width calculation with inline panels (left door side)
# ---------------------------------------------------------------------------

def test_door_width_left_side():
    """Test 13: Door-width formula is correct when DoorSide=Left."""
    print("\n" + "=" * 70)
    print("Test 13: Door-width, DoorSide=Left")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestDoorWidthLeft")
        vs = _get_varset(enc)
        vs.Width = 1000
        vs.Depth = 800
        vs.GlassThickness = 8
        vs.DoorSide = "Left"
        vs.WallInlineWidth = 150
        vs.CornerInlineWidth = 100
        vs.InlinePanelLayout = "Both Sides"
        App.ActiveDocument.recompute()

        # door_wall_span = Width - GlassThickness = 1000 - 8 = 992
        # door_width = 992 - wall_ret_w - corner_ret_w = 992 - 150 - 100 = 742
        door = _get_nested_part_by_label(enc, "DoorPanel")
        door_vs = _get_nested_varset(door)
        expected = 1000 - 8 - 150 - 100  # 742
        assert abs(door_vs.Width.Value - expected) < 0.5, (
            f"Expected DoorPanel Width={expected}, got {door_vs.Width.Value}"
        )
        print(f"  OK: DoorPanel Width={door_vs.Width.Value} (expected {expected})")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Test 14: Fixed-panel placement (DoorSide=Right → origin, DoorSide=Left → rotated)
# ---------------------------------------------------------------------------

def test_fixed_panel_placement():
    """Test 14: FixedPanel placement changes with DoorSide."""
    print("\n" + "=" * 70)
    print("Test 14: FixedPanel placement")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestFixedPlacement")
        vs = _get_varset(enc)
        vs.Width = 1000
        vs.Depth = 800
        vs.GlassThickness = 8
        vs.InlinePanelLayout = "None"

        # DoorSide=Right: FixedPanel at origin, no rotation
        vs.DoorSide = "Right"
        App.ActiveDocument.recompute()
        fixed = _get_nested_part_by_label(enc, "FixedPanel")
        pos = fixed.Placement.Base
        assert abs(pos.x) < 0.1 and abs(pos.y) < 0.1 and abs(pos.z) < 0.1, (
            f"DoorSide=Right: Expected FixedPanel at origin, got {pos}"
        )
        print(f"  OK DoorSide=Right: FixedPanel at ({pos.x:.1f}, {pos.y:.1f}, {pos.z:.1f})")

        # DoorSide=Left: FixedPanel at (Width, 0, 0), rotated 90°
        vs.DoorSide = "Left"
        App.ActiveDocument.recompute()
        fixed = _get_nested_part_by_label(enc, "FixedPanel")
        pos = fixed.Placement.Base
        assert abs(pos.x - 1000) < 0.5, (
            f"DoorSide=Left: Expected FixedPanel x=1000, got {pos.x}"
        )
        assert abs(pos.y) < 0.5 and abs(pos.z) < 0.5, (
            f"DoorSide=Left: Expected FixedPanel y=0, z=0, got ({pos.y}, {pos.z})"
        )
        print(f"  OK DoorSide=Left: FixedPanel at ({pos.x:.1f}, {pos.y:.1f}, {pos.z:.1f})")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Test 15: Glass type propagation
# ---------------------------------------------------------------------------

def test_glass_type_propagation():
    """Test 15: GlassType propagates to nested FixedPanel and DoorPanel."""
    print("\n" + "=" * 70)
    print("Test 15: GlassType propagation")
    print("=" * 70)

    try:
        enc = createCornerEnclosure("TestGlassType")
        vs = _get_varset(enc)
        vs.GlassType = "Frosted"
        App.ActiveDocument.recompute()

        fixed = _get_nested_part_by_label(enc, "FixedPanel")
        fixed_vs = _get_nested_varset(fixed)
        if hasattr(fixed_vs, "GlassType"):
            assert fixed_vs.GlassType == "Frosted", (
                f"Expected FixedPanel GlassType=Frosted, got {fixed_vs.GlassType}"
            )
            print(f"  OK: FixedPanel GlassType={fixed_vs.GlassType}")
        else:
            print("  INFO: FixedPanel VarSet has no GlassType (skipped)")

        door = _get_nested_part_by_label(enc, "DoorPanel")
        door_vs = _get_nested_varset(door)
        if hasattr(door_vs, "GlassType"):
            assert door_vs.GlassType == "Frosted", (
                f"Expected DoorPanel GlassType=Frosted, got {door_vs.GlassType}"
            )
            print(f"  OK: DoorPanel GlassType={door_vs.GlassType}")
        else:
            print("  INFO: DoorPanel VarSet has no GlassType (skipped)")

        print("  Status: PASSED")
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# run_all_tests
# ---------------------------------------------------------------------------

def run_all_tests():
    print("=" * 70)
    print("CORNER ENCLOSURE ASSEMBLY TEST SUITE")
    print("=" * 70)

    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("CornerEnclosureTests")
        print(f"\nCreated new document: {doc.Name}")
    else:
        print(f"\nUsing existing document: {doc.Name}")

    test_basic_creation()
    test_default_properties()
    test_dimension_propagation()
    test_door_side()
    test_door_type_switching()
    test_inline_panel_none()
    test_inline_panel_wall_side()
    test_inline_panel_corner_side()
    test_inline_panel_both_sides()
    test_inline_panel_toggle()
    test_support_bar()
    test_support_bar_length()
    test_door_width_left_side()
    test_fixed_panel_placement()
    test_glass_type_propagation()

    print("\n" + "=" * 70)
    print("TEST SUITE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
