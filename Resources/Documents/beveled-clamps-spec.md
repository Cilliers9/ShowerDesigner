# Bevel Clamps Specification

Source: Showers-Ex-Sliding-Catalogue.pdf, Pages 12-15

All dimensions in mm. Weight ratings calculated for 8mm glass.

---

## CLAMP_SPECS Field Reference

Each clamp type in `HardwareSpecs.py` uses this structure:

```python
"ClampKey": {
    "load_capacity_kg": int,          # max weight per clamp (kg)
    "glass_thickness_range": [int],   # supported glass thicknesses (mm)
    "default_mounting": str,          # "Wall" or "Floor"
    "dimensions": {
        "base_size": float,           # body width/height (mm)
        "base_thickness": float,      # plate thickness (mm)
        "glass_gap": float,           # slot width for glass (mm)
        "cutout_depth": float,        # U-slot depth (mm)
        "cutout_radius": float,       # slot bottom radius (mm)
        "chamfer_size": float,        # bevel chamfer on front face (mm)
    },
    "bounding_box": {
        "width": float,               # X extent (mm)
        "depth": float,               # Y extent (mm)
        "height": float,              # Z extent (mm)
    },
    "product_codes": [                # catalogue variants
        {"code": str, "material": str, "finish": str},
    ],
}
```

---

## Dimension Mapping (Catalogue to Code)

The catalogue technical drawings show these raw measurements.
Below is how they map to `CLAMP_SPECS["dimensions"]` fields:

| Catalogue Dimension | Code Field       | S/S 304 | Brass | Notes                          |
|---------------------|------------------|---------|-------|--------------------------------|
| Body W x H          | `base_size`      | 45      | 50    | Square face of clamp           |
| Plate thickness     | `base_thickness` | 4.5     | 5     | Front/back plate thickness     |
| Glass slot width    | `glass_gap`      | 10      | 10    | Gap between front & back plate |
| Slot depth (20/18)  | `cutout_depth`   | 20      | 20    | Depth of U-slot from top       |
| Corner radius R9/R10| `cutout_radius`  | 9       | 10    | Radius at slot bottom          |
| Bevel chamfer       | `chamfer_size`   | 3       | 3     | Chamfer on front plate edges   |
| Wall gap            | `wall_gap`       | 5       | 5     | Gap between wall and clamp body|

### Bounding Box Derivation

| Clamp Type     | Width        | Depth                      | Height         |
|----------------|--------------|----------------------------|----------------|
| U-Clamp (90°)  | base_size    | base_thickness*2+glass_gap | base_size      |
| L-Clamp (90°)  | base_size    | base_size+glass_gap+bt     | base_size      |
| 180° W2G/G2G   | base_size    | base_thickness*2+glass_gap | base_size*2    |
| 135° G2G       | base_size    | ~70 (angled plate)         | base_size*2    |
| 90° Tee G2G    | base_size*2  | base_thickness*2+glass_gap | base_size+17   |

---

## S/S 304 Bevel Clamps

### Bevel 90° (U-Clamp) Wall to Glass Single Fix Clamp

- **Mounting**: Wall (single fix, no back plate extension)
- **load_capacity_kg**: 45
- **glass_thickness_range**: [6, 8, 10, 12]
- **default_mounting**: "Wall"
- **dimensions**:
  - base_size: 45
  - base_thickness: 4.5
  - glass_gap: 10
  - cutout_depth: 20
  - cutout_radius: 9
  - chamfer_size: 3
- **bounding_box**: { width: 45, depth: 19, height: 45 }

| Code   | Material | Finish          | Glass Thickness |
|--------|----------|-----------------|-----------------|
| GC-401 | S/S 304  | Bright Polished | 6-12mm          |
| GC-491 | S/S 304  | Matte Black     | 6-12mm          |
| GC-481 | S/S 304  | Antique Brass   | 6-12mm          |

### Bevel 90° (L-Clamp) Wall to Glass Clamp

- **Mounting**: Wall (L-bracket with pressure plate)
- **load_capacity_kg**: 45
- **glass_thickness_range**: [6, 8, 10, 12]
- **default_mounting**: "Wall"
- **dimensions**:
  - base_size: 45
  - base_thickness: 4.5
  - glass_gap: 10
  - cutout_depth: 20
  - cutout_radius: 9
  - chamfer_size: 3
