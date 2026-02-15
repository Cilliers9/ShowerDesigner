# Shower Seals Specification

Source: Showers-Ex-Sliding-Catalogue.pdf, Pages 35-42

All dimensions in mm. Lengths are standard stock lengths (2500mm or 3000mm for 10-12mm glass variants).

---

## Seal Categories

| Category | Seal Types | Usage |
|----------|-----------|-------|
| Soft Lip | Centre Lip, 180° Soft Lip, 180° Long Lip, 90° Soft Lip, 135° Soft Lip | Glass edge weatherstripping, flexible fit |
| Bubble | Bubble Seal | Glass edge cushion seal |
| Bottom | Wipe Seal with Bubble, Drip & Wipe Seal | Floor-level water containment |
| Hard Lip | 180° Hard Lip, 135° Hard Lip, 90° Extended Hard Lip, 90° Hard Lip, 90° Hard/Soft Lip, Double Hard Lip (H) | Rigid edge sealing, glass-to-glass or glass-to-wall |
| Magnetic | 90°/180° Magnetic, 180° Flat Magnetic, 135° Magnetic | Door closure seals |
| Infill | 180° G2G Infill Seal | Glass-to-glass gap filler |

---

## SEAL_SPECS Field Reference

Proposed structure for `HardwareSpecs.py`:

```python
"seal_key": {
    "name": str,                      # display name
    "category": str,                  # "soft_lip" | "bubble" | "bottom" | "hard_lip" | "magnetic" | "infill"
    "angle": int,                     # 0 (centre), 90, 135, 180
    "location": str,                  # "side" | "bottom" | "door"
    "dimensions": {
        "soft_lip_length": float,     # flexible lip (mm), 0 if none
        "hard_lip_length": float,     # rigid lip (mm), 0 if none
        "bubble_length": float,       # bubble portion (mm), 0 if none
        "magnet_lip_length": float,   # magnetic lip (mm), 0 if none
    },
    "material": str,                  # "PVC" or "PC" (polycarbonate)
    "glass_thickness_range": [int],   # supported glass thicknesses (mm)
    "stock_length": int,              # standard length in mm (2500 or 3000)
    "product_codes": [
        {"code": str, "glass_thickness": str, "colour": str, "length": int},
    ],
}
```

---

## Soft Lip Seals

### Centre Lip Seal
- **Angle**: 0° (straight/centre)
- **Location**: Side (glass edge)
- **Soft Lip Length**: 12mm
- **Material**: PVC

| Glass Thickness | Length | Colour | Code |
|----------------|--------|--------|------|
| 6-8mm | 2500mm | Clear | TSS-001-8 |
| 8-10mm | 2500mm | Clear | TSS-001-10 |
| 10-12mm | 3000mm | Clear | TUV-001-12 |

---

### 180° Soft Lip Seal
- **Angle**: 180° (inline)
- **Location**: Side (glass edge)
- **Soft Lip Length**: 16mm (6-10mm glass), 20mm (10-12mm glass)
- **Material**: PVC

| Glass Thickness | Length | Soft Lip | Colour | Code |
|----------------|--------|----------|--------|------|
| 4-6mm | 2500mm | 16mm | Clear | TSS-003-6 |
| 6-8mm | 2500mm | 16mm | Clear | TSS-003-8 |
| 6-8mm | 2500mm | 16mm | Black | BSS-003-8 |
| 8-10mm | 2500mm | 16mm | Clear | TSS-003-10 |
| 8-10mm | 2500mm | 16mm | Black | BSS-003-10 |
| 10-12mm | 3000mm | 20mm | Clear | TUV-003-12 |
| 10-12mm | 3000mm | 20mm | Black | BUV-003-12 |

---

### 180° Long Lip Seal
- **Angle**: 180° (inline)
- **Location**: Side (glass edge)
- **Soft Lip Length**: 22mm
- **Material**: PVC

| Glass Thickness | Length | Colour | Code |
|----------------|--------|--------|------|
| 6-8mm | 2500mm | Clear | TSS-003-8-22 |
| 6-8mm | 2500mm | Black | BSS-003-8-22 |
| 8-10mm | 2500mm | Clear | TSS-003-10-22 |
| 8-10mm | 2500mm | Black | BSS-003-10-22 |

---

### 90° Soft Lip Seal
- **Angle**: 90°
- **Location**: Side (glass edge, corner joint)
- **Soft Lip Length**: 8mm
- **Material**: PVC

| Glass Thickness | Length | Colour | Code |
|----------------|--------|--------|------|
| 4-6mm | 2500mm | Clear | TSS-007-6 |
| 6-8mm | 2500mm | Clear | TSS-007-8 |
| 6-8mm | 2500mm | Black | BSS-007-8 |
| 8-10mm | 2500mm | Clear | TSS-007-10 |
| 8-10mm | 2500mm | Black | BSS-007-10 |
| 10-12mm | 3000mm | Clear | TUV-007-12 |

---

### 135° Soft Lip Seal
- **Angle**: 135°
- **Location**: Side (glass edge, angled joint)
- **Soft Lip Length**: 16mm
- **Material**: PVC

