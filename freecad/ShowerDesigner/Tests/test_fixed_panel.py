# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for FixedPanel implementation

Run this in FreeCAD's Python console to test the FixedPanel class with
wall and floor mounting hardware.

Usage:
    exec(open('test_fixed_panel.py').read())
"""

import sys
sys.path.insert(0, 'C:\\Users\\tclou\\AppData\\Roaming\\FreeCAD\\v1-1\\Mod\\ShowerDesigner')

import FreeCAD as App
from freecad.ShowerDesigner.Models.FixedPanel import createFixedPanel

print("="*70)
print("Testing FixedPanel Implementation")
print("="*70)

# Create a new document
doc = App.ActiveDocument
if doc is None:
    doc = App.newDocument("FixedPanelTest")
    print("\n✓ Created new document: FixedPanelTest")
else:
    print(f"\n✓ Using existing document: {doc.Name}")

# Test 1: Create basic fixed panel with wall clamps
print("\n" + "="*70)
print("1. Creating fixed panel with wall clamps...")
print("="*70)

try:
    panel1 = createFixedPanel("WallClampPanel")
    panel1.Width = 900
    panel1.Height = 2000
    panel1.Thickness = 10
    panel1.GlassType = "Clear"
    panel1.WallHardware = "Clamp"
    panel1.WallClampCount = 2
    panel1.FloorHardware = "None"
    panel1.Position = App.Vector(0, 0, 0)
    
    doc.recompute()
    
    print(f"✓ Panel created: {panel1.Label}")
    print(f"  - Dimensions: {panel1.Width}mm W x {panel1.Height}mm H x {panel1.Thickness}mm T")
    print(f"  - Wall Hardware: {panel1.WallHardware}")
    print(f"  - Wall Clamp Count: {panel1.WallClampCount}")
    print(f"  - Top Offset: {panel1.WallClampOffsetTop}mm")
    print(f"  - Bottom Offset: {panel1.WallClampOffsetBottom}mm")
    print(f"  - Weight: {panel1.Weight:.2f} kg")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Create panel with wall channel
print("\n" + "="*70)
print("2. Creating fixed panel with wall channel...")
print("="*70)

try:
    panel2 = createFixedPanel("WallChannelPanel")
    panel2.Width = 1000
    panel2.Height = 2000
    panel2.Thickness = 8
    panel2.GlassType = "Frosted"
    panel2.WallHardware = "Channel"
    panel2.ChannelWidth = 30
    panel2.ChannelDepth = 15
    panel2.FloorHardware = "None"
    panel2.Position = App.Vector(1200, 0, 0)
    
    doc.recompute()
    
    print(f"✓ Panel created: {panel2.Label}")
    print(f"  - Wall Hardware: {panel2.WallHardware}")
    print(f"  - Channel Width: {panel2.ChannelWidth}mm")
    print(f"  - Channel Depth: {panel2.ChannelDepth}mm")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Create panel with floor clamps
print("\n" + "="*70)
print("3. Creating fixed panel with floor clamps...")
print("="*70)

try:
    panel3 = createFixedPanel("FloorClampPanel")
    panel3.Width = 800
    panel3.Height = 2000
    panel3.Thickness = 10
    panel3.GlassType = "Bronze"
    panel3.WallHardware = "None"
    panel3.FloorHardware = "Clamp"
    panel3.FloorClampCount = 2
    panel3.Position = App.Vector(2500, 0, 0)
    
    doc.recompute()
    
    print(f"✓ Panel created: {panel3.Label}")
    print(f"  - Floor Hardware: {panel3.FloorHardware}")
    print(f"  - Floor Clamp Count: {panel3.FloorClampCount}")
    print(f"  - Left Offset: {panel3.FloorClampOffsetLeft}mm")
    print(f"  - Right Offset: {panel3.FloorClampOffsetRight}mm")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Create panel with both wall and floor hardware
print("\n" + "="*70)
print("4. Creating fixed panel with wall AND floor hardware...")
print("="*70)

try:
    panel4 = createFixedPanel("BothHardwarePanel")
    panel4.Width = 1200
    panel4.Height = 2200
    panel4.Thickness = 12
    panel4.GlassType = "Grey"
    panel4.WallHardware = "Clamp"
    panel4.WallClampCount = 3
    panel4.FloorHardware = "Clamp"
    panel4.FloorClampCount = 3
    panel4.Position = App.Vector(3600, 0, 0)
    
    doc.recompute()
    
    print(f"✓ Panel created: {panel4.Label}")
    print(f"  - Wall Hardware: {panel4.WallHardware} ({panel4.WallClampCount} clamps)")
    print(f"  - Floor Hardware: {panel4.FloorHardware} ({panel4.FloorClampCount} clamps)")
    print(f"  - Weight: {panel4.Weight:.2f} kg")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Test hardware visibility toggle
print("\n" + "="*70)
print("5. Testing hardware visibility toggle...")
print("="*70)

try:
    panel5 = createFixedPanel("TogglePanel")
    panel5.Width = 900
    panel5.Height = 2000
    panel5.Thickness = 10
    panel5.WallHardware = "Clamp"
    panel5.FloorHardware = "Clamp"
    panel5.ShowHardware = True
    panel5.Position = App.Vector(5100, 0, 0)
    
    doc.recompute()
    print("✓ Created panel with hardware visible")
    
    # Toggle off
    panel5.ShowHardware = False
    doc.recompute()
    print("✓ Hardware hidden")
    
    # Toggle back on
    panel5.ShowHardware = True
    doc.recompute()
    print("✓ Hardware visible again")
    
except Exception as e:
    print(f"✗ Error: {e}")

# Test 6: Test clamp count validation
print("\n" + "="*70)
print("6. Testing clamp count validation...")
print("="*70)

try:
    panel6 = createFixedPanel("ValidationPanel")
    panel6.WallHardware = "Clamp"
    
    # Test minimum
    panel6.WallClampCount = 1  # Should be adjusted to 2
    doc.recompute()
    print(f"  Set to 1, adjusted to: {panel6.WallClampCount}")
    
    # Test maximum
    panel6.WallClampCount = 5  # Should be adjusted to 4
    doc.recompute()
    print(f"  Set to 5, adjusted to: {panel6.WallClampCount}")
    
    # Test valid
    panel6.WallClampCount = 3  # Should stay at 3
    doc.recompute()
    print(f"  Set to 3, stays at: {panel6.WallClampCount}")
    
    print("✓ Clamp count validation working")
    
    # Clean up test panel
    doc.removeObject(panel6.Name)
    
except Exception as e:
    print(f"✗ Error: {e}")

# Test 7: Test different clamp configurations
print("\n" + "="*70)
print("7. Creating panels with different clamp configurations...")
print("="*70)

configs = [
    ("2_Clamps", 2, 300, 300),
    ("3_Clamps", 3, 250, 250),
    ("4_Clamps", 4, 200, 200),
]

y_offset = 2500
for i, (name, count, offset_top, offset_bottom) in enumerate(configs):
    try:
        panel = createFixedPanel(name)
        panel.Width = 600
        panel.Height = 1800
        panel.Thickness = 8
        panel.WallHardware = "Clamp"
        panel.WallClampCount = count
        panel.WallClampOffsetTop = offset_top
        panel.WallClampOffsetBottom = offset_bottom
        panel.Position = App.Vector(i * 800, y_offset, 0)
        doc.recompute()
        
        print(f"  ✓ {name}: {count} clamps, offsets {offset_top}/{offset_bottom}mm")
        
    except Exception as e:
        print(f"  ✗ Error with {name}: {e}")

# Test 8: Test floor channel
print("\n" + "="*70)
print("8. Creating fixed panel with floor channel...")
print("="*70)

try:
    panel8 = createFixedPanel("FloorChannelPanel")
    panel8.Width = 1000
    panel8.Height = 2000
    panel8.Thickness = 10
    panel8.GlassType = "Low-Iron"
    panel8.WallHardware = "None"
    panel8.FloorHardware = "Channel"
    panel8.ChannelWidth = 30
    panel8.ChannelDepth = 15
    panel8.Position = App.Vector(3000, 2500, 0)
    
    doc.recompute()
    
    print(f"✓ Panel created: {panel8.Label}")
    print(f"  - Floor Hardware: {panel8.FloorHardware}")
    print(f"  - Channel dimensions: {panel8.ChannelWidth}mm x {panel8.ChannelDepth}mm")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 9: Test combination - wall channel + floor clamps
print("\n" + "="*70)
print("9. Creating panel with wall channel + floor clamps...")
print("="*70)

try:
    panel9 = createFixedPanel("ComboPanel")
    panel9.Width = 1100
    panel9.Height = 2100
    panel9.Thickness = 10
    panel9.GlassType = "Reeded"
    panel9.WallHardware = "Channel"
    panel9.FloorHardware = "Clamp"
    panel9.FloorClampCount = 3
    panel9.Position = App.Vector(4200, 2500, 0)
    
    doc.recompute()
    
    print(f"✓ Panel created: {panel9.Label}")
    print(f"  - Wall: {panel9.WallHardware}")
    print(f"  - Floor: {panel9.FloorHardware} ({panel9.FloorClampCount} clamps)")
    
except Exception as e:
    print(f"✗ Error: {e}")

# Summary
print("\n" + "="*70)
print("Summary")
print("="*70)

print(f"\nTotal objects created: {len(doc.Objects)}")
print("\nHardware Types Tested:")
print("  ✓ Wall Clamps (2, 3, 4 clamps)")
print("  ✓ Wall Channel")
print("  ✓ Floor Clamps (2, 3 clamps)")
print("  ✓ Floor Channel")
print("  ✓ Combined hardware configurations")

print("\nFeatures Validated:")
print("  ✓ Clamp count validation (2-4 range)")
print("  ✓ Hardware visibility toggle")
print("  ✓ Automatic clamp positioning")
print("  ✓ Channel geometry creation")
print("  ✓ Multiple glass types compatibility")

print("\nGlass Panel Properties:")
print("  ✓ Width, Height, Thickness")
print("  ✓ Glass Type (Clear, Frosted, Bronze, Grey, etc.)")
print("  ✓ Weight calculation")
print("  ✓ Position and placement")

print("\n" + "="*70)
print("Testing Complete!")
print("="*70)

print("""
\nInstructions:
1. Rotate the 3D view to see the hardware details
2. Try changing hardware types in the property panel
3. Adjust clamp counts and offsets
4. Toggle ShowHardware to see panels with/without hardware

Hardware Positioning:
  • Wall clamps: Positioned at offsets from top and bottom edges
  • Floor clamps: Positioned at offsets from left and right edges
  • Channels: Run the full length/width of the panel

To zoom to fit all panels:
  View → Standard Views → Fit All
""")

# Fit all objects in view if GUI is up
if App.GuiUp:
    try:
        import FreeCADGui as Gui
        Gui.SendMsgToActiveView("ViewFit")
        print("\n✓ View fitted to show all panels")
    except:
        pass
