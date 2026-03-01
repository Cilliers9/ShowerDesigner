# Phase 2: Production-Ready Tools - Implementation Plan

## Overview

This phase transforms ShowerDesigner from a parametric modeling tool into a production-ready design
system. The focus is on output tools (cut lists, export, measurement), user-facing task panels for
guided configuration, and 3D seal visualization — everything needed to go from design to fabrication.

**Last Updated:** 2026-02-27

---

## Status Summary

| Section | Area | Status | Completion |
|---------|------|--------|------------|
| 1.1 | Cut List / Bill of Materials | ○ Not Started | 0% |
| 1.2 | STEP/STL Batch Export | ○ Not Started | 0% |
| 1.3 | Measurement & Dimensioning | ○ Not Started | 0% |
| 2.1 | Enclosure Creation Wizard | ○ Not Started | 0% |
| 2.2 | Hardware Selection Panel | ○ Not Started | 0% |
| 2.3 | Property Validation & Error Display | ○ Not Started | 0% |
| 2.4 | Custom Icons | ○ Not Started | 0% |
| 3.1 | Seal 3D Visualization | ○ Not Started | 0% |
| 3.2 | Cost Estimation | ○ Not Started | 0% |

**Overall Phase 2 Completion: 0%**

### Prerequisites
Phase 1 should be substantially complete before starting Phase 2. Key dependencies:
- Enclosure assemblies (4.1–4.4) must work end-to-end for cut list extraction
- Seal deduction system (3.6) should be finalized for seal visualization
- Hardware specs catalogue should be stable for BOM generation

---

## Task Breakdown

### 1. Production Output Tools

These replace the three placeholder commands already registered in `Commands/__init__.py`
(`ShowerDesigner_Measure`, `ShowerDesigner_CutList`, `ShowerDesigner_Export`).

---

#### 1.1 Cut List / Bill of Materials
**Priority:** High
**Estimated Effort:** High
**Dependencies:** Phase 1 enclosures (4.1–4.4), HardwareSpecs

**Objectives:**
- Extract all glass dimensions, hardware items, and quantities from any enclosure assembly
- Generate a structured BOM with product codes from the catalogue
- Output as in-app table, CSV, and clipboard-ready format

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Data/CutList.py` (pure Python, no FreeCAD imports)

```python
@dataclass
class CutListItem:
    category: str          # "Glass", "Hardware", "Seal"
    component: str         # "Fixed Panel", "Door Panel", etc.
    description: str       # "Clear Tempered 10mm"
    product_code: str      # From catalogue specs
    width: float           # mm (glass only)
    height: float          # mm (glass only)
    quantity: int
    unit: str              # "pc", "mm", "m"
    notes: str             # "Edge: Bright Polish", etc.

class CutListGenerator:
    """Walks an enclosure assembly tree and extracts all components."""

    def generate(self, assembly_obj) -> list[CutListItem]:
        """Extract BOM from an App::Part enclosure assembly."""

    def toCSV(self, items: list[CutListItem]) -> str:
        """Format as CSV string."""

    def toTable(self, items: list[CutListItem]) -> list[list[str]]:
        """Format as row/column table for Qt display."""
```

**File:** `freecad/ShowerDesigner/Commands/CutListCommand.py`

```python
class CutListCommand:
    def Activated(self):
        # Get selected enclosure or active assembly
        # Generate cut list via CutListGenerator
        # Show in a Qt dialog with copy/export buttons

    def IsActive(self):
        # Active when an enclosure or panel assembly is selected
```

**Data extraction strategy:**
- Walk `App::Part` children recursively
- Identify glass children by checking proxy class (`GlassPanelChild`, etc.)
- Read dimensions from the controller's VarSet properties
- Map hardware to catalogue entries via spec keys stored in properties
- Aggregate quantities (e.g., 4× identical clamps → single line with qty=4)

**Output columns:**
| # | Category | Component | Description | Product Code | W×H (mm) | Qty | Unit | Notes |
|---|----------|-----------|-------------|--------------|-----------|-----|------|-------|

**Testing:**
- Generate BOM from each enclosure type (Corner, Alcove, WalkIn, Custom)
- Verify product codes match `HardwareSpecs.py` catalogue entries
- Verify glass dimensions account for seal deductions
- Test CSV export round-trip (import into spreadsheet)

---

#### 1.2 STEP/STL Batch Export
**Priority:** Medium
**Estimated Effort:** Medium
**Dependencies:** None (uses FreeCAD built-in export)

**Objectives:**
- Export individual panels or complete enclosures as STEP, STL, or 3MF files
- Apply consistent naming conventions for manufacturing
- Support batch export (all panels as separate files)

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Commands/ExportCommand.py`

