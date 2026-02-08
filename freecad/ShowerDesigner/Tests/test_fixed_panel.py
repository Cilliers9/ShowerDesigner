# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for FixedPanel assembly implementation.

Run this in FreeCAD's Python console to test the FixedPanel assembly
with individual glass and hardware child objects.

Usage:
    exec(open('test_fixed_panel.py').read())
"""

import sys
sys.path.insert(0, 'C:\\Users\\tclou\\AppData\\Roaming\\FreeCAD\\v1-1\\Mod\\ShowerDesigner')

import FreeCAD as App
from freecad.ShowerDesigner.Models.FixedPanel import createFixedPanel


def _get_varset(part_obj):
    """Helper to find the VarSet child inside an assembly."""
    for child in part_obj.Group:
        if child.TypeId == "App::VarSet":
            return child
    return None


def _get_children_by_prefix(part_obj, prefix):
    """Get child objects whose Label starts with prefix."""
    return [c for c in part_obj.Group if c.Label.startswith(prefix)]


print("=" * 70)
print("Testing FixedPanel Assembly Implementation")
print("=" * 70)

# Create a new document
doc = App.ActiveDocument
if doc is None:
    doc = App.newDocument("FixedPanelTest")
    print("\nCreated new document: FixedPanelTest")
else:
    print(f"\nUsing existing document: {doc.Name}")


# Test 1: Basic assembly structure
print("\n" + "=" * 70)
print("1. Testing basic assembly structure...")
print("=" * 70)

try:
    panel1 = createFixedPanel("WallClampPanel")
    assert panel1.TypeId == "App::Part", f"Expected App::Part, got {panel1.TypeId}"
    print(f"  OK: Object is App::Part")

    vs = _get_varset(panel1)
    assert vs is not None, "VarSet not found in assembly"
    print(f"  OK: VarSet found")

    glass_list = _get_children_by_prefix(panel1, "Glass")
    assert len(glass_list) == 1, f"Expected 1 Glass child, got {len(glass_list)}"
    print(f"  OK: Glass child found")

    # Check VarSet default properties
    assert vs.Width.Value == 900, f"Expected Width=900, got {vs.Width.Value}"
    assert vs.Height.Value == 2000, f"Expected Height=2000, got {vs.Height.Value}"
    assert vs.Thickness.Value == 8, f"Expected Thickness=8, got {vs.Thickness.Value}"
    assert vs.GlassType == "Clear", f"Expected GlassType=Clear, got {vs.GlassType}"
    assert vs.WallHardware == "Clamp", f"Expected WallHardware=Clamp, got {vs.WallHardware}"
    assert vs.FloorHardware == "Clamp", f"Expected FloorHardware=Clamp, got {vs.FloorHardware}"
    print(f"  OK: VarSet default properties correct")

except Exception as e:
    print(f"  FAIL: {e}")
    import traceback
    traceback.print_exc()


# Test 2: Wall clamps created
print("\n" + "=" * 70)
print("2. Testing wall clamp children...")
print("=" * 70)

try:
    vs = _get_varset(panel1)
    vs.WallHardware = "Clamp"
    vs.WallClampCount = 2
    vs.WallMountEdge = "Left"
    doc.recompute()

    wall_clamps = _get_children_by_prefix(panel1, "WallClamp")
    assert len(wall_clamps) == 2, f"Expected 2 WallClamps, got {len(wall_clamps)}"
    print(f"  OK: 2 wall clamps created for Left edge")

    # Test Both edges
    vs.WallMountEdge = "Both"
    doc.recompute()
    wall_clamps = _get_children_by_prefix(panel1, "WallClamp")
    assert len(wall_clamps) == 4, f"Expected 4 WallClamps (Both edges), got {len(wall_clamps)}"
    print(f"  OK: 4 wall clamps created for Both edges")

    # Verify each clamp has a shape
    for clamp in wall_clamps:
        assert hasattr(clamp, "Shape"), f"{clamp.Label} missing Shape"
        assert not clamp.Shape.isNull(), f"{clamp.Label} has null shape"
    print(f"  OK: All clamps have valid shapes")

except Exception as e:
    print(f"  FAIL: {e}")
    import traceback
    traceback.print_exc()


# Test 3: Floor clamps created
print("\n" + "=" * 70)
print("3. Testing floor clamp children...")
print("=" * 70)

try:
    vs = _get_varset(panel1)
    vs.FloorHardware = "Clamp"
    vs.FloorClampCount = 2
    doc.recompute()

    floor_clamps = _get_children_by_prefix(panel1, "FloorClamp")
    assert len(floor_clamps) == 2, f"Expected 2 FloorClamps, got {len(floor_clamps)}"
    print(f"  OK: 2 floor clamps created")

    for clamp in floor_clamps:
        assert not clamp.Shape.isNull(), f"{clamp.Label} has null shape"
    print(f"  OK: All floor clamps have valid shapes")

except Exception as e:
    print(f"  FAIL: {e}")
    import traceback
    traceback.print_exc()


# Test 4: Wall channel
print("\n" + "=" * 70)
print("4. Testing wall channel children...")
print("=" * 70)

try:
    panel2 = createFixedPanel("WallChannelPanel")
    vs2 = _get_varset(panel2)
    vs2.WallHardware = "Channel"
    vs2.WallMountEdge = "Both"
    vs2.FloorHardware = "None"
    doc.recompute()

    channels = _get_children_by_prefix(panel2, "WallChannel")
    assert len(channels) == 2, f"Expected 2 WallChannels (Both), got {len(channels)}"
    print(f"  OK: 2 wall channels created for Both edges")

    for ch in channels:
        assert not ch.Shape.isNull(), f"{ch.Label} has null shape"
    print(f"  OK: All channels have valid shapes")

    # No clamps should exist
    wall_clamps = _get_children_by_prefix(panel2, "WallClamp")
    assert len(wall_clamps) == 0, f"Expected 0 WallClamps when Channel, got {len(wall_clamps)}"
    print(f"  OK: No wall clamps when using channels")

except Exception as e:
    print(f"  FAIL: {e}")
    import traceback
    traceback.print_exc()


# Test 5: Floor channel
print("\n" + "=" * 70)
print("5. Testing floor channel children...")
print("=" * 70)

try:
    panel3 = createFixedPanel("FloorChannelPanel")
    vs3 = _get_varset(panel3)
    vs3.WallHardware = "None"
    vs3.FloorHardware = "Channel"
    doc.recompute()

    floor_channels = _get_children_by_prefix(panel3, "FloorChannel")
    assert len(floor_channels) == 1, f"Expected 1 FloorChannel, got {len(floor_channels)}"
    print(f"  OK: Floor channel created")

    assert not floor_channels[0].Shape.isNull()
    print(f"  OK: Floor channel has valid shape")

except Exception as e:
    print(f"  FAIL: {e}")
    import traceback
    traceback.print_exc()


# Test 6: ShowHardware toggle
print("\n" + "=" * 70)
print("6. Testing ShowHardware toggle...")
print("=" * 70)

try:
    panel4 = createFixedPanel("TogglePanel")
    vs4 = _get_varset(panel4)
    vs4.WallHardware = "Clamp"
    vs4.WallClampCount = 2
    vs4.WallMountEdge = "Left"
    vs4.FloorHardware = "Clamp"
    vs4.FloorClampCount = 2
    vs4.ShowHardware = True
    doc.recompute()

    hw_count_on = len([c for c in panel4.Group
                       if c.TypeId != "App::VarSet" and c.Label != "Glass"])
    assert hw_count_on > 0, "Expected hardware children when ShowHardware=True"
    print(f"  OK: {hw_count_on} hardware children when ShowHardware=True")

    vs4.ShowHardware = False
    doc.recompute()

    hw_count_off = len([c for c in panel4.Group
                        if c.TypeId != "App::VarSet" and c.Label != "Glass"])
    assert hw_count_off == 0, f"Expected 0 hardware children when ShowHardware=False, got {hw_count_off}"
    print(f"  OK: 0 hardware children when ShowHardware=False")

    vs4.ShowHardware = True
    doc.recompute()
    hw_count_back = len([c for c in panel4.Group
                         if c.TypeId != "App::VarSet" and c.Label != "Glass"])
    assert hw_count_back > 0, "Expected hardware children when ShowHardware toggled back on"
    print(f"  OK: Hardware restored when toggled back on")

except Exception as e:
    print(f"  FAIL: {e}")
    import traceback
    traceback.print_exc()


# Test 7: Changing dimensions updates Glass child
print("\n" + "=" * 70)
print("7. Testing dimension changes propagate to Glass...")
print("=" * 70)

try:
    panel5 = createFixedPanel("DimensionPanel")
    vs5 = _get_varset(panel5)
    glass = _get_children_by_prefix(panel5, "Glass")[0]

    vs5.Width = 1200
    vs5.Height = 2400
    vs5.Thickness = 12
    doc.recompute()

    assert glass.Width.Value == 1200, f"Expected Glass Width=1200, got {glass.Width.Value}"
    assert glass.Height.Value == 2400, f"Expected Glass Height=2400, got {glass.Height.Value}"
    assert glass.Thickness.Value == 12, f"Expected Glass Thickness=12, got {glass.Thickness.Value}"
    print(f"  OK: Glass child dimensions updated")

    # Check calculated properties
    expected_area = (1200 / 1000) * (2400 / 1000)
    assert abs(vs5.Area - expected_area) < 0.01, f"Expected Area~{expected_area}, got {vs5.Area}"
    print(f"  OK: Calculated Area = {vs5.Area:.3f} m2")
    assert vs5.Weight > 0, f"Expected positive Weight, got {vs5.Weight}"
    print(f"  OK: Calculated Weight = {vs5.Weight:.2f} kg")

except Exception as e:
    print(f"  FAIL: {e}")
    import traceback
    traceback.print_exc()


# Test 8: Combination - wall channel + floor clamps
print("\n" + "=" * 70)
print("8. Testing combination: wall channel + floor clamps...")
print("=" * 70)

try:
    panel6 = createFixedPanel("ComboPanel")
    vs6 = _get_varset(panel6)
    vs6.WallHardware = "Channel"
    vs6.WallMountEdge = "Left"
    vs6.FloorHardware = "Clamp"
    vs6.FloorClampCount = 3
    doc.recompute()

    wall_channels = _get_children_by_prefix(panel6, "WallChannel")
    floor_clamps = _get_children_by_prefix(panel6, "FloorClamp")
    assert len(wall_channels) == 1, f"Expected 1 WallChannel, got {len(wall_channels)}"
    assert len(floor_clamps) == 3, f"Expected 3 FloorClamps, got {len(floor_clamps)}"
    print(f"  OK: 1 wall channel + 3 floor clamps created")

except Exception as e:
    print(f"  FAIL: {e}")
    import traceback
    traceback.print_exc()


# Summary
print("\n" + "=" * 70)
print("Summary")
print("=" * 70)

total_objects = len(doc.Objects)
assemblies = [o for o in doc.Objects if o.TypeId == "App::Part"]
varsets = [o for o in doc.Objects if o.TypeId == "App::VarSet"]
children = [o for o in doc.Objects if o.TypeId == "Part::FeaturePython"]

print(f"\nTotal objects: {total_objects}")
print(f"  App::Part assemblies: {len(assemblies)}")
print(f"  App::VarSet objects: {len(varsets)}")
print(f"  Part::FeaturePython children: {len(children)}")

print("\nAssembly Features Tested:")
print("  - App::Part container creation")
print("  - VarSet property management")
print("  - Glass child with own ViewProvider")
print("  - Wall clamp children (variable count, Left/Right/Both)")
print("  - Wall channel children")
print("  - Floor clamp children")
print("  - Floor channel children")
print("  - ShowHardware toggle (add/remove children)")
print("  - Dimension propagation to Glass child")
print("  - Calculated properties (Weight, Area)")
print("  - Combination hardware configurations")

print("\n" + "=" * 70)
print("Testing Complete!")
print("=" * 70)

# Fit all objects in view if GUI is up
if App.GuiUp:
    try:
        import FreeCADGui as Gui
        Gui.SendMsgToActiveView("ViewFit")
        print("\nView fitted to show all panels")
    except Exception:
        pass
