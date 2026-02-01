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


# Register placeholder commands
Gui.addCommand('ShowerDesigner_GlassPanel', 
               PlaceholderCommand('Glass Panel', 'Add a glass panel'))
Gui.addCommand('ShowerDesigner_Door', 
               PlaceholderCommand('Door', 'Add a shower door'))
Gui.addCommand('ShowerDesigner_Hardware', 
               PlaceholderCommand('Hardware', 'Add hardware fittings'))
Gui.addCommand('ShowerDesigner_Measure', 
               PlaceholderCommand('Measure', 'Measurement tools'))
Gui.addCommand('ShowerDesigner_CutList', 
               PlaceholderCommand('Cut List', 'Generate cut list'))
Gui.addCommand('ShowerDesigner_Export', 
               PlaceholderCommand('Export', 'Export design'))
