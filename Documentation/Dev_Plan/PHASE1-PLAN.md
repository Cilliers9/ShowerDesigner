# Phase 1: Enhanced Models - Implementation Plan

## Overview

This phase focuses on improving the parametric models to create production-ready shower enclosure designs with proper glass panel systems, door mechanisms, and hardware integration.

**Last Updated:** 2026-03-01

---

## Status Summary

| Section | Area | Status | Completion |
|---------|------|--------|------------|
| 1.1 | GlassPanel class | ✓ Complete | 100% |
| 1.2 | Glass Properties Database | ✓ Complete | 100% |
| 1.3 | Panel Spacing & Constraints | ◐ In Progress | 60% |
| 1.4 | Fixed Panel Implementation | ✓ Complete | 100% |
| 2.1 | Hinged Door System | ✓ Complete | 100% |
| 2.2 | Sliding Door System | ◐ In Progress | 95% |
| 2.3 | Bi-Fold Door System | ✓ Complete | 100% |
| 3.1 | Hinge Catalog | ✓ Complete | 100% |
| 3.2 | Handle and Knob Library | ✓ Complete | 100% |
| 3.3 | Support Bars and Braces | ✓ Complete | 100% |
| 3.4 | Seals and Gaskets (Seal Selection Rules) | ✓ Complete | 100% |
| 3.5 | Clamp Catalog | ✓ Complete | 100% |
| 3.6 | Seal Deduction System | ◐ In Progress | 90% |
| 4.1 | Update CornerEnclosure | ◐ In Progress | 65% |
| 4.2 | Update AlcoveEnclosure | ◐ In Progress | 50% |
| 4.3 | Update WalkInEnclosure | ◐ In Progress | 50% |
| 4.4 | Update CustomEnclosure | ◐ In Progress | 50% |

**Overall Phase 1 Completion: ~86%**

### Architecture Note
All models have been refactored from standalone `Part::FeaturePython` to an `App::Part` assembly architecture.
Each panel/door/enclosure is an `App::Part` container with a hidden `Part::FeaturePython` controller
(`AssemblyBase.py`), a `VarSet` for user-facing properties, and individual child objects (glass, hardware)
with their own view providers. See `Documentation/Dev_Plan/ASSEMBLY-PLAN.MD` for rationale.

---

## Task Breakdown

### 1. Glass Panel System Enhancement

#### 1.1 Separate Panel Objects -- ✓ COMPLETE
**Priority:** High
**Estimated Effort:** Medium
**Dependencies:** None

**Objectives:**
- Create individual `GlassPanel` class as standalone parametric object
- Support for multiple panels per enclosure
- Panel-to-panel relationships (parent/child hierarchy)

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Models/GlassPanel.py`

```python
class GlassPanel:
    """Individual glass panel with properties"""
    
    Properties:
    - Width: App::PropertyLength
    - Height: App::PropertyLength
    - Thickness: App::PropertyLength (6mm, 8mm, 10mm, 12mm)
    - GlassType: App::PropertyEnumeration (Clear, Frosted, Bronze, Grey, Reeded, Low-Iron)
    - EdgeFinish: App::PropertyEnumeration (Bright_Polish, Dull_Polish)
    - TemperType: App::PropertyEnumeration (Tempered, Laminated, None)
    - Position: App::PropertyVector
    - Rotation: App::PropertyAngle
    - AttachmentType: App::PropertyEnumeration (Fixed, Hinged, Sliding)
```

**Integration:**
- Update existing models to use GlassPanel objects
- Add panel management methods: `addPanel()`, `removePanel()`, `getPanels()`
- Implement panel constraints (spacing, alignment)

**Testing:**
- Create standalone panel
- Attach panel to enclosure
- Verify parameter updates
- Test different glass types

---

#### 1.2 Glass Properties Database -- ✓ COMPLETE
**Priority:** Medium
**Estimated Effort:** Low
**Dependencies:** 1.1

**Objectives:**
- Standardized glass specifications
- Weight calculations
- Safety factor validation

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Data/GlassSpecs.py`

```python
GLASS_SPECS = {
    "6mm": {"weight_kg_m2": 15, "min_panel_size": 300, "max_panel_size": 2400},
    "8mm": {"weight_kg_m2": 20, "min_panel_size": 300, "max_panel_size": 3000},
    "10mm": {"weight_kg_m2": 25, "min_panel_size": 400, "max_panel_size": 3600},
    "12mm": {"weight_kg_m2": 30, "min_panel_size": 400, "max_panel_size": 3600}
}

GLASS_TYPES = {
    "Clear": {"light_transmission": 0.90, "opacity": 0.2, "color": (0.7, 0.9, 1.0)},
    "Frosted": {"light_transmission": 0.75, "opacity": 0.8, "color": (0.7, 0.9, 1.0)},
    "Bronze": {"light_transmission": 0.60, "opacity": 0.3, "color": (0.804, 0.498, 0.196)},
    "Grey": {"light_transmission": 0.60, "opacity": 0.3, "color": (0.25, 0.25, 0.25)},
    "Reeded": {"light_transmission": 0.70, "opacity": 0.6, "color": (0.7, 0.9, 1.0)},
    "Low-Iron": {"light_transmission": 0.92, "opacity": 0.0, "color": (1.0, 1.0, 1.0)}
}
```

