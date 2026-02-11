# Monza Range — Bi-Fold (In-Fold) Hinge Specifications

Source: Showers-Ex-Sliding-Catalogue.pdf (page 12)

> Dimensions in mm. **VERIFY ALL DIMENSIONS AGAINST ORIGINAL PDF DRAWINGS.**
> Numbers extracted from catalogue dimension text — some may need correction.
> Self-rising hinges have a cam mechanism that lifts the door 8 mm when opening.

---

## Overview

A bi-fold door uses **two hinge types as a paired set**:

1. **Monza 90 Wall to Glass** — attaches the wall-side panel to the wall
2. **Monza 180 Glass to Glass** — connects the two glass panels at the fold joint

Both are **self-rising** (cam-lift) and **handed** (Left/Right variants).

---

## Configuration Pairing

The L/R hinge hand depends on which wall side and fold direction:

| Configuration | Wall Hinge | Fold Hinge |
|---------------|-----------|------------|
| Left wall, opening inwards | STM-WGH-90R | STM-GGH-180L |
| Right wall, opening inwards | STM-GGH-180R | STM-WGH-90L |
| Left wall, opening outwards | STM-WGH-90L | STM-GGH-180R |
| Right wall, opening outwards | STM-GGH-180L | STM-WGH-90R |

---

## 1. Monza 90 Wall to Glass Self Rising Hinge

**Mounting:** Wall to Glass | **Angle:** 90 | **Type:** Self-Rising (Bi-Fold)

| Code | Material | Finish | Weight Capacity | Glass Thickness |
|------|----------|--------|-----------------|-----------------|
| STM-WGH-90L | Brass | Bright Chrome | 45 kg | 6-12 mm |
| STM-WGH-90R | Brass | Bright Chrome | 45 kg | 6-12 mm |
| MWGH-90LMB | Brass | Matte Black | 45 kg | 6-12 mm |
| MWGH-90RMB | Brass | Matte Black | 45 kg | 6-12 mm |

**Dimensions (VERIFY):**

| Measurement | Value | Notes |
|-------------|-------|-------|
| Wall plate width | 35 mm ||
| Glass plate width | 35 mm ||
| Knuckle depth | 35 mm ||
| Knuckle width | 45 mm ||
| Body height | 80 mm ||
| Body width | 60 mm ||
| Knuckle diameter | 14 mm ||
| Glass to wall offset | 10 mm |
| Rise height | 8 mm | Vertical lift when opening |

---

## 2. Monza 180 Glass to Glass Self Rising Hinge

**Mounting:** Glass to Glass | **Angle:** 180 | **Type:** Self-Rising (Bi-Fold)

| Code | Material | Finish | Weight Capacity | Glass Thickness |
|------|----------|--------|-----------------|-----------------|
| STM-GGH-180L | Brass | Bright Chrome | 45 kg | 6-12 mm |
| STM-GGH-180R | Brass | Bright Chrome | 45 kg | 6-12 mm |
| MGGH-180LMB | Brass | Matte Black | 45 kg | 6-12 mm |
| MGGH-180RMB | Brass | Matte Black | 45 kg | 6-12 mm |

**Dimensions (VERIFY):**

| Measurement | Value | Notes |
|-------------|-------|-------|
| Glass plate width | 35 mm ||
| Knuckle depth | 30 mm ||
| Knuckle width | 45 mm ||
| Body height | 80 mm ||
| Body width | 98 mm ||
| Knuckle diameter | 14 mm ||
| Glass to glass offset | 6 mm |
| Rise height | 8 mm | Vertical lift when opening |

---

## Notes for HardwareSpecs.py Integration

Once dimensions are verified, these would be added as:

```python
MONZA_BIFOLD_HINGE_SPECS = {
    "monza_90_wall_to_glass": {
        "name": "Monza 90 Wall to Glass Self Rising Hinge",
        "mounting_type": "Wall-to-Glass",
        "hinge_category": "Bi-Fold",
        "angle": 90,
        "self_rising": True,
        "rise_height": 6,        # mm — VERIFY
        "self_rise_angle": 45,    # degrees
        "handed": True,           # L/R variants
        "dimensions": {
            "wall_plate_width": 35,   # VERIFY
            "glass_plate_width": 45,  # VERIFY
            "glass_cutout_depth": 25, # VERIFY
            "glass_cutout_width": 35, # VERIFY
            "body_height": 80,
            "body_width": 60,
            "knuckle_diameter": 14,
        },
        "product_codes": [
            {"code": "STM-WGH-90L", "hand": "Left",  "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "STM-WGH-90R", "hand": "Right", "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "MWGH-90LMB",  "hand": "Left",  "material": "Brass", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "MWGH-90RMB",  "hand": "Right", "material": "Brass", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },

    "monza_180_glass_to_glass": {
        "name": "Monza 180 Glass to Glass Self Rising Hinge",
        "mounting_type": "Glass-to-Glass",
        "hinge_category": "Bi-Fold",
        "angle": 180,
        "self_rising": True,
        "rise_height": 6,        # mm — VERIFY
        "self_rise_angle": 49,    # degrees
        "handed": True,           # L/R variants
        "dimensions": {
            "glass_plate_width": 35,   # VERIFY — each side
            "glass_cutout_depth": 28,  # VERIFY — or 30?
            "glass_cutout_width": 45,  # VERIFY
            "body_height": 80,
            "overall_width": 98,
            "knuckle_diameter": 14,
            "knuckle_width": 45,       # VERIFY
        },
        "product_codes": [
            {"code": "STM-GGH-180L", "hand": "Left",  "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "STM-GGH-180R", "hand": "Right", "material": "Brass", "finish": "Bright Chrome",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "MGGH-180LMB",  "hand": "Left",  "material": "Brass", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
            {"code": "MGGH-180RMB",  "hand": "Right", "material": "Brass", "finish": "Matte Black",
             "weight_capacity_kg": 45, "glass_thickness_range": [6, 8, 10, 12]},
        ],
    },
}
```

### Key Differences from Bevel Range

| Feature | Bevel Range | Monza Bi-Fold |
|---------|-------------|---------------|
| Self-rising | No | Yes (cam lift) |
| Handed (L/R) | No | Yes |
| Knuckle diameter | 16 mm | 14 mm |
| Body height | 90 mm | 80 mm |
| Paired set | Individual | Wall + Fold pair required |
| Finishes | 5 options | 2 (Bright Chrome, Matte Black) |

### BiFoldDoor.py Integration

The current `BiFoldDoor.py` uses generic `standard_wall_mount` box hinges for both wall and fold positions. After adding Monza specs:

1. Add `HingeModel` enum to BiFoldDoor VarSet: `["Legacy", "monza_90_wall_to_glass"]` for wall hinges, `["Legacy", "monza_180_glass_to_glass"]` for fold hinges (or a single combined `"Monza"` / `"Legacy"` choice)
2. Create `createMonzaWallHingeShape()` and `createMonzaFoldHingeShape()` in `Hinge.py`
3. Wall hinges use `monza_90_wall_to_glass`, fold hinges use `monza_180_glass_to_glass`
4. Hand selection (L/R) auto-derived from `HingeSide` + `HingeConfiguration`
