# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Custom shower enclosure model
"""

import FreeCAD as App
import Part


class CustomEnclosure:
    """
    Parametric custom shower enclosure object
    """
    
    def __init__(self, obj):
        """
        Initialize the custom enclosure object
        
        Args:
            obj: FreeCAD document object
        """
        obj.Proxy = self
        
        # Add properties
        obj.addProperty("App::PropertyLength", "Width", "Dimensions",
                       "Width of the enclosure").Width = 1000
        obj.addProperty("App::PropertyLength", "Depth", "Dimensions",
                       "Depth of the enclosure").Depth = 1000
        obj.addProperty("App::PropertyLength", "Height", "Dimensions",
                       "Height of the enclosure").Height = 2000
        obj.addProperty("App::PropertyInteger", "PanelCount", "Configuration",
                       "Number of glass panels").PanelCount = 3
        obj.addProperty("App::PropertyLength", "GlassThickness", "Glass",
                       "Thickness of glass panels").GlassThickness = 8
    
    def execute(self, obj):
        """
        Rebuild the geometry when properties change
        """
        # Placeholder - create a simple box for now
        width = obj.Width.Value
        depth = obj.Depth.Value
        height = obj.Height.Value
        thickness = obj.GlassThickness.Value
        
        # Create a simple rectangular enclosure
        panel1 = Part.makeBox(width, thickness, height)
        panel2 = Part.makeBox(thickness, depth, height)
        
        panel1.translate(App.Vector(0, depth - thickness, 0))
        
        shape = panel1.fuse(panel2)
        
        obj.Shape = shape
    
    def onChanged(self, obj, prop):
        """Called when a property changes"""
        pass


def createCustomEnclosure():
    """
    Create a new custom shower enclosure in the active document
    
    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")
    
    obj = doc.addObject("Part::FeaturePython", "CustomEnclosure")
    CustomEnclosure(obj)
    
    if App.GuiUp:
        obj.ViewObject.Proxy = 0
    
    doc.recompute()
    
    App.Console.PrintMessage("Custom enclosure created\n")
    return obj
