# Phase 1: Enhanced Models - Implementation Plan

## Overview

This phase focuses on improving the parametric models to create production-ready shower enclosure designs with proper glass panel systems, door mechanisms, and hardware integration.

---

## Task Breakdown

### 1. Glass Panel System Enhancement

#### 1.1 Separate Panel Objects
**Priority:** High  
**Estimated Effort:** Medium  
**Dependencies:** None

**Objectives:**
- Create individual `GlassPanel` class as standalone parametric object
- Support for multiple panels per enclosure
- Panel-to-panel relationships (parent/child hierarchy)

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Models/GlassPanel.py`

```python
class GlassPanel:
    """Individual glass panel with properties"""
    
    Properties:
    - Width: App::PropertyLength
    - Height: App::PropertyLength
    - Thickness: App::PropertyLength (6mm, 8mm, 10mm, 12mm)
    - GlassType: App::PropertyEnumeration (Clear, Frosted, Bronze, Grey, Reeded, Low-Iron)
    - EdgeFinish: App::PropertyEnumeration (Bright_Polish, Dull_Polish)
    - TemperType: App::PropertyEnumeration (Tempered, Laminated, None)
    - Position: App::PropertyVector
    - Rotation: App::PropertyAngle
    - AttachmentType: App::PropertyEnumeration (Fixed, Hinged, Sliding)
```

**Integration:**
- Update existing models to use GlassPanel objects
- Add panel management methods: `addPanel()`, `removePanel()`, `getPanels()`
- Implement panel constraints (spacing, alignment)

**Testing:**
- Create standalone panel
- Attach panel to enclosure
- Verify parameter updates
- Test different glass types

---

#### 1.2 Glass Properties Database
**Priority:** Medium  
**Estimated Effort:** Low  
**Dependencies:** 1.1

**Objectives:**
- Standardized glass specifications
- Weight calculations
- Safety factor validation

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Data/GlassSpecs.py`

```python
GLASS_SPECS = {
    "6mm": {"weight_kg_m2": 15, "min_panel_size": 300, "max_panel_size": 2400},
    "8mm": {"weight_kg_m2": 20, "min_panel_size": 300, "max_panel_size": 3000},
    "10mm": {"weight_kg_m2": 25, "min_panel_size": 400, "max_panel_size": 3600},
    "12mm": {"weight_kg_m2": 30, "min_panel_size": 400, "max_panel_size": 3600}
}

GLASS_TYPES = {
    "Clear": {"light_transmission": 0.90, "opacity": 0.2, "color": (0.7, 0.9, 1.0)},
    "Frosted": {"light_transmission": 0.75, "opacity": 0.8, "color": (0.7, 0.9, 1.0)},
    "Bronze": {"light_transmission": 0.60, "opacity": 0.3, "color": (0.804, 0.498, 0.196)},
    "Grey": {"light_transmission": 0.60, "opacity": 0.3, "color": (0.25, 0.25, 0.25)},
    "Reeded": {"light_transmission": 0.70, "opacity": 0.6, "color": (0.7, 0.9, 1.0)},
    "Low-Iron": {"light_transmission": 0.92, "opacity": 0.0, "color": (1.0, 1.0, 1.0)}
}
```

**Features:**
- Automatic weight calculation per panel
- Validation against max dimensions
- Visual representation of glass type (transparency/color)

---

#### 1.3 Panel Spacing and Constraints
**Priority:** High  
**Estimated Effort:** Medium  
**Dependencies:** 1.1

**Objectives:**
- Minimum spacing requirements between panels
- Automatic alignment tools
- Constraint visualization

**Implementation Details:**

**Constants:**
```python
MIN_PANEL_SPACING = 2  # mm (minimum gap for seals)
MAX_PANEL_SPACING = 10  # mm (maximum gap for waterproofing)
STANDARD_SPACING = 6  # mm (typical for frameless)
```

**Methods:**
```python
def validateSpacing(panel1, panel2):
    """Check if spacing between panels is within acceptable range"""
    
def autoAlign(panels, alignment_type):
    """Align panels: 'top', 'bottom', 'center'"""
    
def distributeEvenly(panels, total_width):
    """Distribute panels evenly across width"""
```

---