**Features:**
- Automatic weight calculation per panel
- Validation against max dimensions
- Visual representation of glass type (transparency/color)

---

#### 1.3 Panel Spacing and Constraints
**Priority:** High
**Estimated Effort:** Medium
**Dependencies:** 1.1

**Objectives:**
- Minimum spacing requirements between panels
- Automatic alignment tools
- Constraint visualization
- Distinct gap rules for panel-to-wall/floor vs panel-to-panel (for seal fitment)

**What was implemented:**

**File:** `freecad/ShowerDesigner/Data/PanelConstraints.py`
- Constants: `MIN_PANEL_SPACING`, `MAX_PANEL_SPACING`, `STANDARD_SPACING`, `MIN_WALL_CLEARANCE`, `STANDARD_WALL_CLEARANCE`
- `validateSpacing(panel1, panel2)` -- bounding-box gap check with min/max validation
- `checkPanelCollision(panel1, panel2)` -- overlap detection
- `autoAlign(panels, alignment_type)` -- 6 alignment modes (top, bottom, center_vertical, left, right, center_horizontal)
- `distributeEvenly(panels, total_width, axis)` -- equal spacing distribution with range warnings
- `getPanelGap(panel1, panel2, axis)` -- single-axis gap measurement
- `snapToGrid(panel, grid_size)` -- grid snapping utility

**Remaining -- Gap Rules for Seal Fitment:**

Panel spacing must satisfy specific gap ranges so that seals can physically fit the gap.
These are hard constraints driven by the seal products in `CATALOGUE_SEAL_SPECS`.

| Gap Type | Min (mm) | Max (mm) | Purpose |
|----------|----------|----------|---------|
| Panel-to-wall | 2 | 10 | Seal fitment between glass edge and wall surface |
| Panel-to-floor | 2 | 10 | Seal fitment between glass bottom edge and floor/tray |
| Panel-to-panel | 2 | 2 | Seal fitment between adjacent glass panel edges |

Implementation tasks:

1. **Update constants in `PanelConstraints.py`** (data layer, no FreeCAD imports for constants)
   ```python
   # Panel-to-wall and panel-to-floor gap (for seal fitment)
   MIN_WALL_FLOOR_GAP = 2   # mm -- minimum gap
   MAX_WALL_FLOOR_GAP = 10  # mm -- seal cannot span more than 10mm

   # Panel-to-panel gap (for inter-panel seals)
   PANEL_TO_PANEL_GAP = 2   # mm -- fixed gap for panel-to-panel seals
   ```
   Note: `MIN_WALL_CLEARANCE` has been updated to 2mm to match `MIN_WALL_FLOOR_GAP`.

2. **Add validation functions in `PanelConstraints.py`**
   ```python
   def validateWallGap(gap_mm):
       """Validate panel-to-wall or panel-to-floor gap is 2-10mm for seal fitment."""

   def validatePanelToFloorGap(gap_mm):
       """Validate panel-to-floor gap is 2-10mm for seal fitment."""

   def validatePanelToPanelGap(gap_mm):
       """Validate panel-to-panel gap is exactly 2mm for inter-panel seals."""
   ```

3. **Link gap validation to seal selection in `HardwareSpecs.py`**
   - The existing `selectSeal(location, glass_thickness, gap)` function currently ignores the `gap` parameter. It must be updated to filter `CATALOGUE_SEAL_SPECS` entries whose dimensions are compatible with the actual gap.
   - Add a `selectSealForGap(gap_mm, location, glass_thickness)` function that returns only seals whose profile fits within the specified gap.

4. **Integrate gap validation into enclosure assemblies**
   - FixedPanel: validate wall and floor gaps when clamp offsets are set
   - Enclosure models (Corner, Alcove, WalkIn, Custom): validate panel-to-panel gaps when panels are placed adjacent to each other

**Methods (already implemented):**
```python
def validateSpacing(panel1, panel2):
    """Check if spacing between panels is within acceptable range"""

def autoAlign(panels, alignment_type):
    """Align panels: 'top', 'bottom', 'center'"""

def distributeEvenly(panels, total_width):
    """Distribute panels evenly across width"""
```

---

### 1.4 Fixed Panel Implementation -- ✓ COMPLETE
**Priority:** High
**Estimated Effort:** Medium
**Dependencies:** 1.1

**Objectives:**
- Parametric fixed panel with wall and floor fixings.
- Fixing hardware: None, Channels or Clamps

**What was implemented:**

**File:** `freecad/ShowerDesigner/Models/FixedPanel.py`
- `class FixedPanelAssembly(AssemblyController)` -- App::Part assembly containing glass + mounting hardware
- VarSet properties for wall/floor hardware type, clamp count, clamp placement
- `SealDeduction` property (read-only) -- set by parent enclosure to deduct glass on the free edge when adjacent door uses a closing seal (see Task 3.6)
- Automatic clamp spacing calculation with configurable offsets
- Single-clamp configuration support (centered placement)
- Full integration with `Clamp.py` shape builders and `HardwareSpecs.py` specs

