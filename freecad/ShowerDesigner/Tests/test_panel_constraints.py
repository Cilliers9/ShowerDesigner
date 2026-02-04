# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for PanelConstraints implementation

Run this in FreeCAD's Python console to test panel spacing and alignment.
"""

import sys
sys.path.insert(0, '/home/claude')

import FreeCAD as App
from freecad.ShowerDesigner.Models.GlassPanel import createGlassPanel
from freecad.ShowerDesigner.Data.PanelConstraints import (
    validateSpacing,
    checkPanelCollision,
    autoAlign,
    distributeEvenly,
    getPanelGap,
    snapToGrid,
    MIN_PANEL_SPACING,
    MAX_PANEL_SPACING,
    STANDARD_SPACING
)

print("="*70)
print("Testing Panel Constraints Implementation")
print("="*70)

# Create a new document
doc = App.ActiveDocument
if doc is None:
    doc = App.newDocument("ConstraintsTest")
    print("\n✓ Created new document: ConstraintsTest")
else:
    print(f"\n✓ Using existing document: {doc.Name}")

# Test 1: Create test panels
print("\n" + "="*70)
print("1. Creating test panels...")
print("="*70)

try:
    panel1 = createGlassPanel("Panel1")
    panel1.Width = 900
    panel1.Height = 2000
    panel1.Thickness = 8
    panel1.Position = App.Vector(0, 0, 0)

    panel2 = createGlassPanel("Panel2")
    panel2.Width = 900
    panel2.Height = 2000
    panel2.Thickness = 8
    panel2.Position = App.Vector(906, 0, 0)  # 6mm gap (standard)

    panel3 = createGlassPanel("Panel3")
    panel3.Width = 600
    panel3.Height = 2000
    panel3.Thickness = 8
    panel3.Position = App.Vector(1812, 0, 0)

    doc.recompute()

    print("✓ Created 3 test panels")
    print(f"  - Panel1: {panel1.Width}mm wide at {panel1.Position}")
    print(f"  - Panel2: {panel2.Width}mm wide at {panel2.Position}")
    print(f"  - Panel3: {panel3.Width}mm wide at {panel3.Position}")

except Exception as e:
    print(f"✗ Error creating panels: {e}")

# Test 2: Validate spacing
print("\n" + "="*70)
print("2. Testing spacing validation...")
print("="*70)

try:
    is_valid, msg, spacing = validateSpacing(panel1, panel2)
    print(f"Panel1 to Panel2:")
    print(f"  {'✓' if is_valid else '✗'} {msg}")

    is_valid, msg, spacing = validateSpacing(panel2, panel3)
    print(f"Panel2 to Panel3:")
    print(f"  {'✓' if is_valid else '✗'} {msg}")

    # Test with too small spacing
    panel_close = createGlassPanel("PanelClose")
    panel_close.Width = 900
    panel_close.Height = 2000
    panel_close.Thickness = 8
    panel_close.Position = App.Vector(901, 0, 0)  # Only 1mm gap
    doc.recompute()

    is_valid, msg, spacing = validateSpacing(panel1, panel_close)
    print(f"Panel1 to PanelClose (1mm gap):")
    print(f"  {'✓' if is_valid else '✗'} {msg}")

    doc.removeObject(panel_close.Name)

except Exception as e:
    print(f"✗ Error testing spacing: {e}")

# Test 3: Collision detection
print("\n" + "="*70)
print("3. Testing collision detection...")
print("="*70)

try:
    is_colliding, msg = checkPanelCollision(panel1, panel2)
    print(f"Panel1 vs Panel2:")
    print(f"  {'✗ COLLISION' if is_colliding else '✓'} {msg}")

    # Create overlapping panel
    panel_overlap = createGlassPanel("PanelOverlap")
    panel_overlap.Width = 900
    panel_overlap.Height = 2000
    panel_overlap.Thickness = 8
    panel_overlap.Position = App.Vector(800, 0, 0)  # Overlaps panel1
    doc.recompute()

    is_colliding, msg = checkPanelCollision(panel1, panel_overlap)
    print(f"Panel1 vs PanelOverlap:")
    print(f"  {'✗ COLLISION' if is_colliding else '✓'} {msg}")

    doc.removeObject(panel_overlap.Name)

except Exception as e:
    print(f"✗ Error testing collision: {e}")

# Test 4: Gap measurement
print("\n" + "="*70)
print("4. Testing gap measurement...")
print("="*70)

try:
    gap_x = getPanelGap(panel1, panel2, axis='X')
    print(f"Gap between Panel1 and Panel2 (X-axis): {gap_x:.2f}mm")

    gap_x = getPanelGap(panel2, panel3, axis='X')
    print(f"Gap between Panel2 and Panel3 (X-axis): {gap_x:.2f}mm")

except Exception as e:
    print(f"✗ Error measuring gap: {e}")

# Test 5: Auto-alignment
print("\n" + "="*70)
print("5. Testing auto-alignment...")
print("="*70)

try:
    # Create panels at different heights
    panel_a = createGlassPanel("PanelA")
    panel_a.Width = 600
    panel_a.Height = 1800
    panel_a.Position = App.Vector(3000, 0, 0)

    panel_b = createGlassPanel("PanelB")
    panel_b.Width = 600
    panel_b.Height = 1800
    panel_b.Position = App.Vector(3700, 0, 100)  # 100mm higher

    panel_c = createGlassPanel("PanelC")
    panel_c.Width = 600
    panel_c.Height = 1800
    panel_c.Position = App.Vector(4400, 0, 50)  # 50mm higher

    doc.recompute()

    print("Before alignment:")
    print(f"  PanelA Z: {panel_a.Position.z}mm")
    print(f"  PanelB Z: {panel_b.Position.z}mm")
    print(f"  PanelC Z: {panel_c.Position.z}mm")

    # Align to bottom
    success = autoAlign([panel_a, panel_b, panel_c], 'bottom')

    print("After bottom alignment:")
    print(f"  PanelA Z: {panel_a.Position.z}mm")
    print(f"  PanelB Z: {panel_b.Position.z}mm")
    print(f"  PanelC Z: {panel_c.Position.z}mm")

    if success:
        print("✓ Auto-alignment successful")
    else:
        print("✗ Auto-alignment failed")

except Exception as e:
    print(f"✗ Error testing alignment: {e}")

# Test 6: Even distribution
print("\n" + "="*70)
print("6. Testing even distribution...")
print("="*70)

try:
    # Create panels to distribute
    dist_panels = []
    for i in range(4):
        panel = createGlassPanel(f"DistPanel{i}")
        panel.Width = 400
        panel.Height = 1800
        panel.Thickness = 8
        panel.Position = App.Vector(i * 500, 1000, 0)
        dist_panels.append(panel)

    doc.recompute()

    print("Before distribution:")
    for p in dist_panels:
        print(f"  {p.Label} X: {p.Position.x}mm")

    # Distribute across 2400mm
    success = distributeEvenly(dist_panels, total_width=2400, axis='X', start_position=0)

    print("After distribution across 2400mm:")
    for p in dist_panels:
        print(f"  {p.Label} X: {p.Position.x}mm")

    # Calculate actual spacing
    for i in range(len(dist_panels) - 1):
        gap = getPanelGap(dist_panels[i], dist_panels[i+1], axis='X')
        print(f"  Gap {i} to {i+1}: {gap:.2f}mm")

    if success:
        print("✓ Even distribution successful")
    else:
        print("✗ Even distribution failed")

except Exception as e:
    print(f"✗ Error testing distribution: {e}")

# Test 7: Grid snapping
print("\n" + "="*70)
print("7. Testing grid snapping...")
print("="*70)

try:
    snap_panel = createGlassPanel("SnapPanel")
    snap_panel.Width = 600
    snap_panel.Height = 1800
    snap_panel.Position = App.Vector(1234.5, 567.8, 123.4)
    doc.recompute()

    print(f"Before snap: {snap_panel.Position}")

    success = snapToGrid(snap_panel, grid_size=100)

    print(f"After snap (100mm grid): {snap_panel.Position}")

    if success:
        print("✓ Grid snapping successful")
    else:
        print("✗ Grid snapping failed")

except Exception as e:
    print(f"✗ Error testing grid snap: {e}")

# Test 8: Constants verification
print("\n" + "="*70)
print("8. Constraint constants...")
print("="*70)

print(f"  MIN_PANEL_SPACING: {MIN_PANEL_SPACING}mm")
print(f"  MAX_PANEL_SPACING: {MAX_PANEL_SPACING}mm")
print(f"  STANDARD_SPACING: {STANDARD_SPACING}mm")

print("\n" + "="*70)
print("Summary")
print("="*70)

print(f"\nTotal objects created: {len(doc.Objects)}")
print("\nFunctions Tested:")
print("  ✓ validateSpacing() - Check panel spacing")
print("  ✓ checkPanelCollision() - Detect overlaps")
print("  ✓ getPanelGap() - Measure gaps")
print("  ✓ autoAlign() - Align panels")
print("  ✓ distributeEvenly() - Even spacing")
print("  ✓ snapToGrid() - Grid alignment")

print("\n" + "="*70)
print("Testing Complete!")
print("="*70)

# Fit all objects in view if GUI is up
if App.GuiUp:
    try:
        import FreeCADGui as Gui
        Gui.SendMsgToActiveView("ViewFit")
        print("\n✓ View fitted to show all panels")
    except:
        pass
