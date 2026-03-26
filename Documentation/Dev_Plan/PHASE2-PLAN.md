# Phase 2: Production-Ready Tools - Implementation Plan

## Overview

This phase transforms ShowerDesigner from a parametric modeling tool into a production-ready design
system. The focus is on output tools (cut lists, export, measurement), user-facing task panels for
guided configuration, and 3D seal visualization — everything needed to go from design to fabrication.

**Last Updated:** 2026-03-18

---

## Status Summary

| Section | Area | Status | Completion |
|---------|------|--------|------------|
| 1.1 | Cut List / Bill of Materials | ◐ In Progress | 85% |
| 1.2 | STEP/STL Batch Export | ◐ In Progress | 75% |
| 1.3 | Glass Order Drawings (TechDraw) | ○ Not Started | 0% |
| 1.4 | Measurement & Dimensioning | ◐ In Progress | 50% |
| 2.1 | Enclosure Creation Wizard | ○ Not Started | 0% |
| 2.2 | Hardware Selection Panel | ○ Not Started | 0% |
| 2.3 | Property Validation & Error Display | ○ Not Started | 0% |
| 2.4 | Custom Icons | ◐ In Progress | 55% |
| 3.1 | Seal 3D Visualization | ○ Not Started | 0% |
| 3.2 | Cost Estimation | ○ Not Started | 0% |

**Overall Phase 2 Completion: ~30%**

### Prerequisites
Phase 1 is ~95% complete. Key dependencies for remaining Phase 2 tasks:
- Enclosure assemblies (4.1–4.4) are working end-to-end — cut list extraction operational
- Seal deduction system (3.6) should be finalized for seal visualization
- Hardware specs catalogue is stable — BOM generation operational

---

## Task Breakdown

### 1. Production Output Tools

These three commands (`ShowerDesigner_Measure`, `ShowerDesigner_CutList`, `ShowerDesigner_Export`)
are now implemented in `Commands/__init__.py` with working functionality.

---

#### 1.1 Cut List / Bill of Materials -- ◐ IN PROGRESS (85%)
**Priority:** High
**Estimated Effort:** High
**Dependencies:** Phase 1 enclosures (4.1–4.4), HardwareSpecs

**Objectives:**
- Extract all glass dimensions, hardware items, and quantities from any enclosure assembly
- Generate a structured BOM with product codes from the catalogue
- Output as in-app table, CSV, and clipboard-ready format

**What was implemented:**

**File:** `freecad/ShowerDesigner/Data/CutList.py` (pure Python, no FreeCAD imports)
- `CutListItem` dataclass with category, component, description, product_code, dimensions, quantity, unit, notes
- `aggregateItems()` -- groups identical items and sums quantities
- `toCSV()` -- CSV string output

**File:** `freecad/ShowerDesigner/Models/CutListExtractor.py`
- Full tree-walker that recursively extracts components from `App::Part` assemblies
- Identifies glass children, hardware children (hinges, handles, clamps, support bars)
- Reads dimensions from controller VarSet properties
- Maps hardware to catalogue entries via spec keys
- Seal BOM extraction added (commit 88827a0)

**File:** `freecad/ShowerDesigner/Gui/CutListDialog.py`
- Sortable QTableWidget with all BOM columns
- Copy-to-clipboard functionality
- CSV export with file picker

**File:** `freecad/ShowerDesigner/Commands/__init__.py` (CutListCommand)
- Collects selected or all top-level assemblies
- Runs `CutListExtractor`, aggregates items
- Prints console table summary
- Launches `CutListDialog` for interactive use

**File:** `freecad/ShowerDesigner/Tests/test_cut_list.py`
- Test coverage for cut list generation

**Remaining:**
- End-to-end testing with all enclosure types (WalkIn multi-panel, Custom)
- Verify seal items fully covered for all enclosure/door combinations

**Output columns:**
| # | Category | Component | Description | Product Code | W×H (mm) | Qty | Unit | Notes |
|---|----------|-----------|-------------|--------------|-----------|-----|------|-------|