| Glass Thickness | Length | Colour | Code |
|----------------|--------|--------|------|
| 6-8mm | 2500mm | Clear | TSS-005-8 |
| 8-10mm | 2500mm | Clear | TSS-005-10 |

---

## Bubble Seal

### Bubble Seal
- **Angle**: 0° (straight)
- **Location**: Side (glass edge cushion)
- **Bubble Length**: 8mm (standard), 12mm, 24mm variants
- **Material**: PVC

| Glass Thickness | Length | Bubble Length | Colour | Code |
|----------------|--------|-------------|--------|------|
| 4-6mm | 2500mm | 8mm | Clear | TSS-004-6 |
| 6-8mm | 2500mm | 8mm | Clear | TSS-004-8 |
| 6-8mm | 2500mm | 8mm | Black | BSS-004-8 |
| 6-8mm | 2500mm | 12mm | Clear | TSS-004-8-12 |
| 6-8mm | 2500mm | 24mm | Clear | TSS-004-8-24 |
| 6-8mm | 2500mm | 24mm | Black | BSS-004-8-24 |
| 8-10mm | 2500mm | 8mm | Clear | TSS-004-10 |
| 8-10mm | 2500mm | 8mm | Black | BSS-004-10 |

---

## Bottom Seals

### Wipe Seal with Bubble
- **Angle**: 0° (straight, downward)
- **Location**: Bottom (floor seal)
- **Soft Lip Length**: 11mm
- **Bubble Lip Length**: 8mm
- **Material**: PVC

| Glass Thickness | Length | Colour | Code |
|----------------|--------|--------|------|
| 6-8mm | 2500mm | Clear | TSS-009-8 |

---

### Drip & Wipe Seal
- **Angle**: 0° (straight, downward)
- **Location**: Bottom (floor seal with drip rail)
- **Hard Lip Length**: 8mm (drip rail)
- **Soft Lip Length**: 10mm (wipe)
- **Material**: PC (polycarbonate) for clear, PVC for black

| Glass Thickness | Length | Colour | Code |
|----------------|--------|--------|------|
| 6mm | 2500mm | Clear | TSS-009B1-6 |
| 6-8mm | 2500mm | Clear | TSS-009B1-8 |
| 6-8mm | 2500mm | Black | BSS-009B1-8 |
| 8-10mm | 2500mm | Clear | TSS-009B1-10 |
| 8-10mm | 2500mm | Black | BSS-009B1-10 |
| 10-12mm | 2500mm | Clear | TSS-009B1-12 |
| 10-12mm | 2500mm | Black | BSS-009B1-12 |
| 6-8mm | 2500mm | Clear | PSS-009B1-8 |
| 8-10mm | 2500mm | Clear | PSS-009B1-10 |

Note: TSS/BSS codes are PVC material, PSS codes are PC (polycarbonate) material.

---

## Hard Lip Seals

### 180° Hard Lip Seal
- **Angle**: 180° (inline)
- **Location**: Side (glass edge)
- **Hard Lip Length**: 10mm
- **Soft Lip Length**: 5mm
- **Material**: PVC (clear/black), PC (clear)

| Glass Thickness | Length | Colour | Material | Code |
|----------------|--------|--------|----------|------|
| 6-8mm | 2500mm | Clear | PVC | TSS-003A-8 |
| 6-8mm | 2500mm | Black | PVC | BSS-003A-8 |
| 8mm | 2500mm | Clear | PC | PSS-003A-8 |
| 8-10mm | 2500mm | Clear | PVC | TSS-003A-10 |
| 8-10mm | 2500mm | Black | PVC | BSS-003A-10 |
| 10mm | 3000mm | Clear | PC | PUV-003A-10 |
| 10-12mm | 3000mm | Clear | PVC | TUV-003A-12 |

---

### 135° Hard Lip Seal
- **Angle**: 135°
- **Location**: Side (glass edge, angled joint)
- **Hard Lip Length**: 10mm
- **Soft Lip Length**: 5mm
- **Material**: PVC

| Glass Thickness | Length | Colour | Code |
|----------------|--------|--------|------|
| 6-8mm | 2500mm | Clear | TSS-005A-8 |
| 8-10mm | 2500mm | Clear | TSS-005A-10 |

---

### 90° Extended Hard Lip Seal
- **Angle**: 90°
- **Location**: Side (glass edge, corner)
- **Hard Lip Length**: 10mm
- **Soft Lip Length**: 8mm
- **Material**: PVC

| Glass Thickness | Length | Colour | Code |
|----------------|--------|--------|------|
| 6-8mm | 2500mm | Clear | TSS-011A-8 |
| 8-10mm | 2500mm | Clear | TSS-011A-10 |

---

### 90° Hard Lip Seal
- **Angle**: 90°
- **Location**: Side (glass edge, corner)
- **Hard Lip Length**: 10mm
- **Soft Lip Length**: 10mm
- **Material**: PVC

| Glass Thickness | Length | Colour | Code |
|----------------|--------|--------|------|
| 6-8mm | 2500mm | Clear | TSS-011C-8 |
| 8-10mm | 2500mm | Clear | TSS-011C-10 |

---

