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
# Hinge specifications
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

# Bi-fold hinge specs (moved from BiFoldDoor.py)
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

HINGE_PLACEMENT_DEFAULTS = {
    "offset_top": 300,       # mm from top edge
    "offset_bottom": 300,    # mm from bottom edge
    "weight_threshold_3_hinges": 45,  # kg — above this, use 3 hinges
}

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
        "load_capacity_kg": 100,
        "glass_thickness_range": [6, 8, 10, 12],
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
        "load_capacity_kg": 100,
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
        "glass_thickness_range": [6, 8, 10, 12],
        "default_mounting": "Floor",
        "dimensions": {},
        "bounding_box": {"width": 50, "depth": 33, "height": 50},
    },
    "135DEG_Clamp": {
        "load_capacity_kg": 45,
        "glass_thickness_range": [6, 8, 10, 12],
        "default_mounting": "Floor",
        "dimensions": {},
        "bounding_box": {"width": 50, "depth": 50, "height": 50},
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
        return [total_length / 2]
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
