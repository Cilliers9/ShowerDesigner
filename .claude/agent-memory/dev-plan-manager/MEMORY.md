# Dev Plan Manager Memory

## Document Structure Patterns

### PHASE1-PLAN.md Task Format
Tasks follow this structure:
```
#### X.Y Task Name
**Priority:** High/Medium/Low
**Estimated Effort:** Low/Medium/High
**Dependencies:** comma-separated task numbers (e.g., 1.1, 2.1)

**Objectives:**
- Bullet points of goals

**Implementation Details:**
**File:** `path/to/file.py`
```python
# Code snippets showing planned implementation
```

**Methods:** or **Features:**
- Additional details
```

### Section Numbering
- 1. Glass Panel System Enhancement (1.1-1.4)
- 2. Door Implementation (2.1-2.3)
- 3. Hardware Library (3.1-3.5)
- 4. Enhanced Enclosure Models (4.1-4.4)

### Sprint Structure
- Sprint 1 (Week 1-2): Core Glass System
- Sprint 2 (Week 3-4): Door Systems
- Sprint 3 (Week 5-6): Hardware Integration
- Sprint 4 (Week 7-8): Finalization

## Key Dependencies
- Task 1.1 (GlassPanel) is foundational - most other tasks depend on it
- Task 3.5 (Clamp Catalog) depends on 1.4 (Fixed Panel)
- Hardware tasks (3.x) support door/panel tasks
- Task 2.3 (BiFoldDoor) depends on 1.1 and 2.1

## File Locations
- Dev Plan: `Documentation/Dev_Plan/PHASE1-PLAN.md`
- Implementation docs: `Documentation/Dev_Plan/TASK_X.Y_IMPLEMENTATION.md`
- Usage guides: `Documentation/Usage/`

## Implementation Doc Template Pattern
All TASK_X.Y_IMPLEMENTATION.md files follow this structure:
1. Overview (1-sentence summary)
2. Files Created (table)
3. Files Modified (table)
4. Properties (tables grouped by category: Inherited, Configuration, Hardware, Display, Calculated)
5. Key Algorithms (formulas with single/bypass variants where applicable)
6. Visual Elements (numbered list of geometry shapes with dimensions)
7. Validation Rules (grouped by property name, describe clamping/warnings)
8. Usage (Command steps + Python examples)
9. Factory Function (description of createXxx())
10. Testing (numbered table of tests + run instructions)
11. Future Enhancements (Phase 2+ bullet list)

## Design Decisions
- BiFoldDoor is strictly a 2-panel design (no PanelCount property). User confirmed 2026-02-06.
- BiFoldDoor extends GlassPanel directly, NOT HingedDoor -- avoids inheriting unused swing properties.
- All door models share handle pattern: None/Knob/Bar/Pull with HandleHeight/Offset/Length.
- Door models override AttachmentType on init (Hinged for HingedDoor/BiFoldDoor, Sliding for SlidingDoor).
- GlassPanel base has 3 AttachmentType options: Fixed, Hinged, Sliding.

## Code Patterns
- Factory: `createXxx(name="Xxx")` - creates doc, Part::FeaturePython, proxy, ViewProvider, recompute
- Handle sizes: Knob=40mm dia x 15mm, Bar=24mm dia x HandleLength, Pull=20mm dia x 200mm
- Pivot hardware: Cylinders 8mm radius x 30mm height
- Hinge hardware: Boxes 65mm x 20mm x 90mm (W x D x H)

## Recent Changes
- 2026-02-06: Created TASK_2.3_IMPLEMENTATION.md as planning spec (not yet implemented)
- 2026-02-06: Updated PHASE1-PLAN.md Task 2.3 to reflect 2-panel fixed design
- 2026-02-06: Created TASK_2.2_IMPLEMENTATION.md documenting SlidingDoor.py
- 2026-02-05: Added Task 3.5 (Clamp Catalog) to Hardware Library section
