# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Hardware specifications database for shower enclosures.

This module contains standardized specifications for all hardware types:
hinges, handles, clamps, channels, tracks, rollers, support bars, and seals.

Pure Python — no FreeCAD imports. Models import from here, never the reverse.
"""

# ---------------------------------------------------------------------------
# Shared finish list
# ---------------------------------------------------------------------------
HARDWARE_FINISHES = ["Chrome", "Brushed-Nickel", "Matte-Black", "Gold"]

# ---------------------------------------------------------------------------
# Hinge specifications (generic / legacy)
# ---------------------------------------------------------------------------
HINGE_SPECS = {
    "standard_glass_to_glass": {
        "load_capacity_kg": 45,
        "dimensions": {"width": 65, "depth": 20, "height": 90},
        "glass_thickness_range": [6, 8, 10, 12],
        "max_opening_angle": 180,
        "mounting_type": "Glass-to-Glass",
    },
    "heavy_duty_wall_mount": {
        "load_capacity_kg": 100,
        "dimensions": {"width": 70, "depth": 25, "height": 100},
        "glass_thickness_range": [8, 10, 12],
        "max_opening_angle": 110,
        "mounting_type": "Wall",
    },
    "standard_wall_mount": {
        "load_capacity_kg": 45,
        "dimensions": {"width": 65, "depth": 20, "height": 90},
        "glass_thickness_range": [6, 8, 10, 12],
        "max_opening_angle": 110,
        "mounting_type": "Wall",
    },
}

# ---------------------------------------------------------------------------
# Bevel hinge range — from Showers-Ex-Sliding catalogue
# ---------------------------------------------------------------------------

# Finishes available in the Bevel range
BEVEL_FINISHES = [
    "Bright Polished",
    "Antique Brass",
    "Matte Black",
    "Bright Chrome",
    "Satin Chrome",
]

# Product code series → material + finish mapping
BEVEL_CODE_SERIES = {
    "201": {"material": "S/S 304", "finish": "Bright Polished"},
    "281": {"material": "S/S 304", "finish": "Antique Brass"},
    "291": {"material": "S/S 304", "finish": "Matte Black"},
    "301": {"material": "Brass", "finish": "Bright Chrome"},
    "501": {"material": "S/S 304", "finish": "Bright Polished"},
    "581": {"material": "S/S 304", "finish": "Antique Brass"},
    "591": {"material": "S/S 304", "finish": "Matte Black"},
    "701": {"material": "Brass", "finish": "Bright Chrome"},
    "711": {"material": "Brass", "finish": "Satin Chrome"},
    "791": {"material": "Brass", "finish": "Matte Black"},
}

BEVEL_HINGE_SPECS = {
    # ------------------------------------------------------------------
    # 1. Bevel 90° Wall to Glass — Full Plate
    # ------------------------------------------------------------------
    "bevel_90_wall_to_glass_full": {
        "name": "Bevel 90° Wall to Glass Hinge — Full Plate",
        "mounting_type": "Wall-to-Glass",
        "angle": 90,
        "max_opening_angle": 90,
        "dimensions": {
            "wall_plate_width": 50,
            "glass_plate_width": 55,
            "glass_cutout_width": 63,
            "glass_cutout_depth": 41,
            "body_height": 90,
            "body_width": 65,
            "knuckle_depth": 37,
            "knuckle_width": 58,
            "knuckle_diameter": 16,
            "wall_to_glass_offset": 10,
        },
        "product_codes": [
            {"code": "SDH-201-90", "material": "S/S 304", "finish": "Bright Polished",
             "weight_capacity_kg": 35, "glass_thickness_range": [6, 8, 10]},
            {"code": "SDH-291-90", "material": "S/S 304", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-301-90", "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12],
             "adjustable": True},
            {"code": "SDH-501-90", "material": "S/S 304", "finish": "Bright Polished",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-581-90", "material": "S/S 304", "finish": "Antique Brass",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-591-90", "material": "S/S 304", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-701-90", "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },

    # ------------------------------------------------------------------
    # 2. Bevel 90° Wall to Glass — Half Plate
    # ------------------------------------------------------------------
    "bevel_90_wall_to_glass_half": {
        "name": "Bevel 90° Wall to Glass Hinge — Half Plate",
        "mounting_type": "Wall-to-Glass",
        "angle": 90,
        "max_opening_angle": 90,
        "dimensions": {
            "wall_plate_width": 50,
            "glass_plate_width": 55,
            "glass_cutout_width": 63,
            "glass_cutout_depth": 41,
            "body_height": 90,
            "body_width": 65,
            "knuckle_depth": 37,
            "knuckle_width": 58,
            "knuckle_diameter": 16,
            "wall_to_glass_offset": 10,
        },
        "product_codes": [
            {"code": "SDH-201-90HP", "material": "S/S 304", "finish": "Bright Polished",
             "weight_capacity_kg": 35, "glass_thickness_range": [6, 8, 10]},
            {"code": "SDH-281-90HP", "material": "S/S 304", "finish": "Antique Brass",
             "weight_capacity_kg": 35, "glass_thickness_range": [6, 8, 10]},
            {"code": "SDH-291-90HP", "material": "S/S 304", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-301-90HP", "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12],
             "adjustable": True},
            {"code": "SDH-501-90HP", "material": "S/S 304", "finish": "Bright Polished",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-581-90HP", "material": "S/S 304", "finish": "Antique Brass",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-591-90HP", "material": "S/S 304", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-701-90HP", "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-711-90HP", "material": "Brass", "finish": "Satin Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },

    # ------------------------------------------------------------------
    # 3. Bevel 135° Wall to Glass
    # ------------------------------------------------------------------
    "bevel_135_wall_to_glass": {
        "name": "Bevel 135° Wall to Glass Hinge",
        "mounting_type": "Wall-to-Glass",
        "angle": 135,
        "max_opening_angle": 135,
        "dimensions": {
            "wall_plate_width": 50,
            "glass_plate_width": 55,
            "glass_cutout_width": 63,
            "glass_cutout_depth": 41,
            "body_height": 90,
            "body_width": 65,
            "knuckle_depth": 37,
            "knuckle_width": 58,
            "knuckle_diameter": 16,
            "wall_to_glass_offset_inside": 9,
            "wall_to_glass_offset_outside": 17,
            "pivot_offset": 18,
        },
        "product_codes": [
            {"code": "SDH-701-135", "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },

    # ------------------------------------------------------------------
    # 4. Bevel 90° Glass to Glass
    # ------------------------------------------------------------------
    "bevel_90_glass_to_glass": {
        "name": "Bevel 90° Glass to Glass Hinge",
        "mounting_type": "Glass-to-Glass",
        "angle": 90,
        "max_opening_angle": 90,
        "dimensions": {
            "fixed_plate_width": 60,
            "glass_plate_width": 55,
            "glass_cutout_width": 63,
            "glass_cutout_depth": 41,
            "body_height": 90,
            "body_width": 78,
            "knuckle_depth": 37,
            "knuckle_width": 58,
            "knuckle_diameter": 16,
            "glass_to_glass_offset": 10,  # for 8mm glass
        },
        "product_codes": [
            {"code": "SDH-202-90", "material": "S/S 304", "finish": "Bright Polished",
             "weight_capacity_kg": 35, "glass_thickness_range": [6, 8, 10]},
            {"code": "SDH-282-90", "material": "S/S 304", "finish": "Antique Brass",
             "weight_capacity_kg": 35, "glass_thickness_range": [6, 8, 10]},
            {"code": "SDH-292-90", "material": "S/S 304", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-502-90", "material": "S/S 304", "finish": "Bright Polished",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-582-90", "material": "S/S 304", "finish": "Antique Brass",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-592-90", "material": "S/S 304", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-702-90", "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-712-90", "material": "Brass", "finish": "Satin Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },

    # ------------------------------------------------------------------
    # 5. Bevel 135° Glass to Glass — Unequal Cut Out
    # ------------------------------------------------------------------
    "bevel_135_glass_to_glass_unequal": {
        "name": "Bevel 135° Glass to Glass Hinge — Unequal Cut Out",
        "mounting_type": "Glass-to-Glass",
        "angle": 135,
        "max_opening_angle": 135,
        "dimensions": {
            "glass_plate_width_door": 55,
            "glass_plate_width_fix": 43,
            "glass_cutout_width": 63,
            "glass_cutout_depth_door": 41,
            "glass_cutout_depth_fix": 35,
            "body_height": 90,
            "body_width": 65,
            "knuckle_depth_door": 37,
            "knuckle_depth_fix": 27,
            "knuckle_width": 58,
            "knuckle_diameter": 16,
            "glass_to_glass_offset_inside_fix": 7,
            "glass_to_glass_offset_inside_door": 4,
            "glass_to_glass_offset_outside_fix": 11,
            "glass_to_glass_offset_outside_door": 7,
            "pivot_offset": 19,
        },
        "product_codes": [
            {"code": "SDH-202-135", "material": "S/S 304", "finish": "Bright Polished",
             "weight_capacity_kg": 35, "glass_thickness_range": [6, 8, 10]},
            {"code": "SDH-292-135", "material": "S/S 304", "finish": "Matte Black",
             "weight_capacity_kg": 35, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-502-135", "material": "S/S 304", "finish": "Bright Polished",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-592-135", "material": "S/S 304", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-702-135", "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-712-135", "material": "Brass", "finish": "Satin Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },

    # ------------------------------------------------------------------
    # 6. Bevel 135° Glass to Glass — Equal Cut Out
    # ------------------------------------------------------------------
    "bevel_135_glass_to_glass_equal": {
        "name": "Bevel 135° Glass to Glass Hinge — Equal Cut Out",
        "mounting_type": "Glass-to-Glass",
        "angle": 135,
        "max_opening_angle": 135,
        "dimensions": {
            "glass_plate_width": 55,
            "glass_cutout_width": 63,
            "glass_cutout_depth": 41,
            "body_height": 90,
            "body_width": 65,
            "knuckle_depth": 37,
            "knuckle_width": 58,
            "knuckle_diameter": 16,
            "glass_to_glass_offset_inside_fix": 7,
            "glass_to_glass_offset_inside_door": 4,
            "glass_to_glass_offset_outside_fix": 11,
            "glass_to_glass_offset_outside_door": 7,
            "pivot_offset": 19,
        },
        "product_codes": [
            {"code": "SDH-502-135E", "material": "S/S 304", "finish": "Bright Polished",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-582-135E", "material": "S/S 304", "finish": "Antique Brass",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-592-135E", "material": "S/S 304", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },

    # ------------------------------------------------------------------
    # 7. Bevel 180° Glass to Glass
    # ------------------------------------------------------------------
    "bevel_180_glass_to_glass": {
        "name": "Bevel 180° Glass to Glass Hinge",
        "mounting_type": "Glass-to-Glass",
        "angle": 180,
        "max_opening_angle": 180,
        "dimensions": {
            "glass_plate_width": 55,
            "glass_cutout_width": 63,
            "glass_cutout_depth": 41,
            "body_height": 90,
            "body_width": 115,
            "knuckle_depth": 37,
            "knuckle_width": 58,
            "knuckle_diameter": 16,
            "glass_to_glass_offset": 4,  # for 8mm glass
        },
        "product_codes": [
            {"code": "SDH-202-180", "material": "S/S 304", "finish": "Bright Polished",
             "weight_capacity_kg": 35, "glass_thickness_range": [6, 8, 10]},
            {"code": "SDH-282-180", "material": "S/S 304", "finish": "Antique Brass",
             "weight_capacity_kg": 35, "glass_thickness_range": [6, 8, 10]},
            {"code": "SDH-292-180", "material": "S/S 304", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-302-180", "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12],
             "adjustable": True},
            {"code": "SDH-502-180", "material": "S/S 304", "finish": "Bright Polished",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-582-180", "material": "S/S 304", "finish": "Antique Brass",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-592-180", "material": "S/S 304", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-702-180", "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-712-180", "material": "Brass", "finish": "Satin Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },

    # ------------------------------------------------------------------
    # 8. Bevel 360° Glass to Wall Pivot
    # ------------------------------------------------------------------
    "bevel_360_wall_pivot": {
        "name": "Bevel 360° Glass to Wall Pivot Hinge",
        "mounting_type": "Glass-to-Wall-Pivot",
        "angle": 360,
        "max_opening_angle": 360,
        "dimensions": {
            "body_height": 70,
            "body_width": 90,
            "knuckle_width": 58,
            "knuckle_depth": 37,
            "knuckle_diameter": 16,
            "glass_plate_height": 55,
            "glass_cutout_width": 63,
            "glass_cutout_depth": 41,
            "glass_slot_depth": 16,
            "floor_offset": 15,
            "pivot_plate_depth": 20,
            "pivot_plate_height": 9,
        },
        "product_codes": [
            {"code": "SDH-704-360", "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-714-360", "material": "Brass", "finish": "Satin Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "SDH-794-360", "material": "Brass", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },

    # ------------------------------------------------------------------
    # 9. Bevel 360° Glass to Glass Pivot
    # ------------------------------------------------------------------
    "bevel_360_glass_pivot": {
        "name": "Bevel 360° Glass to Glass Pivot Hinge",
        "mounting_type": "Glass-to-Glass-Pivot",
        "angle": 360,
        "max_opening_angle": 360,
        "dimensions": {
            "body_height": 116,
            "body_width": 90,
            "knuckle_width": 58,
            "knuckle_depth": 37,
            "knuckle_diameter": 16,
            "glass_plate_height": 55,
            "glass_cutout_width": 63,
            "glass_cutout_depth": 41,
            "glass_slot_depth": 16,
            "glass_to_glass_offset": 9,
        },
        "product_codes": [
            {"code": "SDH-708-360", "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },

    # ------------------------------------------------------------------
    # 10. Bevel Glass to Glass Tee Hinge 90°
    # ------------------------------------------------------------------
    "bevel_90_tee": {
        "name": "Bevel Glass to Glass Tee Hinge 90°",
        "mounting_type": "Glass-to-Glass-Tee",
        "angle": 90,
        "max_opening_angle": 90,
        "dimensions": {
            "fixed_plate_width": 60,
            "glass_plate_width": 55,
            "glass_cutout_width": 63,
            "glass_cutout_depth": 41,
            "body_height": 90,
            "body_width": 142,
            "knuckle_depth": 37,
            "knuckle_width": 58,
            "knuckle_diameter": 16,
            "fixed_hole_diameter": 16,
            "fixed_hole_depth": 37,
            "fixed_hole_height": 58,
            "glass_to_glass_offset": 10,  # for 8mm glass
        },
        "product_codes": [
            {"code": "H100T", "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "H110T", "material": "Brass", "finish": "Satin Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "H190T", "material": "Brass", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
}

# Bi-fold hinge configuration (fold direction by hand)
BIFOLD_HINGE_SPECS = {
    "Left": {
        "primary_angle": 180,
        "secondary_angle": 45,
        "fold_direction": "Inward",
    },
    "Right": {
        "primary_angle": 180,
        "secondary_angle": 45,
        "fold_direction": "Outward",
    },
}

# ---------------------------------------------------------------------------
# Monza bi-fold self-rising hinge specifications
# ---------------------------------------------------------------------------

MONZA_FINISHES = ["Bright Chrome", "Matte Black"]

MONZA_BIFOLD_HINGE_SPECS = {
    # ------------------------------------------------------------------
    # 1. Monza 90° Wall to Glass Self Rising Hinge
    # ------------------------------------------------------------------
    "monza_90_wall_to_glass": {
        "name": "Monza 90° Wall to Glass Self Rising Hinge",
        "mounting_type": "Wall-to-Glass",
        "hinge_category": "Bi-Fold",
        "angle": 90,
        "self_rising": True,
        "rise_height": 8,
        "handed": True,
        "dimensions": {
            "wall_plate_width": 35,
            "glass_plate_width": 35,
            "knuckle_depth": 35,
            "knuckle_width": 45,
            "body_height": 80,
            "body_width": 60,
            "knuckle_diameter": 14,
            "wall_to_glass_offset": 10,
        },
        "product_codes": [
            {"code": "STM-WGH-90L", "hand": "Left", "material": "Brass",
             "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "STM-WGH-90R", "hand": "Right", "material": "Brass",
             "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "MWGH-90LMB", "hand": "Left", "material": "Brass",
             "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "MWGH-90RMB", "hand": "Right", "material": "Brass",
             "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },

    # ------------------------------------------------------------------
    # 2. Monza 180° Glass to Glass Self Rising Hinge
    # ------------------------------------------------------------------
    "monza_180_glass_to_glass": {
        "name": "Monza 180° Glass to Glass Self Rising Hinge",
        "mounting_type": "Glass-to-Glass",
        "hinge_category": "Bi-Fold",
        "angle": 180,
        "self_rising": True,
        "rise_height": 8,
        "handed": True,
        "dimensions": {
            "glass_plate_width": 35,
            "knuckle_depth": 30,
            "knuckle_width": 45,
            "body_height": 80,
            "body_width": 98,
            "knuckle_diameter": 14,
            "glass_to_glass_offset": 6,
        },
        "product_codes": [
            {"code": "STM-GGH-180L", "hand": "Left", "material": "Brass",
             "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "STM-GGH-180R", "hand": "Right", "material": "Brass",
             "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "MGGH-180LMB", "hand": "Left", "material": "Brass",
             "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "MGGH-180RMB", "hand": "Right", "material": "Brass",
             "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
}

# Configuration pairing: which hand for wall/fold hinge given side + direction
MONZA_PAIRING = {
    ("Left", "Inward"):   {"wall": "Right", "fold": "Left"},
    ("Right", "Inward"):  {"wall": "Left",  "fold": "Right"},
    ("Left", "Outward"):  {"wall": "Left",  "fold": "Right"},
    ("Right", "Outward"): {"wall": "Right", "fold": "Left"},
}

HINGE_PLACEMENT_DEFAULTS = {
    "offset_top": 300,       # mm from top edge
    "offset_bottom": 300,    # mm from bottom edge
    "weight_threshold_3_hinges": 45,  # kg — above this, use 3 hinges
}

# ---------------------------------------------------------------------------
# Door mounting variant → compatible hinge mapping
# ---------------------------------------------------------------------------
DOOR_MOUNTING_VARIANTS = {
    "Wall Mounted": {
        "legacy_types": ["standard_wall_mount", "heavy_duty_wall_mount"],
        "bevel_mounting_types": ["Wall-to-Glass"],
    },
    "Glass Mounted": {
        "legacy_types": ["standard_glass_to_glass"],
        "bevel_mounting_types": ["Glass-to-Glass", "Glass-to-Glass-Tee"],
    },
    "Pivot": {
        "legacy_types": [],
        "bevel_mounting_types": ["Glass-to-Wall-Pivot", "Glass-to-Glass-Pivot"],
    },
}


def getHingeModelsForVariant(variant):
    """
    Return a list of hinge model keys compatible with a door mounting variant.

    Args:
        variant: Key into DOOR_MOUNTING_VARIANTS ("Wall Mounted", etc.)

    Returns:
        list[str]: ["Legacy", ...bevel keys...] or just bevel keys
    """
    info = DOOR_MOUNTING_VARIANTS.get(variant)
    if info is None:
        return ["Legacy"]

    models = []
    # Add "Legacy" entry if there are compatible legacy hinge types
    if info["legacy_types"]:
        models.append("Legacy")

    # Add matching Bevel hinge keys
    for key, spec in BEVEL_HINGE_SPECS.items():
        if spec["mounting_type"] in info["bevel_mounting_types"]:
            models.append(key)

    return models if models else ["Legacy"]

# ---------------------------------------------------------------------------
# Handle specifications
# ---------------------------------------------------------------------------
HANDLE_SPECS = {
    "Knob": {
        "diameter": 40,       # mm
        "depth": 15,          # mm (projection from glass)
        "mounting_type": "Through-bolt",
        "ada_compliant": False,
    },
    "Bar": {
        "diameter": 24,       # mm (bar cross-section)
        "lengths": [300, 450, 600],  # mm available lengths
        "mounting_type": "Through-bolt",
        "ada_compliant": True,
    },
    "Pull": {
        "diameter": 20,       # mm (bar cross-section)
        "lengths": [200, 300, 400],  # mm available lengths
        "mounting_type": "Through-bolt",
        "ada_compliant": True,
    },
    "Towel_Bar": {
        "diameter": 24,       # mm
        "lengths": [300, 450, 600],  # mm
        "mounting_type": "Through-bolt",
        "ada_compliant": True,
    },
}

HANDLE_PLACEMENT_DEFAULTS = {
    "height": 1050,           # mm from floor
    "min_height": 300,        # mm
    "max_height": 1800,       # mm
    "ada_min_height": 900,    # mm
    "ada_max_height": 1200,   # mm
    "offset_from_edge": 75,   # mm
}

# ---------------------------------------------------------------------------
# Support bar specifications
# ---------------------------------------------------------------------------
SUPPORT_BAR_SPECS = {
    "Horizontal": {
        "diameter_range": [12, 25],  # mm
        "default_diameter": 16,
        "mounting": "Glass-to-Wall",
    },
    "Vertical": {
        "diameter_range": [12, 25],
        "default_diameter": 16,
        "mounting": "Glass-to-Floor-to-Ceiling",
    },
    "Diagonal": {
        "diameter_range": [12, 25],
        "default_diameter": 16,
        "mounting": "Glass-to-Wall",
    },
    "Ceiling": {
        "diameter_range": [12, 25],
        "default_diameter": 16,
        "mounting": "Glass-to-Ceiling",
    },
}

SUPPORT_BAR_RULES = {
    "walkin_needs_bar_width": 1000,    # mm — walk-in panels wider than this need a bar
    "fixed_needs_ceiling_height": 2400,  # mm — fixed panels taller than this need ceiling support
}

# ---------------------------------------------------------------------------
# Seal specifications
# ---------------------------------------------------------------------------
SEAL_SPECS = {
    "door_sweep": {
        "thickness": 6,   # mm
        "location": "bottom",
        "description": "Bottom door sweep for water containment",
    },
    "vertical_seal": {
        "thickness": 8,   # mm
        "location": "side",
        "description": "Vertical edge seal between panels",
    },
    "magnetic_seal": {
        "thickness": 10,  # mm
        "location": "side",
        "description": "Magnetic closure seal for door edges",
    },
}

# ---------------------------------------------------------------------------
# Clamp specifications
# ---------------------------------------------------------------------------
CLAMP_SPECS = {
    "U_Clamp": {
        "load_capacity_kg": 45,
        "glass_thickness_range": [6, 8, 10],
        "default_mounting": "Floor",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 10,
            "cutout_depth": 20,
            "cutout_radius": 10,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 45, "depth": 19, "height": 45},
    },
    "L_Clamp": {
        "load_capacity_kg": 45,
        "glass_thickness_range": [6, 8, 10, 12],
        "default_mounting": "Wall",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 10,
            "cutout_depth": 20,
            "cutout_radius": 10,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 45, "depth": 60, "height": 45},
    },
    "180DEG_Clamp": {
        "load_capacity_kg": 45,
        "glass_thickness_range": [6, 8, 10],
        "default_mounting": "Floor",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 10,
            "cutout_depth": 20,
            "cutout_radius": 10,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 45, "depth": 19, "height": 90},
    },
    "135DEG_Clamp": {
        "load_capacity_kg": 45,
        "glass_thickness_range": [6, 8, 10],
        "default_mounting": "Floor",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 10,
            "cutout_depth": 20,
            "cutout_radius": 10,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 45, "depth": 70, "height": 90},
    },
}

CLAMP_PLACEMENT_DEFAULTS = {
    "wall_offset_top": 300,     # mm from top edge
    "wall_offset_bottom": 300,  # mm from bottom edge
    "floor_offset_start": 75,   # mm from panel edge
    "floor_offset_end": 75,     # mm from panel edge
}

# ---------------------------------------------------------------------------
# Channel specifications
# ---------------------------------------------------------------------------
CHANNEL_SPECS = {
    "wall": {"width": 15, "depth": 15},   # mm — U-channel profile
    "floor": {"width": 15, "depth": 15},
}

# ---------------------------------------------------------------------------
# Track profile specifications (moved from SlidingDoor.py)
# ---------------------------------------------------------------------------
TRACK_PROFILES = {
    "Edge": {"width": 10, "height": 30, "max_panels": 1},
    "City": {"width": 25, "height": 30, "max_panels": 1},
    "Ezy": {"width": 20, "height": 25, "max_panels": 1, "glass_thickness": [10, 12]},
    "Soft-Close": {"width": 25, "height": 35, "max_panels": 2},
}

# ---------------------------------------------------------------------------
# Roller specifications
# ---------------------------------------------------------------------------
ROLLER_SPECS = {
    "Standard": {"radius": 8, "height": 15},
    "Soft-Close": {"radius": 8, "height": 15},
}

# ---------------------------------------------------------------------------
# Bottom guide specifications
# ---------------------------------------------------------------------------
BOTTOM_GUIDE_SPECS = {
    "width": 15,   # mm
    "height": 5,   # mm
}


# ===================================================================
# Validation / selection functions
# ===================================================================

def selectHinge(door_weight, glass_thickness):
    """
    Select the most appropriate hinge type for a given door.

    Args:
        door_weight: Door weight in kg
        glass_thickness: Glass thickness in mm

    Returns:
        str: Key into HINGE_SPECS
    """
    thickness = int(glass_thickness)
    if door_weight > 45:
        if thickness in HINGE_SPECS["heavy_duty_wall_mount"]["glass_thickness_range"]:
            return "heavy_duty_wall_mount"
    if thickness in HINGE_SPECS["standard_wall_mount"]["glass_thickness_range"]:
        return "standard_wall_mount"
    return "standard_glass_to_glass"


def calculateHingePlacement(door_height, count, offset_top=None, offset_bottom=None):
    """
    Calculate evenly-spaced hinge Z positions along a door.

    Args:
        door_height: Door height in mm
        count: Number of hinges (2 or 3)
        offset_top: Distance from top (default: HINGE_PLACEMENT_DEFAULTS)
        offset_bottom: Distance from bottom (default: HINGE_PLACEMENT_DEFAULTS)

    Returns:
        list[float]: Z positions in mm from bottom
    """
    if offset_top is None:
        offset_top = HINGE_PLACEMENT_DEFAULTS["offset_top"]
    if offset_bottom is None:
        offset_bottom = HINGE_PLACEMENT_DEFAULTS["offset_bottom"]

    count = max(2, min(3, count))
    positions = [offset_bottom, door_height - offset_top]

    if count >= 3:
        middle = (offset_bottom + (door_height - offset_top)) / 2
        positions.insert(1, middle)

    return sorted(positions)


def validateHingeLoad(hinge_type, weight, count):
    """
    Validate that the selected hinges can support the door weight.

    Args:
        hinge_type: Key into HINGE_SPECS
        weight: Total door weight in kg
        count: Number of hinges

    Returns:
        tuple: (is_valid, message)
    """
    if hinge_type not in HINGE_SPECS:
        return False, f"Unknown hinge type: {hinge_type}"

    capacity = HINGE_SPECS[hinge_type]["load_capacity_kg"]
    total_capacity = capacity * count
    if weight > total_capacity:
        return False, (
            f"Door weight ({weight:.1f} kg) exceeds hinge capacity "
            f"({count}x {capacity} kg = {total_capacity} kg)"
        )
    return True, "Hinge load OK"


def selectClamp(panel_weight, glass_thickness, mounting_type):
    """
    Select the most appropriate clamp type.

    Args:
        panel_weight: Panel weight in kg
        glass_thickness: Glass thickness in mm
        mounting_type: "Wall" or "Floor"

    Returns:
        str: Key into CLAMP_SPECS
    """
    if mounting_type == "Wall":
        return "L_Clamp"
    return "U_Clamp"


def calculateClampPlacement(total_length, count, offset_start=None, offset_end=None):
    """
    Calculate evenly-spaced clamp positions along a length.

    Args:
        total_length: Total length to distribute clamps across (mm)
        count: Number of clamps
        offset_start: Offset from start edge (mm)
        offset_end: Offset from end edge (mm)

    Returns:
        list[float]: Positions in mm
    """
    if offset_start is None:
        offset_start = CLAMP_PLACEMENT_DEFAULTS["wall_offset_bottom"]
    if offset_end is None:
        offset_end = CLAMP_PLACEMENT_DEFAULTS["wall_offset_top"]

    if count == 1:
        return [total_length - offset_end]
    elif count == 2:
        return [offset_start, total_length - offset_end]
    else:
        available = total_length - offset_start - offset_end
        spacing = available / (count - 1)
        return [offset_start + i * spacing for i in range(count)]


def validateClampLoad(clamp_type, weight, count):
    """
    Validate that the selected clamps can support the panel weight.

    Args:
        clamp_type: Key into CLAMP_SPECS
        weight: Total panel weight in kg
        count: Number of clamps

    Returns:
        tuple: (is_valid, message)
    """
    if clamp_type not in CLAMP_SPECS:
        return False, f"Unknown clamp type: {clamp_type}"

    capacity = CLAMP_SPECS[clamp_type]["load_capacity_kg"]
    total_capacity = capacity * count
    if weight > total_capacity:
        return False, (
            f"Panel weight ({weight:.1f} kg) exceeds clamp capacity "
            f"({count}x {capacity} kg = {total_capacity} kg)"
        )
    return True, "Clamp load OK"


def requiresSupportBar(panel_width, panel_height, panel_type):
    """
    Determine if a panel needs a support bar based on its dimensions and type.

    Args:
        panel_width: Panel width in mm
        panel_height: Panel height in mm
        panel_type: "walkin" or "fixed"

    Returns:
        tuple: (required, reason)
    """
    if panel_type == "walkin" and panel_width > SUPPORT_BAR_RULES["walkin_needs_bar_width"]:
        return True, (
            f"Walk-in panel wider than {SUPPORT_BAR_RULES['walkin_needs_bar_width']}mm "
            "requires a support bar"
        )
    if panel_type == "fixed" and panel_height > SUPPORT_BAR_RULES["fixed_needs_ceiling_height"]:
        return True, (
            f"Fixed panel taller than {SUPPORT_BAR_RULES['fixed_needs_ceiling_height']}mm "
            "requires ceiling support"
        )
    return False, "No support bar required"


def validateHandlePlacement(handle_height, ada_required=False):
    """
    Validate handle placement height.

    Args:
        handle_height: Handle height from floor in mm
        ada_required: Whether ADA compliance is required

    Returns:
        tuple: (is_valid, message)
    """
    defaults = HANDLE_PLACEMENT_DEFAULTS
    if ada_required:
        if handle_height < defaults["ada_min_height"]:
            return False, (
                f"ADA requires handle at least {defaults['ada_min_height']}mm from floor "
                f"(current: {handle_height}mm)"
            )
        if handle_height > defaults["ada_max_height"]:
            return False, (
                f"ADA requires handle at most {defaults['ada_max_height']}mm from floor "
                f"(current: {handle_height}mm)"
            )
    else:
        if handle_height < defaults["min_height"]:
            return False, (
                f"Handle height below minimum {defaults['min_height']}mm "
                f"(current: {handle_height}mm)"
            )
        if handle_height > defaults["max_height"]:
            return False, (
                f"Handle height above maximum {defaults['max_height']}mm "
                f"(current: {handle_height}mm)"
            )
    return True, "Handle placement OK"


def selectSeal(location, glass_thickness, gap):
    """
    Select the appropriate seal type.

    Args:
        location: "bottom", "side", or "magnetic"
        glass_thickness: Glass thickness in mm
        gap: Gap size in mm

    Returns:
        str: Key into SEAL_SPECS
    """
    if location == "bottom":
        return "door_sweep"
    elif location == "magnetic":
        return "magnetic_seal"
    return "vertical_seal"
