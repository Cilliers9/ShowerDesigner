# FreeCAD Test-Runner Agent Memory

## Environment
- FreeCAD 1.1.0 on Windows 11, connected via XML-RPC (GUI available, not headless).
- Python 3.13.9 inside FreeCAD; workbench symlinked at `%APPDATA%\FreeCAD\v1-1\Mod\ShowerDesigner`.
- `sys.path.insert(0, 'C:\\Users\\tclou\\AppData\\Roaming\\FreeCAD\\v1-1\\Mod\\ShowerDesigner')` is required before importing workbench modules.

## How to Run Tests
- Tests in this repo are **script-style** (not pytest-compatible without FreeCAD).
  They are designed to be `exec()`'d inside FreeCAD's Python console.
- Use `mcp__freecad__execute_python` to run them. Assign `_result_` to get structured
  output back; do NOT rely on stdout for pass/fail detection.
- Always set a generous `timeout_ms` (30 000–60 000) because `doc.recompute()` can be slow
  over XML-RPC.

## Execution Patterns That Work
1. Wrap each logical test block in its own `try/except` and append to a `results` list.
2. Return `_result_` as a dict with pass counts, per-test details, etc.
3. Call `doc.recompute()` after every batch of property changes — FreeCAD does NOT
   auto-recompute over the RPC bridge.
4. After the main run, do a follow-up geometry sanity check: verify `obj.Shape` is
   non-null and that the number of Solids matches the expected hardware count.

## FixedPanel – Solid-Count Reference (ShowHardware = True)
| Hardware combo              | Expected solids |
|-----------------------------|-----------------|
| Wall Clamp (2) only         | 3  (panel + 2 box clamps) |
| Wall Channel only           | 2  (panel + channel shell) |
| Floor Clamp (2) only        | 3  |
| Wall Clamp (3) + Floor Clamp (3) | 7  (1 + 3 + 3) |
| Wall Clamp (2) + Floor Clamp (2) | 5  (1 + 2 + 2) |
| Wall Channel + Floor Clamp (3)   | 5  (1 + 1 + 3) |
| N clamps only               | N+1 |

NOTE: Clamps are now **box shapes** (40 x 20 x 40 mm), NOT cylinders.
The cylinder-BB 26-gon artefact notes below are historical only.

## Validation Rules (FixedPanel.onChanged)
- WallClampCount and FloorClampCount are clamped to [2, 4].
- Validation fires on property change via `onChanged`; always `doc.recompute()` after
  setting, then read back the value to confirm.

## Known Quirks
- `App::PropertyEnumeration` must be initialised with the list FIRST, then the default
  value in a second assignment (see GlassPanel.__init__ pattern).
- `App::PropertyLength` `.Value` returns a float in mm; printing the property directly
  shows the unit string (e.g. "300.0 mm").
- Objects whose names start with a digit get prefixed with `_` by FreeCAD
  (e.g. "2_Clamps" -> "_2_Clamps").
- `createFixedPanel` calls `doc.recompute()` internally, but property changes made
  AFTER creation require a manual recompute.

## Test Files & What They Cover
| File | Covers |
|------|--------|
| Tests/test_fixed_panel.py | FixedPanel creation, all hardware combos, visibility toggle, clamp-count validation |
| Tests/test_glass_panel.py | Base GlassPanel creation and properties |
| Tests/test_glass_visual.py | Glass visual / view-provider behaviour |
| Tests/test_panel_constraints.py | PanelConstraints spacing / collision logic |

## Cylinder BoundBox Artefact (FreeCAD kernel)
- `Part.makeCylinder` bounding boxes are computed from a **26-sided polygon**
  approximation of the circular cross-section, NOT from the analytic envelope.
- This means the reported BBox min/max in the radial direction is inset by
  `R * (1 - cos(pi/26))`.  For the default ClampDiameter=40 (R=20) this is
  exactly **0.146 mm** per side (BBox span = 39.708 instead of 40.000).
- The inset affects ONLY the two axes perpendicular to the cylinder axis.
- When writing position-check tests for cylinders, use a tolerance of at least
  0.15 mm, or better yet compute the expected inset analytically before comparing.
- Formula: `inset = radius * (1 - cos(pi / 26))`

## FixedPanel – Clamp Geometry Reference (local coordinates)
Panel box: X=[0, W], Y=[0, T], Z=[0, H].  (makeBox(W, T, H))
Clamp box: makeBox(40, 20, 40).  Exact volume = 32000.  6 Plane faces, 12 edges.

### Wall Clamps (box, no rotation)
- Created as makeBox(40, 20, 40).
- Translate: (W/2 - 20, T, z_pos - 20)
- Final doc-space min-corner:
    X: px + W/2 - 20
    Y: py + T              (flush against the back face of the panel)
    Z: pz + z_pos - 20     (centred on the computed z_pos)
- Bounding box spans: X=[min, min+40], Y=[min, min+20], Z=[min, min+40].  Exact, no inset.
- z_pos values come from _calculateClampPositions(H, count, offsetTop, offsetBot).

### Floor Clamps (box, no rotation)
- Created as makeBox(40, 20, 40).
- Translate: (x_pos - 20, -10, -20)
- Final doc-space min-corner:
    X: px + x_pos - 20     (centred on the computed x_pos)
    Y: py - 10             (extends 10 mm in front of panel origin)
    Z: pz - 20             (extends 20 mm below panel origin)
- Bounding box spans: X=[min, min+40], Y=[min, min+20], Z=[min, min+40].  Exact, no inset.
- x_pos values come from _calculateClampPositions(W, count, offsetLeft, offsetRight).

## Stale .pyc Cache – Critical Gotcha (discovered 2026-02-04)
- The `__pycache__/` directory contained `cpython-311.pyc` files even though FreeCAD
  runs Python 3.13.  These were left over from a prior environment or tooling run.
- When the source was changed from `makeCylinder` to `makeBox`, FreeCAD's Python 3.13
  interpreter loaded the `.py` file correctly, but **existing Proxy objects in an
  already-open document retained the old class** (the one that was `exec()`'d at
  document-load time).  `touch()` + `recompute()` was NOT enough to pick up the change.
- **Fix**: delete stale `.pyc` files, `importlib.reload()` the module chain, then create
  objects in a **new document**.  Do NOT rely on recomputing objects in an existing doc.
- The cpython-311 pyc files have been deleted.  If they reappear, something upstream
  (e.g. a linter or IDE) is regenerating them and should be checked.

## Last Run – 2026-02-04 (box-clamp verification)
- All clamps confirmed as box shapes (40 x 20 x 40 mm).
  - 6 Plane faces, 12 edges, volume = 32000 on every clamp solid.
  - Zero Cylinder surfaces anywhere in the geometry.
- Position verification across 6 panels, 20 clamp solids total:
    - 11 wall clamps (configs: 2, 3, 3, 4 clamps)
    - 9 floor clamps  (configs: 2, 3, 3 clamps)
    - **20/20 PASS**.  All min-corners match expected values to sub-mm precision (exact 0.0 delta).
- Wall clamps sit flush against the back face of the panel (Y_min == panel thickness).
- Floor clamps extend 10 mm in front of panel origin (Y_min == -10) and 20 mm below (Z_min == -20).
- Solid counts match the reference table for every hardware combo tested.
