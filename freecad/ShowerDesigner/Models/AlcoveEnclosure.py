# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Alcove shower enclosure model
"""

import FreeCAD as App
import Part


class AlcoveEnclosure:
    """
    Parametric alcove shower enclosure object
    """
    
    def __init__(self, obj):
        """
        Initialize the alcove enclosure object
        
        Args:
            obj: FreeCAD document object
        """
        obj.Proxy = self
        
        # Add properties
        obj.addProperty("App::PropertyLength", "Width", "Dimensions",
                       "Width of the alcove opening").Width = 1200
        obj.addProperty("App::PropertyLength", "Depth", "Dimensions",
                       "Depth of the alcove").Depth = 900
        obj.addProperty("App::PropertyLength", "Height", "Dimensions",
                       "Height of the enclosure").Height = 2000
        obj.addProperty("App::PropertyLength", "GlassThickness", "Glass",
                       "Thickness of glass door").GlassThickness = 8
        obj.addProperty("App::PropertyEnumeration", "DoorType", "Door",
                       "Type of door")
        obj.DoorType = ["Sliding", "Pivot", "Bi-fold"]
        obj.DoorType = "Sliding"
    
    def execute(self, obj):
        """
        Rebuild the geometry when properties change
        """
        # Create a simple door panel for now
        width = obj.Width.Value
        height = obj.Height.Value
        thickness = obj.GlassThickness.Value
        
        # Create door panel
        door = Part.makeBox(width, thickness, height)
        
        obj.Shape = door
    
    def onChanged(self, obj, prop):
        """Called when a property changes"""
        pass


def createAlcoveEnclosure():
    """
    Create a new alcove shower enclosure in the active document
    
    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")
    
    obj = doc.addObject("Part::FeaturePython", "AlcoveEnclosure")
    AlcoveEnclosure(obj)
    
    if App.GuiUp:
        obj.ViewObject.Proxy = 0
    
    doc.recompute()
    
    App.Console.PrintMessage("Alcove enclosure created\n")
    return obj