### 1.4 Fixed Panel Implementation
**Priority:** High  
**Estimated Effort:** Medium  
**Dependencies:** 1.1

**Objectives:**
- Parametric fixed panel with wall and floor fixings.
- Fixing hardware: None, Channels or CLamps
- 

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Models/FixedPanel.py`

```python
class FixedPanel(GlassPanel):
    """Hinged shower door with hardware"""
    
    Additional Properties:
    - WallHardware: App::PropertyEnumeration (None, Channel, Clamp)
    - FloorHardware: App::PropertyEnumeration (None, Channel, Clamp)
    - WallClampCount: App::PropertyInteger (1-2 hinges)
    - WallClampPlacement: App::PropertyVectorList
    - FloorClampCount: App::PropertyInteger (1-2 hinges)
    - FloorClampPlacement: App::PropertyVectorList
```

**Features:**
- Automatic WallClamp spacing calculation (Default: 300mm from top and bottom)
- Automatic FloorCLamp spacing calculation (Default: 75mm from left and right)

**Testing:**
- Test with different panel heights
- Validate clamp placement

---

### 2. Door Implementation

#### 2.1 Hinged Door System
**Priority:** High  
**Estimated Effort:** High  
**Dependencies:** 1.1

**Objectives:**
- Parametric hinged door with swing direction
- Hinge placement calculation
- Opening angle visualization

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Models/HingedDoor.py`

```python
class HingedDoor(GlassPanel):
    """Hinged shower door with hardware"""
    
    Additional Properties:
    - SwingDirection: App::PropertyEnumeration (Inward, Outward)
    - HingeCount: App::PropertyInteger (2-3 hinges)
    - HingePlacement: App::PropertyVectorList
    - OpeningAngle: App::PropertyAngle (default 90°, max 110°)
    - HandlePosition: App::PropertyVector
    - HandleType: App::PropertyEnumeration (Knob, Bar, Pull)
```

**Features:**
- Automatic hinge spacing calculation (top hinge 3000mm from top, bottom 300mm from bottom)
- Swing clearance validation
- Door weight calculation for hinge selection
- Visual representation of swing arc

**Testing:**
- Test both inward/outward swing
- Verify clearance with adjacent walls
- Test with different panel heights
- Validate hinge placement

---

#### 2.2 Sliding Door System
**Priority:** High  
**Estimated Effort:** High  
**Dependencies:** 1.1

**Objectives:**
- Track-based sliding mechanism
- Multi-panel sliding doors

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Models/SlidingDoor.py`

```python
class SlidingDoor(GlassPanel):
    """Sliding shower door with track system"""
    
    Additional Properties:
    - PanelCount: App::PropertyInteger (1-2 panels)
    - TrackType: App::PropertyEnumeration (Edge, City, Ezy, Soft-Close)
    - OverlapWidth: App::PropertyLength (typical 50mm)
    - RollerType: App::PropertyEnumeration (Standard, Soft-Close)
    - TrackFinish: App::PropertyEnumeration (Chrome, Brushed-Nickel, Matte-Black)
```

**Track System:**
- Top track dimensions based on panel count
- Bottom guide/roller placement
- Overlap calculation for bypass doors
- Travel distance limits

**Testing:**
- Single panel sliding
- Track length validation

---

#### 2.3 Bi-Fold Door System
**Priority:** Medium  
**Estimated Effort:** Medium  
**Dependencies:** 1.1, 2.1

**Objectives:**
- Folding panel mechanism
- Pivot point calculation
- Folded position visualization

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Models/BiFoldDoor.py`

```python
class BiFoldDoor(GlassPanel):
    """Bi-fold shower door (fixed 2-panel design)"""

    Additional Properties:
    - FoldDirection: App::PropertyEnumeration (Inward, Outward)
    - HingeSide: App::PropertyEnumeration (Left, Right)
    - PivotType: App::PropertyEnumeration (Inline, Offset)
    - FoldAngle: App::PropertyAngle (0-180, visualization)
    - PanelWidth: App::PropertyLength (auto-calculated = Width / 2)
    - FoldedWidth: App::PropertyLength (auto-calculated)
    - OpeningWidth: App::PropertyLength (auto-calculated)
    - ClearanceDepth: App::PropertyLength (auto-calculated)
```

