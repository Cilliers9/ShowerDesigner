# Glass Visual Properties - Quick Reference

## At a Glance

### 🎨 Glass Type Appearance

```
┌────────────┬────────────────────┬──────────────┬─────────────────────┐
│ Glass Type │ Color (RGB)        │ Transparency │ Best For            │
├────────────┼────────────────────┼──────────────┼─────────────────────┤
│ Clear      │ Light Blue         │ 85%          │ Standard showers    │
│            │ (0.7, 0.9, 1.0)    │              │ Maximum visibility  │
├────────────┼────────────────────┼──────────────┼─────────────────────┤
│ Low-Iron   │ Pure White         │ 90%          │ Luxury installations│
│            │ (1.0, 1.0, 1.0)    │              │ Ultra-clear view    │
├────────────┼────────────────────┼──────────────┼─────────────────────┤
│ Frosted    │ Light Blue         │ 50%          │ Privacy             │
│            │ (0.7, 0.9, 1.0)    │              │ Guest bathrooms     │
├────────────┼────────────────────┼──────────────┼─────────────────────┤
│ Bronze     │ Warm Bronze        │ 60%          │ Traditional style   │
│            │ (0.804, 0.498, 0.196)│            │ Vintage look        │
├────────────┼────────────────────┼──────────────┼─────────────────────┤
│ Grey       │ Dark Grey          │ 60%          │ Modern design       │
│            │ (0.25, 0.25, 0.25) │              │ Contemporary style  │
├────────────┼────────────────────┼──────────────┼─────────────────────┤
│ Reeded     │ Light Blue         │ 55%          │ Art Deco style      │
│            │ (0.7, 0.9, 1.0)    │              │ Textured privacy    │
└────────────┴────────────────────┴──────────────┴─────────────────────┘
```

## 📐 Visual Hierarchy

**Most Transparent → Most Opaque:**
```
Low-Iron (90%) > Clear (85%) > Bronze/Grey (60%) > Reeded (55%) > Frosted (50%)
```

**Warmest → Coolest Color:**
```
Bronze > Clear/Frosted/Reeded > Low-Iron > Grey
```

## 🖼️ Display Settings

### Default Configuration
- **Display Mode:** Flat Lines
- **Line Width:** 2.0 pixels
- **Line Color:** Dark Grey (0.3, 0.3, 0.3)
- **Shading:** Smooth

### Recommended Views
- **Orthographic:** For technical accuracy
- **Perspective:** For realistic appearance
- **Top View:** For layout planning
- **Front View:** For elevation details

## 🔄 How to Change Glass Type

```python
# In FreeCAD Python console or script:
panel.GlassType = "Bronze"  # Visual updates automatically
```

## ⚙️ Advanced Customization

### Manual Color Override (if needed)
```python
# Access ViewObject directly
panel.ViewObject.ShapeColor = (1.0, 0.5, 0.0)  # Orange tint
panel.ViewObject.Transparency = 70
```

### Change Display Mode
```python
panel.ViewObject.DisplayMode = "Shaded"
# Options: "Flat Lines", "Shaded", "Wireframe"
```

### Adjust Edge Appearance
```python
panel.ViewObject.LineWidth = 3.0
panel.ViewObject.LineColor = (0.0, 0.0, 0.0, 1.0)  # Black edges
```

## 🎯 Common Use Cases

### Standard Residential Shower
```python
panel.GlassType = "Clear"
panel.Thickness = 8  # mm
# Result: Transparent, economical
```

### High-End Luxury Installation
```python
panel.GlassType = "Low-Iron"
panel.Thickness = 10  # mm
# Result: Ultra-clear, premium appearance
```

### Privacy-Focused Bathroom
```python
panel.GlassType = "Frosted"
panel.Thickness = 6  # mm
# Result: Obscured view, privacy maintained
```

### Vintage/Traditional Style
```python
panel.GlassType = "Bronze"
panel.Thickness = 8  # mm
# Result: Warm tint, classic look
```

### Modern Minimalist Design
```python
panel.GlassType = "Grey"
panel.Thickness = 10  # mm
# Result: Sleek, contemporary appearance
```

## 🔍 Visual Comparison Tips

### Side-by-Side Testing
```python
# Create multiple panels to compare
types = ["Clear", "Frosted", "Bronze", "Grey"]
for i, glass_type in enumerate(types):
    panel = createGlassPanel(f"{glass_type}_Panel")
    panel.GlassType = glass_type
    panel.Position = App.Vector(i * 1200, 0, 0)
```

### Lighting Considerations
- Increase ambient lighting to see transparency better
- Use directional light to see tinting effects
- Rotate view to see glass from different angles

## 📊 Performance Notes

- **Light panels (Clear, Low-Iron):** Fastest rendering
- **Heavy opacity (Frosted):** Slightly slower due to transparency calculations
- **Multiple panels:** Minimal performance impact (tested up to 50+ panels)

## ⚠️ Important Notes

1. **Transparency is visual only** - doesn't affect weight calculations
2. **Colors are approximations** - actual glass varies by manufacturer
3. **Texture patterns** (Reeded, Frosted) shown via opacity, not actual texture
4. **Edge polish** not visually represented yet (all edges appear same)

## 🚀 Quick Test Command

```python
# Create visual showcase in one command:
exec(open('test_glass_visual.py').read())
```

This creates all glass types side-by-side for easy comparison!