### 90° Hard/Soft Lip Seal
- **Angle**: 90°
- **Location**: Side (glass edge, corner)
- **Hard Lip Length**: 10mm
- **Soft Lip Length**: 14mm
- **Material**: PVC

| Glass Thickness | Length | Colour | Code |
|----------------|--------|--------|------|
| 6-8mm | 2500mm | Black | BSS-004A-8 |
| 10-12mm | 3000mm | Clear | TUV-04A-12 |

---

### Double Hard Lip Seal (H)
- **Angle**: 180° (inline, H-profile)
- **Location**: Side (glass-to-glass inline)
- **Hard Lip Length**: 8mm (both sides)
- **Material**: PC (polycarbonate)

| Glass Thickness | Length | Colour | Code |
|----------------|--------|--------|------|
| 8mm | 3000mm | Clear | TUV-010-8 |
| 10mm | 3000mm | Clear | TUV-010-10 |
| 12mm | 3000mm | Clear | TUV-010-12 |

---

## Magnetic Seals

### 90°/180° Magnetic Seal
- **Angle**: 90° and 180° (universal)
- **Location**: Door edge (closure)
- **Lip Length**: 12mm
- **Inside Measurement**: 10mm (based on 8mm glass)
- **Outside Measurement**: 18mm (based on 8mm glass)
- **Material**: PVC (clear/black/brown), PC (clear)

| Glass Thickness | Length | Colour | Material | Code |
|----------------|--------|--------|----------|------|
| 6-8mm | 2500mm | White | PVC | TSS-008A-8 |
| 6-8mm | 2500mm | Brown | PVC | SM090-08B |
| 6-8mm | 2500mm | Black | PVC | BSS-008A-8 |
| 8mm | 2500mm | White | PC | PSS-008A-8 |
| 8-10mm | 2500mm | White | PVC | TSS-008A-10 |
| 8-10mm | 2500mm | Brown | PVC | SM090-10B |
| 8-10mm | 2500mm | Black | PVC | BSS-008A-10 |
| 10mm | 3000mm | White | PC | PUV-008A-10 |
| 10-12mm | 3000mm | White | PVC | TUV-008A-12 |
| 10-12mm | 3000mm | Brown | PVC | SM090-12B |
| 10-12mm | 3000mm | Black | PVC | BUV-008A-12 |

---

### 180° Flat Magnetic Seal
- **Angle**: 180° (inline flat profile)
- **Location**: Door edge (closure)
- **Lip Length**: 12mm
- **Material**: PVC

| Glass Thickness | Length | Colour | Code |
|----------------|--------|--------|------|
| 6-8mm | 2500mm | White | TSS-008B-8 |
| 6-8mm | 2500mm | Brown | SM180-08B |
| 8-10mm | 2500mm | White | TSS-008B-10 |
| 8-10mm | 2500mm | Brown | SM180-10B |

---

### 135° Magnetic Seal
- **Angle**: 135°
- **Location**: Door edge (closure, angled joint)
- **Lip Length**: 12mm
- **Material**: PVC

| Glass Thickness | Length | Colour | Code |
|----------------|--------|--------|------|
| 6-8mm | 2500mm | White | TSS-008C-8 |
| 6-8mm | 2500mm | Brown | SM135-08B |
| 8-10mm | 2500mm | White | TSS-008C-10 |
| 8-10mm | 2500mm | Brown | SM135-10B |

---

## Infill Seals

### 180° Glass-to-Glass Infill Seal
- **Angle**: 180° (inline)
- **Location**: Glass-to-glass gap filler
- **Inside Measurement**: 8mm (based on 8mm glass)
- **Outside Measurement**: 18mm (based on 8mm glass)
- **Material**: PC (polycarbonate)

| Glass Thickness | Length | Colour | Code |
|----------------|--------|--------|------|
| 6mm | 3000mm | Clear | IS-180-6 |
| 10mm | 3000mm | Clear | IS-180-10 |
| 12mm | 3000mm | Clear | IS-180-12 |

---

## Product Code Conventions

| Prefix | Material | Colour |
|--------|----------|--------|
| TSS- | PVC | Clear (standard 2500mm) |
| TUV- | PVC | Clear (UV-rated 3000mm, for 10-12mm) |
| BSS- | PVC | Black (standard 2500mm) |
| BUV- | PVC | Black (UV-rated 3000mm, for 10-12mm) |
| PSS- | PC | Clear (standard 2500mm) |
| PUV- | PC | Clear (UV-rated 3000mm) |
| SM090- | PVC | Brown (90° magnetic) |
| SM135- | PVC | Brown (135° magnetic) |
| SM180- | PVC | Brown (180° magnetic) |
| IS- | PC | Clear (infill seal) |

## Material Notes

- **PVC**: Standard material for most seals. Flexible, suitable for soft lip and bubble types.
- **PC (Polycarbonate)**: Harder material used for hard lip seals, drip seals, magnetic seals, and infill seals. Better rigidity and clarity.
- Stock lengths: 2500mm (standard) or 3000mm (UV-rated variants for 10-12mm glass)
- Colours: Clear (default), Black, White (magnetic only), Brown (magnetic only)