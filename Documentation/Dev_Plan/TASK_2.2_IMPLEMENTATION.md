# Task 2.2: Sliding Door System - Implementation Summary

## Overview

Implemented a parametric `SlidingDoor` class that extends `GlassPanel` with track-based sliding mechanism, single and bypass (2-panel) configurations, roller hardware, handle placement, and calculated travel/opening properties.

## Files Created

| File | Description |
|------|-------------|
| `freecad/ShowerDesigner/Models/SlidingDoor.py` | Main SlidingDoor class |
| `freecad/ShowerDesigner/Resources/Icons/SlidingDoor.svg` | Toolbar icon |
| `freecad/ShowerDesigner/Tests/test_sliding_door.py` | Test script (14 tests) |

## Files Modified

| File | Changes |
|------|---------|
| `freecad/ShowerDesigner/Commands/__init__.py` | Added `SlidingDoorCommand` class |
| `freecad/ShowerDesigner/init_gui.py` | Updated toolbar to use `ShowerDesigner_SlidingDoor` |

---

## Module-Level Data

### TRACK_PROFILES Dictionary

Defines the four supported track profile specifications used for geometry creation and validation:

| Track Type | Width (mm) | Height (mm) | Max Panels | Glass Restriction |
|------------|-----------|-------------|------------|-------------------|
| Edge | 10 | 30 | 1 | None |
| City | 25 | 30 | 1 | None |
| Ezy | 20 | 25 | 1 | 10mm or 12mm only |
| Soft-Close | 25 | 35 | 2 | None |

---

## SlidingDoor Properties

### Inherited from GlassPanel
- **Dimensions**: Width (900mm), Height (2000mm), Thickness (8mm)
- **Glass**: GlassType, EdgeFinish, TemperType
- **Placement**: Position, Rotation
- **Calculated**: Weight, Area (read-only)
- **AttachmentType**: Overridden to "Sliding" on initialization

### Door Configuration
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| PanelCount | Integer | 1 | Number of panels (1=single, 2=bypass) |
| TrackType | Enum | Edge | Edge, City, Ezy, or Soft-Close |
| SlideDirection | Enum | Right | Left or Right |
| OverlapWidth | Length | 50mm | Overlap width for bypass doors |

### Track Hardware
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| RollerType | Enum | Standard | Standard or Soft-Close |
| TrackFinish | Enum | Chrome | Chrome, Brushed-Nickel, or Matte-Black |

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
| ShowHardware | Bool | True | Show track, rollers, and handle in 3D view |

### Calculated (Read-Only)
| Property | Type | Description |
|----------|------|-------------|
| TrackLength | Length | Total length of the top track |
| TrackHeight | Length | Height of the track profile (from TRACK_PROFILES) |
| TravelDistance | Length | How far the door can slide |
| OpeningWidth | Length | Clear opening when fully open |

---

## Key Algorithms

### Track Length Calculation (`_calculateTrackLength`)
```
Single panel:  TrackLength = Width * 2 + 100  (50mm clearance each side)
Bypass:        TrackLength = Width * 3 - OverlapWidth + 100
```

### Travel Distance
```
Single panel:  TravelDistance = Width
Bypass:        TravelDistance = Width - OverlapWidth
```

### Opening Width
```
Single panel:  OpeningWidth = Width
Bypass:        OpeningWidth = Width - OverlapWidth
```

### Handle Position (`_calculateHandlePosition`)
- X: On the leading edge (opposite to slide direction), offset by `HandleOffset`
  - SlideDirection = "Right": X = HandleOffset (left side)
  - SlideDirection = "Left": X = Width - HandleOffset (right side)
- Y: Centered on glass thickness
- Z: HandleHeight (clamped to max Height - 100mm)

### Bypass Panel Layout
- Panel 1: Placed at origin (Width x Thickness x Height)
- Panel 2: Offset by `(Width - OverlapWidth)` in X and `(Thickness + 25mm)` in Y

---

## Visual Elements

1. **Glass Panel(s)**: Box geometry (Width x Thickness x Height), second panel offset for bypass
2. **Top Track**: Box shape from TRACK_PROFILES dimensions, positioned 5mm above glass top
   - X offset based on SlideDirection: Right starts at -50mm, Left starts at -TrackLength/2
3. **Bottom Guide**: U-channel (15mm wide x 5mm deep), positioned below floor level
   - X offset mirrors top track based on SlideDirection
4. **Rollers**: Cylinders (8mm radius x 15mm height) at 20mm from panel edges, above track
   - 2 rollers per panel (4 total for bypass)
