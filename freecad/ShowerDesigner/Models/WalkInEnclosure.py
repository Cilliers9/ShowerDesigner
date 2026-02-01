# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Walk-in shower enclosure model
"""

import FreeCAD as App
import Part


class WalkInEnclosure:
    """
    Parametric walk-in shower enclosure object
    """
    
    def __init__(self, obj):
        """
        Initialize the walk-in enclosure object
        
        Args:
            obj: FreeCAD document object
        """
        obj.Proxy = self
        
        # Add properties
        obj.addProperty("App::PropertyLength", "Width", "Dimensions",
                       "Width of the glass panel").Width = 1000
        obj.addProperty("App::PropertyLength", "Height", "Dimensions",
                       "Height of the enclosure").Height = 2000
        obj.addProperty("App::PropertyLength", "GlassThickness", "Glass",
                       "Thickness of glass panel").GlassThickness = 10
        obj.addProperty("App::PropertyBool", "SupportBar", "Hardware",
                       "Add support bar").SupportBar = True
        obj.addProperty("App::PropertyLength", "SupportBarHeight", "Hardware",
                       "Height of support bar from top").SupportBarHeight = 100
    
    def execute(self, obj):
        """
        Rebuild the geometry when properties change
        """
        width = obj.Width.Value
        height = obj.Height.Value
        thickness = obj.GlassThickness.Value
        
        # Create main glass panel
        panel = Part.makeBox(width, thickness, height)
        
        shape = panel
        
        # Add support bar if enabled
        if obj.SupportBar:
            bar_height = obj.SupportBarHeight.Value
            bar_radius = 15
            bar = Part.makeCylinder(bar_radius, width)
            bar.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)
            bar.translate(App.Vector(0, thickness/2, height - bar_height))
            shape = shape.fuse(bar)
        
        obj.Shape = shape
    
    def onChanged(self, obj, prop):
        """Called when a property changes"""
        pass


def createWalkInEnclosure():
    """
    Create a new walk-in shower enclosure in the active document
    
    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")
    
    obj = doc.addObject("Part::FeaturePython", "WalkInEnclosure")
    WalkInEnclosure(obj)
    
    if App.GuiUp:
        obj.ViewObject.Proxy = 0
    
    doc.recompute()
    
    App.Console.PrintMessage("Walk-in enclosure created\n")
    return obj
