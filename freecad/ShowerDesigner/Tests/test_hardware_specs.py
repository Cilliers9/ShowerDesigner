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
    CATALOGUE_HANDLE_FINISHES,
    CATALOGUE_HANDLE_SPECS,
    getHandleModelsForCategory,
    lookupHandleProductCode,
    SLIDER_SYSTEM_SPECS,
    SLIDER_FINISHES,
    FLOOR_GUIDE_SPECS,
    validateSliderSystem,
    lookupSliderProductCode,
    BEVEL_CLAMP_SPECS,
    CATALOGUE_STABILISER_FINISHES,
    CATALOGUE_STABILISER_SPECS,
    getStabilisersByProfile,
    getStabilisersByRole,
    lookupStabiliserProductCode,
)

from freecad.ShowerDesigner.Data.SealSpecs import (
    SEAL_SPECS,
    SEAL_COLOURS,
    SEAL_MATERIALS,
    CATALOGUE_SEAL_SPECS,
    selectSeal,
    getSealsByCategory,
    getSealsByAngle,
    getSealsByLocation,
    lookupSealProductCode,
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
    """HANDLE_SPECS now stores minimal catalogue references (model_file + catalogue_key)."""
    for key, spec in HANDLE_SPECS.items():
        assert "model_file" in spec, f"{key} missing model_file"
        assert "catalogue_key" in spec, f"{key} missing catalogue_key"
        assert spec["catalogue_key"] == key, (
            f"{key} catalogue_key mismatch: {spec['catalogue_key']}"
        )


def test_clamp_specs_have_required_keys():
    for key, spec in CLAMP_SPECS.items():
        assert "load_capacity_kg" in spec
        assert "dimensions" in spec
        assert "bounding_box" in spec, f"{key} missing bounding_box"
        bb = spec["bounding_box"]
        assert "width" in bb and "depth" in bb and "height" in bb
        assert "glass_thickness_range" in spec
        assert "default_mounting" in spec
        assert "product_codes" in spec, f"{key} missing product_codes"
        for pc in spec["product_codes"]:
            assert "code" in pc and "material" in pc and "finish" in pc


def test_bevel_clamp_specs_have_required_keys():
    assert len(BEVEL_CLAMP_SPECS) == 13  # 7 S/S 304 + 6 Brass
    for key, spec in BEVEL_CLAMP_SPECS.items():
        assert "name" in spec, f"{key} missing name"
        assert "mounting_type" in spec, f"{key} missing mounting_type"
        assert spec["mounting_type"] in ("Wall-to-Glass", "Glass-to-Glass"), (
            f"{key} invalid mounting_type: {spec['mounting_type']}"
        )
        assert "angle" in spec, f"{key} missing angle"
        assert spec["angle"] in (90, 135, 180), f"{key} invalid angle: {spec['angle']}"
        assert "clamp_shape" in spec, f"{key} missing clamp_shape"
        assert spec["clamp_shape"] in CLAMP_SPECS, (
            f"{key} clamp_shape '{spec['clamp_shape']}' not in CLAMP_SPECS"
        )
        assert "dimensions" in spec, f"{key} missing dimensions"
        dims = spec["dimensions"]
        for dim_key in ("base_size", "base_thickness", "glass_gap",
                        "cutout_depth", "cutout_radius", "chamfer_size"):
            assert dim_key in dims, f"{key} dimensions missing {dim_key}"
        assert "bounding_box" in spec, f"{key} missing bounding_box"
        assert "product_codes" in spec, f"{key} missing product_codes"
        assert len(spec["product_codes"]) > 0, f"{key} has empty product_codes"
        for pc in spec["product_codes"]:
            assert "code" in pc and "material" in pc and "finish" in pc
            assert "glass_thickness_range" in pc, (
                f"{key}/{pc['code']} missing glass_thickness_range"
            )


def test_bevel_clamp_product_codes_unique():
    all_codes = []
    for spec in BEVEL_CLAMP_SPECS.values():
        for pc in spec["product_codes"]:
            all_codes.append(pc["code"])
    assert len(all_codes) == len(set(all_codes)), "Duplicate product codes in BEVEL_CLAMP_SPECS"


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


def test_seal_colours_and_materials():
    assert len(SEAL_COLOURS) >= 4
    assert "Clear" in SEAL_COLOURS
    assert "Black" in SEAL_COLOURS
    assert len(SEAL_MATERIALS) == 2
    assert "PVC" in SEAL_MATERIALS
    assert "PC" in SEAL_MATERIALS


def test_catalogue_seal_specs_structure():
    required_keys = {"name", "category", "angle", "location", "dimensions",
                     "material", "product_codes"}
    valid_categories = {"soft_lip", "bubble", "bottom", "hard_lip", "magnetic",
                        "infill"}
    valid_locations = {"side", "bottom", "door"}
    valid_angles = {0, 90, 135, 180}
    for key, spec in CATALOGUE_SEAL_SPECS.items():
        for rk in required_keys:
            assert rk in spec, f"{key} missing '{rk}'"
        assert spec["category"] in valid_categories, (
            f"{key} has invalid category '{spec['category']}'"
        )
        assert spec["location"] in valid_locations, (
            f"{key} has invalid location '{spec['location']}'"
        )
        assert spec["angle"] in valid_angles, (
            f"{key} has invalid angle {spec['angle']}"
        )
        assert spec["material"] in SEAL_MATERIALS, (
            f"{key} has invalid material '{spec['material']}'"
        )
        assert len(spec["product_codes"]) > 0, f"{key} has no product codes"
        for pc in spec["product_codes"]:
            assert "code" in pc, f"{key} product_code missing 'code'"
            assert "glass_thickness" in pc, f"{key}/{pc['code']} missing 'glass_thickness'"
            assert "colour" in pc, f"{key}/{pc['code']} missing 'colour'"
            assert "length" in pc, f"{key}/{pc['code']} missing 'length'"
            assert pc["length"] in (2500, 3000), (
                f"{key}/{pc['code']} invalid length {pc['length']}"
            )


def test_catalogue_seal_specs_count():
    assert len(CATALOGUE_SEAL_SPECS) == 18


def test_catalogue_seal_product_codes_unique():
    seen = {}
    for key, spec in CATALOGUE_SEAL_SPECS.items():
        for pc in spec["product_codes"]:
            code = pc["code"]
            assert code not in seen, (
                f"Duplicate product code '{code}' in '{key}' and '{seen[code]}'"
            )
            seen[code] = key


def test_catalogue_seal_categories_populated():
    for cat in ("soft_lip", "bubble", "bottom", "hard_lip", "magnetic", "infill"):
        result = getSealsByCategory(cat)
        assert len(result) >= 1, f"No seals in category '{cat}'"


def test_getSealsByCategory_soft_lip():
    result = getSealsByCategory("soft_lip")
    assert len(result) == 5
    assert "centre_lip" in result
    assert "180_soft_lip" in result
    assert "135_soft_lip" in result


def test_getSealsByCategory_magnetic():
    result = getSealsByCategory("magnetic")
    assert len(result) == 3
    assert "90_180_magnetic" in result
    assert "180_flat_magnetic" in result
    assert "135_magnetic" in result


def test_getSealsByCategory_empty():
    result = getSealsByCategory("nonexistent")
    assert result == []


def test_getSealsByAngle_90():
    result = getSealsByAngle(90)
    assert "90_soft_lip" in result
    assert "90_hard_lip" in result
    assert "90_180_magnetic" in result


def test_getSealsByAngle_180():
    result = getSealsByAngle(180)
    assert "180_soft_lip" in result
    assert "180_hard_lip" in result
    assert "double_hard_lip_h" in result
    assert "180_g2g_infill" in result


def test_getSealsByLocation_bottom():
    result = getSealsByLocation("bottom")
    assert len(result) == 2
    assert "wipe_seal_bubble" in result
    assert "drip_wipe_seal" in result


def test_getSealsByLocation_door():
    result = getSealsByLocation("door")
    assert len(result) == 3
    assert "90_180_magnetic" in result


def test_lookupSealProductCode_known():
    key, pc = lookupSealProductCode("TSS-003-8")
    assert key == "180_soft_lip"
    assert pc["glass_thickness"] == "6-8"
    assert pc["colour"] == "Clear"


def test_lookupSealProductCode_magnetic():
    key, pc = lookupSealProductCode("PSS-008A-8")
    assert key == "90_180_magnetic"
    assert pc["material"] == "PC"


def test_lookupSealProductCode_infill():
    key, pc = lookupSealProductCode("IS-180-10")
    assert key == "180_g2g_infill"
    assert pc["glass_thickness"] == "10"


def test_lookupSealProductCode_unknown():
    key, pc = lookupSealProductCode("NONEXISTENT-999")
    assert key is None
    assert pc is None


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
    assert positions[0] == 700  # 1000 - wall_offset_top (300)


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
    valid, msg = validateClampLoad("L_Clamp", 100, 2)
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
    # Now returns catalogue key when a catalogue seal spans the gap
    assert result == "wipe_seal_bubble"


def test_selectSeal_side():
    result = selectSeal("side", 8, 5)
    # Now returns catalogue key when a catalogue seal spans the gap
    assert result == "centre_lip"


def test_selectSeal_magnetic():
    result = selectSeal("magnetic", 8, 5)
    # Now returns catalogue key when a catalogue seal spans the gap
    assert result == "90_180_magnetic"


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
# Catalogue handle specs tests
# -----------------------------------------------------------------------

def test_catalogue_handle_finishes_not_empty():
    assert len(CATALOGUE_HANDLE_FINISHES) >= 4
    assert "Bright Polished" in CATALOGUE_HANDLE_FINISHES
    assert "Matte Black" in CATALOGUE_HANDLE_FINISHES


def test_catalogue_handle_specs_structure():
    required_keys = {"name", "category", "mounting_type", "dimensions", "product_codes"}
    valid_categories = {"Knob", "Pull", "Towel_Bar", "Flush", "Custom_Kit"}
    for key, spec in CATALOGUE_HANDLE_SPECS.items():
        for rk in required_keys:
            assert rk in spec, f"{key} missing '{rk}'"
        assert spec["category"] in valid_categories, (
            f"{key} has invalid category '{spec['category']}'"
        )
        assert len(spec["product_codes"]) > 0, f"{key} has no product codes"


def test_catalogue_handle_product_codes_unique():
    seen = {}
    for key, spec in CATALOGUE_HANDLE_SPECS.items():
        for pc in spec["product_codes"]:
            code = pc["code"]
            assert code not in seen, (
                f"Duplicate product code '{code}' in '{key}' and '{seen[code]}'"
            )
            seen[code] = key


def test_catalogue_handle_product_codes_have_material_finish():
    for key, spec in CATALOGUE_HANDLE_SPECS.items():
        for pc in spec["product_codes"]:
            assert "material" in pc, f"{key}/{pc['code']} missing 'material'"
            assert "finish" in pc, f"{key}/{pc['code']} missing 'finish'"


def test_catalogue_handle_towel_rail_lengths():
    towel_keys = [
        k for k, s in CATALOGUE_HANDLE_SPECS.items()
        if s["category"] == "Towel_Bar" and "rail_lengths" in s
    ]
    assert len(towel_keys) >= 4, "Expected at least 4 towel rail entries with rail_lengths"
    for key in towel_keys:
        lengths = CATALOGUE_HANDLE_SPECS[key]["rail_lengths"]
        assert len(lengths) >= 2, f"{key} should have multiple rail lengths"
        for pc in CATALOGUE_HANDLE_SPECS[key]["product_codes"]:
            assert "rail_length" in pc, f"{key}/{pc['code']} missing 'rail_length'"
            assert pc["rail_length"] in lengths, (
                f"{key}/{pc['code']} rail_length {pc['rail_length']} not in {lengths}"
            )


def test_getHandleModelsForCategory_knob():
    knobs = getHandleModelsForCategory("Knob")
    assert len(knobs) == 3
    assert "mushroom_knob_b2b" in knobs
    assert "groove_knob_b2b" in knobs
    assert "square_knob_b2b" in knobs


def test_getHandleModelsForCategory_towel_bar():
    towels = getHandleModelsForCategory("Towel_Bar")
    assert len(towels) == 5
    assert "towel_rail_round_finnial" in towels


def test_getHandleModelsForCategory_empty():
    result = getHandleModelsForCategory("NonexistentCategory")
    assert result == []


def test_lookupHandleProductCode_known():
    key, pc = lookupHandleProductCode("DK-201")
    assert key == "mushroom_knob_b2b"
    assert pc["material"] == "Brass"
    assert pc["finish"] == "Bright Chrome"


def test_lookupHandleProductCode_towel_rail():
    key, pc = lookupHandleProductCode("BH-040")
    assert key == "towel_rail_round_finnial"
    assert pc["rail_length"] == 400


def test_lookupHandleProductCode_unknown():
    key, pc = lookupHandleProductCode("NONEXISTENT-999")
    assert key is None
    assert pc is None


# -----------------------------------------------------------------------
# Slider system specs tests
# -----------------------------------------------------------------------

def test_slider_system_specs_structure():
    required_keys = {
        "name", "max_door_width", "max_weight_kg",
        "door_glass_thickness", "fixed_glass_thickness",
        "dimensions", "components", "product_codes",
    }
    for key, spec in SLIDER_SYSTEM_SPECS.items():
        for rk in required_keys:
            assert rk in spec, f"{key} missing '{rk}'"
        assert len(spec["product_codes"]) > 0, f"{key} has no product codes"
        assert len(spec["components"]) > 0, f"{key} has no components"


def test_slider_system_specs_three_systems():
    assert "duplo" in SLIDER_SYSTEM_SPECS
    assert "edge_slider" in SLIDER_SYSTEM_SPECS
    assert "city_slider" in SLIDER_SYSTEM_SPECS
    assert len(SLIDER_SYSTEM_SPECS) == 3


def test_slider_system_duplo_has_tube_dims():
    dims = SLIDER_SYSTEM_SPECS["duplo"]["dimensions"]
    assert "tube_diameter" in dims
    assert "tube_spacing_ctc" in dims


def test_slider_system_edge_city_have_track_dims():
    for key in ("edge_slider", "city_slider"):
        dims = SLIDER_SYSTEM_SPECS[key]["dimensions"]
        assert "track_width" in dims, f"{key} missing track_width"
        assert "track_height" in dims, f"{key} missing track_height"


def test_slider_system_product_codes_unique():
    seen = {}
    for key, spec in SLIDER_SYSTEM_SPECS.items():
        for pc in spec["product_codes"]:
            code = pc["code"]
            assert code not in seen, (
                f"Duplicate product code '{code}' in '{key}' and '{seen[code]}'"
            )
            seen[code] = key


def test_slider_system_product_codes_have_material_finish():
    for key, spec in SLIDER_SYSTEM_SPECS.items():
        for pc in spec["product_codes"]:
            assert "material" in pc, f"{key}/{pc['code']} missing 'material'"
            assert "finish" in pc, f"{key}/{pc['code']} missing 'finish'"


def test_slider_system_components_have_code():
    for key, spec in SLIDER_SYSTEM_SPECS.items():
        for role, comp in spec["components"].items():
            assert "code" in comp, f"{key}/{role} missing 'code'"
            assert "qty_per_system" in comp, f"{key}/{role} missing 'qty_per_system'"


def test_slider_system_all_have_floor_guide():
    for key, spec in SLIDER_SYSTEM_SPECS.items():
        assert "floor_guide" in spec["components"], (
            f"{key} missing floor_guide component"
        )
        assert spec["components"]["floor_guide"]["code"] == "SL-0099P"


def test_slider_system_city_has_roller_variants():
    city = SLIDER_SYSTEM_SPECS["city_slider"]
    assert "roller_variants" in city
    assert "clip_in" in city["roller_variants"]
    assert "heavy_duty" in city["roller_variants"]


def test_slider_system_city_roller_variants_required_keys():
    city = SLIDER_SYSTEM_SPECS["city_slider"]
    required_keys = {
        "code", "glass_cutout_depth", "door_top_deduction",
        "fixed_door_clearance", "max_weight_kg", "door_glass_thickness",
    }
    for variant_key, variant in city["roller_variants"].items():
        for rk in required_keys:
            assert rk in variant, f"city_slider variant '{variant_key}' missing '{rk}'"


def test_slider_system_city_heavy_duty_weight():
    city = SLIDER_SYSTEM_SPECS["city_slider"]
    hd = city["roller_variants"]["heavy_duty"]
    assert hd["max_weight_kg"] == 90


def test_slider_system_city_clip_in_weight():
    city = SLIDER_SYSTEM_SPECS["city_slider"]
    clip = city["roller_variants"]["clip_in"]
    assert clip["max_weight_kg"] == 45


def test_slider_system_city_variant_glass_thickness():
    city = SLIDER_SYSTEM_SPECS["city_slider"]
    clip = city["roller_variants"]["clip_in"]
    hd = city["roller_variants"]["heavy_duty"]
    assert clip["door_glass_thickness"] == [6, 8]
    assert hd["door_glass_thickness"] == [8, 10]
    # Top-level is union of both
    for t in clip["door_glass_thickness"] + hd["door_glass_thickness"]:
        assert t in city["door_glass_thickness"]


def test_slider_system_city_corner_capable():
    city = SLIDER_SYSTEM_SPECS["city_slider"]
    assert city.get("corner_slider_capable") is True


def test_slider_finishes():
    assert len(SLIDER_FINISHES) >= 3
    assert "Bright Polished" in SLIDER_FINISHES
    assert "Matte Black" in SLIDER_FINISHES


def test_floor_guide_specs():
    assert FLOOR_GUIDE_SPECS["code"] == "SL-0099P"
    assert FLOOR_GUIDE_SPECS["width"] == 30
    assert FLOOR_GUIDE_SPECS["height"] == 23
    assert FLOOR_GUIDE_SPECS["length"] == 50
    assert FLOOR_GUIDE_SPECS["depth"] == 19


def test_validateSliderSystem_ok():
    valid, msg = validateSliderSystem("edge_slider", 800, 40, 8)
    assert valid is True


def test_validateSliderSystem_width_exceeded():
    valid, msg = validateSliderSystem("duplo", 900, 20, 6)
    assert valid is False
    assert "width" in msg.lower()


def test_validateSliderSystem_weight_exceeded():
    valid, msg = validateSliderSystem("duplo", 700, 30, 6)
    assert valid is False
    assert "weight" in msg.lower()


def test_validateSliderSystem_glass_unsupported():
    valid, msg = validateSliderSystem("duplo", 700, 20, 10)
    assert valid is False
    assert "thickness" in msg.lower()


def test_validateSliderSystem_unknown_system():
    valid, msg = validateSliderSystem("nonexistent", 800, 30, 8)
    assert valid is False


def test_validateSliderSystem_city_wide_range():
    # City supports 6, 8, 10mm glass
    valid, msg = validateSliderSystem("city_slider", 800, 40, 10)
    assert valid is True
    valid, msg = validateSliderSystem("city_slider", 800, 40, 6)
    assert valid is True



def test_lookupSliderProductCode_known():
    key, pc = lookupSliderProductCode("RST-2000B")
    assert key == "edge_slider"
    assert pc["material"] == "S/S 304"
    assert pc["finish"] == "Bright Polished"


def test_lookupSliderProductCode_city():
    key, pc = lookupSliderProductCode("CSLT-2000MB")
    assert key == "city_slider"
    assert pc["finish"] == "Matte Black"


def test_lookupSliderProductCode_unknown():
    key, pc = lookupSliderProductCode("NONEXISTENT-999")
    assert key is None
    assert pc is None


# -----------------------------------------------------------------------
# Catalogue stabiliser specs tests
# -----------------------------------------------------------------------

def test_catalogue_stabiliser_finishes_not_empty():
    assert len(CATALOGUE_STABILISER_FINISHES) >= 6
    assert "Bright Chrome" in CATALOGUE_STABILISER_FINISHES
    assert "Matte Black" in CATALOGUE_STABILISER_FINISHES
    assert "Brushed" in CATALOGUE_STABILISER_FINISHES


def test_catalogue_stabiliser_specs_count():
    assert len(CATALOGUE_STABILISER_SPECS) == 18


def test_catalogue_stabiliser_specs_structure():
    required_keys = {"name", "profile_shape", "component_type", "bar_diameter",
                     "dimensions", "product_codes"}
    valid_profiles = {"round", "square"}
    valid_types = {"connector", "bar"}
    for key, spec in CATALOGUE_STABILISER_SPECS.items():
        for rk in required_keys:
            assert rk in spec, f"{key} missing '{rk}'"
        assert spec["profile_shape"] in valid_profiles, (
            f"{key} has invalid profile_shape '{spec['profile_shape']}'"
        )
        assert spec["component_type"] in valid_types, (
            f"{key} has invalid component_type '{spec['component_type']}'"
        )
        assert spec["bar_diameter"] == 19, f"{key} bar_diameter != 19"
        assert len(spec["product_codes"]) > 0, f"{key} has no product codes"
        for pc in spec["product_codes"]:
            assert "code" in pc and "material" in pc and "finish" in pc


def test_catalogue_stabiliser_connectors_have_role():
    for key, spec in CATALOGUE_STABILISER_SPECS.items():
        if spec["component_type"] == "connector":
            assert "connector_role" in spec, f"{key} connector missing connector_role"
            assert "bore" in spec, f"{key} connector missing bore"
            assert "angle_adjustable" in spec, f"{key} connector missing angle_adjustable"


def test_catalogue_stabiliser_bars_have_lengths():
    for key, spec in CATALOGUE_STABILISER_SPECS.items():
        if spec["component_type"] == "bar":
            assert "bar_lengths" in spec, f"{key} bar missing bar_lengths"
            assert len(spec["bar_lengths"]) >= 2, f"{key} should have multiple bar lengths"
            for pc in spec["product_codes"]:
                assert "bar_length" in pc, f"{key}/{pc['code']} missing bar_length"
                assert pc["bar_length"] in spec["bar_lengths"], (
                    f"{key}/{pc['code']} bar_length {pc['bar_length']} not in {spec['bar_lengths']}"
                )


def test_catalogue_stabiliser_product_codes_unique():
    seen = {}
    for key, spec in CATALOGUE_STABILISER_SPECS.items():
        for pc in spec["product_codes"]:
            code = pc["code"]
            assert code not in seen, (
                f"Duplicate product code '{code}' in '{key}' and '{seen[code]}'"
            )
            seen[code] = key


def test_catalogue_stabiliser_round_count():
    round_keys = [k for k, s in CATALOGUE_STABILISER_SPECS.items()
                  if s["profile_shape"] == "round"]
    assert len(round_keys) == 12  # 11 connectors + 1 bar


def test_catalogue_stabiliser_square_count():
    square_keys = [k for k, s in CATALOGUE_STABILISER_SPECS.items()
                   if s["profile_shape"] == "square"]
    assert len(square_keys) == 6  # 5 connectors + 1 bar


def test_getStabilisersByProfile_round():
    result = getStabilisersByProfile("round")
    assert len(result) == 12
    assert "round_wall_flange" in result
    assert "round_19_bar" in result


def test_getStabilisersByProfile_square():
    result = getStabilisersByProfile("square")
    assert len(result) == 6
    assert "square_wall_flange" in result
    assert "square_19_bar" in result


def test_getStabilisersByRole_wall_flange():
    result = getStabilisersByRole("wall_flange")
    assert len(result) == 2
    assert "round_wall_flange" in result
    assert "square_wall_flange" in result


def test_getStabilisersByRole_tee_coupler():
    result = getStabilisersByRole("tee_coupler")
    assert len(result) == 2
    assert "round_tee_coupler" in result
    assert "square_tee_coupler" in result


def test_lookupStabiliserProductCode_known():
    key, pc = lookupStabiliserProductCode("KA-101-19")
    assert key == "round_wall_flange"
    assert pc["material"] == "Brass"
    assert pc["finish"] == "Bright Chrome"


def test_lookupStabiliserProductCode_bar():
    key, pc = lookupStabiliserProductCode("SB19-2000B")
    assert key == "round_19_bar"
    assert pc["bar_length"] == 2000
    assert pc["finish"] == "Bright Polished"


def test_lookupStabiliserProductCode_unknown():
    key, pc = lookupStabiliserProductCode("NONEXISTENT-999")
    assert key is None
    assert pc is None


def test_support_bar_specs_default_diameter_19():
    for key, spec in SUPPORT_BAR_SPECS.items():
        assert spec["default_diameter"] == 19, (
            f"SUPPORT_BAR_SPECS['{key}'] default_diameter should be 19, got {spec['default_diameter']}"
        )


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