**Calculations:**
- Panel width = Total Width / 2
- Pivot point offset (inline = 0mm vs offset = 15mm)
- Folded width = PanelWidth + Thickness [+ PivotOffset]
- Opening width = Width - FoldedWidth
- Clearance depth = PanelWidth + PivotOffset

---

### 3. Hardware Library

#### 3.1 Hinge Catalog
**Priority:** High  
**Estimated Effort:** Medium  
**Dependencies:** 2.1

**Objectives:**
- Standard hinge types and specifications
- Load capacity calculations
- Automatic hinge selection

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Data/HardwareSpecs.py`

```python
HINGES = {
    "standard_glass_to_glass": {
        "name": "Glass-to-Glass Hinge",
        "max_load_kg": 45,
        "glass_thickness": [8, 10, 12],
        "opening_angle": 90,
        "model_file": "StandardGTG.step"
    },
    "heavy_duty_wall_mount": {
        "name": "Heavy Duty Wall Mount",
        "max_load_kg": 100,
        "glass_thickness": [10, 12],
        "opening_angle": 90,
        "soft_close" : True,
        "model_file": "HeavyDutyGTWHinge.step"
    },
    "standard_wall_mount": {
        "name": "Standard Wall Mount",
        "max_load_kg": 45,
        "glass_thickness": [8, 10, 12],
        "opening_angle": 90,
        "model_file": "StandardGTWHinge.step"
    }
}
```

**File:** `freecad/ShowerDesigner/Models/Hinge.py`

```python
class Hinge:
    """Parametric hinge object"""
    
    Properties:
    - HingeType: App::PropertyEnumeration (from HINGES dict)
    - Position: App::PropertyVector
    - Rotation: App::PropertyAngle
    - LoadCapacity: App::PropertyFloat (read-only)
    - Finish: App::PropertyEnumeration (Chrome, Brushed, Matte-Black, Gold)
```

**Methods:**
```python
def selectHinge(door_weight, glass_thickness):
    """Automatically select appropriate hinge based on requirements"""
    
def calculateHingePlacement(door_height, panel_count):
    """Calculate optimal hinge positions"""
    
def validateLoad(hinge_type, total_door_weight, hinge_count):
    """Verify hinges can support door weight"""
```

---

#### 3.2 Handle and Knob Library
**Priority:** Medium  
**Estimated Effort:** Low  
**Dependencies:** None

**Objectives:**
- Standard handle types
- Ergonomic placement
- ADA compliance options

**Implementation Details:**

```python
HANDLES = {
    "towel_bar": {
        "name": "Towel Bar Handle",
        "lengths": [300, 450, 600],  # mm
        "mounting": "back-to-back",
        "ada_compliant": True,
        "model_file": "TowelBar.step"
    },
    "pull_handle": {
        "name": "Pull Handle",
        "lengths": [200, 300, 400],
        "mounting": "single-sided",
        "ada_compliant": True,
        "model_file": "PullHandle.step"
    },
    "knob": {
        "name": "Round Knob",
        "diameter": 40,  # mm
        "mounting": "single-sided",
        "ada_compliant": False,
        "model_file": "Knob.step"
    }
}
```

**Placement Guidelines:**
- Height: 1000-1100mm from floor (ADA: 900-1200mm)
- Offset from edge: minimum 75mm
- Clearance from walls: minimum 50mm

---

#### 3.3 Support Bars and Braces
**Priority:** Medium  
**Estimated Effort:** Medium  
**Dependencies:** 1.1

**Objectives:**
- Structural support for large panels
- Wall-to-glass bracing
- Ceiling support for walk-ins

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Models/SupportBar.py`

```python
class SupportBar:
    """Support bar/brace for glass panels"""
    
    Properties:
    - BarType: App::PropertyEnumeration (Horizontal, Vertical, Diagonal, Ceiling)
    - Length: App::PropertyLength
    - Diameter: App::PropertyLength (typical 12-25mm)
    - Finish: App::PropertyEnumeration
    - AttachmentPoints: App::PropertyVectorList
```

**Usage:**
- Walk-in panels > 1000mm wide: require support bar
- Fixed panels > 2400mm high: require ceiling support
- Glass-to-glass corners: require stabilizing bar

---