**Testing:**
- Generate BOM from each enclosure type (Corner, Alcove, WalkIn, Custom)
- Verify product codes match `HardwareSpecs.py` catalogue entries
- Verify glass dimensions account for seal deductions
- Test CSV export round-trip (import into spreadsheet)

---

#### 1.2 STEP/STL Batch Export -- ◐ IN PROGRESS (75%)
**Priority:** Medium
**Estimated Effort:** Medium
**Dependencies:** None (uses FreeCAD built-in export)

**Objectives:**
- Export individual panels or complete enclosures as STEP, STL, or 3MF files
- Apply consistent naming conventions for manufacturing
- Support batch export (all panels as separate files)

**What was implemented:**

**File:** `freecad/ShowerDesigner/Gui/ExportDialog.py`
- Format selection: STEP, STL, 3MF, IGES, OBJ
- Output directory picker with custom prefix option
- Batch part table with checkboxes (select all/none)
- `exportShape()` handles per-format FreeCAD export calls
- `collectExportables()` walks assembly tree to find exportable parts
- Auto-naming with `{Enclosure}_{Component}_{WxHxT}` convention

**File:** `freecad/ShowerDesigner/Commands/__init__.py` (ExportCommand)
- Collects export targets from selection or active document
- Launches `ExportDialog` for interactive use

**Naming convention:**
```
{EnclosureType}_{Component}_{Width}x{Height}x{Thickness}.step
Example: CornerEnclosure_FixedPanel_800x2000x10.step
Example: CornerEnclosure_HingedDoor_700x2000x8.step
```

**Remaining:**
- Manifest file generation listing all exported parts
- Testing/validation that exports work correctly for all formats
- Fused assembly single-file export option

**Testing:**
- Export single panel → verify STEP opens in external CAD
- Batch export enclosure → verify all parts present
- Verify naming convention applied correctly
- Test with each supported format (STEP, STL, 3MF, IGES, OBJ)

---

#### 1.3 Glass Order Drawings (TechDraw)
**Priority:** High
**Estimated Effort:** High
**Dependencies:** Phase 1 enclosures (4.1–4.4), HardwareSpecs, Hinge/Clamp/Handle models

**Objectives:**
- Generate per-panel technical drawings for glass ordering/fabrication
- Show panel outline with all cutouts, notches, and holes dimensioned
- Use existing SVG templates from `Resources/Documents/Drawing templates/`
- Output as multi-page TechDraw document with assembly overview + individual panel sheets
- Export as PDF for glass supplier handoff

**Available Templates:**

| Template | Purpose |
|----------|---------|
| `A4_Portrait_Assembly.svg` | Assembly overview page (all panels in context) |
| `A4_Portrait_Panel.svg` | Fixed panel sheet (outline + clamp notch positions) |
| `A4_Portrait_Door.svg` | Door panel sheet (outline + hinge cutouts + handle hole) |
| `A4_Portrait_Hinge.svg` | Hinge cutout detail sheet (enlarged cutout dims) |
| `A4_Portrait_Blank.svg` | Blank template for additional detail views |

All templates are A4 portrait with standard title blocks (`freecad:editable` fields for title,
identification_number, date_of_issue, scale, part_material, creator, etc.).

**Reference:** `Resources/Documents/Drawing templates/Example of Corner documentation.pdf`
— Example output showing corner enclosure with return panel, inline panel, and door panel.

**Per-Panel Drawing Content:**

**Fixed Panels (return, inline):**
- Panel outline with width × height dimensions
- Clamp/bracket notch positions with offset dimensions from edges
- Notch detail view (20mm notch with R10 radius from `Notch.png`)
- Hole details for glass to glass Clamp/bracket (20mm hole located 20mm from edge or 20mm + glass thickness from edge)
- Glass thickness, type, edge finish in title block
- Hinge cut out if glass to glass hinge on door next to it. (Hinge panel needs to use `A4_Portrait_Hinge.svg`)

