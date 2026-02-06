# Task 2.3: Bi-Fold Door System - Implementation Specification

**Status: Planned - Not Yet Implemented**

**Priority:** Medium
**Estimated Effort:** Medium
**Dependencies:** 1.1 (GlassPanel), 2.1 (HingedDoor)
**Sprint:** 4 (Week 7-8) - Finalization

---

## Overview

Parametric `BiFoldDoor` class that extends `GlassPanel` with a two-panel folding mechanism, pivot point calculation, fold direction, and folded position visualization. The bi-fold door consists of two hinged panels that fold against each other to open, providing a wide opening in confined spaces where a full-swing or sliding door is not practical.

## Files to Create

| File | Description |
|------|-------------|
| `freecad/ShowerDesigner/Models/BiFoldDoor.py` | Main BiFoldDoor class |
| `freecad/ShowerDesigner/Resources/Icons/BiFoldDoor.svg` | Toolbar icon |
| `freecad/ShowerDesigner/Tests/test_bifold_door.py` | Test script |

## Files to Modify

| File | Changes |
|------|---------|
| `freecad/ShowerDesigner/Commands/__init__.py` | Add `BiFoldDoorCommand` class |
| `freecad/ShowerDesigner/init_gui.py` | Update toolbar to include `ShowerDesigner_BiFoldDoor` |

---

## Module-Level Data

### PIVOT_SPECS Dictionary

Defines pivot hardware specifications used for geometry and placement calculations:

| Pivot Type | Offset (mm) | Max Load (kg) | Description |
|------------|-------------|---------------|-------------|
| Inline | 0 | 40 | Pivot axis aligned with glass edge; panels fold flat |
| Offset | 15 | 50 | Pivot axis offset from glass edge; allows seal clearance |

```python
PIVOT_SPECS = {
    "Inline": {"offset": 0, "max_load_kg": 40, "description": "Flush pivot, panels fold flat"},
    "Offset": {"offset": 15, "max_load_kg": 50, "description": "Offset pivot, allows seal gap"},
}
```

---

## BiFoldDoor Properties

### Inherited from GlassPanel
- **Dimensions**: Width (900mm), Height (2000mm), Thickness (8mm)
- **Glass**: GlassType, EdgeFinish, TemperType
- **Placement**: Position, Rotation
- **Calculated**: Weight, Area (read-only)
- **AttachmentType**: Overridden to "Hinged" on initialization (bi-fold is a hinged variant)

### Door Configuration
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| FoldDirection | Enum | Inward | Inward or Outward |
| HingeSide | Enum | Left | Which side is fixed to the wall (Left or Right) |
| PivotType | Enum | Inline | Inline or Offset pivot mechanism |
| FoldAngle | Angle | 0 | Current fold angle for visualization (0 = closed, 180 = fully open) |

### Pivot Hardware
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| PivotFinish | Enum | Chrome | Chrome, Brushed-Nickel, Matte-Black, or Gold |
| PivotOffset | Length | 0mm | Pivot axis offset from glass edge (auto-set from PivotType) |

### Handle Hardware
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| HandleType | Enum | Bar | None, Knob, Bar, or Pull |
| HandleHeight | Length | 1050mm | Height from floor (300-1800mm) |
| HandleOffset | Length | 75mm | Distance from door edge |
| HandleLength | Length | 300mm | Bar handle length (for Bar type) |

### Hardware Display
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| ShowHardware | Bool | True | Show pivot and handle hardware in 3D view |
| ShowFoldedPosition | Bool | False | Show ghost outline of fully folded position |

### Calculated (Read-Only)
| Property | Type | Description |
|----------|------|-------------|
| PanelWidth | Length | Width of each fold panel (Width / 2) |
| FoldedWidth | Length | Total width when fully folded against the wall |
| OpeningWidth | Length | Clear opening when fully folded open |
| ClearanceDepth | Length | How far the folded panels project from the wall plane |

---

## Key Algorithms

### Panel Width Calculation (`_calculatePanelWidth`)
```
PanelWidth = Width / 2
```
For a 900mm opening: each panel is 450mm wide.

### Folded Width Calculation (`_calculateFoldedWidth`)
```
Inline pivot:
  FoldedWidth = PanelWidth + Thickness

Offset pivot:
  FoldedWidth = PanelWidth + Thickness + PivotOffset
```
This accounts for the two glass panels stacking together and any pivot offset when the door is fully folded.

### Opening Width Calculation
```
OpeningWidth = Width - FoldedWidth
```
The clear passage width after subtracting the folded panel stack.

