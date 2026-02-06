# Fixed Panel Quick Reference

## Creating a Fixed Panel

### Via GUI
1. Switch to **ShowerDesigner** workbench
2. Click **Fixed Panel** in Components toolbar
3. Configure properties in Property Editor

### Via Python
```python
from freecad.ShowerDesigner.Models.FixedPanel import createFixedPanel
panel = createFixedPanel("MyPanel")
```

---

## Hardware Types at a Glance

### Wall Hardware

| Type | Use Case | Pros | Cons |
|------|----------|------|------|
| **None** | Special installations | Clean look | No support |
| **Clamp** | Frameless showers | Modern, adjustable | Visible hardware |
| **Channel** | Semi-frameless | Maximum stability | More visible |

### Floor Hardware

| Type | Use Case | Pros | Cons |
|------|----------|------|------|
| **None** | Walk-in showers (default) | Clean look | No bottom support |
| **Clamp** | High-traffic areas | Secure, adjustable | Installation complexity |
| **Channel** | Maximum stability | Continuous support | Most visible |

---

## Quick Configurations

### Standard Walk-In Panel
```python
panel.WallHardware = "Clamp"
panel.WallClampCount = 2
panel.FloorHardware = "None"
```

### High-Stability Panel
```python
panel.WallHardware = "Clamp"
panel.WallClampCount = 3
panel.FloorHardware = "Clamp"
panel.FloorClampCount = 2
```

### Maximum Support (Large Panel)
```python
panel.WallHardware = "Channel"
panel.FloorHardware = "Clamp"
panel.FloorClampCount = 3
```

---

## Common Settings

### Clamp Offsets

**Wall Clamps:**
- **Small panels (< 1800mm):** 250mm top/bottom
- **Standard panels (1800-2200mm):** 300mm top/bottom (default)
- **Large panels (> 2200mm):** 200mm top/bottom (more clamps needed)

**Floor Clamps:**
- **Narrow panels (< 800mm):** 50mm left/right
- **Standard panels (800-1200mm):** 75mm left/right (default)
- **Wide panels (> 1200mm):** 100mm left/right

### Clamp Counts

| Panel Height | Recommended Wall Clamps |
|--------------|-------------------------|
| < 1800mm | 2 |
| 1800-2200mm | 2-3 |
| > 2200mm | 3-4 |

| Panel Width | Recommended Floor Clamps |
|-------------|--------------------------|
| < 900mm | 2 |
| 900-1500mm | 2-3 |
| > 1500mm | 3-4 |

---

## Hardware Visibility

### During Design
```python
panel.ShowHardware = True  # See mounting positions
```

### For Export (Glass Only)
```python
panel.ShowHardware = False  # Hide hardware
# Export panel geometry
```

### For Assembly Instructions
```python
panel.ShowHardware = True  # Show mounting hardware
# Export with hardware visible
```

---

## Property Groups

### Dimensions
- Width, Height, Thickness
- Glass Type, Edge Finish, Temper Type
- Position, Rotation

### Wall Hardware
- Hardware Type (None/Channel/Clamp)
- Clamp Count (2-4)
- Offsets from edges
- Channel dimensions

### Floor Hardware
- Hardware Type (None/Channel/Clamp)
- Clamp Count (2-4)
- Offsets from edges

### Hardware Display
- Clamp Diameter (50mm default)
- Clamp Thickness (10mm default)
- Show Hardware (toggle)

### Calculated (Read-Only)
- Weight (kg)
- Area (m²)

---

## Workflow Tips

### 1. Start Simple
Create panel → Set dimensions → Choose glass type → Add wall hardware

### 2. Adjust Hardware
Start with 2 clamps → Increase if panel is large → Add floor support if needed

### 3. Fine-Tune Offsets
Use defaults first → Adjust based on specific installation → Consider wall studs

### 4. Validate
Check weight → Ensure hardware capacity → Verify spacing

### 5. Export
Hide hardware for glass cutting → Show hardware for installation guides

---

## Troubleshooting

### "Clamp count won't change"
- Valid range is 2-4
- Will auto-correct to nearest valid value

### "Hardware not visible"
- Check `ShowHardware = True`
- Call `doc.recompute()`

### "Clamps in wrong positions"
- Check offset values
- Verify panel height/width
- Ensure clamp count is correct

### "Channel not showing"
- Hardware type must be "Channel"
- Check channel dimensions > 0
- Verify ShowHardware is True

---

## Keyboard Shortcuts (Future)

| Shortcut | Action |
|----------|--------|
| Ctrl+Shift+F | Create Fixed Panel |
| H | Toggle Hardware Visibility |
| W | Cycle Wall Hardware Types |
| F | Cycle Floor Hardware Types |

*Note: Shortcuts not yet implemented*

---

## Related Documentation

- [Glass Panel Basics](./GLASS_VISUAL_QUICK_REFERENCE.md)
- [Task 1.4 Implementation](../Dev_Plan/TASK_1.4_IMPLEMENTATION.md)
- [Phase 1 Plan](../Dev_Plan/PHASE1-PLAN.md)

---

## Examples

### Example 1: Standard Walk-In
```python
panel = createFixedPanel("WalkIn")
panel.Width = 1000
panel.Height = 2000
panel.Thickness = 10
panel.GlassType = "Clear"
panel.WallHardware = "Clamp"
panel.WallClampCount = 2
```

### Example 2: High-Traffic Area
```python
panel = createFixedPanel("HighTraffic")
panel.Width = 1200
panel.Height = 2200
panel.Thickness = 12
panel.WallHardware = "Clamp"
panel.WallClampCount = 3
panel.FloorHardware = "Clamp"
panel.FloorClampCount = 3
```

### Example 3: Corner Panel
```python
panel = createFixedPanel("CornerPanel")
panel.Width = 900
panel.Height = 2000
panel.Thickness = 10
panel.WallHardware = "Channel"
panel.FloorHardware = "None"
panel.Position = App.Vector(0, 0, 0)
```