**Features:**
- Automatic WallClamp spacing calculation (Default: 300mm from top and bottom)
- Automatic FloorClamp spacing calculation (Default: 75mm from left and right)
- Single-clamp centered placement fix (commit e925695)
- Seal deduction applied to free (non-wall-mounted) edge based on `WallMountEdge`

**Testing:**
- Test with different panel heights
- Validate clamp placement for 1-clamp and 2-clamp configurations

---

### 2. Door Implementation

#### 2.1 Hinged Door System -- ✓ COMPLETE
**Priority:** High
**Estimated Effort:** High
**Dependencies:** 1.1

**Objectives:**
- Parametric hinged door with swing direction
- Hinge placement calculation
- Opening angle visualization

**What was implemented:**

**File:** `freecad/ShowerDesigner/Models/HingedDoor.py`
- `class HingedDoorAssembly(AssemblyController)` -- App::Part assembly containing glass + hinges + handle
- VarSet properties: Width, Height, Thickness, SwingDirection, HingeCount, OpeningAngle, HandleType, MountingVariant, DoorSeal, ClosingAgainst
- Mounting variants: Wall-to-Glass, Glass-to-Glass, Glass-to-Glass-90 (via `DOOR_MOUNTING_VARIANTS`)
- Bevel hinge 3D model integration (commit 2f7d3f6)
- Automatic hinge placement from `HINGE_PLACEMENT_DEFAULTS`
- Seal deduction applied to handle-side glass edge (see Task 3.6)

**Features:**
- Automatic hinge spacing calculation
- Door weight calculation for hinge selection
- Bevel hinge 3D shapes rendered per mounting variant
- Handle object as child assembly member

---

#### 2.2 Sliding Door System -- ◐ IN PROGRESS (95%)
**Priority:** High
**Estimated Effort:** High
**Dependencies:** 1.1

**Objectives:**
- Track-based sliding mechanism
- Multi-panel sliding doors

**What was implemented:**

**File:** `freecad/ShowerDesigner/Models/SlidingDoor.py`
- `class SlidingDoorAssembly(AssemblyController)` -- App::Part assembly containing glass + track + rollers + guides
- VarSet properties: Width, Height, Thickness, SliderSystem, TrackFinish, HandleType, DoorSeal, ClosingAgainst
- Per-system glass deduction logic via `_calculateGlassDeductions()` (see Task 3.6)
- Slide-direction-aware glass placement offsets

**Data specs** in `freecad/ShowerDesigner/Data/HardwareSpecs.py`:
- `SLIDER_SYSTEM_SPECS` -- 3 complete slider systems from catalogue:
  - Duplo (top-hung, single-track, 30kg capacity)
  - Edge Slider (top-hung, single-track, 50kg capacity)
  - City Slider (top-hung, single-track, 60kg capacity)
  - Each with track profiles, roller specs, bottom guides, floor guides, product codes
- `TRACK_PROFILES`, `ROLLER_SPECS`, `BOTTOM_GUIDE_SPECS`, `FLOOR_GUIDE_SPECS` -- Generic specs
- `CHANNEL_SPECS` -- Channel dimensions
- Helper functions: `validateSliderSystem()`, `getSliderSystemsByType()`, `lookupSliderProductCode()`

**Remaining:**
- Slider system 3D geometry refinements in progress

---

#### 2.3 Bi-Fold Door System -- ✓ COMPLETE
**Priority:** Medium
**Estimated Effort:** Medium
**Dependencies:** 1.1, 2.1

**Objectives:**
- Folding panel mechanism
- Pivot point calculation
- Folded position visualization

**What was implemented:**

**File:** `freecad/ShowerDesigner/Models/BiFoldDoor.py`
- `class BiFoldDoorAssembly(AssemblyController)` -- App::Part assembly containing 2 glass panels + hinges + handle
- VarSet properties: Width, Height, Thickness, FoldDirection, HingeSide, FoldAngle, SillPlate, DoorSeal, ClosingAgainst
- Monza bi-fold hinge integration (commit 3432104)
- Auto-calculated: PanelWidth, FoldedWidth, OpeningWidth, ClearanceDepth, GlassWidth, GlassHeight
- `MONZA_BIFOLD_HINGE_SPECS` and `MONZA_PAIRING` in HardwareSpecs.py
- `_calculateGlassDeductions()` -- per-edge deduction logic with hinge-side-aware panel placement (see Task 3.6)

**Calculations:**
- Panel width = Total Width / 2
- Pivot point offset (inline = 0mm vs offset = 15mm)
- Folded width = PanelWidth + Thickness [+ PivotOffset]
- Opening width = Width - FoldedWidth
- Clearance depth = PanelWidth + PivotOffset
- Glass deductions applied per edge (wall side, free side, top, bottom) based on hardware and seal type

---

### 3. Hardware Library

#### 3.1 Hinge Catalog -- ✓ COMPLETE
**Priority:** High
**Estimated Effort:** Medium
**Dependencies:** 2.1

