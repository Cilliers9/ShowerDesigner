# Task 2.1: Hinged Door System - Implementation Summary

## Overview

Implemented a parametric `HingedDoor` class that extends `GlassPanel` with swing direction, hinge hardware, handle placement, and optional swing arc visualization.

## Files Created

| File | Description |
|------|-------------|
| `freecad/ShowerDesigner/Models/HingedDoor.py` | Main HingedDoor class |
| `freecad/ShowerDesigner/Resources/Icons/HingedDoor.svg` | Toolbar icon |
| `freecad/ShowerDesigner/Tests/test_hinged_door.py` | Test script |

## Files Modified

| File | Changes |
|------|---------|
| `freecad/ShowerDesigner/Commands/__init__.py` | Added `HingedDoorCommand` class |
| `freecad/ShowerDesigner/init_gui.py` | Updated toolbar to use `ShowerDesigner_HingedDoor` |

---

## HingedDoor Properties

### Inherited from GlassPanel
- **Dimensions**: Width (900mm), Height (2000mm), Thickness (8mm)
- **Glass**: GlassType, EdgeFinish, TemperType
- **Placement**: Position, Rotation
- **Calculated**: Weight, Area (read-only)

### Door Configuration
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| SwingDirection | Enum | Inward | Inward or Outward |
| HingeSide | Enum | Left | Left or Right |
| OpeningAngle | Angle | 90 | Max opening angle (capped at 110) |

### Hinge Hardware
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| HingeCount | Integer | 2 | Number of hinges (2-3) |
| HingeOffsetTop | Length | 300mm | Distance from top to first hinge |
| HingeOffsetBottom | Length | 300mm | Distance from bottom to last hinge |
| HingeFinish | Enum | Chrome | Hardware finish color |

### Handle Hardware
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| HandleType | Enum | Bar | None, Knob, Bar, or Pull |
| HandleHeight | Length | 1050mm | Height from floor (300-1800mm) |
| HandleOffset | Length | 75mm | Distance from door edge |
| HandleLength | Length | 300mm | Bar handle length |

### Hardware Display
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| ShowHardware | Bool | True | Show hinges and handle |
| ShowSwingArc | Bool | False | Show floor swing arc |
| HingeWidth | Length | 90mm | Hinge visualization width |
| HingeDepth | Length | 20mm | Hinge visualization depth |
| HingeHeight | Length | 65mm | Hinge visualization height |

### Calculated (Read-Only)
| Property | Type | Description |
|----------|------|-------------|
| RecommendedHingeCount | Integer | Based on door weight (2 for ≤45kg, 3 for >45kg) |

---

## Key Algorithms

### Hinge Placement
```
Bottom hinge: HingeOffsetBottom from bottom edge
Top hinge: Height - HingeOffsetTop from bottom edge
Third hinge (if count=3): Centered between top and bottom hinges
```

### Handle Position
- X: Opposite side from hinges, offset by `HandleOffset`
- Y: Centered on glass thickness
- Z: `HandleHeight` from floor

### Weight-Based Recommendations
- ≤45kg: 2 hinges recommended
- >45kg: 3 hinges recommended

---

## Visual Elements

1. **Glass Panel**: Box geometry (Width × Thickness × Height)
2. **Hinges**: Box shapes (90×20×65mm) at calculated Z positions
3. **Handle**:
   - Knob: Cylinder 40mm diameter × 15mm depth
   - Bar: Cylinder 24mm diameter × HandleLength
   - Pull: Cylinder 20mm diameter × 200mm
4. **Swing Arc**: 2D arc on floor plane showing clearance radius

---

## Usage

### Create via Command
1. Open ShowerDesigner workbench
2. Click "Hinged Door" in Components toolbar
3. Adjust properties in FreeCAD property panel

### Create via Python
```python
from freecad.ShowerDesigner.Models.HingedDoor import createHingedDoor

door = createHingedDoor("MyDoor")
door.Width = 800
door.Height = 2100
door.HingeSide = "Right"
door.SwingDirection = "Outward"
door.HandleType = "Pull"
door.ShowSwingArc = True
App.ActiveDocument.recompute()
```

---

## Testing

Run tests in FreeCAD Python console:
```python
exec(open(r'path/to/test_hinged_door.py').read())
```

Or call individual test functions:
```python
from freecad.ShowerDesigner.Tests.test_hinged_door import run_all_tests
run_all_tests()
```

---

## Validation Rules

1. **HingeCount**: Clamped to range 2-3
2. **OpeningAngle**: Clamped to max 110 degrees
3. **HandleHeight**: Clamped to range 300-1800mm

---

## Future Enhancements (Phase 2+)

- Door animation (smooth open/close)
- Collision detection with walls
- Glass-to-glass hinge type
- Soft-close hinge option
- Custom handle models (STEP import)
