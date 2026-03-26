# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Command definitions for ShowerDesigner workbench
"""

import FreeCADGui as Gui
from freecad.ShowerDesigner.Misc.Resources import asIcon


class CornerEnclosureCommand:
    """Create a corner shower enclosure"""
    
    def GetResources(self):
        return {
            'Pixmap': asIcon('CornerEnclosure'),
            'MenuText': 'Corner Enclosure',
            'ToolTip': 'Create a corner shower enclosure'
        }
    
    def Activated(self):
        from freecad.ShowerDesigner.Models.CornerEnclosure import createCornerEnclosure
        createCornerEnclosure()
    
    def IsActive(self):
        return True


class AlcoveEnclosureCommand:
    """Create an alcove shower enclosure"""
    
    def GetResources(self):
        return {
            'Pixmap': asIcon('AlcoveEnclosure'),
            'MenuText': 'Alcove Enclosure',
            'ToolTip': 'Create an alcove shower enclosure'
        }
    
    def Activated(self):
        from freecad.ShowerDesigner.Models.AlcoveEnclosure import createAlcoveEnclosure
        createAlcoveEnclosure()
    
    def IsActive(self):
        return True


class WalkInEnclosureCommand:
    """Create a walk-in shower enclosure"""
    
    def GetResources(self):
        return {
            'Pixmap': asIcon('WalkInEnclosure'),
            'MenuText': 'Walk-In Enclosure',
            'ToolTip': 'Create a walk-in shower enclosure'
        }
    
    def Activated(self):
        from freecad.ShowerDesigner.Models.WalkInEnclosure import createWalkInEnclosure
        createWalkInEnclosure()
    
    def IsActive(self):
        return True


class CustomEnclosureCommand:
    """Create a custom shower enclosure"""
    
    def GetResources(self):
        return {
            'Pixmap': asIcon('CustomEnclosure'),
            'MenuText': 'Custom Enclosure',
            'ToolTip': 'Create a custom shower enclosure'
        }
    
    def Activated(self):
        from freecad.ShowerDesigner.Models.CustomEnclosure import createCustomEnclosure
        createCustomEnclosure()
    
    def IsActive(self):
        return True


# Register all commands
Gui.addCommand('ShowerDesigner_CornerEnclosure', CornerEnclosureCommand())
Gui.addCommand('ShowerDesigner_AlcoveEnclosure', AlcoveEnclosureCommand())
Gui.addCommand('ShowerDesigner_WalkInEnclosure', WalkInEnclosureCommand())
Gui.addCommand('ShowerDesigner_CustomEnclosure', CustomEnclosureCommand())

# Placeholder commands for components and tools
class PlaceholderCommand:
    """Placeholder for future commands"""
    
    def __init__(self, name, tooltip):
        self.name = name
        self.tooltip = tooltip
    
    def GetResources(self):
        return {
            'Pixmap': asIcon('Logo'),
            'MenuText': self.name,
            'ToolTip': self.tooltip
        }
    
    def Activated(self):
        import FreeCAD as App
        App.Console.PrintMessage(f"{self.name} - Coming soon!\n")
    
    def IsActive(self):
        return True


# Component Commands

class GlassPanelCommand:
    """Create a basic glass panel"""
    
    def GetResources(self):
        return {
            'Pixmap': asIcon('Logo'),
            'MenuText': 'Glass Panel',
            'ToolTip': 'Create a basic glass panel'
        }
    
    def Activated(self):
        from freecad.ShowerDesigner.Models.GlassPanel import createGlassPanel
        createGlassPanel()
    
    def IsActive(self):
        return True


class FixedPanelCommand:
    """Create a fixed panel with mounting hardware"""

    def GetResources(self):
        return {
            'Pixmap': asIcon('FixedPanel'),
            'MenuText': 'Fixed Panel',
            'ToolTip': 'Create a fixed panel with wall/floor mounting hardware'
        }

    def Activated(self):
        from freecad.ShowerDesigner.Models.FixedPanel import createFixedPanel
        createFixedPanel()

    def IsActive(self):
        return True


class HingedDoorCommand:
    """Create a hinged shower door"""

    def GetResources(self):
        return {
            'Pixmap': asIcon('HingedDoor'),
            'MenuText': 'Hinged Door',
            'ToolTip': 'Create a hinged shower door with hardware'
        }

    def Activated(self):
        from freecad.ShowerDesigner.Models.HingedDoor import createHingedDoor
        createHingedDoor()

    def IsActive(self):
        return True


class SlidingDoorCommand:
    """Create a sliding shower door"""

    def GetResources(self):
        return {
            'Pixmap': asIcon('SlidingDoor'),
            'MenuText': 'Sliding Door',
            'ToolTip': 'Create a sliding shower door with track hardware'
        }

    def Activated(self):
        from freecad.ShowerDesigner.Models.SlidingDoor import createSlidingDoor
        createSlidingDoor()

    def IsActive(self):
        return True


class BiFoldDoorCommand:
    """Create a bi-fold shower door"""

    def GetResources(self):
        return {
            'Pixmap': asIcon('BiFoldDoor'),
            'MenuText': 'Bi-Fold Door',
            'ToolTip': 'Create a bi-fold shower door with pivot hardware'
        }

    def Activated(self):
        from freecad.ShowerDesigner.Models.BiFoldDoor import createBiFoldDoor
        createBiFoldDoor()

    def IsActive(self):
        return True


class HingeCommand:
    """Create a standalone hinge fitting"""

    def GetResources(self):
        return {
            'Pixmap': asIcon('Logo'),
            'MenuText': 'Hinge',
            'ToolTip': 'Create a standalone hinge fitting'
        }

    def Activated(self):
        from freecad.ShowerDesigner.Models.Hinge import createHinge
        createHinge()

    def IsActive(self):
        return True


class ClampCommand:
    """Create a standalone clamp fitting"""

    def GetResources(self):
        return {
            'Pixmap': asIcon('Logo'),
            'MenuText': 'Clamp',
            'ToolTip': 'Create a standalone clamp fitting'
        }

    def Activated(self):
        from freecad.ShowerDesigner.Models.Clamp import createClamp
        createClamp()

    def IsActive(self):
        return True


class SupportBarCommand:
    """Create a standalone support bar"""

    def GetResources(self):
        return {
            'Pixmap': asIcon('Logo'),
            'MenuText': 'Support Bar',
            'ToolTip': 'Create a support bar (stabilizer)'
        }

    def Activated(self):
        from freecad.ShowerDesigner.Models.SupportBar import createSupportBar
        createSupportBar()

    def IsActive(self):
        return True


class CutListCommand:
    """Generate a cut list / bill of materials from selected assemblies"""

    def GetResources(self):
        return {
            'Pixmap': asIcon('Logo'),
            'MenuText': 'Cut List',
            'ToolTip': 'Generate cut list / bill of materials',
        }

    def Activated(self):
        import FreeCAD as App

        from freecad.ShowerDesigner.Data.CutList import (
            aggregateItems,
            toConsoleTable,
        )
        from freecad.ShowerDesigner.Gui.CutListDialog import CutListDialog
        from freecad.ShowerDesigner.Models.CutListExtractor import CutListExtractor

        doc = App.ActiveDocument
        if doc is None:
            App.Console.PrintError("Cut List: No active document.\n")
            return

        # Collect from selection, or fall back to all top-level App::Part objects
        sel = Gui.Selection.getSelection()
        targets = []
        if sel:
            targets = list(sel)
        else:
            for obj in doc.Objects:
                if obj.TypeId == "App::Part" and getattr(obj, "InList", None) == []:
                    targets.append(obj)

        if not targets:
            App.Console.PrintMessage("Cut List: No assemblies found in document.\n")
            return

        extractor = CutListExtractor()
        all_items = []
        for obj in targets:
            all_items.extend(extractor.extract(obj))

        if not all_items:
            App.Console.PrintMessage("Cut List: No BOM items found.\n")
            return

        aggregated = aggregateItems(all_items)

        # Also print to console for quick reference
        App.Console.PrintMessage("\n=== Cut List / Bill of Materials ===\n")
        App.Console.PrintMessage(toConsoleTable(aggregated))
        App.Console.PrintMessage(
            f"Total items: {sum(i.quantity for i in aggregated)}\n\n"
        )

        # Show dialog
        dlg = CutListDialog(aggregated, Gui.getMainWindow())
        dlg.exec_()

    def IsActive(self):
        import FreeCAD as App
        return App.ActiveDocument is not None


class GlassShelfCommand:
    """Create a standalone glass shelf"""

    def GetResources(self):
        return {
            'Pixmap': asIcon('Logo'),
            'MenuText': 'Glass Shelf',
            'ToolTip': 'Create a corner glass shelf'
        }

    def Activated(self):
        from freecad.ShowerDesigner.Models.GlassShelf import createGlassShelf
        createGlassShelf()

    def IsActive(self):
        return True


class MeasureCommand:
    """Toggle 3D dimension annotations on enclosures."""

    _DIM_GROUP_LABEL = "Dimensions"

    def GetResources(self):
        return {
            'Pixmap': asIcon('Logo'),
            'MenuText': 'Measure',
            'ToolTip': 'Toggle 3D dimension annotations on enclosures',
        }

    def Activated(self):
        import FreeCAD as App

        doc = App.ActiveDocument
        if doc is None:
            App.Console.PrintError("Measure: No active document.\n")
            return

        # Collect targets: selection or all top-level App::Part objects
        sel = Gui.Selection.getSelection()
        targets = []
        if sel:
            targets = list(sel)
        else:
            for obj in doc.Objects:
                if obj.TypeId == "App::Part" and getattr(obj, "InList", None) == []:
                    targets.append(obj)

        if not targets:
            App.Console.PrintMessage("Measure: No assemblies found in document.\n")
            return

        # Toggle logic: exists+visible → hide; exists+hidden → delete+regenerate; absent → create
        existing_groups = []
        for part_obj in targets:
            grp = self._findDimGroup(part_obj)
            if grp is not None:
                existing_groups.append((part_obj, grp))

        if existing_groups:
            # Check if any are visible
            any_visible = False
            for _part_obj, grp in existing_groups:
                if App.GuiUp and grp.ViewObject.Visibility:
                    any_visible = True
                    break

            if any_visible:
                # Hide all
                for _part_obj, grp in existing_groups:
                    if App.GuiUp:
                        grp.ViewObject.Visibility = False
                App.Console.PrintMessage("Measure: Dimensions hidden.\n")
                return
            else:
                # Delete and regenerate
                for part_obj, grp in existing_groups:
                    self._removeDimGroup(doc, part_obj, grp)

        # Create fresh dimensions
        self._createDimensions(doc, targets)

    def _findDimGroup(self, part_obj):
        """Find an existing Dimensions group inside an App::Part."""
        for child in getattr(part_obj, "Group", []):
            if (
                child.TypeId == "App::DocumentObjectGroup"
                and child.Label == self._DIM_GROUP_LABEL
            ):
                return child
        return None

    def _removeDimGroup(self, doc, part_obj, grp):
        """Remove a Dimensions group and all its children."""
        for child in list(grp.Group):
            grp.removeObject(child)
            doc.removeObject(child.Name)
        part_obj.removeObject(grp)
        doc.removeObject(grp.Name)

    def _createDimensions(self, doc, targets):
        """Run DimensionExtractor and create Draft dimension objects."""
        import FreeCAD as App

        try:
            import Draft
        except ImportError:
            App.Console.PrintError(
                "Measure: Draft workbench not available.\n"
            )
            return

        from freecad.ShowerDesigner.Data.DimensionSpecs import DIM_COLORS
        from freecad.ShowerDesigner.Models.DimensionExtractor import DimensionExtractor

        extractor = DimensionExtractor()
        total = 0

        for part_obj in targets:
            items = extractor.extract(part_obj)
            if not items:
                continue

            # Create group inside the App::Part
            grp = doc.addObject("App::DocumentObjectGroup", self._DIM_GROUP_LABEL)
            grp.Label = self._DIM_GROUP_LABEL
            part_obj.addObject(grp)

            for item in items:
                p1 = App.Vector(*item.p1)
                p2 = App.Vector(*item.p2)
                off_dir = App.Vector(*item.offset_direction)
                midpoint = (p1 + p2) * 0.5
                dim_line_pt = midpoint + off_dir * item.offset_distance

                dim = Draft.make_linear_dimension(p1, p2, dim_line_pt)
                dim.Label = item.label
                grp.addObject(dim)

                # Style by category
                if App.GuiUp and hasattr(dim, "ViewObject"):
                    vobj = dim.ViewObject
                    color = DIM_COLORS.get(item.category, (0.0, 0.0, 0.0))
                    if hasattr(vobj, "LineColor"):
                        vobj.LineColor = color
                    if hasattr(vobj, "TextColor"):
                        vobj.TextColor = color
                    if hasattr(vobj, "FontSize"):
                        vobj.FontSize = 60
                    if hasattr(vobj, "ArrowSize"):
                        vobj.ArrowSize = 15

                total += 1

        doc.recompute()
        App.Console.PrintMessage(
            f"Measure: Created {total} dimension annotations.\n"
        )

    def IsActive(self):
        import FreeCAD as App
        return App.ActiveDocument is not None


class ExportCommand:
    """Export enclosure parts as STEP, STL, 3MF, IGES, or OBJ"""

    def GetResources(self):
        return {
            'Pixmap': asIcon('Logo'),
            'MenuText': 'Export',
            'ToolTip': 'Export parts to STEP / STL / 3MF / IGES / OBJ',
        }

    def Activated(self):
        import FreeCAD as App

        from freecad.ShowerDesigner.Gui.ExportDialog import ExportDialog

        doc = App.ActiveDocument
        if doc is None:
            App.Console.PrintError("Export: No active document.\n")
            return

        # Collect from selection, or fall back to all top-level App::Part objects
        sel = Gui.Selection.getSelection()
        targets = []
        if sel:
            targets = list(sel)
        else:
            for obj in doc.Objects:
                if obj.TypeId == "App::Part" and getattr(obj, "InList", None) == []:
                    targets.append(obj)

        if not targets:
            App.Console.PrintMessage("Export: No assemblies found in document.\n")
            return

        dlg = ExportDialog(targets, Gui.getMainWindow())
        dlg.exec_()

    def IsActive(self):
        import FreeCAD as App
        return App.ActiveDocument is not None


class GlassOrderCommand:
    """Generate TechDraw glass order drawings from selected assemblies"""

    def GetResources(self):
        return {
            'Pixmap': asIcon('Logo'),
            'MenuText': 'Glass Order Drawings',
            'ToolTip': 'Generate per-panel TechDraw drawings for glass ordering',
        }

    def Activated(self):
        import FreeCAD as App

        from freecad.ShowerDesigner.Models.GlassOrderDrawing import (
            GlassOrderDrawingGenerator,
        )

        doc = App.ActiveDocument
        if doc is None:
            App.Console.PrintError("Glass Order Drawings: No active document.\n")
            return

        # Collect from selection, or fall back to all top-level App::Part objects
        sel = Gui.Selection.getSelection()
        targets = []
        if sel:
            targets = list(sel)
        else:
            for obj in doc.Objects:
                if obj.TypeId == "App::Part" and getattr(obj, "InList", None) == []:
                    targets.append(obj)

        if not targets:
            App.Console.PrintMessage(
                "Glass Order Drawings: No assemblies found in document.\n"
            )
            return

        generator = GlassOrderDrawingGenerator()
        total_pages = 0
        for obj in targets:
            pages = generator.generate(obj)
            total_pages += len(pages)

        if total_pages > 0:
            doc.recompute()
            App.Console.PrintMessage(
                f"Glass Order Drawings: Created {total_pages} drawing page(s).\n"
            )
        else:
            App.Console.PrintMessage(
                "Glass Order Drawings: No glass panels found.\n"
            )

    def IsActive(self):
        import FreeCAD as App
        return App.ActiveDocument is not None


# Register component commands
Gui.addCommand('ShowerDesigner_GlassPanel', GlassPanelCommand())
Gui.addCommand('ShowerDesigner_FixedPanel', FixedPanelCommand())
Gui.addCommand('ShowerDesigner_HingedDoor', HingedDoorCommand())
Gui.addCommand('ShowerDesigner_SlidingDoor', SlidingDoorCommand())
Gui.addCommand('ShowerDesigner_BiFoldDoor', BiFoldDoorCommand())
Gui.addCommand('ShowerDesigner_Hinge', HingeCommand())
Gui.addCommand('ShowerDesigner_Clamp', ClampCommand())
Gui.addCommand('ShowerDesigner_SupportBar', SupportBarCommand())
Gui.addCommand('ShowerDesigner_GlassShelf', GlassShelfCommand())
Gui.addCommand('ShowerDesigner_Measure', MeasureCommand())
Gui.addCommand('ShowerDesigner_CutList', CutListCommand())
Gui.addCommand('ShowerDesigner_Export', ExportCommand())
Gui.addCommand('ShowerDesigner_GlassOrder', GlassOrderCommand())