**Objectives:**
- Standard hinge types and specifications
- Load capacity calculations
- Automatic hinge selection

**What was implemented:**

**Data specs** in `freecad/ShowerDesigner/Data/HardwareSpecs.py`:
- `HINGE_SPECS` -- 3 generic types (standard G2G, heavy duty wall, standard wall)
- `BEVEL_HINGE_SPECS` -- 10 Bevel-range hinges from catalogue (90/135 wall-to-glass, 90/135/180 glass-to-glass, 360 pivots, tee)
- `BIFOLD_HINGE_SPECS` -- Bi-fold pivot hinge specs
- `MONZA_BIFOLD_HINGE_SPECS` -- 2 Monza hinges (90 wall-to-glass, 180 glass-to-glass) with product codes
- `DOOR_MOUNTING_VARIANTS` -- Wall-to-Glass, Glass-to-Glass, Glass-to-Glass-90 variant definitions
- `HINGE_PLACEMENT_DEFAULTS` -- Standard offsets for 2-hinge and 3-hinge setups
- Helper: `getHingeModelsForVariant(variant)`

**3D model** in `freecad/ShowerDesigner/Models/Hinge.py`:
- `createHingeShape()` -- Generic parametric hinge shape
- `createBevelHingeShape()` -- Bevel hinge 3D geometry from catalogue dimensions
- `createMonzaWallHingeShape()` / `createMonzaFoldHingeShape()` -- Monza hinge 3D shapes
- `class Hinge` -- `Part::FeaturePython` with HingeType, MountingType, Finish, GlassThickness
- `createHinge()` -- Factory function

**Validation functions** in HardwareSpecs.py:
- `selectHinge(door_weight, glass_thickness)`
- `calculateHingePlacement(door_height, count, offset_top, offset_bottom)`
- `validateHingeLoad(hinge_type, weight, count)`

---

#### 3.2 Handle and Knob Library -- ✓ COMPLETE
**Priority:** Medium
**Estimated Effort:** Low
**Dependencies:** None

**Objectives:**
- Standard handle types
- Ergonomic placement
- ADA compliance options

**What was implemented:**

**Data specs** in `freecad/ShowerDesigner/Data/HardwareSpecs.py`:
- `HANDLE_SPECS` -- 3 generic types (towel bar, pull handle, knob)
- `CATALOGUE_HANDLE_SPECS` -- 18 catalogue entries across categories:
  - Knobs (3): mushroom, groove, square (back-to-back)
  - Pull handles (2): round, square
  - Towel rails (5): round/square finnial, round/square knob, bow handle
  - Flush handles (2): with plate, without plate
  - Custom kits (5): towel rail, glass towel rail, knob kit, double rail, pull handle
  - Each with product codes, dimensions, material/finish options
- `CATALOGUE_HANDLE_FINISHES` -- 7 available finishes
- `HANDLE_PLACEMENT_DEFAULTS` -- Standard height, offset, and ADA height ranges

**3D model** in `freecad/ShowerDesigner/Models/Handle.py`:
- `createHandleShape(handle_type, length, position)` -- Parametric handle geometry
- `class Handle` -- `Part::FeaturePython` with HandleType, Length, Finish
- `createHandle()` -- Factory function

**Validation functions** in HardwareSpecs.py:
- `validateHandlePlacement(handle_height, ada_required)`
- `getHandleModelsForCategory(category)`
- `lookupHandleProductCode(code)`

---

#### 3.3 Support Bars and Braces -- ✓ COMPLETE
**Priority:** Medium
**Estimated Effort:** Medium
**Dependencies:** 1.1

**Objectives:**
- Structural support for large panels
- Wall-to-glass bracing
- Ceiling support for walk-ins

**What was implemented:**

**Data specs** in `freecad/ShowerDesigner/Data/HardwareSpecs.py`:
- `SUPPORT_BAR_SPECS` -- 4 types (Horizontal, Diagonal, Ceiling, Corner)
- `SUPPORT_BAR_RULES` -- Auto-requirement thresholds (width > 1000mm, height > 2400mm)
- `requiresSupportBar(panel_width, panel_height, panel_type)` -- Validation function

**3D model** in `freecad/ShowerDesigner/Models/SupportBar.py`:
- `createSupportBarShape(bar_type, length, diameter)` -- Parametric bar geometry
- `class SupportBar` -- `Part::FeaturePython` with BarType, Length, Diameter, Finish
- `createSupportBar()` -- Factory function

**Remaining:**
- Catalogue-level support bar specs (product codes, detailed dimensions) not yet added

---

#### 3.4 Seals and Gaskets -- ✓ COMPLETE
**Priority:** Medium
**Estimated Effort:** Low
**Dependencies:** 1.1, 2.1, 2.2

**Objectives:**
- Water seal visualization
- Seal type selection per location with catalogue seal names
- Gap calculation

**What was implemented:**