**Door Panels:**
- Panel outline with width × height dimensions
- Hinge cutout positions with offset dimensions from top/bottom edges
- Hinge cutout detail view (37×63mm cutout with R8 radius from `HingeCutOut.png`)
- Handle hole position with offset dimensions from edge
- Glass thickness, type, edge finish in title block

**Assembly Overview Page:**
- All panels shown in assembled position (top-down or front view)
- Overall enclosure dimensions (width, depth, height)
- Panel identification labels matching individual sheet numbers

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Models/GlassOrderDrawing.py`

```python
class GlassOrderDrawingGenerator:
    """Generates TechDraw pages for glass ordering from an enclosure assembly."""

    TEMPLATE_DIR = "Resources/Documents/Drawing templates/"
    TEMPLATES = {
        "assembly": "A4_Portrait_Assembly.svg",
        "panel": "A4_Portrait_Panel.svg",
        "door": "A4_Portrait_Door.svg",
        "hinge_detail": "A4_Portrait_Hinge.svg",
        "blank": "A4_Portrait_Blank.svg",
    }

    def generate(self, assembly_obj) -> list[TechDraw.Page]:
        """Generate full drawing set for an enclosure assembly."""
        # 1. Create assembly overview page
        # 2. For each panel child:
        #    - Select template (Panel vs Door)
        #    - Create TechDraw page with front view projection
        #    - Add dimension annotations (panel W×H)
        #    - Add cutout/notch detail views with dimensions
        #    - Fill title block fields from assembly properties
        # 3. Add hinge detail pages if door panels present

    def _createPanelPage(self, panel_obj, template: str) -> TechDraw.Page:
        """Create a single panel drawing page."""

    def _addCutoutDimensions(self, page, panel_obj):
        """Add hinge cutout, notch, and hole dimensions to a page."""

    def _addHardwarePositions(self, page, panel_obj):
        """Dimension hardware positions relative to panel edges."""

    def _fillTitleBlock(self, page, panel_obj, sheet_num: int):
        """Populate title block editable fields."""
```

**File:** `freecad/ShowerDesigner/Commands/__init__.py` (GlassOrderCommand)

```python
class GlassOrderCommand:
    def Activated(self):
        # Get selected enclosure assembly
        # Run GlassOrderDrawingGenerator.generate()
        # Optionally export all pages as single PDF

    def IsActive(self):
        # Active when an enclosure assembly is selected