### Clearance Depth Calculation (`_calculateClearanceDepth`)
```
ClearanceDepth = PanelWidth + PivotOffset
```
Maximum depth the panels project perpendicular to the opening when at 90 degrees mid-fold. Applies to both Inward and Outward fold directions (direction determines which side of the opening the projection occurs on).

### Pivot Point Positions (`_calculatePivotPositions`)
```
Wall pivot (fixed panel to wall):
  HingeSide = Left:  X = 0
  HingeSide = Right: X = Width

Panel-to-panel pivot (center fold joint):
  X = Width / 2  (i.e., PanelWidth from the hinge side)

Each pivot location has two Z positions:
  Bottom pivot: 300mm from floor
  Top pivot: Height - 300mm from top
```

---

## Visual Elements

1. **Glass Panels**: Two box geometries, each `PanelWidth x Thickness x Height`, placed edge-to-edge when closed (FoldAngle = 0)
2. **Pivot Hardware**: Cylinder shapes (8mm radius x 30mm height) at each pivot point -- two cylinders at the wall pivot (top and bottom) and two at the center fold joint (top and bottom), totaling 4 pivot cylinders
3. **Handle**: On the free edge (opposite from HingeSide), following the same pattern as HingedDoor:
   - Knob: Cylinder 40mm diameter x 15mm depth
   - Bar: Cylinder 24mm diameter x HandleLength
   - Pull: Cylinder 20mm diameter x 200mm
4. **Folded Position Ghost** (when ShowFoldedPosition = True): Wireframe or transparent outline showing the two-panel stack against the hinge side wall

---

## Planned Methods

### Core Methods (override GlassPanel)

```python
def __init__(self, obj):
    """Initialize bi-fold door with fold and pivot properties."""

def execute(self, obj):
    """Rebuild geometry: panels, pivots, handle, folded ghost."""

def onChanged(self, obj, prop):
    """Validate constraints on property changes."""
```

### Private Calculation Methods

```python
def _calculatePanelWidth(self, obj):
    """Return Width / 2."""

def _calculateFoldedWidth(self, obj):
    """Return total stacked width when fully folded."""

def _calculateClearanceDepth(self, obj):
    """Return max perpendicular projection during fold."""

def _calculatePivotPositions(self, obj):
    """Return list of (X, Z_bottom, Z_top) tuples for wall and center pivots."""

def _calculateHandlePosition(self, obj):
    """Return App.Vector for handle center on free edge."""
```

### Private Geometry Methods

```python
def _createPanels(self, obj):
    """Create two box shapes arranged edge-to-edge."""

def _createPivots(self, obj):
    """Create cylinder shapes at each pivot position."""

def _createHandle(self, obj):
    """Create handle shape (reuse pattern from HingedDoor)."""

def _createFoldedGhost(self, obj):
    """Create transparent wireframe of fully folded position."""

def _updateBifoldProperties(self, obj):
    """Update all calculated read-only properties (PanelWidth, FoldedWidth, OpeningWidth, ClearanceDepth)."""
```

### Factory Function

```python
def createBiFoldDoor(name="BiFoldDoor"):
    """
    Create a new bi-fold door in the active document.

    - Adds a Part::FeaturePython object
    - Initializes BiFoldDoor proxy
    - Attempts GlassPanelViewProvider; falls back to basic with 70% transparency
    - Calls doc.recompute() and prints confirmation
    - Returns the FreeCAD document object
    """
```

---

## Validation Rules

### FoldAngle (onChanged)
- Clamped to range 0-180 degrees
- 0 = fully closed, 180 = fully folded open

### PivotType (onChanged)
- Switching PivotType updates PivotOffset automatically from PIVOT_SPECS
- Inline: PivotOffset = 0mm
- Offset: PivotOffset = 15mm

### HandleHeight (onChanged)
- Clamped to range 300-1800mm (same as HingedDoor and SlidingDoor)

### Width (onChanged)
- Minimum: 400mm (each panel must be at least 200mm wide)
- Maximum: Per GlassPanel/GlassSpecs thickness-based limits

---

## Usage

### Create via Command
1. Open ShowerDesigner workbench
2. Click "Bi-Fold Door" in Components toolbar
3. Adjust properties in FreeCAD property panel

### Create via Python
```python
from freecad.ShowerDesigner.Models.BiFoldDoor import createBiFoldDoor

door = createBiFoldDoor("MyBiFold")
door.Width = 800
door.Height = 2100
door.FoldDirection = "Inward"
door.PivotType = "Offset"
door.HingeSide = "Left"
door.HandleType = "Pull"
door.ShowFoldedPosition = True
App.ActiveDocument.recompute()

print(f"Panel width: {door.PanelWidth.Value}mm")    # 400mm
print(f"Folded width: {door.FoldedWidth.Value}mm")   # 423mm (400 + 8 + 15)
print(f"Opening: {door.OpeningWidth.Value}mm")        # 377mm
```