**Data specs** in `freecad/ShowerDesigner/Data/SealSpecs.py` (extracted from HardwareSpecs.py):
- `SEAL_SPECS` -- 3 generic types (door sweep, vertical seal, magnetic seal)
- `SEAL_COLOURS` -- 4 available colours (Clear, Black, White, Brown)
- `SEAL_MATERIALS` -- PVC (flexible), PC (polycarbonate rigid)
- `CATALOGUE_SEAL_SPECS` -- 18 seal types across 6 categories from catalogue pp. 35-42:
  - Soft lip (5): centre lip, 180/90/135 soft lip, 180 long lip
  - Bubble (1): bubble seal (8/12/24mm variants)
  - Bottom (2): wipe seal with bubble, drip & wipe seal
  - Hard lip (6): 180/135/90 hard lip, 90 extended, 90 hard/soft, double hard lip H
  - Magnetic (3): 90/180 magnetic, 180 flat magnetic, 135 magnetic
  - Infill (1): 180 glass-to-glass infill seal
  - Each with product codes, glass thickness ranges, PVC/PC material, clear/black colour options
- Reference document: `Resources/Documents/seals-spec.md`

**Per-location seal option lists** in `freecad/ShowerDesigner/Data/SealSpecs.py` (added commit 668f024):
- 10 per-model seal option lists using catalogue seal names:
  - `FIXED_PANEL_WALL_SEAL_OPTIONS`, `FIXED_PANEL_FLOOR_SEAL_OPTIONS`, `FIXED_PANEL_PANEL_SEAL_OPTIONS`
  - `HINGED_DOOR_HINGE_SIDE_SEAL_OPTIONS`, `HINGED_DOOR_FLOOR_SEAL_OPTIONS`, `HINGED_DOOR_CLOSING_SEAL_OPTIONS`
  - `SLIDING_DOOR_FLOOR_SEAL_OPTIONS`, `SLIDING_DOOR_CLOSING_SEAL_OPTIONS`, `SLIDING_DOOR_BACK_SEAL_OPTIONS`
  - `BIFOLD_DOOR_FLOOR_SEAL_OPTIONS`, `BIFOLD_DOOR_WALL_HINGE_SEAL_OPTIONS`, `BIFOLD_DOOR_FOLD_HINGE_SEAL_OPTIONS`
- `_SEAL_NAME_TO_DEDUCTION_KEY` -- Mapping from catalogue seal names to legacy deduction keys
- `CORNER_DOOR_CONSTRAINTS` updated to use catalogue seal names

**Model integration** (commit 668f024):
- `FixedPanel.py`: Added `WallSeal`, `FloorSeal`, `PanelSeal` enum properties using catalogue names
- `HingedDoor.py`: Replaced single `DoorSeal` with `HingeSideSeal`, `FloorSeal`, `ClosingSeal`
- `SlidingDoor.py`: Replaced single `DoorSeal` with `FloorSeal`, `ClosingSeal`, `BackSeal`
- `BiFoldDoor.py`: Replaced single `DoorSeal` with `FloorSeal`, `WallHingeSeal`, `FoldHingeSeal`
- `CornerEnclosure.py`: Updated `DoorSeal` references to `ClosingSeal`, magnet seal check updated for catalogue names
- `getDoorSealDeduction()` updated to accept both legacy and catalogue seal names via `_SEAL_NAME_TO_DEDUCTION_KEY` mapping

**Helper functions** in SealSpecs.py:
- `selectSeal(location, glass_thickness, gap)` -- legacy seal selection
- `getSealsByCategory(category)`
- `getSealsByAngle(angle)`
- `getSealsByLocation(location)`
- `lookupSealProductCode(code)`
- `getDoorSealDeduction(seal_type, closing_against)` -- now accepts both legacy and catalogue names

**Architecture note:** Seal data was extracted from `HardwareSpecs.py` into its own
`Data/SealSpecs.py` module to keep the data layer manageable. The module follows the
same pure-Python pattern (no FreeCAD imports). Door seal deduction logic and
enclosure constraint data also live in this file (see Task 3.6).

**Remaining:**
- No `Models/Seal.py` yet -- 3D geometry model for seal visualization not created (deferred to Phase 2)

---

#### 3.5 Clamp Catalog -- ✓ COMPLETE
**Priority:** High
**Estimated Effort:** Medium
**Dependencies:** 1.4

**Objectives:**
- Standard clamp types for fixed panel mounting
- Wall clamp and floor clamp specifications
- Load capacity and glass thickness compatibility
- Automatic clamp selection based on panel requirements

**What was implemented:**

**Data specs** in `freecad/ShowerDesigner/Data/HardwareSpecs.py`:
- `CLAMP_SPECS` -- 7 generic types: U_Clamp, L_Clamp, 90DEG_Clamp, 180DEG_Clamp, 135DEG_G2G_Clamp, Glass_Clamp, Floor_Clamp (with dimensions, load capacity, glass thickness range)
- `BEVEL_CLAMP_SPECS` -- 13 Bevel-range catalogue clamps:
  - Wall-to-Glass S/S 304 (3): 90 U-clamp, 90 L-clamp, 180
  - Glass-to-Glass S/S 304 (4): 90, 135, 180, 90 tee
  - Wall-to-Glass Brass (3): 90 U-clamp, 90 L-clamp, 180
  - Glass-to-Glass Brass (3): 90, 135, 180
  - Each with product codes, dimensions, material/finish, glass thickness ranges