```

**Title Block Field Mapping:**
| Template Field | Source |
|---------------|--------|
| `title` | Panel label (e.g., "Return Panel", "Door Panel") |
| `identification_number` | Auto-generated (e.g., "CE-001-RP") |
| `part_material` | Glass type + thickness (e.g., "10mm Tempered Clear") |
| `scale` | Auto-calculated to fit panel on page |
| `date_of_issue` | Current date |
| `creator` | From FreeCAD preferences or assembly property |
| `sheet_number` | Page N of total |

**Cutout/Notch Specifications (from hardware models):**
- **Hinge cutout**: 37mm × 63mm with R8 corner radius (from `HingeCutOut.png`)
- **Clamp notch**: 20mm × 20mm with R10 corner radius (from `Notch.png`)
- **Handle hole**: Diameter and position from handle spec in `HardwareSpecs.py`
- Dimensions sourced from hardware model specs, not hardcoded

**Testing:**
- Generate drawing set for each enclosure type (Corner, Alcove, WalkIn)
- Verify cutout positions match hardware positions in 3D model
- Verify dimensions are accurate and readable
- Export as PDF and verify all pages present
- Test with different hinge/clamp/handle combinations
- Verify title block fields populated correctly

---

#### 1.4 Measurement & Dimensioning -- ◐ IN PROGRESS (50%)
**Priority:** Medium
**Estimated Effort:** High
**Dependencies:** None

**Objectives:**
- Add automated dimension annotations to the 3D view
- Show overall enclosure dimensions, glass sizes, hardware positions
- Generate 2D projection views for installation drawings (TechDraw integration)

**What was implemented (Phase 1.4a — 3D Dimension Annotations):**

**File:** `freecad/ShowerDesigner/Data/DimensionSpecs.py` (pure Python, no FreeCAD imports)
- `DimensionItem` dataclass with label, value, unit, category
- Offset constants for dimension line positioning
- Color categories for visual grouping (overall, panel, hardware)

**File:** `freecad/ShowerDesigner/Models/DimensionExtractor.py`
- Full assembly tree walker for extracting dimensions
- Overall dimensions (Width/Height/Depth) from VarSet properties
- Panel dimensions (GlassChild width/height)
- Hardware positions (Hinge, Handle, SupportBar locations)
- Returns structured list of `DimensionItem` objects

**File:** `freecad/ShowerDesigner/Commands/__init__.py` (MeasureCommand)
- Toggle-based: creates or removes "Dimensions" group
- Uses `DimensionExtractor` to gather all measurements
- Creates Draft dimension annotations in 3D view

**File:** `freecad/ShowerDesigner/Tests/test_dimensions.py`
- Pure data tests for `DimensionItem` and constants

**Remaining (Phase 1.4b — TechDraw Integration):**
- TechDraw page with standard views (front, side, top)
- Auto-place dimensions on the drawing
- Title block with enclosure specs (glass type, thickness, hardware)
- PDF export for installer handoff
- Live dimension update when parameters change
- Testing with real assemblies across all enclosure types

**Phases:**
- **1.4a**: 3D dimension annotations — ✓ Implemented
- **1.4b**: TechDraw installation drawings — Not started

**Testing:**
- Add dimensions to each enclosure type
- Verify dimensions update when parameters change
- Test TechDraw page generation
- Export drawing as PDF

---

### 2. User Interface & Usability

---

#### 2.1 Enclosure Creation Wizard
**Priority:** High
**Estimated Effort:** High
**Dependencies:** Phase 1 enclosures complete

**Objectives:**
- Step-by-step Qt task panel for creating enclosures
- Replace manual VarSet property editing with guided workflow
- Preview updates in real-time as user makes selections

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Gui/EnclosureWizard.py`

**Wizard Steps:**

**Step 1: Enclosure Type**
- Visual cards showing Corner, Alcove, Walk-In, Custom
- Brief description and typical use case for each

**Step 2: Dimensions**
- Width, height, depth inputs with validation
- Real-time 3D preview updates
- Min/max constraints from `PanelConstraints.py`

**Step 3: Glass Configuration**
- Glass type, thickness, edge finish, tempering
- Dropdowns populated from `GlassSpecs.py`
- Weight calculation shown in real-time

**Step 4: Door Selection** (if applicable)
- Door type: Hinged, Sliding, Bi-Fold
- Door position: Left, Right, Center
- Opening direction (hinged doors)
- Populated from available mounting variants

**Step 5: Hardware**
- Hinge model selection (filtered by door type)
- Handle selection with visual previews
- Clamp type for fixed panels
- Support bar configuration (Walk-In)

**Step 6: Review & Create**
- Summary table of all selections
- Estimated glass weight
- "Create" button generates the full assembly

**Qt Implementation:**
```python
class EnclosureWizard(QtWidgets.QWidget):
    """Multi-step task panel for enclosure creation."""

    def __init__(self):
        self.steps = [
            TypeStep(),
            DimensionStep(),
            GlassStep(),
            DoorStep(),
            HardwareStep(),
            ReviewStep(),
        ]
        self.currentStep = 0

    def show(self):
        Gui.Control.showDialog(self)
```

**Testing:**
- Complete wizard flow for each enclosure type
- Verify created assembly matches wizard selections
- Test validation (invalid dimensions, incompatible hardware)
- Test back/forward navigation preserves state

---

#### 2.2 Hardware Selection Panel
**Priority:** Medium
**Estimated Effort:** Medium
**Dependencies:** 2.1 (can share UI patterns)