- **bounding_box**: { width: 45, depth: 60, height: 45 }

| Code   | Material | Finish          | Glass Thickness |
|--------|----------|-----------------|-----------------|
| GC-402 | S/S 304  | Bright Polished | 6-12mm          |
| GC-492 | S/S 304  | Matte Black     | 6-12mm          |
| GC-482 | S/S 304  | Antique Brass   | 6-12mm          |

### Bevel 180° Wall to Glass Clamp

- **Mounting**: Wall (inline, extends vertically)
- **load_capacity_kg**: 45
- **glass_thickness_range**: [6, 8, 10, 12]
- **default_mounting**: "Wall"
- **dimensions**:
  - base_size: 45
  - base_thickness: 4.5
  - glass_gap: 10
  - cutout_depth: 20
  - cutout_radius: 9
  - chamfer_size: 3
- **bounding_box**: { width: 45, depth: 19, height: 101 }

| Code   | Material | Finish          | Glass Thickness |
|--------|----------|-----------------|-----------------|
| GC-403 | S/S 304  | Bright Polished | 6-12mm          |
| GC-483 | S/S 304  | Antique Brass   | 6-12mm          |
| GC-493 | S/S 304  | Matte Black     | 6-12mm          |

### Bevel 90° Glass to Glass Clamp

- **Mounting**: Glass-to-Glass (two glass slots at 90°)
- **load_capacity_kg**: 45
- **glass_thickness_range**: [6, 8, 10, 12]
- **default_mounting**: "Floor"
- **dimensions**:
  - base_size: 45
  - base_thickness: 4.5
  - glass_gap: 10
  - cutout_depth: 20
  - cutout_radius: 9
  - chamfer_size: 3
- **bounding_box**: { width: 45, depth: 45, height: 45 }
- **glass_plate**: 24 x 32, thickness: 18

| Code   | Material | Finish          | Glass Thickness |
|--------|----------|-----------------|-----------------|
| GC-404 | S/S 304  | Bright Polished | 6-12mm          |
| GC-494 | S/S 304  | Matte Black     | 6-12mm          |
| GC-484 | S/S 304  | Antique Brass   | 6-12mm          |

### Bevel 135° Glass to Glass Clamp

- **Mounting**: Glass-to-Glass (two glass slots at 135°)
- **load_capacity_kg**: 45
- **glass_thickness_range**: [6, 8, 10, 12]
- **default_mounting**: "Floor"
- **dimensions**:
  - base_size: 45
  - base_thickness: 4.5
  - glass_gap: 10
  - cutout_depth: 20
  - cutout_radius: 9
  - chamfer_size: 3
- **bounding_box**: { width: 45, depth: 70, height: 92 }
- **glass_plate**: 24 x 24, thickness: 18

| Code   | Material | Finish          | Glass Thickness |
|--------|----------|-----------------|-----------------|
| GC-405 | S/S 304  | Bright Polished | 6-12mm          |
| GC-495 | S/S 304  | Matte Black     | 6-12mm          |
| GC-485 | S/S 304  | Antique Brass   | 6-12mm          |

### Bevel 180° Glass to Glass Clamp

- **Mounting**: Glass-to-Glass (two glass slots at 180°, inline)
- **load_capacity_kg**: 45
- **glass_thickness_range**: [6, 8, 10, 12]
- **default_mounting**: "Floor"
- **dimensions**:
  - base_size: 45
  - base_thickness: 4.5
  - glass_gap: 10
  - cutout_depth: 20
  - cutout_radius: 9
  - chamfer_size: 3
- **bounding_box**: { width: 45, depth: 19, height: 101 }
- **cutouts**:
  - dividing_panel: 22 x 18
  - inline_panel: 18 x 56
  - overall_plate: 56 x 24

| Code   | Material | Finish          | Glass Thickness |
|--------|----------|-----------------|-----------------|
| GC-406 | S/S 304  | Bright Polished | 6-12mm          |
| GC-496 | S/S 304  | Matte Black     | 6-12mm          |
| GC-486 | S/S 304  | Antique Brass   | 6-12mm          |

