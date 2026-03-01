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
            toCSV,
        )
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

        # Print to console
        App.Console.PrintMessage("\n=== Cut List / Bill of Materials ===\n")
        App.Console.PrintMessage(toConsoleTable(aggregated))
        App.Console.PrintMessage(
            f"Total items: {sum(i.quantity for i in aggregated)}\n\n"
        )

        # Copy CSV to clipboard
        csv_text = toCSV(aggregated)
        try:
            from PySide import QtWidgets  # type: ignore[import-untyped]
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(csv_text)
            App.Console.PrintMessage("CSV copied to clipboard.\n")
        except Exception:
            App.Console.PrintMessage(
                "Could not copy to clipboard. CSV output:\n" + csv_text
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
Gui.addCommand('ShowerDesigner_Measure',
               PlaceholderCommand('Measure', 'Measurement tools'))
Gui.addCommand('ShowerDesigner_CutList', CutListCommand())
Gui.addCommand('ShowerDesigner_Export',
               PlaceholderCommand('Export', 'Export design'))
