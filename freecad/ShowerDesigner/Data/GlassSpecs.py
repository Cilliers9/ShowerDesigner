# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Glass specifications database for shower enclosures.

This module contains standardized specifications for different glass types,
thicknesses, and their properties.
"""

# Glass thickness specifications
GLASS_SPECS = {
    "6mm": {
        "weight_kg_m2": 15,
        "min_panel_size": 300,  # mm
        "max_panel_size": 2400,  # mm
        "typical_use": "Light-duty applications, small panels"
    },
    "8mm": {
        "weight_kg_m2": 20,
        "min_panel_size": 300,
        "max_panel_size": 3200,
        "typical_use": "Standard shower enclosures"
    },
    "10mm": {
        "weight_kg_m2": 25,
        "min_panel_size": 400,
        "max_panel_size": 4000,
        "typical_use": "Frameless enclosures, heavy-duty applications"
    },
    "12mm": {
        "weight_kg_m2": 30,
        "min_panel_size": 400,
        "max_panel_size": 4000,
        "typical_use": "Extra-large frameless panels, luxury applications"
    }
}

# Glass type specifications with visual properties
GLASS_TYPES = {
    "Clear": {
        "light_transmission": 0.90,
        "opacity": 0.2,
        "color": (0.7, 0.9, 1.0),  # RGB values (0-1)
        "description": "Standard clear glass, high transparency"
    },
    "Frosted": {
        "light_transmission": 0.75,
        "opacity": 0.8,
        "color": (0.7, 0.9, 1.0),
        "description": "Etched or sandblasted for privacy"
    },
    "Bronze": {
        "light_transmission": 0.60,
        "opacity": 0.3,
        "color": (0.804, 0.498, 0.196),  # Bronze color
        "description": "Tinted bronze glass"
    },
    "Grey": {
        "light_transmission": 0.60,
        "opacity": 0.3,
        "color": (0.25, 0.25, 0.25),  # Grey color
        "description": "Tinted grey glass"
    },
    "Reeded": {
        "light_transmission": 0.70,
        "opacity": 0.6,
        "color": (0.7, 0.9, 1.0),
        "description": "Textured vertical pattern for privacy"
    },
    "Low-Iron": {
        "light_transmission": 0.92,
        "opacity": 0.0,
        "color": (1.0, 1.0, 1.0),  # Pure white
        "description": "Ultra-clear glass with minimal green tint"
    }
}

# Edge finish specifications
EDGE_FINISHES = {
    "Bright_Polish": {
        "description": "Highly polished, mirror-like finish",
        "typical_use": "Premium frameless enclosures"
    },
    "Dull_Polish": {
        "description": "Smooth but not mirror-polished",
        "typical_use": "Standard applications, semi-frameless"
    }
}

# Tempering type specifications
TEMPER_TYPES = {
    "Tempered": {
        "description": "Heat-treated for safety, shatters into small pieces",
        "strength_multiplier": 4,  # vs annealed glass
        "required_for_shower": True
    },
    "Laminated": {
        "description": "Two glass layers with plastic interlayer",
        "strength_multiplier": 1,
        "required_for_shower": False,
        "extra_thickness": 0.28  # mm (typical PVB interlayer)
    },
    "None": {
        "description": "Annealed glass (not recommended for showers)",
        "strength_multiplier": 1,
        "required_for_shower": False
    }
}


def validateGlassThickness(thickness_mm):
    """
    Validate if a glass thickness is standard.

    Args:
        thickness_mm: Thickness in millimeters

    Returns:
        tuple: (is_valid, message)
    """
    thickness_key = f"{int(thickness_mm)}mm"
    if thickness_key in GLASS_SPECS:
        return True, f"Valid thickness: {thickness_key}"
    else:
        valid_thicknesses = ", ".join(GLASS_SPECS.keys())
        return False, f"Non-standard thickness. Standard options: {valid_thicknesses}"


def validatePanelSize(width_mm, height_mm, thickness_mm):
    """
    Validate if panel dimensions are within acceptable range for given thickness.

    Args:
        width_mm: Panel width in millimeters
        height_mm: Panel height in millimeters
        thickness_mm: Glass thickness in millimeters

    Returns:
        tuple: (is_valid, message)
    """
    thickness_key = f"{int(thickness_mm)}mm"

    if thickness_key not in GLASS_SPECS:
        return False, f"Invalid thickness: {thickness_mm}mm"

    specs = GLASS_SPECS[thickness_key]
    max_dimension = max(width_mm, height_mm)

    if max_dimension < specs["min_panel_size"]:
        return False, f"Panel too small. Minimum: {specs['min_panel_size']}mm"

    if max_dimension > specs["max_panel_size"]:
        return False, f"Panel too large. Maximum for {thickness_key}: {specs['max_panel_size']}mm"

    return True, "Panel size valid"


def calculatePanelWeight(width_mm, height_mm, thickness_mm):
    """
    Calculate the weight of a glass panel.

    Args:
        width_mm: Panel width in millimeters
        height_mm: Panel height in millimeters
        thickness_mm: Glass thickness in millimeters

    Returns:
        float: Weight in kilograms
    """
    thickness_key = f"{int(thickness_mm)}mm"

    # Calculate area in m²
    area_m2 = (width_mm / 1000.0) * (height_mm / 1000.0)

    if thickness_key in GLASS_SPECS:
        weight_per_m2 = GLASS_SPECS[thickness_key]["weight_kg_m2"]
        return area_m2 * weight_per_m2
    else:
        # Approximate weight for non-standard thickness
        # Glass density: ~2.5 kg per mm per m²
        return area_m2 * 2.5 * thickness_mm


def getGlassColor(glass_type):
    """
    Get the RGB color for a glass type.

    Args:
        glass_type: Type of glass (e.g., "Clear", "Bronze")

    Returns:
        tuple: RGB values (0-1 range) or None if type not found
    """
    if glass_type in GLASS_TYPES:
        return GLASS_TYPES[glass_type]["color"]
    return None


def getGlassOpacity(glass_type):
    """
    Get the opacity value for a glass type.

    Args:
        glass_type: Type of glass

    Returns:
        float: Opacity value (0=transparent, 1=opaque) or None if type not found
    """
    if glass_type in GLASS_TYPES:
        return GLASS_TYPES[glass_type]["opacity"]
    return None