- `CLAMP_PLACEMENT_DEFAULTS` -- Standard offsets for wall and floor clamps

**3D model** in `freecad/ShowerDesigner/Models/Clamp.py`:
- Shape builders (9 total):
  - `_buildGlassClamp()` -- Standard glass clamp
  - `_buildUClamp()` -- U-channel wall clamp
  - `_buildLClamp()` -- L-bracket wall clamp
  - `_build180degClamp()` -- 180-degree inline clamp
  - `_build135degClamp()` -- 135-degree angled clamp
  - `_build90degG2GClamp()` -- 90-degree glass-to-glass clamp
  - `_build180degG2GClamp()` -- 180-degree glass-to-glass clamp
  - `_build135degG2GClamp()` -- 135-degree glass-to-glass clamp
  - `_build90degTeeClamp()` -- 90-degree tee junction clamp
  - `_buildPlaceholderBox()` -- Fallback placeholder
- `createClampShape(clamp_type)` -- Dispatches to correct builder
- `class Clamp` -- `Part::FeaturePython` with ClampType, MountingType, Finish, GlassThickness
- `createClamp()` -- Factory function

**Validation functions** in HardwareSpecs.py:
- `selectClamp(panel_weight, glass_thickness, mounting_type)`
- `calculateClampPlacement(total_length, count, offset_start, offset_end)`
- `validateClampLoad(clamp_type, weight, count)`

**Integration with FixedPanel:** Fully integrated -- FixedPanel assembly auto-places clamps based on panel dimensions

---

#### 3.6 Seal Deduction System -- ◐ IN PROGRESS (85%)
**Priority:** High
**Estimated Effort:** Medium
**Dependencies:** 3.4, 2.1, 2.2, 2.3, 1.4

**Objectives:**
- Glass width/height deductions driven by closing seal type
- Per-door-type seal selection with appropriate options
- Enclosure-level constraint enforcement (which seals and mounting types are valid)
- Return panel deduction when adjacent door uses magnet seal

**What was implemented:**

**Data layer** in `freecad/ShowerDesigner/Data/SealSpecs.py`:
- `DOOR_SEAL_DEDUCTIONS` -- Width deduction (mm) per seal type applied to the handle side of door glass; magnet seals vary by what the door closes against (Inline Panel: 24mm, Return Panel: 10mm, Wall: 34mm), other seal types are flat values (Hard Lip: 5mm, Bubble: 7mm, Side Lip: 5mm, No Seal: 3mm)
- `HINGED_DOOR_SEAL_OPTIONS` -- 5 seal types for hinged/bi-fold doors (No Seal, Magnet, Hard Lip, Bubble, Side Lip)
- `SLIDING_DOOR_SEAL_OPTIONS` -- 3 seal types for sliding doors (No Seal, Magnet, Bubble)
- `CLOSING_AGAINST_OPTIONS` -- 3 targets (Inline Panel, Return Panel, Wall)
- `CORNER_DOOR_CONSTRAINTS` -- Constraint dict keyed by whether DoorSide == HingeSide; each entry defines allowed `mounting_types`, `seal_options`, and `closing_against` value
- `getDoorSealDeduction(seal_type, closing_against)` -- Returns mm deduction for given seal/target combination
- `getCornerDoorConstraints(closes_on_panel)` -- Returns constraint dict for corner enclosure door
- `getReturnPanelMagnetDeduction(glass_thickness)` -- Returns fixed panel deduction (10 + glass_thickness mm) when adjacent door uses magnet seal

**HingedDoor integration** in `freecad/ShowerDesigner/Models/HingedDoor.py`:
- New VarSet properties: `DoorSeal` (enum, "Seal" group), `ClosingAgainst` (enum, "Seal" group)
- `execute()` applies `getDoorSealDeduction()` to the handle-side glass edge (opposite hinge side)

**BiFoldDoor integration** in `freecad/ShowerDesigner/Models/BiFoldDoor.py`:
- New VarSet properties: `DoorSeal`, `ClosingAgainst`, `SillPlate` (bool)
- New calculated properties: `GlassWidth`, `GlassHeight` (read-only)
- New `_calculateGlassDeductions()` method with per-edge deduction logic
- Panel placement now hinge-side-aware with proper X/Z offsets

**SlidingDoor integration** in `freecad/ShowerDesigner/Models/SlidingDoor.py`:
- New VarSet properties: `DoorSeal` (uses `SLIDING_DOOR_SEAL_OPTIONS`), `ClosingAgainst`
- New `_calculateGlassDeductions()` method accounting for per-system top/bottom clearances:
  - Duplo: floor clearance from `door_panel_floor_clearance`
  - Edge Slider: floor clearance from `door_floor_clearance`
  - City Slider: top deduction from roller variant `door_top_deduction`, bottom from `door_bottom_deduction`
- Seal deduction applied to handle side (opposite slide direction)
- Glass placement offset based on `SlideDirection`