```python
class ExportCommand:
    def Activated(self):
        # Show export dialog with options:
        #   - Format: STEP / STL / 3MF
        #   - Scope: Selected object / Entire enclosure / Individual parts
        #   - Naming: Auto (enclosure_component_WxH) / Custom prefix
        #   - Output directory picker

    def IsActive(self):
        # Active when any ShowerDesigner object is selected
```

**Naming convention:**
```
{EnclosureType}_{Component}_{Width}x{Height}x{Thickness}.step
Example: CornerEnclosure_FixedPanel_800x2000x10.step
Example: CornerEnclosure_HingedDoor_700x2000x8.step
```

**Batch export flow:**
1. Walk assembly tree to find all geometric children
2. For each child with a `Shape`: export to chosen format
3. Optionally export fused assembly as single file
4. Generate manifest file listing all exported parts

**Testing:**
- Export single panel → verify STEP opens in external CAD
- Batch export enclosure → verify all parts present
- Verify naming convention applied correctly
- Test with each supported format (STEP, STL, 3MF)

---

#### 1.3 Measurement & Dimensioning
**Priority:** Medium
**Estimated Effort:** High
**Dependencies:** None

**Objectives:**
- Add automated dimension annotations to the 3D view
- Show overall enclosure dimensions, glass sizes, hardware positions
- Generate 2D projection views for installation drawings (TechDraw integration)

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Commands/MeasureCommand.py`

```python
class MeasureCommand:
    def Activated(self):
        # Options:
        #   1. "Show Dimensions" - Add 3D dimension annotations
        #   2. "Installation Drawing" - Generate TechDraw sheet

    def IsActive(self):
        # Active when an enclosure is selected
```

**3D Dimension Annotations:**
- Overall width, height, depth of enclosure
- Individual glass panel dimensions (W × H)
- Gap measurements (panel-to-panel, panel-to-wall)
- Hardware positions (hinge heights, handle height, support bar position)
- Use `Draft.makeDimension()` or custom annotation objects

**TechDraw Integration:**
- Create a TechDraw page with standard views (front, side, top)
- Auto-place dimensions on the drawing
- Include title block with enclosure specs (glass type, thickness, hardware)
- Export as PDF for installer handoff

**Phases:**
- **1.3a**: 3D dimension annotations (simpler, immediate value)
- **1.3b**: TechDraw installation drawings (more complex, deferred if needed)

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

#### 2.4 Custom Icons
**Priority:** Low
**Estimated Effort:** Low
**Dependencies:** None

**Objectives:**
- Create distinct SVG icons for each component command
- Replace generic `Logo` icon usage

**Icon List:**

| Command | Current Icon | New Icon Description |
|---------|-------------|---------------------|
| GlassPanel | Logo | Single glass panel outline |
| FixedPanel | Logo | Panel with clamp brackets |
| HingedDoor | Logo | Panel with hinge symbol |
| SlidingDoor | Logo | Panel with arrow/track |
| BiFoldDoor | Logo | Two folded panels |
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
    CutList.py              # BOM generation (pure Python)
    CostEstimation.py       # Cost calculator (pure Python)
    default_prices.json     # Default price list
  Models/
    Seal.py                 # Seal 3D geometry + child proxy
  Gui/
    EnclosureWizard.py      # Multi-step creation wizard
    HardwareSelector.py     # Hardware browsing panel
    CutListDialog.py        # BOM display dialog
    ExportDialog.py         # Export options dialog
  Commands/
    CutListCommand.py       # Cut list command (replaces placeholder)
    ExportCommand.py        # Export command (replaces placeholder)
    MeasureCommand.py       # Measure command (replaces placeholder)
  Validation.py             # Assembly validation rules
  Resources/icons/          # SVG icons for all commands
```

---

## Implementation Order

Recommended sequence based on dependencies and value:

1. **1.1 Cut List / BOM** — Highest standalone value, no UI dependency
2. **3.1 Seal 3D Visualization** — Completes Phase 1 gap, improves visual fidelity
3. **2.3 Property Validation** — Foundation for wizard error handling
4. **2.1 Enclosure Creation Wizard** — Major usability improvement
5. **1.2 STEP/STL Export** — Straightforward FreeCAD integration
6. **2.2 Hardware Selection Panel** — Enhances wizard and standalone use
7. **1.3 Measurement & Dimensioning** — Complex but high value for installers
8. **2.4 Custom Icons** — Polish, can be done anytime
9. **3.2 Cost Estimation** — Builds on cut list, lowest priority

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
- New commands replace the three placeholder registrations in `Commands/__init__.py`
- All files must include LGPL-3.0 license headers
- Maintain camelCase methods for FreeCAD convention