**Objectives:**
- Dedicated task panel for browsing and selecting hardware
- Filter by compatibility (door type, glass thickness, mounting style)
- Show product codes, dimensions, and 3D preview

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Gui/HardwareSelector.py`

```python
class HardwareSelector(QtWidgets.QWidget):
    """Browsable hardware catalogue with filters."""

    def __init__(self, hardware_type: str, context: dict):
        # hardware_type: "hinge", "handle", "clamp", "support_bar"
        # context: {"door_type": "hinged", "glass_thickness": 10, ...}

    Filters:
        - Hardware type (hinge, handle, clamp, support bar)
        - Brand/family (Bevel, Monza, generic)
        - Glass thickness compatibility
        - Mounting style (wall, glass-to-glass)
        - Search by product code
```

**Integration:**
- Called from EnclosureWizard Step 5
- Also accessible standalone via toolbar for modifying existing assemblies
- Selection updates the assembly's VarSet properties

**Testing:**
- Filter by each criteria
- Verify compatibility filtering is correct
- Select hardware and verify assembly updates

---

#### 2.3 Property Validation & Error Display
**Priority:** Medium
**Estimated Effort:** Medium
**Dependencies:** None

**Objectives:**
- Validate property combinations and show clear error messages
- Prevent invalid configurations before they cause geometry failures
- Use FreeCAD's built-in notification system

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Validation.py`

```python
@dataclass
class ValidationResult:
    valid: bool
    errors: list[str]    # Blocking issues
    warnings: list[str]  # Non-blocking advisories

class AssemblyValidator:
    """Validates an enclosure assembly configuration."""

    def validate(self, assembly_obj) -> ValidationResult:
        """Run all validation checks on an assembly."""

    Rules:
        - Glass dimensions within min/max (from PanelConstraints)
        - Glass thickness adequate for panel size (weight/safety)
        - Hardware compatible with glass thickness
        - Gap dimensions valid for selected seal type
        - Door opening doesn't collide with fixed panels
        - Support bar required for panels > 1200mm wide
        - Total weight within hinge/track rating
```

**Error display:**
- `App.Console.PrintError()` for critical issues
- `App.Console.PrintWarning()` for advisories
- Optional: colored indicators on the model tree (red/yellow icons)
- Validation runs automatically on `execute()` and on-demand via menu

**Testing:**
- Trigger each validation rule
- Verify error messages are clear and actionable
- Test that valid configurations pass without warnings

---

#### 2.4 Custom Icons -- ◐ IN PROGRESS (55%)
**Priority:** Low
**Estimated Effort:** Low
**Dependencies:** None

**Objectives:**
- Create distinct SVG icons for each component command
- Replace generic `Logo` icon usage

**What was implemented:**
- 9 dedicated SVG icons in `Resources/icons/`: AlcoveEnclosure, BiFoldDoor, CornerEnclosure, CustomEnclosure, FixedPanel, HingedDoor, SlidingDoor, WalkInEnclosure, Logo

**Icon List:**

| Command | Current Icon | New Icon Description |
|---------|-------------|---------------------|
| GlassPanel | Logo | Single glass panel outline |
| FixedPanel | ✓ Has icon | Keep existing |
| HingedDoor | ✓ Has icon | Keep existing |
| SlidingDoor | ✓ Has icon | Keep existing |
| BiFoldDoor | ✓ Has icon | Keep existing |
| CornerEnclosure | ✓ Has icon | Keep existing |
| AlcoveEnclosure | ✓ Has icon | Keep existing |
| WalkInEnclosure | ✓ Has icon | Keep existing |
| CustomEnclosure | ✓ Has icon | Keep existing |
| Hinge | Logo | Hinge bracket |
| Handle | Logo | Door handle |
| Clamp | Logo | Clamp bracket |
| SupportBar | Logo | Support bar |
| Measure | Logo | Ruler/dimension |
| CutList | Logo | Spreadsheet/list |
| Export | Logo | Download/export arrow |

**File location:** `freecad/ShowerDesigner/Resources/icons/`
**Format:** SVG, 64×64px, consistent line weight and style

**Testing:**
- All icons display correctly in toolbar and menu
- Icons are visually distinct at small sizes (24×24px toolbar)

---

### 3. Advanced Features

---

