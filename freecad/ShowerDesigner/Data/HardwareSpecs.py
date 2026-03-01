# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Hardware specifications database for shower enclosures.

This module contains standardized specifications for all hardware types:
hinges, handles, clamps, channels, tracks, rollers, and support bars.
Seal specs live in SealSpecs.py (re-exported here for backward compatibility).

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
            "glass_to_glass_offset": 5,  # for 8mm glass
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
            "body_height": 90,
            "body_width": 70,
            "knuckle_width": 58,
            "knuckle_depth": 37,
            "knuckle_diameter": 16,
            "glass_plate_width": 55,
            "glass_cutout_width": 63,
            "glass_cutout_depth": 41,
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
            "body_height": 90,
            "body_width": 116,
            "knuckle_width": 58,
            "knuckle_depth": 37,
            "knuckle_diameter": 16,
            "glass_plate_width": 55,
            "glass_cutout_width": 63,
            "glass_cutout_depth": 41,
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
        "legacy_types": [],
        "bevel_mounting_types": ["Wall-to-Glass"],
    },
    "Glass Mounted": {
        "legacy_types": [],
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

    models = []

    # Add matching Bevel hinge keys
    for key, spec in BEVEL_HINGE_SPECS.items():
        if spec["mounting_type"] in info["bevel_mounting_types"]:
            models.append(key)

    return models

# ---------------------------------------------------------------------------
# Handle specifications
# ---------------------------------------------------------------------------
HANDLE_SPECS = {
    "mushroom_knob_b2b": {
        "model_file": "MushroomKnob.FCStd",
        "catalogue_key": "mushroom_knob_b2b",
    },
    "pull_handle_round": {
        "model_file": "RoundPullHandle.FCStd",
        "catalogue_key": "pull_handle_round",
    },
    "flush_handle_with_plate": {
        "model_file": "FlushHandlePlate.FCStd",
        "catalogue_key": "flush_handle_with_plate",
    },
}

# ---------------------------------------------------------------------------
# Catalogue handle/knob/towel-rail specifications — from Showers-Ex-Sliding
# ---------------------------------------------------------------------------

CATALOGUE_HANDLE_FINISHES = [
    "Bright Polished",
    "Bright Chrome",
    "Brushed",
    "Satin Chrome",
    "Antique Brass",
    "Matte Black",
]

CATALOGUE_HANDLE_SPECS = {
    # ------------------------------------------------------------------
    # 1. Door Knobs
    # ------------------------------------------------------------------
    "mushroom_knob_b2b": {
        "name": "Back to Back Mushroom Knob",
        "category": "Knob",
        "mounting_type": "Through-bolt",
        "back_to_back": True,
        "hole_size": 14,
        "dimensions": {
            "knob_diameter": 35,
            "projection": 22,
            "base_diameter": 22,
        },
        "product_codes": [
            {"code": "DK-201", "material": "Brass", "finish": "Bright Chrome"},
            {"code": "DK-291", "material": "Brass", "finish": "Matte Black"},
            {"code": "DK-201A", "material": "Aluminium", "finish": "Bright Chrome"},
            {"code": "DK-211A", "material": "Aluminium", "finish": "Brushed"},
            {"code": "DK-281A", "material": "Aluminium", "finish": "Antique Brass"},
            {"code": "DK-291A", "material": "Aluminium", "finish": "Matte Black"},
            {"code": "DK-501", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "DK-511", "material": "S/S 304", "finish": "Brushed"},
        ],
    },
    "groove_knob_b2b": {
        "name": "Back to Back Small Groove Knob",
        "category": "Knob",
        "mounting_type": "Through-bolt",
        "back_to_back": True,
        "hole_size": 14,
        "dimensions": {
            "knob_diameter": 30,
            "projection": 28,
            "groove_diameter": 27,
        },
        "product_codes": [
            {"code": "DK-204A", "material": "Aluminium", "finish": "Bright Chrome"},
            {"code": "DK-504", "material": "S/S 304", "finish": "Bright Polished"},
        ],
    },
    "square_knob_b2b": {
        "name": "Back to Back Square Knob",
        "category": "Knob",
        "mounting_type": "Through-bolt",
        "back_to_back": True,
        "hole_size": 14,
        "dimensions": {
            "knob_width": 30,
            "projection": 30,
            "base_diameter": 22,
        },
        "product_codes": [
            {"code": "DK-202A", "material": "Aluminium", "finish": "Bright Chrome"},
            {"code": "DK-292A", "material": "Aluminium", "finish": "Matte Black"},
        ],
    },

    # ------------------------------------------------------------------
    # 2. Pull Handles
    # ------------------------------------------------------------------
    "pull_handle_round": {
        "name": "Pull Handle (Round)",
        "category": "Pull",
        "mounting_type": "Through-bolt",
        "back_to_back": False,
        "hole_size": 14,
        "dimensions": {
            "ctc": 200,
            "tube_diameter": 19,
            "projection": 61,
            "standoff_depth": 42,
        },
        "product_codes": [
            {"code": "BH-010", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "BH-810", "material": "S/S 304", "finish": "Antique Brass"},
            {"code": "BH-910", "material": "S/S 304", "finish": "Matte Black"},
        ],
    },
    "pull_handle_square": {
        "name": "Square Pull Handle",
        "category": "Pull",
        "mounting_type": "Through-bolt",
        "back_to_back": False,
        "hole_size": 14,
        "dimensions": {
            "ctc": 200,
            "tube_size": 19,
            "projection": 61,
            "standoff_depth": 42,
        },
        "product_codes": [
            {"code": "SH-010", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "SH-810", "material": "S/S 304", "finish": "Antique Brass"},
            {"code": "SH-910", "material": "S/S 304", "finish": "Matte Black"},
        ],
    },

    # ------------------------------------------------------------------
    # 3. Towel Rails
    # ------------------------------------------------------------------
    "towel_rail_round_finnial": {
        "name": "Towel Rail with Finnials (Round)",
        "category": "Towel_Bar",
        "mounting_type": "Through-bolt",
        "back_to_back": False,
        "hole_size": 14,
        "rail_lengths": [300, 400, 600],
        "dimensions": {
            "tube_diameter": 19,
            "projection": 61,
            "finnial_width": 42,
            "rail_offset": 24,
        },
        "product_codes": [
            {"code": "BH-030", "rail_length": 300,
             "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "BH-040", "rail_length": 400,
             "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "BH-060", "rail_length": 600,
             "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "BH-840", "rail_length": 400,
             "material": "S/S 304", "finish": "Antique Brass"},
            {"code": "BH-930", "rail_length": 300,
             "material": "S/S 304", "finish": "Matte Black"},
            {"code": "BH-940", "rail_length": 400,
             "material": "S/S 304", "finish": "Matte Black"},
            {"code": "BH-960", "rail_length": 600,
             "material": "S/S 304", "finish": "Matte Black"},
        ],
    },
    "towel_rail_square_finnial": {
        "name": "Square Towel Rail with Finnials",
        "category": "Towel_Bar",
        "mounting_type": "Through-bolt",
        "back_to_back": False,
        "hole_size": 14,
        "rail_lengths": [300, 400, 600],
        "dimensions": {
            "tube_size": 19,
            "projection": 61,
            "finnial_width": 42,
        },
        "product_codes": [
            {"code": "SH-0300", "rail_length": 300,
             "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "SH-0400", "rail_length": 400,
             "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "SH-0600", "rail_length": 600,
             "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "SH-9400", "rail_length": 400,
             "material": "S/S 304", "finish": "Matte Black"},
            {"code": "SH-9600", "rail_length": 600,
             "material": "S/S 304", "finish": "Matte Black"},
        ],
    },
    "towel_rail_round_knob": {
        "name": "Towel Rail with Back Knob (Round)",
        "category": "Towel_Bar",
        "mounting_type": "Through-bolt",
        "back_to_back": False,
        "hole_size": 14,
        "rail_lengths": [300, 400, 600],
        "dimensions": {
            "tube_diameter": 19,
            "projection": 61,
            "knob_end_width": 42,
        },
        "product_codes": [
            {"code": "DK-201-H300", "rail_length": 300,
             "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "DK-201-H400", "rail_length": 400,
             "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "DK-201-H600", "rail_length": 600,
             "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "DK-211-H400", "rail_length": 400,
             "material": "S/S 304", "finish": "Brushed"},
            {"code": "DK-281-H400", "rail_length": 400,
             "material": "S/S 304", "finish": "Antique Brass"},
            {"code": "DK-291-H300", "rail_length": 300,
             "material": "S/S 304", "finish": "Matte Black"},
            {"code": "DK-291-H400", "rail_length": 400,
             "material": "S/S 304", "finish": "Matte Black"},
            {"code": "DK-291-H600", "rail_length": 600,
             "material": "S/S 304", "finish": "Matte Black"},
        ],
    },
    "towel_rail_square_knob": {
        "name": "Square Towel Rail with Back Knob",
        "category": "Towel_Bar",
        "mounting_type": "Through-bolt",
        "back_to_back": False,
        "hole_size": 14,
        "rail_lengths": [300, 400, 600],
        "dimensions": {
            "tube_size": 19,
            "projection": 61,
            "knob_end_width": 42,
        },
        "product_codes": [
            {"code": "DK-202-H300", "rail_length": 300,
             "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "DK-202-H400", "rail_length": 400,
             "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "DK-202-H600", "rail_length": 600,
             "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "DK-292-H400", "rail_length": 400,
             "material": "S/S 304", "finish": "Matte Black"},
            {"code": "DK-292-H600", "rail_length": 600,
             "material": "S/S 304", "finish": "Matte Black"},
        ],
    },
    "towel_rail_bow_handle": {
        "name": "Towel Rail with Pull Handle (Bow)",
        "category": "Towel_Bar",
        "mounting_type": "Through-bolt",
        "back_to_back": False,
        "hole_size": 14,
        "dimensions": {
            "rail_ctc": 400,
            "handle_ctc": 200,
            "tube_diameter": 19,
            "projection": 61,
            "standoff_depth": 42,
        },
        "product_codes": [
            {"code": "BH-001", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "BH-901", "material": "S/S 304", "finish": "Matte Black"},
        ],
    },

    # ------------------------------------------------------------------
    # 4. Flush Handles
    # ------------------------------------------------------------------
    "flush_handle_with_plate": {
        "name": "Flush Handle with Plate",
        "category": "Flush",
        "mounting_type": "Flush",
        "back_to_back": False,
        "hole_size": 57,
        "dimensions": {
            "outer_diameter": 65,
            "plate_diameter": 54,
            "plate_thickness": 5,
            "recess_depth": 6,
        },
        "product_codes": [
            {"code": "FH-055P", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "FH-055N", "material": "S/S 304", "finish": "Brushed"},
            {"code": "FH-055MB", "material": "S/S 304", "finish": "Matte Black"},
        ],
    },
    "flush_handle_no_plate": {
        "name": "Flush Handle — No Plate",
        "category": "Flush",
        "mounting_type": "Flush",
        "back_to_back": False,
        "hole_size": 57,
        "dimensions": {
            "outer_diameter": 65,
            "total_depth": 48,
        },
        "product_codes": [
            {"code": "FH-155P", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "FH-155MB", "material": "S/S 304", "finish": "Matte Black"},
        ],
    },

    # ------------------------------------------------------------------
    # 5. Custom Kits (variable length)
    # ------------------------------------------------------------------
    "custom_towel_rail_handle_kit": {
        "name": "Custom Towel Rail and Handle Kit",
        "category": "Custom_Kit",
        "mounting_type": "Through-bolt",
        "back_to_back": False,
        "hole_size": 12,
        "variable_length": True,
        "dimensions": {
            "tube_diameter": 19,
            "projection": 60,
            "standoff_depth": 48,
            "bracket_depth": 37,
            "offset": 25,
        },
        "product_codes": [
            {"code": "BTK-ET", "material": "S/S 304", "finish": "Bright Polished"},
        ],
    },
    "custom_glass_towel_rail_kit": {
        "name": "Custom Glass Towel Rail Kit",
        "category": "Custom_Kit",
        "mounting_type": "Through-bolt",
        "back_to_back": False,
        "hole_size": 12,
        "variable_length": True,
        "dimensions": {
            "tube_diameter": 19,
            "projection": 60,
            "standoff_depth": 47,
        },
        "product_codes": [
            {"code": "STA-TRK-ET", "material": "S/S 304", "finish": "Bright Polished"},
        ],
    },
    "custom_glass_towel_rail_knob_kit": {
        "name": "Custom Glass Towel Rail Kit with Back Knob",
        "category": "Custom_Kit",
        "mounting_type": "Through-bolt",
        "back_to_back": False,
        "hole_size": 12,
        "variable_length": True,
        "dimensions": {
            "tube_diameter": 19,
            "projection": 60,
            "standoff_depth": 47,
        },
        "product_codes": [
            {"code": "STA-TRKK-ET", "material": "S/S 304", "finish": "Bright Polished"},
        ],
    },
    "custom_double_towel_rail_kit": {
        "name": "Custom Double Towel Rail Kit Wall Mount",
        "category": "Custom_Kit",
        "mounting_type": "Wall-mount",
        "back_to_back": False,
        "hole_size": 12,
        "variable_length": True,
        "dimensions": {
            "tube_diameter": 19,
            "total_projection": 140,
            "bracket_width": 50,
            "rail_spacing": 76,
        },
        "product_codes": [
            {"code": "SS-DTR-KIT", "material": "S/S 304", "finish": "Bright Polished"},
        ],
    },
    "custom_pull_handle_kit": {
        "name": "Custom Pull Handle Kit",
        "category": "Custom_Kit",
        "mounting_type": "Through-bolt",
        "back_to_back": False,
        "hole_size": 12,
        "variable_length": True,
        "dimensions": {
            "tube_diameter": 19,
            "projection": 48,
            "standoff_depth": 35,
        },
        "product_codes": [
            {"code": "STA-PH-KIT", "material": "S/S 304", "finish": "Bright Polished"},
        ],
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
        "default_diameter": 19,
        "mounting": "Glass-to-Wall",
    },
    "Vertical": {
        "diameter_range": [12, 25],
        "default_diameter": 19,
        "mounting": "Glass-to-Floor-to-Ceiling",
    },
    "Diagonal": {
        "diameter_range": [12, 25],
        "default_diameter": 19,
        "mounting": "Glass-to-Wall",
    },
    "Ceiling": {
        "diameter_range": [12, 25],
        "default_diameter": 19,
        "mounting": "Glass-to-Ceiling",
    },
}

SUPPORT_BAR_RULES = {
    "walkin_needs_bar_width": 1000,    # mm — walk-in panels wider than this need a bar
    "fixed_needs_ceiling_height": 2400,  # mm — fixed panels taller than this need ceiling support
}

# ---------------------------------------------------------------------------
# Catalogue stabiliser specifications — from Showers-Ex-Sliding-Catalogue, pp. 42–48
# ---------------------------------------------------------------------------

CATALOGUE_STABILISER_FINISHES = [
    "Bright Chrome",
    "Satin Chrome",
    "Bright Polished",
    "Antique Brass",
    "Matte Black",
    "Brushed",
]

CATALOGUE_STABILISER_SPECS = {
    # ------------------------------------------------------------------
    # Round connectors (11 entries)
    # ------------------------------------------------------------------
    "round_adjustable_wall_bracket": {
        "name": "Adjustable Wall Mount Bracket",
        "profile_shape": "round",
        "component_type": "connector",
        "connector_role": "adjustable_wall_bracket",
        "bar_diameter": 19,
        "bore": 19.268,
        "angle_adjustable": True,
        "angle_range": [90, 270],
        "angle_fixed": None,
        "hole_size": None,
        "dimensions": {"width": 35, "depth": 48, "height": 54},
        "product_codes": [
            {"code": "GSH-301", "material": "Brass", "finish": "Bright Chrome"},
            {"code": "GSH-311", "material": "Brass", "finish": "Satin Chrome"},
        ],
    },
    "round_adjustable_glass_bracket": {
        "name": "Adjustable Glass Mount Bracket",
        "profile_shape": "round",
        "component_type": "connector",
        "connector_role": "adjustable_glass_bracket",
        "bar_diameter": 19,
        "bore": 19.6,
        "angle_adjustable": True,
        "angle_range": [90, 270],
        "angle_fixed": None,
        "hole_size": 14,
        "dimensions": {"width": 29, "depth": 28, "height": 48},
        "product_codes": [
            {"code": "GSH-401", "material": "Brass", "finish": "Bright Chrome"},
            {"code": "GSH-411", "material": "Brass", "finish": "Satin Chrome"},
        ],
    },
    "round_adjustable_90_flange": {
        "name": "90deg Adjustable Flange",
        "profile_shape": "round",
        "component_type": "connector",
        "connector_role": "adjustable_90_flange",
        "bar_diameter": 19,
        "bore": 19.6,
        "angle_adjustable": True,
        "angle_range": [90, 270],
        "angle_fixed": None,
        "hole_size": None,
        "dimensions": {"diameter": 43.5},
        "product_codes": [
            {"code": "KA-003-19", "material": "Brass", "finish": "Bright Chrome"},
        ],
    },
    "round_wall_flange": {
        "name": "Wall Flange",
        "profile_shape": "round",
        "component_type": "connector",
        "connector_role": "wall_flange",
        "bar_diameter": 19,
        "bore": 19.6,
        "angle_adjustable": False,
        "angle_range": None,
        "angle_fixed": 90,
        "hole_size": None,
        "dimensions": {"diameter": 35, "projection": 25},
        "product_codes": [
            {"code": "KA-101-19", "material": "Brass", "finish": "Bright Chrome"},
            {"code": "KA-111-19", "material": "Brass", "finish": "Satin Chrome"},
            {"code": "KA-181-19", "material": "Brass", "finish": "Antique Brass"},
            {"code": "KA-191-19", "material": "Brass", "finish": "Matte Black"},
        ],
    },
    "round_glass_mount_straight": {
        "name": "Glass Mount (straight through)",
        "profile_shape": "round",
        "component_type": "connector",
        "connector_role": "glass_mount_straight",
        "bar_diameter": 19,
        "bore": 19.5,
        "angle_adjustable": False,
        "angle_range": None,
        "angle_fixed": None,
        "hole_size": 12,
        "dimensions": {"width": 53, "height": 25},
        "product_codes": [
            {"code": "KA-102-19", "material": "Brass", "finish": "Bright Chrome"},
            {"code": "KA-112-19", "material": "Brass", "finish": "Satin Chrome"},
            {"code": "KA-182-19", "material": "Brass", "finish": "Antique Brass"},
            {"code": "KA-192-19", "material": "Brass", "finish": "Matte Black"},
        ],
    },
    "round_glass_mount_offset": {
        "name": "Glass Mount Stabiliser",
        "profile_shape": "round",
        "component_type": "connector",
        "connector_role": "glass_mount_offset",
        "bar_diameter": 19,
        "bore": 19.5,
        "angle_adjustable": False,
        "angle_range": None,
        "angle_fixed": None,
        "hole_size": 12,
        "dimensions": {"width": 53, "height": 25, "length": 60},
        "product_codes": [
            {"code": "KA-103-19", "material": "Brass", "finish": "Bright Chrome"},
            {"code": "KA-113-19", "material": "Brass", "finish": "Satin Chrome"},
            {"code": "KA-183-19", "material": "Brass", "finish": "Antique Brass"},
            {"code": "KA-193-19", "material": "Brass", "finish": "Matte Black"},
        ],
    },
    "round_adjustable_90_glass_mount": {
        "name": "Adjustable 90deg Glass Mount",
        "profile_shape": "round",
        "component_type": "connector",
        "connector_role": "adjustable_90_glass_mount",
        "bar_diameter": 19,
        "bore": 19.5,
        "angle_adjustable": True,
        "angle_range": [80, 100],
        "angle_fixed": None,
        "hole_size": None,
        "dimensions": {"width": 57, "depth": 50, "height": 25},
        "product_codes": [
            {"code": "KA-106-19", "material": "Brass", "finish": "Bright Chrome"},
        ],
    },
    "round_wall_mount_45": {
        "name": "Wall Mount 45deg",
        "profile_shape": "round",
        "component_type": "connector",
        "connector_role": "wall_mount_45",
        "bar_diameter": 19,
        "bore": 19.6,
        "angle_adjustable": False,
        "angle_range": None,
        "angle_fixed": 45,
        "hole_size": None,
        "dimensions": {"projection": 25},
        "product_codes": [
            {"code": "KA-107-19", "material": "Brass", "finish": "Bright Chrome"},
            {"code": "KA-187-19", "material": "Brass", "finish": "Antique Brass"},
            {"code": "KA-197-19", "material": "Brass", "finish": "Matte Black"},
        ],
    },
    "round_tee_coupler": {
        "name": "Tee-Coupler",
        "profile_shape": "round",
        "component_type": "connector",
        "connector_role": "tee_coupler",
        "bar_diameter": 19,
        "bore": 19.6,
        "angle_adjustable": False,
        "angle_range": None,
        "angle_fixed": 90,
        "hole_size": None,
        "dimensions": {"width": 70, "height": 65, "projection": 25},
        "product_codes": [
            {"code": "KA-108-19", "material": "Brass", "finish": "Bright Chrome"},
            {"code": "KA-118-19", "material": "Brass", "finish": "Satin Chrome"},
            {"code": "KA-188-19", "material": "Brass", "finish": "Antique Brass"},
            {"code": "KA-198-19", "material": "Brass", "finish": "Matte Black"},
        ],
    },
    "round_90deg_fixed_connector": {
        "name": "90deg Fixed Connector",
        "profile_shape": "round",
        "component_type": "connector",
        "connector_role": "90deg_fixed_connector",
        "bar_diameter": 19,
        "bore": 19.5,
        "angle_adjustable": False,
        "angle_range": None,
        "angle_fixed": 90,
        "hole_size": None,
        "dimensions": {"width": 60, "height": 25, "arm_a": 24, "arm_b": 20},
        "product_codes": [
            {"code": "KA-109-19", "material": "Brass", "finish": "Bright Chrome"},
        ],
    },
    "round_through_glass_flange": {
        "name": "Through Glass Flange",
        "profile_shape": "round",
        "component_type": "connector",
        "connector_role": "through_glass_flange",
        "bar_diameter": 19,
        "bore": 20.4,
        "angle_adjustable": False,
        "angle_range": None,
        "angle_fixed": None,
        "hole_size": 14,
        "dimensions": {"diameter": 30, "depth": 20.4},
        "product_codes": [
            {"code": "DP-GFT", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "DP-GFT-MB", "material": "S/S 304", "finish": "Matte Black"},
        ],
    },
    # ------------------------------------------------------------------
    # Round bars (1 entry, 16 product codes)
    # ------------------------------------------------------------------
    "round_19_bar": {
        "name": "19mm Round Support Bar",
        "profile_shape": "round",
        "component_type": "bar",
        "bar_diameter": 19,
        "wall_thickness": 1,
        "bar_lengths": [1000, 1500, 2000, 3000],
        "dimensions": {"outer_diameter": 19, "inner_diameter": 17},
        "product_codes": [
            # 1000 mm — S/S 304
            {"code": "SB19-1000A", "material": "S/S 304", "finish": "Antique Brass",
             "bar_length": 1000},
            {"code": "SB19-1000B", "material": "S/S 304", "finish": "Bright Polished",
             "bar_length": 1000},
            {"code": "SB19-1000N", "material": "S/S 304", "finish": "Brushed",
             "bar_length": 1000},
            # 1000 mm — Aluminium
            {"code": "SBA19-1000MB", "material": "Aluminium", "finish": "Matte Black",
             "bar_length": 1000},
            # 1500 mm — S/S 304
            {"code": "SB19-1500A", "material": "S/S 304", "finish": "Antique Brass",
             "bar_length": 1500},
            {"code": "SB19-1500B", "material": "S/S 304", "finish": "Bright Polished",
             "bar_length": 1500},
            {"code": "SB19-1500N", "material": "S/S 304", "finish": "Brushed",
             "bar_length": 1500},
            # 1500 mm — Aluminium
            {"code": "SBA19-1500MB", "material": "Aluminium", "finish": "Matte Black",
             "bar_length": 1500},
            # 2000 mm — S/S 304
            {"code": "SB19-2000A", "material": "S/S 304", "finish": "Antique Brass",
             "bar_length": 2000},
            {"code": "SB19-2000B", "material": "S/S 304", "finish": "Bright Polished",
             "bar_length": 2000},
            {"code": "SB19-2000N", "material": "S/S 304", "finish": "Brushed",
             "bar_length": 2000},
            # 2000 mm — Aluminium
            {"code": "SBA19-2000MB", "material": "Aluminium", "finish": "Matte Black",
             "bar_length": 2000},
            # 3000 mm — S/S 304
            {"code": "SB19-3000A", "material": "S/S 304", "finish": "Antique Brass",
             "bar_length": 3000},
            {"code": "SB19-3000B", "material": "S/S 304", "finish": "Bright Polished",
             "bar_length": 3000},
            {"code": "SB19-3000N", "material": "S/S 304", "finish": "Brushed",
             "bar_length": 3000},
            # 3000 mm — Aluminium
            {"code": "SBA19-3000MB", "material": "Aluminium", "finish": "Matte Black",
             "bar_length": 3000},
        ],
    },
    # ------------------------------------------------------------------
    # Square connectors (5 entries)
    # ------------------------------------------------------------------
    "square_wall_flange": {
        "name": "Square Wall Flange",
        "profile_shape": "square",
        "component_type": "connector",
        "connector_role": "wall_flange",
        "bar_diameter": 19,
        "bore": 19.6,
        "angle_adjustable": False,
        "angle_range": None,
        "angle_fixed": 90,
        "hole_size": None,
        "dimensions": {"width": 26, "height": 28},
        "product_codes": [
            {"code": "KA-201-19", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "KA-291-19", "material": "S/S 304", "finish": "Matte Black"},
        ],
    },
    "square_glass_mount_straight": {
        "name": "Square Glass Mount (straight through)",
        "profile_shape": "square",
        "component_type": "connector",
        "connector_role": "glass_mount_straight",
        "bar_diameter": 19,
        "bore": 19.6,
        "angle_adjustable": False,
        "angle_range": None,
        "angle_fixed": None,
        "hole_size": 12,
        "dimensions": {"width": 51, "height": 28},
        "product_codes": [
            {"code": "KA-202-19", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "KA-292-19", "material": "S/S 304", "finish": "Matte Black"},
        ],
    },
    "square_glass_mount_offset": {
        "name": "Square Glass Mount",
        "profile_shape": "square",
        "component_type": "connector",
        "connector_role": "glass_mount_offset",
        "bar_diameter": 19,
        "bore": 19.6,
        "angle_adjustable": False,
        "angle_range": None,
        "angle_fixed": None,
        "hole_size": 12,
        "dimensions": {"width": 50, "height": 28},
        "product_codes": [
            {"code": "KA-203-19", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "KA-293-19", "material": "S/S 304", "finish": "Matte Black"},
        ],
    },
    "square_wall_mount_45": {
        "name": "Square Wall Mount 45deg",
        "profile_shape": "square",
        "component_type": "connector",
        "connector_role": "wall_mount_45",
        "bar_diameter": 19,
        "bore": 19.6,
        "angle_adjustable": False,
        "angle_range": None,
        "angle_fixed": 45,
        "hole_size": None,
        "dimensions": {"width": 26, "height": 26, "length": 74},
        "product_codes": [
            {"code": "KA-207-19", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "KA-297-19", "material": "S/S 304", "finish": "Matte Black"},
        ],
    },
    "square_tee_coupler": {
        "name": "Square Tee-Coupler",
        "profile_shape": "square",
        "component_type": "connector",
        "connector_role": "tee_coupler",
        "bar_diameter": 19,
        "bore": 19.6,
        "angle_adjustable": False,
        "angle_range": None,
        "angle_fixed": 90,
        "hole_size": None,
        "dimensions": {"width": 62},
        "product_codes": [
            {"code": "KA-208-19", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "KA-298-19", "material": "S/S 304", "finish": "Matte Black"},
        ],
    },
    # ------------------------------------------------------------------
    # Square bars (1 entry, 8 product codes)
    # ------------------------------------------------------------------
    "square_19_bar": {
        "name": "19mm Square Support Bar",
        "profile_shape": "square",
        "component_type": "bar",
        "bar_diameter": 19,
        "wall_thickness": 1.5,
        "bar_lengths": [1000, 1500, 2000, 3000],
        "dimensions": {"outer_size": 19, "inner_size": 16},
        "product_codes": [
            # 1000 mm
            {"code": "ST19-1000B", "material": "S/S 304", "finish": "Bright Polished",
             "bar_length": 1000},
            {"code": "STA19-1000MB", "material": "Aluminium", "finish": "Matte Black",
             "bar_length": 1000},
            # 1500 mm
            {"code": "ST19-1500B", "material": "S/S 304", "finish": "Bright Polished",
             "bar_length": 1500},
            {"code": "STA19-1500MB", "material": "Aluminium", "finish": "Matte Black",
             "bar_length": 1500},
            # 2000 mm
            {"code": "ST19-2000B", "material": "S/S 304", "finish": "Bright Polished",
             "bar_length": 2000},
            {"code": "STA19-2000MB", "material": "Aluminium", "finish": "Matte Black",
             "bar_length": 2000},
            # 3000 mm
            {"code": "ST19-3000B", "material": "S/S 304", "finish": "Bright Polished",
             "bar_length": 3000},
            {"code": "STA19-3000MB", "material": "Aluminium", "finish": "Matte Black",
             "bar_length": 3000},
        ],
    },
}

# ---------------------------------------------------------------------------
# Seal specifications — re-exported from SealSpecs for backward compatibility
# ---------------------------------------------------------------------------
from freecad.ShowerDesigner.Data.SealSpecs import (  # noqa: F401, E402
    SEAL_COLOURS,
    SEAL_MATERIALS,
    SEAL_SPECS,
    CATALOGUE_SEAL_SPECS,
    selectSeal,
    getSealsByCategory,
    getSealsByAngle,
    getSealsByLocation,
    lookupSealProductCode,
)

# ---------------------------------------------------------------------------
# Clamp specifications
# ---------------------------------------------------------------------------
CLAMP_SPECS = {
    "U_Clamp": {
        "load_capacity_kg": 45,
        "glass_thickness_range": [6, 8, 10, 12],
        "default_mounting": "Floor",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 10,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 45, "depth": 19, "height": 45},
        "product_codes": [
            {"code": "GC-401", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "GC-491", "material": "S/S 304", "finish": "Matte Black"},
            {"code": "GC-481", "material": "S/S 304", "finish": "Antique Brass"},
        ],
    },
    "L_Clamp": {
        "load_capacity_kg": 45,
        "glass_thickness_range": [6, 8, 10, 12],
        "default_mounting": "Wall",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 10,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 45, "depth": 60, "height": 45},
        "product_codes": [
            {"code": "GC-402", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "GC-492", "material": "S/S 304", "finish": "Matte Black"},
            {"code": "GC-482", "material": "S/S 304", "finish": "Antique Brass"},
        ],
    },
    "180DEG_Clamp": {
        "load_capacity_kg": 45,
        "glass_thickness_range": [6, 8, 10, 12],
        "default_mounting": "Floor",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 10,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 45, "depth": 19, "height": 90},
        "product_codes": [
            {"code": "GC-403", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "GC-483", "material": "S/S 304", "finish": "Antique Brass"},
            {"code": "GC-493", "material": "S/S 304", "finish": "Matte Black"},
        ],
    },
    "135DEG_G2G_Clamp": {
        "load_capacity_kg": 45,
        "glass_thickness_range": [6, 8, 10, 12],
        "default_mounting": "Floor",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 8,
            "cutout_depth": 24,
            "cutout_radius": 10,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 45, "depth": 50, "height": 77},
        "product_codes": [
            {"code": "GC-405", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "GC-495", "material": "S/S 304", "finish": "Matte Black"},
            {"code": "GC-485", "material": "S/S 304", "finish": "Antique Brass"},
        ],
    },
    "90DEG_G2G_Clamp": {
        "load_capacity_kg": 45,
        "glass_thickness_range": [6, 8, 10, 12],
        "default_mounting": "Floor",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 8,
            "cutout_depth": 24,
            "cutout_radius": 10,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 45, "depth": 45, "height": 45},
        "product_codes": [
            {"code": "GC-404", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "GC-494", "material": "S/S 304", "finish": "Matte Black"},
            {"code": "GC-484", "material": "S/S 304", "finish": "Antique Brass"},
        ],
    },
    "180DEG_G2G_Clamp": {
        "load_capacity_kg": 45,
        "glass_thickness_range": [6, 8, 10, 12],
        "default_mounting": "Floor",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 8,
            "cutout_depth": 24,
            "cutout_radius": 10,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 45, "depth": 19, "height": 90},
        "product_codes": [
            {"code": "GC-406", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "GC-496", "material": "S/S 304", "finish": "Matte Black"},
            {"code": "GC-486", "material": "S/S 304", "finish": "Antique Brass"},
        ],
    },
    "90DEG_Tee_Clamp": {
        "load_capacity_kg": 45,
        "glass_thickness_range": [6, 8, 10, 12],
        "default_mounting": "Floor",
        "dimensions": {
            "base_size": 45,
            "inline_plate" : 101,
            "base_thickness": 4.5,
            "glass_gap": 8,
            "cutout_depth": 22,
            "inline_cutout" : 56,
            "cutout_radius": 10,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 90, "depth": 45, "height": 45},
        "product_codes": [
            {"code": "GC-407", "material": "S/S 304", "finish": "Bright Polished"},
            {"code": "GC-487", "material": "S/S 304", "finish": "Antique Brass"},
            {"code": "GC-497", "material": "S/S 304", "finish": "Matte Black"},
        ],
    },
}