5. **Handle**:
   - Knob: Cylinder 40mm diameter x 15mm depth
   - Bar: Cylinder 24mm diameter x HandleLength
   - Pull: Cylinder 20mm diameter x 200mm

---

## Validation Rules

### PanelCount (onChanged)
- Clamped to range 1-2
- PanelCount = 2 only allowed with Soft-Close track type
- If bypass requested with non-Soft-Close track, resets to 1 with warning

### TrackType (onChanged)
- Switching away from Soft-Close with PanelCount = 2 resets PanelCount to 1 with warning
- Ezy track: warns if glass thickness is not 10mm or 12mm (does not force change)

### Thickness (onChanged)
- When TrackType is Ezy, warns if thickness is not 10mm or 12mm

### HandleHeight (onChanged)
- Clamped to range 300-1800mm

### OverlapWidth (onChanged)
- Minimum: 20mm
- Maximum: Width / 2

---

## Usage

### Create via Command
1. Open ShowerDesigner workbench
2. Click "Sliding Door" in Components toolbar
3. Adjust properties in FreeCAD property panel

### Create via Python
```python
from freecad.ShowerDesigner.Models.SlidingDoor import createSlidingDoor

door = createSlidingDoor("MySlider")
door.Width = 1000
door.Height = 2100
door.TrackType = "City"
door.SlideDirection = "Left"
door.HandleType = "Pull"
App.ActiveDocument.recompute()
```

### Bypass Configuration
```python
door = createSlidingDoor("BypassDoor")
door.TrackType = "Soft-Close"  # Must set BEFORE PanelCount = 2
door.PanelCount = 2
door.Width = 900
door.OverlapWidth = 50
App.ActiveDocument.recompute()

print(f"Opening: {door.OpeningWidth.Value}mm")   # 850mm
print(f"Travel: {door.TravelDistance.Value}mm")   # 850mm
```

---

## Factory Function

### `createSlidingDoor(name="SlidingDoor")`

Creates a new SlidingDoor in the active document (or creates a new document if none exists).

- Adds a `Part::FeaturePython` object
- Initializes `SlidingDoor` proxy
- Attempts to use `GlassPanelViewProvider` for visual styling; falls back to basic view provider with 70% transparency
- Calls `doc.recompute()` and prints confirmation message
- Returns the FreeCAD document object

---

## Testing

### Test Suite (14 tests)

| # | Test | What It Validates |
|---|------|-------------------|
| 1 | `test_basic_creation` | Default property values (Width, Height, Thickness, AttachmentType, PanelCount, TrackType, SlideDirection, OverlapWidth, RollerType, TrackFinish, ShowHardware) |
| 2 | `test_panel_count_validation` | PanelCount clamped to range 1-2 |
| 3 | `test_track_type_bypass_constraint` | Soft-Close allows PanelCount=2; Edge, City, Ezy reset to 1 |
| 4 | `test_ezy_track_glass_constraint` | Ezy track warns on incompatible glass thickness (6mm, 8mm); accepts 10mm, 12mm |
| 5 | `test_track_types` | All four track types produce correct TrackHeight from TRACK_PROFILES |
| 6 | `test_overlap_calculations` | OpeningWidth = Width - OverlapWidth; OverlapWidth min/max clamping |
| 7 | `test_travel_distance` | Single panel travel = Width; Bypass travel = Width - OverlapWidth |
| 8 | `test_track_length` | Single track = Width*2 + 100; Bypass track = Width*3 - OverlapWidth + 100 |
| 9 | `test_hardware_visibility` | ShowHardware toggle changes bounding box size |
| 10 | `test_bypass_configuration` | 2-panel creates compound shape with correct OpeningWidth and TravelDistance |
| 11 | `test_track_finishes` | Chrome, Brushed-Nickel, Matte-Black all accepted |
| 12 | `test_slide_directions` | Left and Right both accepted |
| 13 | `test_roller_types` | Standard and Soft-Close both accepted |
| 14 | `test_position_and_rotation` | Position vector and rotation angle applied correctly |

### Running Tests

In FreeCAD Python console:
```python
exec(open(r'path/to/test_sliding_door.py').read())
```

Or call individual test functions:
```python
from freecad.ShowerDesigner.Tests.test_sliding_door import run_all_tests
run_all_tests()
```

---

## Future Enhancements (Phase 2+)

- Door animation (smooth slide open/close)
- Soft-close damper visualization on Soft-Close track
- Detailed roller carriage geometry (replace cylinders with shaped profiles)
- Panel stop/bumper hardware
- Anti-jump track clips
- Custom handle models (STEP import)
- Water deflector strip on bottom edge