#### 3.1 Seal 3D Visualization
**Priority:** High
**Estimated Effort:** High
**Dependencies:** Phase 1 seal specs (3.4), seal deduction system (3.6)

**Objectives:**
- Create `Models/Seal.py` with 3D seal geometry
- Show seals as thin profiles along glass edges in the assembly
- Seal type selection drives glass deductions automatically

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Models/Seal.py`

```python
def createSealProfile(seal_type: str, glass_thickness: float) -> Part.Wire:
    """Create a 2D seal cross-section profile.

    Seal types from SealSpecs.py:
    - U-channel (wraps glass edge)
    - Magnetic (door-to-door)
    - Sweep/wiper (door bottom)
    - Bulb seal (panel-to-wall)
    - Fin seal (panel-to-panel)
    """

def createSealShape(profile: Part.Wire, edge_path: Part.Edge) -> Part.Shape:
    """Sweep seal profile along a glass edge to create 3D geometry."""

class SealChild:
    """Child proxy for seal objects within assemblies."""

    def __init__(self, obj):
        obj.addProperty("App::PropertyEnumeration", "SealType", "Seal", "Seal profile type")
        obj.addProperty("App::PropertyEnumeration", "Edge", "Seal", "Which glass edge")
        # Edge options: Top, Bottom, Left, Right, HingeEdge, LatchEdge

    def execute(self, obj):
        # Look up seal spec from SealSpecs.py
        # Create profile and sweep along parent glass edge
        # Position at glass edge with correct offset
```

**Seal profiles (cross-sections):**
- **U-Channel**: U-shape wrapping glass edge, ~12mm wide × 20mm deep
- **Magnetic**: Rectangular with magnetic strip, ~10mm × 15mm
- **Sweep/Wiper**: Triangular fin angled downward, ~8mm × 30mm
- **Bulb Seal**: Round bulb + compression fin, ~6mm × 12mm
- **Fin Seal**: Thin flexible fin, ~2mm × 15mm

**Integration with existing assemblies:**
- Add seal children to HingedDoor, SlidingDoor, BiFoldDoor assemblies
- Seal type selection in VarSet drives:
  1. Seal child geometry update
  2. Glass deduction recalculation (via existing seal deduction system)
- Default seal assignments per door/panel type from `SealSpecs.SEAL_ASSIGNMENTS`

**View provider:**
- Transparent rubber-like material (dark grey, slight transparency)
- Separate visibility toggle from glass and hardware
- Lower detail level (seals are visual reference, not manufacturing geometry)

**Testing:**
- Create each seal profile type
- Verify sweep along straight and angled edges
- Verify seal dimensions match `SealSpecs.py` catalogue entries
- Test seal deduction integration (glass shrinks when seal added)
- Visual check: seals appear correctly positioned at glass edges

---

#### 3.2 Cost Estimation
**Priority:** Low
**Estimated Effort:** Medium
**Dependencies:** 1.1 (Cut List)

**Objectives:**
- Calculate material cost from glass area, hardware quantities, and seal lengths
- User-supplied price list (editable defaults)
- Show cost breakdown by category

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Data/CostEstimation.py`

```python
@dataclass
class PriceEntry:
    product_code: str
    description: str
    unit_price: float    # User's currency
    unit: str            # "per_sqm", "per_m", "per_pc"

class CostEstimator:
    """Calculate material costs from a cut list."""

    def __init__(self, price_list: dict[str, PriceEntry]):
        self.prices = price_list

    def estimate(self, cut_list: list[CutListItem]) -> CostBreakdown:
        """Calculate costs per item and totals."""

@dataclass
class CostBreakdown:
    items: list[CostLineItem]
    subtotal_glass: float
    subtotal_hardware: float
    subtotal_seals: float
    total: float
```

**Price list management:**
- Default prices stored in JSON file (`Data/default_prices.json`)
- User can override via preferences or import CSV
- Prices are per-unit: glass = per m², hardware = per piece, seals = per meter

**Testing:**
- Estimate cost for sample enclosure
- Verify calculations (area × price, quantity × price)
- Test with missing prices (show "N/A" not crash)