# ---------------------------------------------------------------------------
# Bevel clamp specifications — from Showers-Ex-Sliding-Catalogue, pp. 12–15
# ---------------------------------------------------------------------------

BEVEL_CLAMP_SPECS = {
    # ------------------------------------------------------------------
    # Wall to Glass — S/S 304 (45 mm body, R9)
    # ------------------------------------------------------------------
    "bevel_90_u_clamp_w2g": {
        "name": "Bevel 90° (U-Clamp) Wall to Glass Single Fix Clamp",
        "mounting_type": "Wall-to-Glass",
        "angle": 90,
        "clamp_shape": "U_Clamp",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 9,
            "chamfer_size": 3,
            "wall_gap": 5,
        },
        "bounding_box": {"width": 45, "depth": 19, "height": 45},
        "product_codes": [
            {"code": "GC-401", "material": "S/S 304", "finish": "Bright Polished",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-491", "material": "S/S 304", "finish": "Matte Black",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-481", "material": "S/S 304", "finish": "Antique Brass",
             "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
    "bevel_90_l_clamp_w2g": {
        "name": "Bevel 90° (L-Clamp) Wall to Glass Clamp",
        "mounting_type": "Wall-to-Glass",
        "angle": 90,
        "clamp_shape": "L_Clamp",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 9,
            "chamfer_size": 3,
            "wall_gap": 5,
        },
        "bounding_box": {"width": 45, "depth": 60, "height": 45},
        "product_codes": [
            {"code": "GC-402", "material": "S/S 304", "finish": "Bright Polished",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-492", "material": "S/S 304", "finish": "Matte Black",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-482", "material": "S/S 304", "finish": "Antique Brass",
             "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
    "bevel_180_w2g": {
        "name": "Bevel 180° Wall to Glass Clamp",
        "mounting_type": "Wall-to-Glass",
        "angle": 180,
        "clamp_shape": "180DEG_Clamp",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 9,
            "chamfer_size": 3,
            "wall_gap": 5,
        },
        "bounding_box": {"width": 45, "depth": 19, "height": 101},
        "product_codes": [
            {"code": "GC-403", "material": "S/S 304", "finish": "Bright Polished",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-483", "material": "S/S 304", "finish": "Antique Brass",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-493", "material": "S/S 304", "finish": "Matte Black",
             "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
    # ------------------------------------------------------------------
    # Glass to Glass — S/S 304 (45 mm body, R9)
    # ------------------------------------------------------------------
    "bevel_90_g2g": {
        "name": "Bevel 90° Glass to Glass Clamp",
        "mounting_type": "Glass-to-Glass",
        "angle": 90,
        "clamp_shape": "90DEG_G2G_Clamp",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 9,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 45, "depth": 45, "height": 45},
        "product_codes": [
            {"code": "GC-404", "material": "S/S 304", "finish": "Bright Polished",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-494", "material": "S/S 304", "finish": "Matte Black",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-484", "material": "S/S 304", "finish": "Antique Brass",
             "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
    "bevel_135_g2g": {
        "name": "Bevel 135° Glass to Glass Clamp",
        "mounting_type": "Glass-to-Glass",
        "angle": 135,
        "clamp_shape": "135DEG_G2G_Clamp",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 9,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 45, "depth": 50, "height": 77},
        "product_codes": [
            {"code": "GC-405", "material": "S/S 304", "finish": "Bright Polished",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-495", "material": "S/S 304", "finish": "Matte Black",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-485", "material": "S/S 304", "finish": "Antique Brass",
             "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
    "bevel_180_g2g": {
        "name": "Bevel 180° Glass to Glass Clamp",
        "mounting_type": "Glass-to-Glass",
        "angle": 180,
        "clamp_shape": "180DEG_G2G_Clamp",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 9,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 45, "depth": 19, "height": 90},
        "product_codes": [
            {"code": "GC-406", "material": "S/S 304", "finish": "Bright Polished",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-496", "material": "S/S 304", "finish": "Matte Black",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-486", "material": "S/S 304", "finish": "Antique Brass",
             "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
    "bevel_90_g2g_tee": {
        "name": "Bevel 90° Glass to Glass Tee Clamp",
        "mounting_type": "Glass-to-Glass",
        "angle": 90,
        "clamp_shape": "90DEG_Tee_Clamp",
        "dimensions": {
            "base_size": 45,
            "base_thickness": 4.5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 9,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 90, "depth": 45, "height": 45},
        "product_codes": [
            {"code": "GC-407", "material": "S/S 304", "finish": "Bright Polished",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-487", "material": "S/S 304", "finish": "Antique Brass",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-497", "material": "S/S 304", "finish": "Matte Black",
             "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
    # ------------------------------------------------------------------
    # Wall to Glass — Brass (50 mm body, R10)
    # ------------------------------------------------------------------
    "bevel_90_u_clamp_w2g_brass": {
        "name": "Bevel 90° (U-Clamp) Wall to Glass Single Fix Clamp (Brass)",
        "mounting_type": "Wall-to-Glass",
        "angle": 90,
        "clamp_shape": "U_Clamp",
        "dimensions": {
            "base_size": 50,
            "base_thickness": 5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 10,
            "chamfer_size": 3,
            "wall_gap": 5,
        },
        "bounding_box": {"width": 50, "depth": 20, "height": 50},
        "product_codes": [
            {"code": "GC-701", "material": "Brass", "finish": "Bright Chrome",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-711", "material": "Brass", "finish": "Satin Chrome",
             "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
    "bevel_90_l_clamp_w2g_brass": {
        "name": "Bevel 90° (L-Clamp) Wall to Glass Clamp (Brass)",
        "mounting_type": "Wall-to-Glass",
        "angle": 90,
        "clamp_shape": "L_Clamp",
        "dimensions": {
            "base_size": 50,
            "base_thickness": 5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 10,
            "chamfer_size": 3,
            "wall_gap": 5,
        },
        "bounding_box": {"width": 50, "depth": 65, "height": 50},
        "product_codes": [
            {"code": "GC-702", "material": "Brass", "finish": "Bright Chrome",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-712", "material": "Brass", "finish": "Satin Chrome",
             "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
    "bevel_180_w2g_brass": {
        "name": "Bevel 180° Wall to Glass Clamp (Brass)",
        "mounting_type": "Wall-to-Glass",
        "angle": 180,
        "clamp_shape": "180DEG_Clamp",
        "dimensions": {
            "base_size": 50,
            "base_thickness": 5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 10,
            "chamfer_size": 3,
            "wall_gap": 5,
        },
        "bounding_box": {"width": 50, "depth": 20, "height": 101},
        "product_codes": [
            {"code": "GC-703", "material": "Brass", "finish": "Bright Chrome",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-713", "material": "Brass", "finish": "Satin Chrome",
             "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
    # ------------------------------------------------------------------
    # Glass to Glass — Brass (50 mm body, R10)
    # ------------------------------------------------------------------
    "bevel_90_g2g_brass": {
        "name": "Bevel 90° Glass to Glass Clamp (Brass)",
        "mounting_type": "Glass-to-Glass",
        "angle": 90,
        "clamp_shape": "90DEG_G2G_Clamp",
        "dimensions": {
            "base_size": 50,
            "base_thickness": 5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 10,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 50, "depth": 50, "height": 50},
        "product_codes": [
            {"code": "GC-704", "material": "Brass", "finish": "Bright Chrome",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-714", "material": "Brass", "finish": "Satin Chrome",
             "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
    "bevel_135_g2g_brass": {
        "name": "Bevel 135° Glass to Glass Clamp (Brass)",
        "mounting_type": "Glass-to-Glass",
        "angle": 135,
        "clamp_shape": "135DEG_G2G_Clamp",
        "dimensions": {
            "base_size": 50,
            "base_thickness": 5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 10,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 50, "depth": 54, "height": 85},
        "product_codes": [
            {"code": "GC-705", "material": "Brass", "finish": "Bright Chrome",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-715", "material": "Brass", "finish": "Satin Chrome",
             "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
    "bevel_180_g2g_brass": {
        "name": "Bevel 180° Glass to Glass Clamp (Brass)",
        "mounting_type": "Glass-to-Glass",
        "angle": 180,
        "clamp_shape": "180DEG_G2G_Clamp",
        "dimensions": {
            "base_size": 50,
            "base_thickness": 5,
            "glass_gap": 8,
            "cutout_depth": 20,
            "cutout_radius": 10,
            "chamfer_size": 3,
        },
        "bounding_box": {"width": 50, "depth": 20, "height": 100},
        "product_codes": [
            {"code": "GC-706", "material": "Brass", "finish": "Bright Chrome",
             "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "GC-716", "material": "Brass", "finish": "Satin Chrome",
             "glass_thickness_range": [6, 8, 10, 12]},
        ],
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
# Glass edge deductions by hardware type (mm per edge)
# ---------------------------------------------------------------------------
GLASS_DEDUCTIONS = {
    "wall_clamp": 5,   # Wall-to-glass clamp
    "g2g_clamp": 2,    # Glass-to-glass clamp
    "channel": 6,       # Wall or floor channel
    "sill_plate": 18,    # Door sill plate under door
    "no_sill_plate": 8,  # No Door sill under door
    "bevel_90_wall_to_glass_full": 10,
    "bevel_90_wall_to_glass_half": 10,
    "bevel_135_wall_to_glass": 17,
    "bevel_90_glass_to_glass": 10,
    "bevel_135_glass_to_glass_unequal": 11,
    "bevel_135_glass_to_glass_equal": 11,
    "bevel_180_glass_to_glass": 5,
    "bevel_360_wall_pivot": 15,
    "bevel_360_glass_pivot": 9,
    "bevel_90_tee": 10,
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

# ---------------------------------------------------------------------------
# Floor guide specifications (shared across all slider systems)
# ---------------------------------------------------------------------------
FLOOR_GUIDE_SPECS = {
    "code": "SL-0099P",
    "width": 30,    # mm
    "height": 23,   # mm
    "length": 50,   # mm
    "depth": 19,    # mm
}

# ---------------------------------------------------------------------------
# Slider system specifications — from Showers-Catalogue-Including-Sliders
# ---------------------------------------------------------------------------

SLIDER_FINISHES = ["Bright Polished", "Matte Black", "Natural"]

SLIDER_SYSTEM_SPECS = {
    # ------------------------------------------------------------------
    # 1. Duplo — Double tube support bar system
    # ------------------------------------------------------------------
    "duplo": {
        "name": "Duplo Double Tube Slider System",
        "max_door_width": 750,
        "max_weight_kg": 27,
        "fixed_door_clearance": 13,
        "fixed_door_overlap": 50,
        "door_glass_thickness": [6],
        "fixed_glass_thickness": [6, 8],
        "dimensions": {
            "tube_diameter": 19,
            "tube_length_stock": 2000,
            "tube_spacing_ctc": 46,
            "door_fixed_height_diff": 88,
            "lower_tube_to_fixed_panel": 24,
            "fixed_panel_to_door_clearance": 13,
            "fixed_panel_floor_deduction": 5,
            "door_panel_floor_clearance": 12,
            "door_fixed_overlap": 50,
            "door_wheel_hole_diameter": 12,
            "door_wheel_hole_from_top": 42,
            "door_wheel_hole_from_handle_side": 43,
            "door_wheel_hole_from_fixed_side": 20,
            "return_panel_width_deduction": 25,
            "return_panel_tube_hole_diameter": 12,
            "return_panel_tube_hole_from_front": 25,
            "return_panel_tube_hole_from_top": 20,
            "roller_wheel_diameter": 25,
            "roller_wheel_width": 26,
            "wall_flange_projection": 10,
        },
        "components": {
            "tube":         {"code": "SB19-2000B", "qty_per_system": 2},
            "wall_flange":  {"code": "DP-FLW",     "qty_per_system": 4},
            "wall_plate":   {"code": "DP-FPL",     "qty_per_system": 2},
            "roller_wheel": {"code": "DP-RWH",     "qty_per_system": 2},
            "tube_support": {"code": "DP-TSGP",    "qty_per_system": 1},
            "floor_guide":  {"code": "SL-0099P",   "qty_per_system": 1},
        },
        "product_codes": [
            {"code": "SB19-2000B", "material": "S/S 304",
             "finish": "Bright Polished"},
        ],
    },

    # ------------------------------------------------------------------
    # 2. Edge Slider — Rectangular tube track system
    # ------------------------------------------------------------------
    "edge_slider": {
        "name": "Edge Slider System",
        "max_door_width": 850,
        "max_weight_kg": 45,
        "fixed_door_clearance": 26,
        "fixed_door_overlap": 50,
        "door_glass_thickness": [6, 8],
        "fixed_glass_thickness": [8, 10],
        "adjustable_height": True,
        "dimensions": {
            "track_width": 10,
            "track_height": 30,
            "track_length_stock": 2000,
            "wall_flange_projection": 30,
            "wheel_center_from_top": 60,
            "wheel_ctc_to_antilift": 60,
            "track_center_from_top": 90,
            "door_floor_clearance": 12,
            "fixed_panel_floor_deduction": 5,
            "fixed_panel_door_clearance": 26,
            "door_fixed_overlap": 50,
            "track_to_fixed_hole_diameter": 12,
            "track_to_fixed_hole_from_top": 90,
            "track_to_fixed_hole_from_side": 60,
            "door_wheel_hole_diameter": 16,
            "door_wheel_antilift_from_side": 80,
            "door_antilift_hole_diameter": 10,
            "return_panel_track_hole_diameter": 10,
            "return_panel_track_hole_from_top": 90,
            "return_panel_track_hole_from_front": 18,
            "roller_wheel_diameter": 30,
        },
        "components": {
            "slider_track":          {"code": "RST-2000B", "qty_per_system": 1},
            "roller_wheel":          {"code": "EDS-RWH",   "qty_per_system": 2},
            "anti_lift_pin":         {"code": "EDS-ALP",   "qty_per_system": 2},
            "door_stop":             {"code": "EDS-DS",    "qty_per_system": 2},
            "wall_flange":           {"code": "EDS-WFL",   "qty_per_system": 2},
            "glass_connector_clamp": {"code": "EDS-GCC",   "qty_per_system": 2},
            "floor_guide":           {"code": "SL-0099P",  "qty_per_system": 1},
        },
        "product_codes": [
            {"code": "RST-2000B", "material": "S/S 304",
             "finish": "Bright Polished"},
            {"code": "RST-2000MB", "material": "S/S 304",
             "finish": "Matte Black"},
        ],
    },

    # ------------------------------------------------------------------
    # 3. City Slider — Track + fixed adapter system
    # ------------------------------------------------------------------
    "city_slider": {
        "name": "City Slider System",
        "max_door_width": 900,
        "max_weight_kg": 90,
        "fixed_door_clearance": 16,
        "fixed_door_overlap": 50,
        "door_glass_thickness": [6, 8, 10],
        "fixed_glass_thickness": [6, 8],
        "has_fixed_adapter": True,
        "corner_slider_capable": True,
        "mounting_options": ["inline", "corner", "ceiling", "wall"],
        "dimensions": {
            "track_width": 55,
            "track_height": 50,
            "track_length_stock": 2000,
            "fixed_adapter_length_stock": 2000,
            "track_center_from_top": 25,
            "wheel_center_from_top": 25,
            "wall_flange_projection": 30,
            "roller_wheel_diameter": 24,
            "fixing_deduction_top": 26,
            "door_top_deduction_hd": 54,
            "door_top_deduction_clip": 56,
            "door_bottom_deduction": 10,
            "glass_cutout_depth_hd": 24,
            "glass_cutout_depth_clip": 26,
            "fixed_door_clearance_hd": 16,
            "fixed_door_clearance_clip": 12,
            "door_runner_hole_diameter": 14,
            "door_runner_hole_from_sides": 100,
            "mounting_hole_spacing": 100,
        },
        "roller_variants": {
            "clip_in":    {"code": "CSL-RWH",    "glass_cutout_depth": 26,
                           "door_top_deduction": 56, "fixed_door_clearance": 12,
                           "max_weight_kg": 45, "door_glass_thickness": [6, 8]},
            "heavy_duty": {"code": "CSL-RWH-HD", "glass_cutout_depth": 24,
                           "door_top_deduction": 54, "fixed_door_clearance": 16,
                           "max_weight_kg": 90, "door_glass_thickness": [8, 10]},
        },
        "components": {
            "slider_track":  {"code": "CSLT-2000B", "qty_per_system": 1},
            "fixed_adapter": {"code": "CSLF-2000B", "qty_per_system": 1},
            "roller_wheel":  {"code": "CSL-RWH",    "qty_per_system": 2,
                              "variant_hd": "CSL-RWH-HD"},
            "door_stopper":  {"code": "CSL-DBC",    "qty_per_system": 2},
            "floor_guide":   {"code": "SL-0099P",   "qty_per_system": 1},
        },
        "product_codes": [
            {"code": "CSLT-2000B", "material": "S/S 304",
             "finish": "Bright Polished"},
            {"code": "CSLT-2000MB", "material": "S/S 304",
             "finish": "Matte Black"},
            {"code": "CSLF-2000B", "material": "Aluminium",
             "finish": "Natural"},
        ],
    },
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


def isGlassToGlassClamp(clamp_type):
    """Return True if the clamp type is a glass-to-glass variant.

    Glass-to-glass clamp keys contain 'G2G' or 'Tee' in their name.
    Everything else (U_Clamp, L_Clamp, 180DEG_Clamp) is wall-to-glass.
    """
    return "G2G" in clamp_type or "Tee" in clamp_type


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


def getHandleModelsForCategory(category):
    """
    Return catalogue handle model keys matching a legacy handle category.

    Args:
        category: Legacy HANDLE_SPECS key ("Knob", "Bar", "Pull", "Towel_Bar")
                  or extended category ("Flush", "Custom_Kit")

    Returns:
        list[str]: Matching keys from CATALOGUE_HANDLE_SPECS
    """
    return [
        key for key, spec in CATALOGUE_HANDLE_SPECS.items()
        if spec["category"] == category
    ]


def lookupHandleProductCode(code):
    """
    Find the catalogue entry and variant for a product code.

    Args:
        code: Product code string (e.g. "DK-201", "BH-040")

    Returns:
        tuple: (handle_key, product_code_dict) or (None, None)
    """
    for key, spec in CATALOGUE_HANDLE_SPECS.items():
        for pc in spec["product_codes"]:
            if pc["code"] == code:
                return key, pc
    return None, None


def getStabilisersByProfile(profile_shape):
    """
    Return catalogue stabiliser keys matching a profile shape.

    Args:
        profile_shape: "round" or "square"

    Returns:
        list[str]: Matching keys from CATALOGUE_STABILISER_SPECS
    """
    return [
        key for key, spec in CATALOGUE_STABILISER_SPECS.items()
        if spec["profile_shape"] == profile_shape
    ]


def getStabilisersByRole(connector_role):
    """
    Return catalogue stabiliser keys matching a connector role.

    Args:
        connector_role: e.g. "wall_flange", "tee_coupler", "glass_mount_straight"

    Returns:
        list[str]: Matching keys from CATALOGUE_STABILISER_SPECS (connectors only)
    """
    return [
        key for key, spec in CATALOGUE_STABILISER_SPECS.items()
        if spec["component_type"] == "connector"
        and spec.get("connector_role") == connector_role
    ]


def lookupStabiliserProductCode(code):
    """
    Find the catalogue entry and variant for a stabiliser product code.

    Args:
        code: Product code string (e.g. "KA-101-19", "SB19-2000B")

    Returns:
        tuple: (stabiliser_key, product_code_dict) or (None, None)
    """
    for key, spec in CATALOGUE_STABILISER_SPECS.items():
        for pc in spec["product_codes"]:
            if pc["code"] == code:
                return key, pc
    return None, None


def validateSliderSystem(system_key, door_width, door_weight, glass_thickness):
    """
    Validate that a slider system can support the given door configuration.

    Args:
        system_key: Key into SLIDER_SYSTEM_SPECS
        door_width: Door width in mm
        door_weight: Door weight in kg
        glass_thickness: Glass thickness in mm

    Returns:
        tuple: (is_valid, message)
    """
    if system_key not in SLIDER_SYSTEM_SPECS:
        return False, f"Unknown slider system: {system_key}"

    spec = SLIDER_SYSTEM_SPECS[system_key]

    if door_width > spec["max_door_width"]:
        return False, (
            f"Door width ({door_width}mm) exceeds {spec['name']} maximum "
            f"({spec['max_door_width']}mm)"
        )

    if door_weight > spec["max_weight_kg"]:
        return False, (
            f"Door weight ({door_weight:.1f}kg) exceeds {spec['name']} maximum "
            f"({spec['max_weight_kg']}kg)"
        )

    thickness = int(glass_thickness)
    if thickness not in spec["door_glass_thickness"]:
        return False, (
            f"Glass thickness ({thickness}mm) not supported by {spec['name']} "
            f"(supported: {spec['door_glass_thickness']})"
        )

    return True, f"{spec['name']} configuration OK"




def lookupSliderProductCode(code):
    """
    Find the slider system entry for a product code.

    Args:
        code: Product code string (e.g. "RST-2000B", "CSLT-2000B")

    Returns:
        tuple: (system_key, product_code_dict) or (None, None)
    """
    for key, spec in SLIDER_SYSTEM_SPECS.items():
        for pc in spec["product_codes"]:
            if pc["code"] == code:
                return key, pc
    return None, None