**FixedPanel integration** in `freecad/ShowerDesigner/Models/FixedPanel.py`:
- New VarSet property: `SealDeduction` (read-only, set by parent enclosure)
- Deduction applied to the free (non-wall-mounted) edge based on `WallMountEdge`

**CornerEnclosure integration** in `freecad/ShowerDesigner/Models/CornerEnclosure.py`:
- Imports `getCornerDoorConstraints()` and `getReturnPanelMagnetDeduction()` from SealSpecs
- New `_applyDoorConstraints(door_vs, closes_on_panel)` method dynamically filters the nested door's `MountingType` and `DoorSeal` enums based on corner geometry
- New `_filterEnum(varset, prop, allowed)` helper for safe enum list replacement
- `execute()` calculates `fixed_panel_seal_ded` and propagates to FixedPanel's `SealDeduction` when magnet seal is active
- Bug fix: fixed panel placement vector corrected (removed erroneous thickness Y-offset)
- Bug fix: door width now properly subtracts glass thickness from depth

**ChildProxies updates** in `freecad/ShowerDesigner/Models/ChildProxies.py`:
- Minor refinements to child proxy classes supporting the seal deduction flow

**Remaining:**
- AlcoveEnclosure seal/constraint integration (same pattern as CornerEnclosure)
- WalkInEnclosure and CustomEnclosure seal deduction propagation
- Seal deduction validation (warn if deduction exceeds panel width)

---

### 4. Enhanced Enclosure Models

#### 4.1 Update CornerEnclosure -- ◐ IN PROGRESS (65%)
**Priority:** High
**Estimated Effort:** Medium
**Dependencies:** 1.1, 2.1, 3.6

**What was implemented:**
- `class CornerEnclosureAssembly(AssemblyController)` -- App::Part assembly
- Contains nested App::Part children: BackPanel (FixedPanel) + SidePanel (FixedPanel, HingedDoor, or SlidingDoor)
- VarSet with DoorType selection, per-panel dimensions
- Door constraint enforcement via `_applyDoorConstraints()` -- dynamically filters nested door's MountingType and DoorSeal enums based on whether door closes against return panel or wall (uses `CORNER_DOOR_CONSTRAINTS` from SealSpecs)
- Fixed panel seal deduction propagation -- when door uses magnet seal, FixedPanel's `SealDeduction` is set via `getReturnPanelMagnetDeduction(glass_thickness)`
- Bug fix: fixed panel placement vector corrected (removed erroneous thickness Y-offset)
- Bug fix: door width now subtracts glass thickness from depth for correct glass-to-glass fit
- Corner layout research: `Resources/Documents/Possible corner enclosure layout - Sheet1.csv`

**Remaining:**
- Additional door configuration options (left/right variants)
- Three-panel layout option
- Hardware property refinement

---

#### 4.2 Update AlcoveEnclosure -- ◐ IN PROGRESS (50%)
**Priority:** High
**Estimated Effort:** Medium
**Dependencies:** 1.1, 2.1, 2.2

**What was implemented:**
- `class AlcoveEnclosureAssembly(AssemblyController)` -- App::Part assembly
- Contains nested App::Part Door child (HingedDoor, SlidingDoor, or BiFoldDoor)
- VarSet with DoorType, Width, Height

**Remaining:**
- Fixed side panel support
- Return panel option
- Proper track placement refinement for sliders

---

#### 4.3 Update WalkInEnclosure -- ◐ IN PROGRESS (50%)
**Priority:** High
**Estimated Effort:** Medium
**Dependencies:** 1.1, 3.3

**What was implemented:**
- `class WalkInEnclosureAssembly(AssemblyController)` -- App::Part assembly
- Contains nested App::Part Panel (FixedPanel assembly)
- VarSet with Width, Height, support bar options

**Remaining:**
- Multiple panel configurations (Double-L, Double-Parallel)
- Ceiling-mounted support option
- Support bar height configuration

---

#### 4.4 Update CustomEnclosure -- ◐ IN PROGRESS (50%)
**Priority:** Low
**Estimated Effort:** High
**Dependencies:** All above

**What was implemented:**
- `class CustomEnclosureAssembly(AssemblyController)` -- App::Part assembly
- Dynamic panel/door addition via `addPanel()` method
- VarSet with configurable panel roles

**Remaining:**
- Free-form panel placement UI
- Mix of door types in single enclosure
- Advanced hardware placement logic

---

## Implementation Order

### Sprint 1 (Week 1-2): Core Glass System -- ✓ COMPLETE
1. ✓ Create GlassPanel class (1.1)
2. ✓ Implement glass specs database (1.2)
3. ✓ Add panel spacing/constraints (1.3)
4. ◐ Update CornerEnclosure to use GlassPanel (4.1) -- assembly refactored, features remain

### Sprint 2 (Week 3-4): Door Systems -- ✓ COMPLETE
1. ✓ Implement HingedDoor (2.1) -- with Bevel hinge integration
2. ◐ Implement SlidingDoor (2.2) -- 3 slider systems, geometry refinements remain
3. ◐ Update AlcoveEnclosure (4.2) -- assembly refactored, features remain
4. ✓ Testing and refinement

