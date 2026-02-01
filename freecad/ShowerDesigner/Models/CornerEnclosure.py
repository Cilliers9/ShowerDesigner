# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Corner shower enclosure model
"""

import FreeCAD as App
import Part


class CornerEnclosure:
    """
    Parametric corner shower enclosure object
    """
    
    def __init__(self, obj):
        """
        Initialize the corner enclosure object
        
        Args:
            obj: FreeCAD document object
        """
        obj.Proxy = self
        
        # Add properties
        obj.addProperty("App::PropertyLength", "Width", "Dimensions",
                       "Width of the enclosure").Width = 900
        obj.addProperty("App::PropertyLength", "Depth", "Dimensions",
                       "Depth of the enclosure").Depth = 900
        obj.addProperty("App::PropertyLength", "Height", "Dimensions",
                       "Height of the enclosure").Height = 2000
        obj.addProperty("App::PropertyLength", "GlassThickness", "Glass",
                       "Thickness of glass panels").GlassThickness = 8
        obj.addProperty("App::PropertyEnumeration", "GlassType", "Glass",
                       "Type of glass")
        obj.GlassType = ["Clear", "Frosted", "Tinted", "Pattern"]
        obj.GlassType = "Clear"
        obj.addProperty("App::PropertyBool", "ShowFrame", "Display",
                       "Show frame profile").ShowFrame = True
        obj.addProperty("App::PropertyLength", "FrameWidth", "Frame",
                       "Width of frame profile").FrameWidth = 25
    
    def execute(self, obj):
        """
        Rebuild the geometry when properties change
        
        Args:
            obj: FreeCAD document object
        """
        # Create the enclosure geometry
        width = obj.Width.Value
        depth = obj.Depth.Value
        height = obj.Height.Value
        thickness = obj.GlassThickness.Value
        
        # Create back panel (along X axis)
        back_panel = Part.makeBox(width, thickness, height)
        
        # Create side panel (along Y axis)
        side_panel = Part.makeBox(thickness, depth, height)
        
        # Position panels at corner
        back_panel.translate(App.Vector(0, depth - thickness, 0))
        
        # Combine panels
        shape = back_panel.fuse(side_panel)
        
        # Add frame if enabled
        if obj.ShowFrame:
            frame_width = obj.FrameWidth.Value
            
            # Vertical frame posts
            post1 = Part.makeCylinder(frame_width/2, height)
            post2 = Part.makeCylinder(frame_width/2, height)
            post3 = Part.makeCylinder(frame_width/2, height)
            
            post1.translate(App.Vector(0, depth, 0))
            post2.translate(App.Vector(width, depth, 0))
            post3.translate(App.Vector(width, 0, 0))
            
            shape = shape.fuse([post1, post2, post3])
        
        obj.Shape = shape
    
    def onChanged(self, obj, prop):
        """
        Called when a property changes
        """
        pass


def createCornerEnclosure():
    """
    Create a new corner shower enclosure in the active document
    
    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")
    
    obj = doc.addObject("Part::FeaturePython", "CornerEnclosure")
    CornerEnclosure(obj)
    
    if App.GuiUp:
        obj.ViewObject.Proxy = 0  # Simple view provider
    
    doc.recompute()
    
    App.Console.PrintMessage("Corner enclosure created\n")
    return obj