#### 3.4 Seals and Gaskets
**Priority:** Medium  
**Estimated Effort:** Low  
**Dependencies:** 1.1, 2.1, 2.2

**Objectives:**
- Water seal visualization
- Seal type selection
- Gap calculation

**Implementation Details:**

```python
SEALS = {
    "door_sweep": {
        "name": "Door Bottom Sweep",
        "thickness": 6,  # mm
        "gap_range": [0, 10],  # mm
        "length": "door_width"
    },
    "vertical_seal": {
        "name": "Vertical H-Channel",
        "thickness": 8,
        "glass_thickness": [8, 10, 12],
        "length": "door_height"
    },
    "magnetic_seal": {
        "name": "Magnetic Door Seal",
        "thickness": 10,
        "gap_range": [2, 6],
        "length": "door_height"
    }
}
```

---

#### 3.5 Clamp Catalog
**Priority:** High
**Estimated Effort:** Medium
**Dependencies:** 1.4

**Objectives:**
- Standard clamp types for fixed panel mounting
- Wall clamp and floor clamp specifications
- Load capacity and glass thickness compatibility
- Automatic clamp selection based on panel requirements

**Implementation Details:**

**File:** `freecad/ShowerDesigner/Data/HardwareSpecs.py` (extend existing)

```python
CLAMPS = {
    "wall_clamp_standard": {
        "name": "Standard Wall Clamp",
        "max_load_kg": 30,
        "glass_thickness": [8, 10, 12],
        "mounting": "wall",
        "model_file": "WallClampStandard.step"
    },
    "wall_clamp_heavy_duty": {
        "name": "Heavy Duty Wall Clamp",
        "max_load_kg": 50,
        "glass_thickness": [10, 12],
        "mounting": "wall",
        "model_file": "WallClampHeavyDuty.step"
    },
    "floor_clamp_standard": {
        "name": "Standard Floor Clamp",
        "max_load_kg": 40,
        "glass_thickness": [8, 10, 12],
        "mounting": "floor",
        "model_file": "FloorClampStandard.step"
    },
    "floor_clamp_adjustable": {
        "name": "Adjustable Floor Clamp",
        "max_load_kg": 50,
        "glass_thickness": [8, 10, 12],
        "mounting": "floor",
        "height_range": [10, 25],  # mm adjustment range
        "model_file": "FloorClampAdjustable.step"
    }
}
```

**File:** `freecad/ShowerDesigner/Models/Clamp.py`

```python
class Clamp:
    """Parametric clamp object for fixed panel mounting"""

    Properties:
    - ClampType: App::PropertyEnumeration (from CLAMPS dict)
    - Position: App::PropertyVector
    - Rotation: App::PropertyAngle
    - LoadCapacity: App::PropertyFloat (read-only)
    - Finish: App::PropertyEnumeration (Chrome, Brushed, Matte-Black, Gold)
    - MountingType: App::PropertyEnumeration (Wall, Floor)
```

**Methods:**
```python
def selectClamp(panel_weight, glass_thickness, mounting_type):
    """Automatically select appropriate clamp based on requirements"""

def calculateClampPlacement(panel_width, panel_height, mounting_type):
    """Calculate optimal clamp positions based on panel dimensions"""

def validateLoad(clamp_type, panel_weight, clamp_count):
    """Verify clamps can support panel weight"""
```

**Integration with FixedPanel:**
- Auto-select clamp type based on glass thickness and panel weight
- Calculate required number of clamps based on panel dimensions
- Validate total load capacity against panel weight

---

### 4. Enhanced Enclosure Models

#### 4.1 Update CornerEnclosure
**Priority:** High  
**Estimated Effort:** Medium  
**Dependencies:** 1.1, 2.1

**Updates:**
- Replace simple boxes with GlassPanel objects
- Add door configuration options
- Implement hinge placement
- Add hardware properties

**New Properties:**
```python
- DoorConfiguration: App::PropertyEnumeration (LeftHinged, RightHinged, LeftSliding, RightSliding)
- PanelLayout: App::PropertyEnumeration (TwoPanel, ThreePanel)
- IncludeHardware: App::PropertyBool
```

---

#### 4.2 Update AlcoveEnclosure
**Priority:** High  
**Estimated Effort:** Medium  
**Dependencies:** 1.1, 2.1, 2.2