### Outward Fold Example
```python
door = createBiFoldDoor("OutwardBiFold")
door.Width = 900
door.FoldDirection = "Outward"
door.PivotType = "Inline"
door.HingeSide = "Right"
App.ActiveDocument.recompute()

print(f"Panel width: {door.PanelWidth.Value}mm")      # 450mm
print(f"Folded width: {door.FoldedWidth.Value}mm")     # 458mm (450 + 8)
print(f"Opening: {door.OpeningWidth.Value}mm")          # 442mm
print(f"Clearance depth: {door.ClearanceDepth.Value}mm") # 450mm (projects outward)
```

---

## Factory Function

### `createBiFoldDoor(name="BiFoldDoor")`

Creates a new BiFoldDoor in the active document (or creates a new document if none exists).

- Adds a `Part::FeaturePython` object
- Initializes `BiFoldDoor` proxy
- Attempts to use `GlassPanelViewProvider` for visual styling; falls back to basic view provider with 70% transparency
- Calls `doc.recompute()` and prints confirmation message
- Returns the FreeCAD document object

---

## Testing

### Test Suite (planned, 13 tests)

| # | Test | What It Validates |
|---|------|-------------------|
| 1 | `test_basic_creation` | Default property values (Width, Height, Thickness, AttachmentType, FoldDirection, PivotType, HingeSide, FoldAngle, ShowHardware) |
| 2 | `test_panel_width_calculation` | PanelWidth = Width / 2 for various widths |
| 3 | `test_folded_width_inline` | FoldedWidth = PanelWidth + Thickness for Inline pivot |
| 4 | `test_folded_width_offset` | FoldedWidth = PanelWidth + Thickness + 15 for Offset pivot |
| 5 | `test_opening_width` | OpeningWidth = Width - FoldedWidth |
| 6 | `test_clearance_depth_inline` | ClearanceDepth = PanelWidth for Inline pivot |
| 7 | `test_clearance_depth_offset` | ClearanceDepth = PanelWidth + 15 for Offset pivot |
| 8 | `test_fold_direction` | Inward and Outward both accepted |
| 9 | `test_pivot_type_switching` | Switching PivotType updates PivotOffset automatically |
| 10 | `test_hinge_side` | Left and Right both accepted; handle appears on opposite side |
| 11 | `test_handle_types` | None, Knob, Bar, Pull all accepted and rendered |
| 12 | `test_hardware_visibility` | ShowHardware toggle changes compound shape content |
| 13 | `test_position_and_rotation` | Position vector and rotation angle applied correctly |

### Running Tests

In FreeCAD Python console:
```python
exec(open(r'path/to/test_bifold_door.py').read())
```

Or call individual test functions:
```python
from freecad.ShowerDesigner.Tests.test_bifold_door import run_all_tests
run_all_tests()
```

---

## Design Rationale

### Why extend GlassPanel directly (not HingedDoor)?
Although the bi-fold door has hinged joints, it does not share the single-swing arc logic, hinge placement algorithm, or swing clearance calculation of HingedDoor. The bi-fold door's two-panel folding mechanism is fundamentally different. Extending GlassPanel directly avoids inheriting unused HingedDoor properties (SwingDirection, OpeningAngle, HingeCount, etc.) and keeps the class hierarchy clean. The dependency on Task 2.1 (HingedDoor) is for design pattern reference and shared handle code, not inheritance.

### Why fixed 2-panel design?
Bi-fold shower doors are universally a 2-panel configuration in the shower industry. Unlike room dividers or patio doors that may use 3+ panels, shower bi-fold doors fold a single pair of panels. This keeps the implementation focused and avoids unnecessary complexity.

### Why include FoldAngle?
FoldAngle allows the user to visualize intermediate fold positions for clearance checking, similar to HingedDoor's OpeningAngle + ShowSwingArc combination. Default of 0 (closed) shows the door in its normal resting state.

---

## Future Enhancements (Phase 2+)

- Fold animation (smooth open/close with intermediate positions)
- Collision detection with walls and adjacent panels during fold
- Magnetic catch/latch hardware at closed position
- Rise-and-fall pivot mechanism (lifts panel as it folds to clear floor lip)
- Water seal strips along pivot edges
- Custom pivot hardware models (STEP import)
- Integration with enclosure models (AlcoveEnclosure, CornerEnclosure)
