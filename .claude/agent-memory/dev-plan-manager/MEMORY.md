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

## Glass Shelf System (2026-03-07)
- `Models/GlassShelf.py`: Standalone Part::FeaturePython, pentagonal profile with step notches
- `createGlassShelfShape()`: Reusable shape builder (XY plane, Z extrusion)
- Clearance logic: wall=5mm, glass=PanelThickness+2mm (from GLASS_SHELF_SPECS)
- CornerEnclosure integration: 4 shelf positions, dynamic filtering by layout
- `_getShelfCornerInfo()`: Returns origin, rotation, edge lengths, surface types per position
- Shelf clamp rotation pattern: Clamp1=Rotation(rot, 0, -90), Clamp2=Rotation(-90+rot, 0, -90)
- G2G clamps get 8mm perpendicular offset; clamp Z = shelf height + thickness
- Data: GLASS_SHELF_SPECS + SHELF_CLAMP_MAPPING in HardwareSpecs.py

## Implementation Status (2026-03-07 review)
Overall: ~91% complete.

### Complete Tasks
1.1 GlassPanel, 1.2 GlassSpecs, 1.4 FixedPanel, 2.1 HingedDoor, 2.3 BiFoldDoor,
3.1 Hinge Catalog, 3.2 Handle Library, 3.3 SupportBar, 3.4 Seals, 3.5 Clamp Catalog

### Near-Complete
2.2 SlidingDoor (95%), 3.6 SealDeduction (90%), 4.1 CornerEnclosure (95%),
4.2 AlcoveEnclosure (95%)

### In Progress
4.3 WalkInEnclosure (70%), 4.4 CustomEnclosure (60%)

### Not Started
- Models/Seal.py (3D seal geometry -- deferred to Phase 2)
- Documentation and examples
- Code quality (Black, Ruff, tooltips)

## Existing Commands (Commands/__init__.py)
- Enclosures: Corner, Alcove, WalkIn, Custom (all functional)
- Components: GlassPanel, FixedPanel, HingedDoor, SlidingDoor, BiFoldDoor, Hinge, Clamp, SupportBar
- Tools: Measure (placeholder), CutList (placeholder), Export (placeholder)

## HardwareSpecs.py Contents (~96KB, ~2530 lines)
- Hinges: HINGE_SPECS(3), BEVEL_HINGE_SPECS(10), BIFOLD_HINGE_SPECS, MONZA_BIFOLD_HINGE_SPECS(2)
- Handles: HANDLE_SPECS(3), CATALOGUE_HANDLE_SPECS(18)
- Clamps: CLAMP_SPECS(7), BEVEL_CLAMP_SPECS(13)
- Sliders: SLIDER_SYSTEM_SPECS(3 systems), TRACK/ROLLER/GUIDE specs
- Shelves: GLASS_SHELF_SPECS, SHELF_CLAMP_MAPPING
- 15+ validation/helper functions

## Key Dependencies
- Task 1.1 (GlassPanel) is foundational
- Task 3.6 (Seal Deduction) depends on 3.4, 2.1, 2.2, 2.3, 1.4
- Enclosure tasks (4.x) depend on panels + doors + hardware
- Glass shelf uses ClampChild from ChildProxies + SHELF_CLAMP_MAPPING from HardwareSpecs

## File Locations
- Dev Plan: `Documentation/Dev_Plan/PHASE1-PLAN.md`
- Phase 2 Plan: `Documentation/Dev_Plan/PHASE2-PLAN.md`
- Assembly Plan: `Documentation/Dev_Plan/ASSEMBLY-PLAN.MD`
- Implementation docs: `Documentation/Dev_Plan/TASK_X.Y_IMPLEMENTATION.md`
- Catalogue reviews: `Resources/Documents/`

## Common Pitfalls
- Status table % at top of PHASE1-PLAN.md can drift from section heading % -- always update both
- PHASE2-PLAN.md references Phase 1 completion % in prerequisites -- must be kept in sync
- "Additional completed work" section at bottom of PHASE1-PLAN.md tracks unplanned additions

## User Preferences for Plan Updates
- User prefers conservative status estimates
- Do larger, comprehensive edits rather than many small ones

## Plan Update Log
- 2026-03-07: Glass shelf system documented in 4.1, added to "Additional completed work"
- 2026-03-07: Fixed AlcoveEnclosure section heading (was 75%, corrected to 95%)
- 2026-03-07: Updated PHASE2-PLAN.md prerequisites from ~88% to ~91%
- 2026-03-01: Task 3.4 marked COMPLETE (per-location seal selection, commit 668f024)
- 2026-03-01: Task 3.6 status table corrected from 100% to 90% (was premature)
- 2026-02-24: Added Task 3.6, updated status percentages
- 2026-02-27: Full project review for Phase 2 planning
