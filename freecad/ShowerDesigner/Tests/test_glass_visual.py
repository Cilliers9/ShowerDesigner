# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Visual test script for GlassPanel visual properties

This script creates multiple glass panels with different glass types
to demonstrate the visual appearance in FreeCAD's 3D view.

Run this in FreeCAD's Python console:
    exec(open('test_glass_visual.py').read())
"""

import sys
sys.path.insert(0, '/home/claude')

import FreeCAD as App
from freecad.ShowerDesigner.Models.GlassPanel import createGlassPanel

print("="*70)
print("Visual Glass Properties Test")
print("="*70)

# Create a new document
doc = App.ActiveDocument
if doc is None:
    doc = App.newDocument("GlassVisualTest")
    print("\n✓ Created new document: GlassVisualTest")
else:
    print(f"\n✓ Using existing document: {doc.Name}")

# Glass types to test with their expected appearance
glass_types = [
    ("Clear", "Very transparent, slight blue tint"),
    ("Frosted", "Semi-transparent, privacy glass"),
    ("Bronze", "Bronze tint, moderate transparency"),
    ("Grey", "Grey tint, moderate transparency"),
    ("Reeded", "Textured appearance, semi-transparent"),
    ("Low-Iron", "Ultra-clear, minimal tint")
]

print("\n" + "="*70)
print("Creating glass panel showcase...")
print("="*70)

panels = []
x_offset = 0
spacing = 1200  # mm spacing between panels

for i, (glass_type, description) in enumerate(glass_types):
    print(f"\n{i+1}. Creating {glass_type} panel...")

    try:
        # Create panel
        panel = createGlassPanel(f"{glass_type}Panel")

        # Set standard dimensions
        panel.Width = 900
        panel.Height = 2000
        panel.Thickness = 10

        # Set glass type
        panel.GlassType = glass_type

        # Position panels in a row
        panel.Position = App.Vector(x_offset, 0, 0)
        x_offset += spacing

        # Recompute to apply changes
        doc.recompute()

        panels.append(panel)

        # Display properties
        print(f"   ✓ Panel created: {panel.Label}")
        print(f"   - Glass Type: {glass_type}")
        print(f"   - Description: {description}")

        if App.GuiUp and hasattr(panel, "ViewObject"):
            vobj = panel.ViewObject
            print(f"   - Shape Color: {vobj.ShapeColor}")
            print(f"   - Transparency: {vobj.Transparency}%")
            print(f"   - Display Mode: {vobj.DisplayMode}")

    except Exception as e:
        print(f"   ✗ Error creating {glass_type} panel: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*70)
print("Testing property changes...")
print("="*70)

if panels:
    test_panel = panels[0]
    print(f"\nTesting dynamic glass type changes on: {test_panel.Label}")

    original_type = test_panel.GlassType

    # Test changing glass types
    test_sequence = ["Frosted", "Bronze", "Clear"]

    for new_type in test_sequence:
        try:
            print(f"\n   Changing to {new_type}...")
            test_panel.GlassType = new_type
            doc.recompute()

            if App.GuiUp:
                vobj = test_panel.ViewObject
                print(f"   ✓ Color: {vobj.ShapeColor}")
                print(f"   ✓ Transparency: {vobj.Transparency}%")
            else:
                print(f"   ✓ Type changed (GUI not available)")

        except Exception as e:
            print(f"   ✗ Error: {e}")

    # Restore original
    test_panel.GlassType = original_type
    doc.recompute()
    print(f"\n   ✓ Restored to original type: {original_type}")

print("\n" + "="*70)
print("Creating comparison panels with different thicknesses...")
print("="*70)

# Create panels with different thicknesses
thicknesses = [6, 8, 10, 12]
y_offset = 2500  # mm offset from first row

print("\nCreating thickness comparison (all Clear glass):")

for i, thickness in enumerate(thicknesses):
    try:
        panel = createGlassPanel(f"Clear_{thickness}mm")
        panel.Width = 600
        panel.Height = 1800
        panel.Thickness = thickness
        panel.GlassType = "Clear"
        panel.Position = App.Vector(i * 800, y_offset, 0)
        doc.recompute()

        print(f"   ✓ {thickness}mm panel: Weight = {panel.Weight:.2f} kg")

    except Exception as e:
        print(f"   ✗ Error creating {thickness}mm panel: {e}")

print("\n" + "="*70)
print("Summary")
print("="*70)

print(f"\nTotal panels created: {len(doc.Objects)}")
print("\nVisual Properties Applied:")
print("  • Color tinting based on glass type")
print("  • Transparency levels for different glass types")
print("  • Edge highlighting with subtle line colors")
print("  • Flat Lines display mode for best visibility")

print("\n" + "="*70)
print("Instructions:")
print("="*70)
print("""
1. Rotate the 3D view to see the panels from different angles
2. Try changing glass types in the property panel
3. Observe how transparency and color change in real-time
4. Compare the different glass types side-by-side

Glass Type Visual Guide:
  • Clear: Very transparent with slight blue tint
  • Frosted: More opaque for privacy
  • Bronze: Warm bronze tint
  • Grey: Neutral grey tint
  • Reeded: Textured appearance
  • Low-Iron: Ultra-clear, minimal tint

To zoom to fit all panels:
  View → Standard Views → Fit All
""")

print("\n" + "="*70)
print("Visual Test Complete!")
print("="*70)

# Fit all objects in view if GUI is up
if App.GuiUp:
    try:
        import FreeCADGui as Gui
        Gui.SendMsgToActiveView("ViewFit")
        print("\n✓ View fitted to show all panels")
    except:
        pass
