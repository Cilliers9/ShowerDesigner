# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Seal specifications database for shower enclosures.

This module contains standardized specifications for all seal types:
soft lip, hard lip, bubble, magnetic, infill, and bottom seals.

Pure Python — no FreeCAD imports. Models import from here, never the reverse.
"""

# ---------------------------------------------------------------------------
# Seal specifications
# ---------------------------------------------------------------------------

# Available seal colours
SEAL_COLOURS = ["Clear", "Black", "White", "Brown"]

# Material codes:  PVC = flexible, PC = polycarbonate (rigid)
SEAL_MATERIALS = ["PVC", "PC"]

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
# Catalogue seal specs — from Showers-Ex-Sliding catalogue pp. 35-42
# ---------------------------------------------------------------------------
CATALOGUE_SEAL_SPECS = {
    # ------------------------------------------------------------------
    # Soft Lip Seals
    # ------------------------------------------------------------------
    "centre_lip": {
        "name": "Centre Lip Seal",
        "category": "soft_lip",
        "angle": 0,
        "location": "side",
        "dimensions": {
            "soft_lip_length": 12,
        },
        "material": "PVC",
        "product_codes": [
            {"code": "TSS-001-8", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500},
            {"code": "TSS-001-10", "glass_thickness": "8-10", "colour": "Clear",
             "length": 2500},
            {"code": "TUV-001-12", "glass_thickness": "10-12", "colour": "Clear",
             "length": 3000},
        ],
    },
    "180_soft_lip": {
        "name": "180\u00b0 Soft Lip Seal",
        "category": "soft_lip",
        "angle": 180,
        "location": "side",
        "dimensions": {
            "soft_lip_length": 16,  # 20mm for 10-12mm glass
        },
        "material": "PVC",
        "product_codes": [
            {"code": "TSS-003-6", "glass_thickness": "4-6", "colour": "Clear",
             "length": 2500},
            {"code": "TSS-003-8", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500},
            {"code": "BSS-003-8", "glass_thickness": "6-8", "colour": "Black",
             "length": 2500},
            {"code": "TSS-003-10", "glass_thickness": "8-10", "colour": "Clear",
             "length": 2500},
            {"code": "BSS-003-10", "glass_thickness": "8-10", "colour": "Black",
             "length": 2500},
            {"code": "TUV-003-12", "glass_thickness": "10-12", "colour": "Clear",
             "length": 3000},
            {"code": "BUV-003-12", "glass_thickness": "10-12", "colour": "Black",
             "length": 3000},
        ],
    },
    "180_long_lip": {
        "name": "180\u00b0 Long Lip Seal",
        "category": "soft_lip",
        "angle": 180,
        "location": "side",
        "dimensions": {
            "soft_lip_length": 22,
        },
        "material": "PVC",
        "product_codes": [
            {"code": "TSS-003-8-22", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500},
            {"code": "BSS-003-8-22", "glass_thickness": "6-8", "colour": "Black",
             "length": 2500},
            {"code": "TSS-003-10-22", "glass_thickness": "8-10", "colour": "Clear",
             "length": 2500},
            {"code": "BSS-003-10-22", "glass_thickness": "8-10", "colour": "Black",
             "length": 2500},
        ],
    },
    "90_soft_lip": {
        "name": "90\u00b0 Soft Lip Seal",
        "category": "soft_lip",
        "angle": 90,
        "location": "side",
        "dimensions": {
            "soft_lip_length": 8,
        },
        "material": "PVC",
        "product_codes": [
            {"code": "TSS-007-6", "glass_thickness": "4-6", "colour": "Clear",
             "length": 2500},
            {"code": "TSS-007-8", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500},
            {"code": "BSS-007-8", "glass_thickness": "6-8", "colour": "Black",
             "length": 2500},
            {"code": "TSS-007-10", "glass_thickness": "8-10", "colour": "Clear",
             "length": 2500},
            {"code": "BSS-007-10", "glass_thickness": "8-10", "colour": "Black",
             "length": 2500},
            {"code": "TUV-007-12", "glass_thickness": "10-12", "colour": "Clear",
             "length": 3000},
        ],
    },
    "135_soft_lip": {
        "name": "135\u00b0 Soft Lip Seal",
        "category": "soft_lip",
        "angle": 135,
        "location": "side",
        "dimensions": {
            "soft_lip_length": 16,
        },
        "material": "PVC",
        "product_codes": [
            {"code": "TSS-005-8", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500},
            {"code": "TSS-005-10", "glass_thickness": "8-10", "colour": "Clear",
             "length": 2500},
        ],
    },
    # ------------------------------------------------------------------
    # Bubble Seals
    # ------------------------------------------------------------------
    "bubble_seal": {
        "name": "Bubble Seal",
        "category": "bubble",
        "angle": 0,
        "location": "side",
        "dimensions": {
            "bubble_length": 8,  # standard; 12mm and 24mm variants exist
        },
        "material": "PVC",
        "product_codes": [
            {"code": "TSS-004-6", "glass_thickness": "4-6", "colour": "Clear",
             "length": 2500},
            {"code": "TSS-004-8", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500},
            {"code": "BSS-004-8", "glass_thickness": "6-8", "colour": "Black",
             "length": 2500},
            {"code": "TSS-004-8-12", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500},
            {"code": "TSS-004-8-24", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500},
            {"code": "BSS-004-8-24", "glass_thickness": "6-8", "colour": "Black",
             "length": 2500},
            {"code": "TSS-004-10", "glass_thickness": "8-10", "colour": "Clear",
             "length": 2500},
            {"code": "BSS-004-10", "glass_thickness": "8-10", "colour": "Black",
             "length": 2500},
        ],
    },
    # ------------------------------------------------------------------
    # Bottom Seals
    # ------------------------------------------------------------------
    "wipe_seal_bubble": {
        "name": "Wipe Seal with Bubble",
        "category": "bottom",
        "angle": 0,
        "location": "bottom",
        "dimensions": {
            "soft_lip_length": 11,
            "bubble_length": 8,
        },
        "material": "PVC",
        "product_codes": [
            {"code": "TSS-009-8", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500},
        ],
    },
    "drip_wipe_seal": {
        "name": "Drip & Wipe Seal",
        "category": "bottom",
        "angle": 0,
        "location": "bottom",
        "dimensions": {
            "hard_lip_length": 8,
            "soft_lip_length": 10,
        },
        "material": "PVC",  # PVC standard; PC variants exist
        "product_codes": [
            {"code": "TSS-009B1-6", "glass_thickness": "6", "colour": "Clear",
             "length": 2500, "material": "PVC"},
            {"code": "TSS-009B1-8", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500, "material": "PVC"},
            {"code": "BSS-009B1-8", "glass_thickness": "6-8", "colour": "Black",
             "length": 2500, "material": "PVC"},
            {"code": "TSS-009B1-10", "glass_thickness": "8-10", "colour": "Clear",
             "length": 2500, "material": "PVC"},
            {"code": "BSS-009B1-10", "glass_thickness": "8-10", "colour": "Black",
             "length": 2500, "material": "PVC"},
            {"code": "TSS-009B1-12", "glass_thickness": "10-12", "colour": "Clear",
             "length": 2500, "material": "PVC"},
            {"code": "BSS-009B1-12", "glass_thickness": "10-12", "colour": "Black",
             "length": 2500, "material": "PVC"},
            {"code": "PSS-009B1-8", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500, "material": "PC"},
            {"code": "PSS-009B1-10", "glass_thickness": "8-10", "colour": "Clear",
             "length": 2500, "material": "PC"},
        ],
    },
    # ------------------------------------------------------------------
    # Hard Lip Seals
    # ------------------------------------------------------------------
    "180_hard_lip": {
        "name": "180\u00b0 Hard Lip Seal",
        "category": "hard_lip",
        "angle": 180,
        "location": "side",
        "dimensions": {
            "hard_lip_length": 10,
            "soft_lip_length": 5,
        },
        "material": "PVC",  # PVC standard; PC variants exist
        "product_codes": [
            {"code": "TSS-003A-8", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500, "material": "PVC"},
            {"code": "BSS-003A-8", "glass_thickness": "6-8", "colour": "Black",
             "length": 2500, "material": "PVC"},
            {"code": "TSS-003A-10", "glass_thickness": "8-10", "colour": "Clear",
             "length": 2500, "material": "PVC"},
            {"code": "BSS-003A-10", "glass_thickness": "8-10", "colour": "Black",
             "length": 2500, "material": "PVC"},
            {"code": "TUV-003A-12", "glass_thickness": "10-12", "colour": "Clear",
             "length": 3000, "material": "PVC"},
            {"code": "PSS-003A-8", "glass_thickness": "8", "colour": "Clear",
             "length": 2500, "material": "PC"},
            {"code": "PUV-003A-10", "glass_thickness": "10", "colour": "Clear",
             "length": 3000, "material": "PC"},
        ],
    },
    "135_hard_lip": {
        "name": "135\u00b0 Hard Lip Seal",
        "category": "hard_lip",
        "angle": 135,
        "location": "side",
        "dimensions": {
            "hard_lip_length": 10,
            "soft_lip_length": 5,
        },
        "material": "PVC",
        "product_codes": [
            {"code": "TSS-005A-8", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500},
            {"code": "TSS-005A-10", "glass_thickness": "8-10", "colour": "Clear",
             "length": 2500},
        ],
    },
    "90_extended_hard_lip": {
        "name": "90\u00b0 Extended Hard Lip Seal",
        "category": "hard_lip",
        "angle": 90,
        "location": "side",
        "dimensions": {
            "hard_lip_length": 10,
            "soft_lip_length": 8,
        },
        "material": "PVC",
        "product_codes": [
            {"code": "TSS-011A-8", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500},
            {"code": "TSS-011A-10", "glass_thickness": "8-10", "colour": "Clear",
             "length": 2500},
        ],
    },
    "90_hard_lip": {
        "name": "90\u00b0 Hard Lip Seal",
        "category": "hard_lip",
        "angle": 90,
        "location": "side",
        "dimensions": {
            "hard_lip_length": 10,
            "soft_lip_length": 10,
        },
        "material": "PVC",
        "product_codes": [
            {"code": "TSS-011C-8", "glass_thickness": "6-8", "colour": "Clear",
             "length": 2500},
            {"code": "TSS-011C-10", "glass_thickness": "8-10", "colour": "Clear",
             "length": 2500},
        ],
    },
    "90_hard_soft_lip": {
        "name": "90\u00b0 Hard/Soft Lip Seal",
        "category": "hard_lip",
        "angle": 90,
        "location": "side",
        "dimensions": {
            "hard_lip_length": 10,
            "soft_lip_length": 14,
        },
        "material": "PVC",
        "product_codes": [
            {"code": "BSS-004A-8", "glass_thickness": "6-8", "colour": "Black",
             "length": 2500},
            {"code": "TUV-04A-12", "glass_thickness": "10-12", "colour": "Clear",
             "length": 3000},
        ],
    },
    "double_hard_lip_h": {
        "name": "Double Hard Lip Seal (H)",
        "category": "hard_lip",
        "angle": 180,
        "location": "side",
        "dimensions": {
            "hard_lip_length": 8,
        },
        "material": "PC",
        "product_codes": [
            {"code": "TUV-010-8", "glass_thickness": "8", "colour": "Clear",
             "length": 3000},
            {"code": "TUV-010-10", "glass_thickness": "10", "colour": "Clear",
             "length": 3000},
            {"code": "TUV-010-12", "glass_thickness": "12", "colour": "Clear",
             "length": 3000},
        ],
    },
    # ------------------------------------------------------------------
    # Magnetic Seals
    # ------------------------------------------------------------------
    "90_180_magnetic": {
        "name": "90\u00b0/180\u00b0 Magnetic Seal",
        "category": "magnetic",
        "angle": 90,  # works at 90 and 180
        "location": "door",
        "dimensions": {
            "magnet_lip_length": 12,
            "inside_measurement": 10,   # based on 8mm glass
            "outside_measurement": 18,  # based on 8mm glass
        },
        "material": "PVC",  # PVC standard; PC variants exist
        "product_codes": [
            {"code": "TSS-008A-8", "glass_thickness": "6-8", "colour": "White",
             "length": 2500, "material": "PVC"},
            {"code": "SM090-08B", "glass_thickness": "6-8", "colour": "Brown",
             "length": 2500, "material": "PVC"},
            {"code": "BSS-008A-8", "glass_thickness": "6-8", "colour": "Black",
             "length": 2500, "material": "PVC"},
            {"code": "TSS-008A-10", "glass_thickness": "8-10", "colour": "White",
             "length": 2500, "material": "PVC"},
            {"code": "SM090-10B", "glass_thickness": "8-10", "colour": "Brown",
             "length": 2500, "material": "PVC"},
            {"code": "BSS-008A-10", "glass_thickness": "8-10", "colour": "Black",
             "length": 2500, "material": "PVC"},
            {"code": "TUV-008A-12", "glass_thickness": "10-12", "colour": "White",
             "length": 3000, "material": "PVC"},
            {"code": "SM090-12B", "glass_thickness": "10-12", "colour": "Brown",
             "length": 3000, "material": "PVC"},
            {"code": "BUV-008A-12", "glass_thickness": "10-12", "colour": "Black",
             "length": 3000, "material": "PVC"},
            {"code": "PSS-008A-8", "glass_thickness": "8", "colour": "White",
             "length": 2500, "material": "PC"},
            {"code": "PUV-008A-10", "glass_thickness": "10", "colour": "White",
             "length": 3000, "material": "PC"},
        ],
    },
    "180_flat_magnetic": {
        "name": "180\u00b0 Flat Magnetic Seal",
        "category": "magnetic",
        "angle": 180,
        "location": "door",
        "dimensions": {
            "magnet_lip_length": 12,
        },
        "material": "PVC",
        "product_codes": [
            {"code": "TSS-008B-8", "glass_thickness": "6-8", "colour": "White",
             "length": 2500},
            {"code": "SM180-08B", "glass_thickness": "6-8", "colour": "Brown",
             "length": 2500},
            {"code": "TSS-008B-10", "glass_thickness": "8-10", "colour": "White",
             "length": 2500},
            {"code": "SM180-10B", "glass_thickness": "8-10", "colour": "Brown",
             "length": 2500},
        ],
    },
    "135_magnetic": {
        "name": "135\u00b0 Magnetic Seal",
        "category": "magnetic",
        "angle": 135,
        "location": "door",
        "dimensions": {
            "magnet_lip_length": 12,
        },
        "material": "PVC",
        "product_codes": [
            {"code": "TSS-008C-8", "glass_thickness": "6-8", "colour": "White",
             "length": 2500},
            {"code": "SM135-08B", "glass_thickness": "6-8", "colour": "Brown",
             "length": 2500},
            {"code": "TSS-008C-10", "glass_thickness": "8-10", "colour": "White",
             "length": 2500},
            {"code": "SM135-10B", "glass_thickness": "8-10", "colour": "Brown",
             "length": 2500},
        ],
    },
    # ------------------------------------------------------------------
    # Infill Seals
    # ------------------------------------------------------------------
    "180_g2g_infill": {
        "name": "180\u00b0 Glass to Glass Infill Seal",
        "category": "infill",
        "angle": 180,
        "location": "side",
        "dimensions": {
            "inside_measurement": 8,    # based on 8mm glass
            "outside_measurement": 18,  # based on 8mm glass
        },
        "material": "PC",
        "product_codes": [
            {"code": "IS-180-6", "glass_thickness": "6", "colour": "Clear",
             "length": 3000},
            {"code": "IS-180-10", "glass_thickness": "10", "colour": "Clear",
             "length": 3000},
            {"code": "IS-180-12", "glass_thickness": "12", "colour": "Clear",
             "length": 3000},
        ],
    },
}


# ---------------------------------------------------------------------------
# Seal helper functions
# ---------------------------------------------------------------------------

def selectSeal(location, glass_thickness, gap):
    """
    Select the appropriate seal type (legacy).

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