### Sprint 3 (Week 5-6): Hardware Integration -- ✓ COMPLETE
1. ✓ Create Hinge catalog and class (3.1) -- Bevel + Monza + generic specs + 3D models
2. ✓ Create Handle library (3.2) -- 18 catalogue entries + 3D model
3. ◐ Implement SupportBar (3.3) -- model complete, catalogue specs pending
4. ✓ Create Clamp catalog and class (3.5) -- 7 generic + 13 Bevel clamps + 9 shape builders
5. ◐ Update WalkInEnclosure (4.3) -- assembly refactored, features remain

### Sprint 4 (Week 7-8): Finalization -- ◐ IN PROGRESS
1. ✓ Implement BiFoldDoor (2.3) -- with Monza hinges + glass deductions + SillPlate
2. ✓ Add Seals system (3.4) -- data specs (18 types) + per-location seal selection with catalogue names on all models
3. ◐ Seal Deduction System (3.6) -- data layer + door integration complete, enclosure propagation in progress
4. ◐ Update CustomEnclosure (4.4) -- assembly refactored, features remain
5. ○ Documentation and examples -- not started

### Additional completed work (not originally planned):
- ✓ Assembly architecture refactor (all models migrated to App::Part pattern)
- ✓ `AssemblyBase.py` -- Reusable base class for assembly controllers
- ✓ `ChildProxies.py` -- Shared child proxy classes for assembly members
- ✓ `HardwareViewProvider.py` / `GlassPanelViewProvider.py` -- Dedicated view providers
- ✓ `SLIDER_SYSTEM_SPECS` -- 3 complete slider system specs from catalogue
- ✓ `CATALOGUE_SEAL_SPECS` -- 18 seal types with product codes
- ✓ `CATALOGUE_HANDLE_SPECS` -- 18 handle types with product codes
- ✓ `BEVEL_CLAMP_SPECS` -- 13 Bevel clamp entries with product codes
- ✓ Door mounting variants system (`DOOR_MOUNTING_VARIANTS`)
- ✓ `Data/SealSpecs.py` -- Seal data extracted from HardwareSpecs into dedicated module
- ✓ Per-location seal selection rules -- 10 option lists with catalogue seal names across all models
- ✓ `_SEAL_NAME_TO_DEDUCTION_KEY` -- Backward-compatible mapping from catalogue to legacy seal names
- ◐ `DOOR_SEAL_DEDUCTIONS` + `CORNER_DOOR_CONSTRAINTS` -- Seal deduction and enclosure constraint system
- ◐ Glass deduction methods added to HingedDoor, BiFoldDoor, SlidingDoor, FixedPanel
- ◐ CornerEnclosure door constraint filtering and fixed panel seal deduction propagation

---

## Success Criteria

### Functionality
- [x] Create individual glass panels with properties
- [x] Hinged doors open/close visually in 3D
- [x] Sliding doors show track system
- [x] Automatic hinge placement based on door weight
- [x] Support bars calculated for large panels
- [x] All enclosure types use new panel system (assembly architecture)

### Quality
- [x] All models follow LGPL license headers
- [ ] Code formatted with Black
- [ ] No Ruff linting errors
- [ ] Documentation for each new class
- [ ] Example files for each door type

### User Experience
- [x] Properties grouped logically (via VarSet in assemblies)
- [ ] Tooltips explain each parameter
- [x] Models update in real-time
- [x] Reasonable default values
- [ ] Validation prevents invalid configurations

---

## Testing Strategy

### Unit Testing
- Test each component in isolation
- Verify property constraints
- Check geometry generation

### Integration Testing
- Test complete enclosures
- Verify hardware placement
- Check panel relationships

### Manual Testing in FreeCAD
- Create each enclosure type
- Modify all properties
- Export to STEP format
- Visual inspection of hardware

---

## Documentation Requirements

### Code Documentation
- Docstrings for all classes and methods
- Inline comments for complex calculations
- Type hints for all functions

### User Documentation
- Update `Documentation/Usage/` with new features
- Create examples for each door type
- Hardware selection guide
- Glass specification guide

### Developer Documentation
- Architecture overview of panel system
- Hardware integration guide
- Adding new hardware types guide

---

## Future Enhancements (Phase 2+)

- Door animation (open/close with constraints)
- Collision detection between panels
- Stress analysis for large panels
- Custom hardware import (STEP files)
- Material cost estimation
- Installation sequence generator

---

## Notes

- Prioritize frameless shower compatibility (most common)
- All dimensions in millimeters
- Support both metric and imperial display
- Consider manufacturing tolerances (±2mm typical)
- Glass edge treatment affects dimensions
- Building codes vary by region (note in documentation)

---

## Resources

- [FreeCAD Part Module](https://wiki.freecad.org/Part_Module)
- [FeaturePython Objects](https://wiki.freecad.org/FeaturePython_Objects)
- Glass Industry Standards (GANA, SGCC, SESEMA)
- Shower Door Manufacturers' Specs
