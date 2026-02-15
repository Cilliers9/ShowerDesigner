# Dev Plan Manager Memory

## Document Structure Patterns

### PHASE1-PLAN.md Task Format
Tasks use `#### X.Y Name -- STATUS_MARKER` format.
Status markers: `✓ COMPLETE`, `◐ IN PROGRESS (X%)`, `○ NOT STARTED`
Completed tasks have "What was implemented:" sections; in-progress have "Remaining:" sections.

### Section Numbering
- 1. Glass Panel System Enhancement (1.1-1.4)
- 2. Door Implementation (2.1-2.3)
- 3. Hardware Library (3.1-3.5)
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

## Implementation Status (2026-02-14)
Overall: ~84% complete (user-adjusted percentages).
- Status summary table added to top of PHASE1-PLAN.md
- All 16 task sections updated with implementation details
- Success criteria partially checked off
- "Additional completed work" section documents unplanned deliverables

### HardwareSpecs.py Contents (~2530 lines)
- Hinges: HINGE_SPECS(3), BEVEL_HINGE_SPECS(10), BIFOLD_HINGE_SPECS, MONZA_BIFOLD_HINGE_SPECS(2)
- Handles: HANDLE_SPECS(3), CATALOGUE_HANDLE_SPECS(18)
- Clamps: CLAMP_SPECS(7), BEVEL_CLAMP_SPECS(13)
- Seals: SEAL_SPECS(3), CATALOGUE_SEAL_SPECS(18 types, 6 categories)
- Sliders: SLIDER_SYSTEM_SPECS(3 systems), TRACK/ROLLER/GUIDE specs
- 15+ validation/helper functions

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

## User Preferences for Plan Updates
- User prefers conservative status estimates (e.g., enclosures at 50%, not 100%)
- User accepts large batch edits for section rewrites but may reject small individual edits
- Do larger, comprehensive edits rather than many small ones

## Remaining Work
1. Seal 3D model (Models/Seal.py) -- not started
2. SlidingDoor geometry refinements
3. Enclosure enhancements (4.1-4.4) -- all at ~50%
4. Catalogue-level support bar specs
5. Documentation and examples
6. Code quality (Black formatting, Ruff, tooltips)
