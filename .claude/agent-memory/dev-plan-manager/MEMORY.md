# Dev Plan Manager Memory

## Document Structure Patterns

### PHASE1-PLAN.md Task Format
Tasks use `#### X.Y Name -- STATUS_MARKER` format.
Status markers: `✓ COMPLETE`, `◐ IN PROGRESS (X%)`, `○ NOT STARTED`
Completed tasks have "What was implemented:" sections; in-progress have "Remaining:" sections.

### Section Numbering
- 1. Glass Panel System Enhancement (1.1-1.4)
- 2. Door Implementation (2.1-2.3)
- 3. Hardware Library (3.1-3.6)
- 4. Enhanced Enclosure Models (4.1-4.4)

### Sprint Structure
- Sprint 1 (Week 1-2): Core Glass System -- COMPLETE
- Sprint 2 (Week 3-4): Door Systems -- COMPLETE
- Sprint 3 (Week 5-6): Hardware Integration -- COMPLETE
- Sprint 4 (Week 7-8): Finalization -- IN PROGRESS

## Architecture Evolution (CRITICAL)
- Major unplanned refactor: standalone Part::FeaturePython -> App::Part assembly architecture
- Plan shows inheritance (`class HingedDoor(GlassPanel)`) but reality is composition via assemblies
- AssemblyController in AssemblyBase.py is the base for ALL panel/door/enclosure models
- Each assembly: VarSet + GlassChild + hardware child proxies (ChildProxies.py)
- See: ASSEMBLY-PLAN.MD

## Seal System Architecture (2026-02-24)
- Seal specs extracted into dedicated `Data/SealSpecs.py` (separate from HardwareSpecs.py)
- Door seal deduction system: DOOR_SEAL_DEDUCTIONS, per-door-type seal options
- CornerEnclosure uses CORNER_DOOR_CONSTRAINTS for dynamic enum filtering
- FixedPanel has read-only SealDeduction property set by parent enclosure
- BiFoldDoor added: SillPlate, _calculateGlassDeductions(), GlassWidth/GlassHeight calculated props
- SlidingDoor: per-system glass deductions (duplo/edge_slider/city_slider), slide-direction offsets

## Implementation Status (2026-03-01 review)
Overall: ~86% complete.

### Complete Tasks
1.1 GlassPanel, 1.2 GlassSpecs, 1.4 FixedPanel, 2.1 HingedDoor, 2.3 BiFoldDoor,
3.1 Hinge Catalog, 3.2 Handle Library, 3.3 SupportBar, 3.4 Seals, 3.5 Clamp Catalog

### Near-Complete
2.2 SlidingDoor (95%), 3.6 SealDeduction (90% -- enclosure propagation pending)

### In Progress
1.3 PanelConstraints (60%), 4.1 CornerEnclosure (65%), 4.2-4.4 Enclosures (50% each)

### Not Started
- Models/Seal.py (3D seal geometry)
- Documentation and examples
- Code quality (Black, Ruff, tooltips)

## Existing Commands (Commands/__init__.py)
- Enclosures: Corner, Alcove, WalkIn, Custom (all functional)
- Components: GlassPanel, FixedPanel, HingedDoor, SlidingDoor, BiFoldDoor, Hinge, Clamp, SupportBar
- Tools: Measure (placeholder), CutList (placeholder), Export (placeholder)

## Phase 2 Hints (from PHASE1-PLAN.md "Future Enhancements")
- Door animation (open/close with constraints)
- Collision detection between panels
- Stress analysis for large panels
- Custom hardware import (STEP files)
- Material cost estimation
- Installation sequence generator

## HardwareSpecs.py Contents (~96KB, ~2530 lines)
- Hinges: HINGE_SPECS(3), BEVEL_HINGE_SPECS(10), BIFOLD_HINGE_SPECS, MONZA_BIFOLD_HINGE_SPECS(2)
- Handles: HANDLE_SPECS(3), CATALOGUE_HANDLE_SPECS(18)
- Clamps: CLAMP_SPECS(7), BEVEL_CLAMP_SPECS(13)
- Sliders: SLIDER_SYSTEM_SPECS(3 systems), TRACK/ROLLER/GUIDE specs
- 15+ validation/helper functions

## Key Dependencies
- Task 1.1 (GlassPanel) is foundational
- Task 3.6 (Seal Deduction) depends on 3.4, 2.1, 2.2, 2.3, 1.4
- Enclosure tasks (4.x) depend on panels + doors + hardware

## File Locations
- Dev Plan: `Documentation/Dev_Plan/PHASE1-PLAN.md`
- Assembly Plan: `Documentation/Dev_Plan/ASSEMBLY-PLAN.MD`
- Implementation docs: `Documentation/Dev_Plan/TASK_X.Y_IMPLEMENTATION.md`
- Catalogue reviews: `Resources/Documents/`

## User Preferences for Plan Updates
- User prefers conservative status estimates
- Do larger, comprehensive edits rather than many small ones

## Plan Update Log
- 2026-03-01: Task 3.4 marked COMPLETE (per-location seal selection, commit 668f024)
- 2026-03-01: Task 3.6 status table corrected from 100% to 90% (was premature)
- 2026-03-01: Updated MIN_WALL_FLOOR_GAP/MIN_WALL_CLEARANCE from 6mm to 2mm in Task 1.3
- 2026-02-24: Added Task 3.6, updated status percentages, overall 84->87%
- 2026-02-27: Full project review for Phase 2 planning