def getSealsByCategory(category):
    """
    Return catalogue seal keys matching a category.

    Args:
        category: "soft_lip", "bubble", "bottom", "hard_lip", "magnetic",
                  or "infill"

    Returns:
        list[str]: Matching keys from CATALOGUE_SEAL_SPECS
    """
    return [
        key for key, spec in CATALOGUE_SEAL_SPECS.items()
        if spec["category"] == category
    ]


def getSealsByAngle(angle):
    """
    Return catalogue seal keys matching an angle.

    Args:
        angle: Joint angle in degrees (0, 90, 135, 180)

    Returns:
        list[str]: Matching keys from CATALOGUE_SEAL_SPECS
    """
    return [
        key for key, spec in CATALOGUE_SEAL_SPECS.items()
        if spec["angle"] == angle
    ]


def getSealsByLocation(location):
    """
    Return catalogue seal keys matching a location.

    Args:
        location: "side", "bottom", or "door"

    Returns:
        list[str]: Matching keys from CATALOGUE_SEAL_SPECS
    """
    return [
        key for key, spec in CATALOGUE_SEAL_SPECS.items()
        if spec["location"] == location
    ]


def lookupSealProductCode(code):
    """
    Find the catalogue seal entry for a product code.

    Args:
        code: Product code string (e.g. "TSS-003-8", "PSS-008A-8")

    Returns:
        tuple: (seal_key, product_code_dict) or (None, None)
    """
    for key, spec in CATALOGUE_SEAL_SPECS.items():
        for pc in spec["product_codes"]:
            if pc["code"] == code:
                return key, pc
    return None, None
