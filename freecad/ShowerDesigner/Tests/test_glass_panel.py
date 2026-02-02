# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for GlassPanel implementation

Run this in FreeCAD's Python console to test the GlassPanel class.
"""

import sys
sys.path.insert(0, '/home/claude')

from freecad.ShowerDesigner.Models.GlassPanel import createGlassPanel
from freecad.ShowerDesigner.Data.GlassSpecs import (
    validateGlassThickness,
    validatePanelSize,
    calculatePanelWeight,
    getGlassColor,
    getGlassOpacity
)

print("="*60)
print("Testing GlassPanel Implementation")
print("="*60)

# Test 1: Create a basic glass panel
print("\n1. Creating basic glass panel...")
try:
    panel1 = createGlassPanel("TestPanel1")
    print(f"   ✓ Panel created: {panel1.Label}")
    print(f"   - Width: {panel1.Width}")
    print(f"   - Height: {panel1.Height}")
    print(f"   - Thickness: {panel1.Thickness}")
    print(f"   - Weight: {panel1.Weight:.2f} kg")
    print(f"   - Area: {panel1.Area:.2f} m²")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Test glass thickness validation
print("\n2. Testing glass thickness validation...")
test_thicknesses = [6, 8, 10, 12, 5, 15]
for thickness in test_thicknesses:
    is_valid, msg = validateGlassThickness(thickness)
    status = "✓" if is_valid else "✗"
    print(f"   {status} {thickness}mm: {msg}")

# Test 3: Test panel size validation
print("\n3. Testing panel size validation...")
test_cases = [
    (900, 2000, 8, "Standard panel"),
    (200, 500, 6, "Too small"),
    (2000, 4000, 8, "Too large for 8mm"),
    (2000, 3500, 10, "Valid for 10mm"),
]
for width, height, thickness, description in test_cases:
    is_valid, msg = validatePanelSize(width, height, thickness)
    status = "✓" if is_valid else "✗"
    print(f"   {status} {description} ({width}x{height}mm, {thickness}mm): {msg}")

# Test 4: Test weight calculation
print("\n4. Testing weight calculations...")
test_panels = [
    (900, 2000, 8),
    (1000, 2000, 10),
    (600, 1800, 6),
]
for width, height, thickness in test_panels:
    weight = calculatePanelWeight(width, height, thickness)
    area = (width/1000) * (height/1000)
    print(f"   {width}x{height}mm @ {thickness}mm: {weight:.2f} kg ({area:.2f} m²)")

# Test 5: Test glass types and colors
print("\n5. Testing glass types...")
glass_types = ["Clear", "Frosted", "Bronze", "Grey", "Reeded", "Low-Iron"]
for glass_type in glass_types:
    color = getGlassColor(glass_type)
    opacity = getGlassOpacity(glass_type)
    print(f"   {glass_type}: RGB{color}, Opacity: {opacity}")

# Test 6: Modify panel properties
print("\n6. Testing property modifications...")
try:
    panel1.Width = 1200
    panel1.Height = 2200
    panel1.Thickness = 10
    panel1.GlassType = "Bronze"
    panel1.Document.recompute()
    print(f"   ✓ Modified panel properties")
    print(f"   - New dimensions: {panel1.Width} x {panel1.Height} x {panel1.Thickness}")
    print(f"   - Glass type: {panel1.GlassType}")
    print(f"   - Updated weight: {panel1.Weight:.2f} kg")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 7: Create multiple panels with different types
print("\n7. Creating multiple panel types...")
panel_configs = [
    ("ClearPanel", 900, 2000, 8, "Clear"),
    ("FrostedPanel", 600, 1800, 6, "Frosted"),
    ("BronzePanel", 1000, 2000, 10, "Bronze"),
]
for name, width, height, thickness, glass_type in panel_configs:
    try:
        panel = createGlassPanel(name)
        panel.Width = width
        panel.Height = height
        panel.Thickness = thickness
        panel.GlassType = glass_type
        panel.Document.recompute()
        print(f"   ✓ {name}: {width}x{height}mm, {thickness}mm {glass_type}")
    except Exception as e:
        print(f"   ✗ Error creating {name}: {e}")

print("\n" + "="*60)
print("Testing Complete!")
print("="*60)