---

## Success Criteria

### Must Have (Phase 2 Complete)
- [ ] Cut list generation works for all enclosure types
- [ ] CSV export produces valid, importable files
- [ ] STEP export works for individual parts and full assemblies
- [ ] Glass order drawings generate per-panel TechDraw sheets with cutout/notch/hole dimensions
- [ ] Enclosure creation wizard guides user through full setup
- [ ] Seal 3D visualization shows correct profiles on glass edges
- [ ] Property validation catches common configuration errors

### Should Have
- [ ] TechDraw installation drawings with auto-dimensioning
- [ ] Hardware selection panel with filtering
- [ ] Cost estimation with editable price list
- [ ] All commands have distinct custom icons

### Nice to Have
- [ ] Batch export with manifest file
- [ ] Price list import/export (CSV)
- [ ] Measurement annotations update when parameters change

---

## File Structure (New Files)

```
freecad/ShowerDesigner/
  Data/
    CutList.py              # ✓ BOM generation (pure Python)
    DimensionSpecs.py       # ✓ Dimension data layer (pure Python)
    CostEstimation.py       # ○ Cost calculator (pure Python) — not started
    default_prices.json     # ○ Default price list — not started
  Models/
    CutListExtractor.py     # ✓ Assembly tree walker for BOM extraction
    DimensionExtractor.py   # ✓ Assembly tree walker for measurements
    GlassOrderDrawing.py    # ○ TechDraw glass order drawing generator — not started
    Seal.py                 # ○ Seal 3D geometry + child proxy — not started
  Gui/
    CutListDialog.py        # ✓ BOM display dialog
    ExportDialog.py         # ✓ Export options dialog
    EnclosureWizard.py      # ○ Multi-step creation wizard — not started
    HardwareSelector.py     # ○ Hardware browsing panel — not started
  Commands/__init__.py      # ✓ CutList, Export, Measure commands (integrated)
  Validation.py             # ○ Assembly validation rules — not started
  Resources/icons/          # ◐ 9 of ~17 commands have dedicated icons
  Resources/Documents/Drawing templates/  # ✓ SVG templates for TechDraw glass order drawings
  Tests/
    test_cut_list.py        # ✓ Cut list tests
    test_dimensions.py      # ✓ Dimension data tests
```

---

## Implementation Order

Recommended sequence based on dependencies, value, and current progress:

1. ~~**1.1 Cut List / BOM**~~ — 85% complete, finish end-to-end testing
2. ~~**1.2 STEP/STL Export**~~ — 75% complete, finish manifest + validation
3. **1.3 Glass Order Drawings** — High priority, critical for glass supplier ordering
4. ~~**1.4 Measurement & Dimensioning**~~ — 50% complete (1.4a done), TechDraw next
5. **3.1 Seal 3D Visualization** — Completes Phase 1 gap, improves visual fidelity
6. **2.3 Property Validation** — Foundation for wizard error handling
7. **2.1 Enclosure Creation Wizard** — Major usability improvement
8. **2.2 Hardware Selection Panel** — Enhances wizard and standalone use
9. **2.4 Custom Icons** — 55% complete, remaining 8 icons needed
10. **3.2 Cost Estimation** — Builds on cut list, lowest priority

---

## Future Enhancements (Phase 3+)

- Door animation (open/close with constraints)
- Collision detection between panels (runtime)
- Stress analysis for large panels
- Custom hardware import (STEP files from manufacturers)
- Installation sequence generator
- Template system (save/reload enclosure configurations)
- Multi-language support
- Cloud export (share designs via link)

---

## Notes

- All new Data layer files must remain pure Python (no FreeCAD imports)
- GUI files use the existing Qt compatibility layer (`from freecad.ShowerDesigner.Qt...`)
- Commands follow existing pattern: `GetResources()`, `Activated()`, `IsActive()`
- CutList, Export, and Measure commands are implemented directly in `Commands/__init__.py` (not separate files)
- All files must include LGPL-3.0 license headers
- Maintain camelCase methods for FreeCAD convention