**Updates:**
- Support for sliding and pivot doors
- Fixed side panels
- Proper track placement for sliders

**New Properties:**
```python
- SidePanelType: App::PropertyEnumeration (Fixed, Return, None)
- ReturnPanelWidth: App::PropertyLength
```

---

#### 4.3 Update WalkInEnclosure
**Priority:** High  
**Estimated Effort:** Medium  
**Dependencies:** 1.1, 3.3

**Updates:**
- Support bar integration
- Multiple panel configurations
- Ceiling-mounted options

**New Properties:**
```python
- PanelConfiguration: App::PropertyEnumeration (Single, Double-L, Double-Parallel)
- CeilingSupport: App::PropertyBool
- SupportBarHeight: App::PropertyLength
```

---

#### 4.4 Update CustomEnclosure
**Priority:** Low  
**Estimated Effort:** High  
**Dependencies:** All above

**Updates:**
- Free-form panel placement
- Mix of door types
- Advanced hardware placement

---

## Implementation Order

### Sprint 1 (Week 1-2): Core Glass System
1. Create GlassPanel class (1.1)
2. Implement glass specs database (1.2)
3. Add panel spacing/constraints (1.3)
4. Update CornerEnclosure to use GlassPanel (4.1)

### Sprint 2 (Week 3-4): Door Systems
1. Implement HingedDoor (2.1)
2. Implement SlidingDoor (2.2)
3. Update AlcoveEnclosure (4.2)
4. Testing and refinement

### Sprint 3 (Week 5-6): Hardware Integration
1. Create Hinge catalog and class (3.1)
2. Create Handle library (3.2)
3. Implement SupportBar (3.3)
4. Create Clamp catalog and class (3.5)
5. Update WalkInEnclosure (4.3)

### Sprint 4 (Week 7-8): Finalization
1. Implement BiFoldDoor (2.3)
2. Add Seals system (3.4)
3. Update CustomEnclosure (4.4)
4. Documentation and examples

---

## Success Criteria

### Functionality
- [ ] Create individual glass panels with properties
- [ ] Hinged doors open/close visually in 3D
- [ ] Sliding doors show track system
- [ ] Automatic hinge placement based on door weight
- [ ] Support bars calculated for large panels
- [ ] All enclosure types use new panel system

### Quality
- [ ] All models follow LGPL license headers
- [ ] Code formatted with Black
- [ ] No Ruff linting errors
- [ ] Documentation for each new class
- [ ] Example files for each door type

### User Experience
- [ ] Properties grouped logically
- [ ] Tooltips explain each parameter
- [ ] Models update in real-time
- [ ] Reasonable default values
- [ ] Validation prevents invalid configurations

---

## Testing Strategy

### Unit Testing
- Test each component in isolation
- Verify property constraints
- Check geometry generation

### Integration Testing
- Test complete enclosures
- Verify hardware placement
- Check panel relationships

### Manual Testing in FreeCAD
- Create each enclosure type
- Modify all properties
- Export to STEP format
- Visual inspection of hardware

---

## Documentation Requirements

### Code Documentation
- Docstrings for all classes and methods
- Inline comments for complex calculations
- Type hints for all functions

### User Documentation
- Update `Documentation/Usage/` with new features
- Create examples for each door type
- Hardware selection guide
- Glass specification guide

### Developer Documentation
- Architecture overview of panel system
- Hardware integration guide
- Adding new hardware types guide

---

## Future Enhancements (Phase 2+)

- Door animation (open/close with constraints)
- Collision detection between panels
- Stress analysis for large panels
- Custom hardware import (STEP files)
- Material cost estimation
- Installation sequence generator

---

## Notes

- Prioritize frameless shower compatibility (most common)
- All dimensions in millimeters
- Support both metric and imperial display
- Consider manufacturing tolerances (±2mm typical)
- Glass edge treatment affects dimensions
- Building codes vary by region (note in documentation)

---

## Resources

- [FreeCAD Part Module](https://wiki.freecad.org/Part_Module)
- [FeaturePython Objects](https://wiki.freecad.org/FeaturePython_Objects)
- Glass Industry Standards (GANA, SGCC, SESEMA)
- Shower Door Manufacturers' Specs
