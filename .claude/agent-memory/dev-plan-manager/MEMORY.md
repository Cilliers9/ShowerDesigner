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

## Implementation Status (2026-02-24 review)
Overall: ~87% complete (adjusted from plan's 84%).
Uncommitted work: +402 lines across 7 files (seal deduction system).

### HardwareSpecs.py Contents (~2530 lines)
- Hinges: HINGE_SPECS(3), BEVEL_HINGE_SPECS(10), BIFOLD_HINGE_SPECS, MONZA_BIFOLD_HINGE_SPECS(2)
- Handles: HANDLE_SPECS(3), CATALOGUE_HANDLE_SPECS(18)
- Clamps: CLAMP_SPECS(7), BEVEL_CLAMP_SPECS(13)
- Sliders: SLIDER_SYSTEM_SPECS(3 systems), TRACK/ROLLER/GUIDE specs
- 15+ validation/helper functions

### SealSpecs.py (new dedicated file)
- SEAL_SPECS(3 generic), CATALOGUE_SEAL_SPECS(18 types, 6 categories)
- DOOR_SEAL_DEDUCTIONS, CORNER_DOOR_CONSTRAINTS
- Helper functions for seal selection, deductions, door constraints

### Missing: Models/Seal.py (3D seal geometry not created)

## Key Dependencies
- Task 1.1 (GlassPanel) is foundational
- Task 3.5 (Clamp Catalog) depends on 1.4 (Fixed Panel)
- Task 2.3 (BiFoldDoor) depends on 1.1 and 2.1

## File Locations
- Dev Plan: `Documentation/Dev_Plan/PHASE1-PLAN.md`
- Assembly Plan: `Documentation/Dev_Plan/ASSEMBLY-PLAN.MD`
- Implementation docs: `Documentation/Dev_Plan/TASK_X.Y_IMPLEMENTATION.md`
- Catalogue reviews: `Resources/Documents/`
- Corner layout research: `Resources/Documents/Possible corner enclosure layout - Sheet1.csv`

## User Preferences for Plan Updates
- User prefers conservative status estimates (e.g., enclosures at 50%, not 100%)
- User accepts large batch edits for section rewrites but may reject small individual edits
- Do larger, comprehensive edits rather than many small ones

## Remaining Work (prioritized)
1. Commit seal deduction work (7 modified files)
2. Seal 3D model (Models/Seal.py) -- not started
3. Panel gap validation tied to seal fitment (Task 1.3 remaining)
4. Enclosure enhancements (4.1-4.4) -- CornerEnclosure ~65%, others ~50%
5. Catalogue-level support bar specs (Task 3.3)
6. AlcoveEnclosure: fixed side panel, return panel, track refinement
7. WalkInEnclosure: multi-panel configs, ceiling support
8. Documentation and examples
9. Code quality (Black formatting, Ruff, tooltips)

## Plan Update Log
- 2026-02-24: Added Task 3.6 (Seal Deduction System) to PHASE1-PLAN.md. Updated
  status percentages for 2.2 (90->95%), 3.4 (60->80%), 4.1 (50->65%). Updated
  Task descriptions for 1.4, 2.1, 2.2, 2.3, 3.4, 4.1 to reflect seal integration.
  Overall completion updated from 84% to 87%. No Project_Summary.md exists.
