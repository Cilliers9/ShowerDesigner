# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for HardwareSpecs data layer.

Pure Python tests — no FreeCAD required. Can run with plain pytest.

Run:
    pytest freecad/ShowerDesigner/Tests/test_hardware_specs.py
"""

import sys
sys.path.insert(
    0, r"C:\Users\tclou\AppData\Roaming\FreeCAD\v1-1\Mod\ShowerDesigner"
)

from freecad.ShowerDesigner.Data.HardwareSpecs import (
    HARDWARE_FINISHES,
    HINGE_SPECS,
    BIFOLD_HINGE_SPECS,
    HINGE_PLACEMENT_DEFAULTS,
    HANDLE_SPECS,
    HANDLE_PLACEMENT_DEFAULTS,
    SUPPORT_BAR_SPECS,
    SUPPORT_BAR_RULES,
    SEAL_SPECS,
    CLAMP_SPECS,
    CLAMP_PLACEMENT_DEFAULTS,
    CHANNEL_SPECS,
    TRACK_PROFILES,
    ROLLER_SPECS,
    BOTTOM_GUIDE_SPECS,
    selectHinge,
    calculateHingePlacement,
    validateHingeLoad,
    selectClamp,
    calculateClampPlacement,
    validateClampLoad,
    requiresSupportBar,
    validateHandlePlacement,
    selectSeal,
)


# -----------------------------------------------------------------------
# Data integrity tests
# -----------------------------------------------------------------------

def test_hardware_finishes_not_empty():
    assert len(HARDWARE_FINISHES) >= 4
    assert "Chrome" in HARDWARE_FINISHES
    assert "Matte-Black" in HARDWARE_FINISHES


def test_hinge_specs_have_required_keys():
    for key, spec in HINGE_SPECS.items():
        assert "load_capacity_kg" in spec, f"{key} missing load_capacity_kg"
        assert "dimensions" in spec, f"{key} missing dimensions"
        dims = spec["dimensions"]
        assert "width" in dims and "depth" in dims and "height" in dims
        assert "glass_thickness_range" in spec
        assert "mounting_type" in spec


def test_bifold_hinge_specs():
    assert "Left" in BIFOLD_HINGE_SPECS
    assert "Right" in BIFOLD_HINGE_SPECS
    for key, spec in BIFOLD_HINGE_SPECS.items():
        assert "primary_angle" in spec
        assert "secondary_angle" in spec
        assert "fold_direction" in spec


def test_handle_specs_have_required_keys():
    for key, spec in HANDLE_SPECS.items():
        assert "diameter" in spec or "lengths" in spec, f"{key} missing dimensions"
        assert "mounting_type" in spec
        assert "ada_compliant" in spec


def test_clamp_specs_have_required_keys():
    for key, spec in CLAMP_SPECS.items():
        assert "load_capacity_kg" in spec
        assert "dimensions" in spec
        assert "bounding_box" in spec, f"{key} missing bounding_box"
        bb = spec["bounding_box"]
        assert "width" in bb and "depth" in bb and "height" in bb
        assert "glass_thickness_range" in spec
        assert "default_mounting" in spec


def test_track_profiles_have_required_keys():
    for key, spec in TRACK_PROFILES.items():
        assert "width" in spec
        assert "height" in spec
        assert "max_panels" in spec


def test_support_bar_specs():
    for key, spec in SUPPORT_BAR_SPECS.items():
        assert "diameter_range" in spec
        assert len(spec["diameter_range"]) == 2
        assert spec["diameter_range"][0] <= spec["diameter_range"][1]


def test_seal_specs():
    for key, spec in SEAL_SPECS.items():
        assert "thickness" in spec
        assert "location" in spec


def test_channel_specs():
    assert "wall" in CHANNEL_SPECS
    assert "floor" in CHANNEL_SPECS
    for key, spec in CHANNEL_SPECS.items():
        assert "width" in spec
        assert "depth" in spec


def test_roller_specs():
    assert "Standard" in ROLLER_SPECS
    assert "Soft-Close" in ROLLER_SPECS
    for key, spec in ROLLER_SPECS.items():
        assert "radius" in spec
        assert "height" in spec


def test_bottom_guide_specs():
    assert "width" in BOTTOM_GUIDE_SPECS
    assert "height" in BOTTOM_GUIDE_SPECS


# -----------------------------------------------------------------------
# Validation function tests
# -----------------------------------------------------------------------

def test_selectHinge_light_door():
    result = selectHinge(30, 8)
    assert result == "standard_wall_mount"


def test_selectHinge_heavy_door():
    result = selectHinge(60, 10)
    assert result == "heavy_duty_wall_mount"


def test_selectHinge_thin_glass_heavy():
    # 6mm glass is not in heavy_duty range, should fall back
    result = selectHinge(60, 6)
    assert result == "standard_wall_mount"


def test_calculateHingePlacement_2_hinges():
    positions = calculateHingePlacement(2000, 2)
    assert len(positions) == 2
    assert positions[0] == 300  # offset_bottom
    assert positions[1] == 1700  # 2000 - 300


def test_calculateHingePlacement_3_hinges():
    positions = calculateHingePlacement(2000, 3)
    assert len(positions) == 3
    assert positions[0] == 300
    assert positions[1] == 1000  # midpoint
    assert positions[2] == 1700


def test_calculateHingePlacement_custom_offsets():
    positions = calculateHingePlacement(2000, 2, offset_top=200, offset_bottom=250)
    assert len(positions) == 2
    assert positions[0] == 250
    assert positions[1] == 1800


def test_validateHingeLoad_ok():
    valid, msg = validateHingeLoad("standard_wall_mount", 40, 2)
    assert valid is True


def test_validateHingeLoad_exceeded():
    valid, msg = validateHingeLoad("standard_wall_mount", 100, 2)
    assert valid is False
    assert "exceeds" in msg


def test_validateHingeLoad_unknown_type():
    valid, msg = validateHingeLoad("nonexistent_type", 10, 2)
    assert valid is False


def test_selectClamp_wall():
    result = selectClamp(20, 8, "Wall")
    assert result == "L_Clamp"


def test_selectClamp_wall_heavy():
    result = selectClamp(40, 10, "Wall")
    assert result == "L_Clamp"


def test_selectClamp_floor():
    result = selectClamp(30, 8, "Floor")
    assert result == "U_Clamp"


def test_selectClamp_floor_heavy():
    result = selectClamp(45, 10, "Floor")
    assert result == "U_Clamp"


def test_calculateClampPlacement_1():
    positions = calculateClampPlacement(1000, 1)
    assert len(positions) == 1
    assert positions[0] == 500  # center


def test_calculateClampPlacement_2():
    positions = calculateClampPlacement(2000, 2, 300, 300)
    assert len(positions) == 2
    assert positions[0] == 300
    assert positions[1] == 1700


def test_calculateClampPlacement_3():
    positions = calculateClampPlacement(2000, 3, 300, 300)
    assert len(positions) == 3
    assert positions[0] == 300
    assert positions[1] == 1000
    assert positions[2] == 1700


def test_validateClampLoad_ok():
    valid, msg = validateClampLoad("L_Clamp", 25, 2)
    assert valid is True


def test_validateClampLoad_exceeded():
    valid, msg = validateClampLoad("L_Clamp", 70, 2)
    assert valid is False


def test_requiresSupportBar_walkin_wide():
    required, reason = requiresSupportBar(1200, 2000, "walkin")
    assert required is True


def test_requiresSupportBar_walkin_narrow():
    required, reason = requiresSupportBar(800, 2000, "walkin")
    assert required is False


def test_requiresSupportBar_fixed_tall():
    required, reason = requiresSupportBar(900, 2500, "fixed")
    assert required is True


def test_requiresSupportBar_fixed_short():
    required, reason = requiresSupportBar(900, 2000, "fixed")
    assert required is False


def test_validateHandlePlacement_ok():
    valid, msg = validateHandlePlacement(1050)
    assert valid is True


def test_validateHandlePlacement_too_low():
    valid, msg = validateHandlePlacement(200)
    assert valid is False


def test_validateHandlePlacement_too_high():
    valid, msg = validateHandlePlacement(2000)
    assert valid is False


def test_validateHandlePlacement_ada_ok():
    valid, msg = validateHandlePlacement(1000, ada_required=True)
    assert valid is True


def test_validateHandlePlacement_ada_too_low():
    valid, msg = validateHandlePlacement(800, ada_required=True)
    assert valid is False


def test_validateHandlePlacement_ada_too_high():
    valid, msg = validateHandlePlacement(1300, ada_required=True)
    assert valid is False


def test_selectSeal_bottom():
    result = selectSeal("bottom", 8, 5)
    assert result == "door_sweep"


def test_selectSeal_side():
    result = selectSeal("side", 8, 5)
    assert result == "vertical_seal"


def test_selectSeal_magnetic():
    result = selectSeal("magnetic", 8, 5)
    assert result == "magnetic_seal"


# -----------------------------------------------------------------------
# Cross-reference tests (data consistency)
# -----------------------------------------------------------------------

def test_hinge_placement_defaults_consistent():
    assert HINGE_PLACEMENT_DEFAULTS["offset_top"] > 0
    assert HINGE_PLACEMENT_DEFAULTS["offset_bottom"] > 0
    assert HINGE_PLACEMENT_DEFAULTS["weight_threshold_3_hinges"] > 0


def test_handle_placement_defaults_consistent():
    d = HANDLE_PLACEMENT_DEFAULTS
    assert d["min_height"] < d["height"] < d["max_height"]
    assert d["ada_min_height"] < d["ada_max_height"]


def test_clamp_placement_defaults_consistent():
    d = CLAMP_PLACEMENT_DEFAULTS
    assert d["wall_offset_top"] > 0
    assert d["wall_offset_bottom"] > 0
    assert d["floor_offset_start"] > 0
    assert d["floor_offset_end"] > 0


# -----------------------------------------------------------------------
# Runner for FreeCAD console usage
# -----------------------------------------------------------------------

def run_all_tests():
    """Run all tests and print results (for FreeCAD console)."""
    import inspect
    test_funcs = [
        (name, func)
        for name, func in sorted(globals().items())
        if name.startswith("test_") and callable(func)
    ]

    passed = 0
    failed = 0

    print("=" * 70)
    print("HARDWARE SPECS TEST SUITE")
    print("=" * 70)

    for name, func in test_funcs:
        try:
            func()
            print(f"  PASSED: {name}")
            passed += 1
        except AssertionError as e:
            print(f"  FAILED: {name} - {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR:  {name} - {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed out of {len(test_funcs)} tests")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