### Bevel 90° Glass to Glass Tee Clamp

- **Mounting**: Glass-to-Glass (T-junction, 3 glass slots)
- **load_capacity_kg**: 45
- **glass_thickness_range**: [6, 8, 10, 12]
- **default_mounting**: "Floor"
- **dimensions**:
  - base_size: 45
  - base_thickness: 4.5
  - glass_gap: 10
  - cutout_depth: 20
  - cutout_radius: 9
  - chamfer_size: 3
- **bounding_box**: { width: 90, depth: 45, height: 62 }
- **glass_plate**: 24 x 24, thickness: 18
- **cutouts**:
  - dividing_panel: 22 x 18
  - inline_panel: 18 x 56

| Code   | Material | Finish          | Glass Thickness |
|--------|----------|-----------------|-----------------|
| GC-407 | S/S 304  | Bright Polished | 6-12mm          |
| GC-487 | S/S 304  | Antique Brass   | 6-12mm          |
| GC-497 | S/S 304  | Matte Black     | 6-12mm          |

---

## Brass Bevel Clamps

Brass series uses larger body (50mm vs 45mm) and R10 corner radius.

### Bevel 90° (U-Clamp) Wall to Glass Single Fix Clamp

- **Mounting**: Wall (single fix)
- **load_capacity_kg**: 45
- **glass_thickness_range**: [6, 8, 10, 12]
- **default_mounting**: "Wall"
- **dimensions**:
  - base_size: 50
  - base_thickness: 5
  - glass_gap: 10
  - cutout_depth: 20
  - cutout_radius: 10
  - chamfer_size: 3
- **bounding_box**: { width: 50, depth: 20, height: 50 }

| Code   | Material | Finish        | Glass Thickness |
|--------|----------|---------------|-----------------|
| GC-701 | Brass    | Bright Chrome | 6-12mm          |
| GC-711 | Brass    | Satin Chrome  | 6-12mm          |

### Bevel 90° (L-Clamp) Wall to Glass Clamp

- **Mounting**: Wall (L-bracket)
- **load_capacity_kg**: 45
- **glass_thickness_range**: [6, 8, 10, 12]
- **default_mounting**: "Wall"
- **dimensions**:
  - base_size: 50
  - base_thickness: 5
  - glass_gap: 10
  - cutout_depth: 20
  - cutout_radius: 10
  - chamfer_size: 3
- **bounding_box**: { width: 50, depth: 65, height: 50 }

| Code   | Material | Finish        | Glass Thickness |
|--------|----------|---------------|-----------------|
| GC-702 | Brass    | Bright Chrome | 6-12mm          |
| GC-712 | Brass    | Satin Chrome  | 6-12mm          |

### Bevel 180° Wall to Glass Clamp

- **Mounting**: Wall (inline)
- **load_capacity_kg**: 45
- **glass_thickness_range**: [6, 8, 10, 12]
- **default_mounting**: "Wall"
- **dimensions**:
  - base_size: 50
  - base_thickness: 5
  - glass_gap: 10
  - cutout_depth: 20
  - cutout_radius: 10
  - chamfer_size: 3
- **bounding_box**: { width: 50, depth: 20, height: 101 }

| Code   | Material | Finish        | Glass Thickness |
|--------|----------|---------------|-----------------|
| GC-703 | Brass    | Bright Chrome | 6-12mm          |
| GC-713 | Brass    | Satin Chrome  | 6-12mm          |

### Bevel 90° Glass to Glass Clamp

- **Mounting**: Glass-to-Glass
- **load_capacity_kg**: 45
- **glass_thickness_range**: [6, 8, 10, 12]
- **default_mounting**: "Floor"
- **dimensions**:
  - base_size: 50
  - base_thickness: 5
  - glass_gap: 10
  - cutout_depth: 20
  - cutout_radius: 10
  - chamfer_size: 3
- **bounding_box**: { width: 50, depth: 50, height: 50 }
- **glass_plate**: 24 x 32, thickness: 20

| Code   | Material | Finish        | Glass Thickness |
|--------|----------|---------------|-----------------|
| GC-704 | Brass    | Bright Chrome | 6-12mm          |
| GC-714 | Brass    | Satin Chrome  | 6-12mm          |

### Bevel 135° Glass to Glass Clamp

- **Mounting**: Glass-to-Glass
- **load_capacity_kg**: 45
- **glass_thickness_range**: [6, 8, 10, 12]
- **default_mounting**: "Floor"
- **dimensions**:
  - base_size: 50
  - base_thickness: 5
  - glass_gap: 10
  - cutout_depth: 20
  - cutout_radius: 10
  - chamfer_size: 3
- **bounding_box**: { width: 50, depth: 75, height: 103 }
- **glass_plate**: 20 x 25 x 25

| Code   | Material | Finish        | Glass Thickness |
|--------|----------|---------------|-----------------|
| GC-705 | Brass    | Bright Chrome | 6-12mm          |
| GC-715 | Brass    | Satin Chrome  | 6-12mm          |

### Bevel 180° Glass to Glass Clamp

- **Mounting**: Glass-to-Glass (inline)
- **load_capacity_kg**: 45
- **glass_thickness_range**: [6, 8, 10, 12]
- **default_mounting**: "Floor"
- **dimensions**:
  - base_size: 50
  - base_thickness: 5
  - glass_gap: 10
  - cutout_depth: 20
  - cutout_radius: 10
  - chamfer_size: 3
- **bounding_box**: { width: 50, depth: 20, height: 101 }
- **glass_plate**: 24 x 24, thickness: 20

| Code   | Material | Finish        | Glass Thickness |
|--------|----------|---------------|-----------------|
| GC-706 | Brass    | Bright Chrome | 6-12mm          |
| GC-716 | Brass    | Satin Chrome  | 6-12mm          |

---

## Placement Defaults

From `CLAMP_PLACEMENT_DEFAULTS` in HardwareSpecs.py:

| Parameter            | Value | Unit | Notes                     |
|----------------------|-------|------|---------------------------|
| wall_offset_top      | 300   | mm   | From top edge of panel    |
| wall_offset_bottom   | 300   | mm   | From bottom edge of panel |
| floor_offset_start   | 75    | mm   | From panel side edge      |
| floor_offset_end     | 75    | mm   | From panel side edge      |

---

## Finishes Summary

### S/S 304 Finishes
| Finish          | Code Suffix | Example   |
|-----------------|-------------|-----------|
| Bright Polished | -4xx        | GC-401    |
| Antique Brass   | -48x        | GC-481    |
| Matte Black     | -49x        | GC-491    |

### Brass Finishes
| Finish        | Code Suffix | Example   |
|---------------|-------------|-----------|
| Bright Chrome | -7xx        | GC-701    |
| Satin Chrome  | -71x        | GC-711    |

---

## Cross-Reference: All Bevel Clamp Types

| Type                   | Angle | Mounting    | S/S 304 Code | Brass Code | base_size |
|------------------------|-------|-------------|--------------|------------|-----------|
| U-Clamp (single fix)   | 90°   | Wall-Glass  | GC-401       | GC-701     | 45 / 50   |
| L-Clamp                | 90°   | Wall-Glass  | GC-402       | GC-702     | 45 / 50   |
| Wall-Glass Inline      | 180°  | Wall-Glass  | GC-403       | GC-703     | 45 / 50   |
| Glass-Glass            | 90°   | Glass-Glass | GC-404       | GC-704     | 45 / 50   |
| Glass-Glass            | 135°  | Glass-Glass | GC-405       | GC-705     | 45 / 50   |
| Glass-Glass Inline     | 180°  | Glass-Glass | GC-406       | GC-706     | 45 / 50   |
| Glass-Glass Tee        | 90°   | Glass-Glass | GC-407       | --         | 45 / --   |

---

## Notes

- Current `CLAMP_SPECS` in HardwareSpecs.py has 4 types: U_Clamp, L_Clamp, 180DEG_Clamp, 135DEG_Clamp
- Current code uses `cutout_radius: 10` for all — catalogue shows R9 for S/S 304, R10 for Brass
- Glass-to-glass clamp types (90°, 135°, 180°, Tee) are not yet in CLAMP_SPECS
- The 180° wall-to-glass and 180° glass-to-glass have different geometries but same bounding box height (101)
- Tee clamp is only available in S/S 304 (no Brass variant in catalogue)
