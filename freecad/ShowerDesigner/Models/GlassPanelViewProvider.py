# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
ViewProvider for glass panels - handles visual appearance in FreeCAD 3D view
"""

import FreeCAD as App


class GlassPanelViewProvider:
    """
    ViewProvider for GlassPanel objects.
    
    Handles the visual representation of glass panels including transparency,
    color tinting, and display properties based on glass type.
    """
    
    def __init__(self, vobj):
        """
        Initialize the view provider.
        
        Args:
            vobj: ViewObject for the glass panel
        """
        vobj.Proxy = self
        self.Object = vobj.Object
    
    def attach(self, vobj):
        """
        Setup the scene sub-graph of the view provider.
        
        Args:
            vobj: ViewObject
        """
        self.Object = vobj.Object
    
    def updateData(self, obj, prop):
        """
        Called when a property of the FeaturePython object changes.
        
        Args:
            obj: The FeaturePython object
            prop: Name of the property that changed
        """
        # Update visual properties when glass type changes
        if prop == "GlassType":
            self.updateVisualProperties(obj)
    
    def onChanged(self, vobj, prop):
        """
        Called when a ViewObject property changes.
        
        Args:
            vobj: ViewObject
            prop: Name of the property that changed
        """
        pass
    
    def updateVisualProperties(self, obj):
        """
        Update the visual appearance based on glass type.
        
        Args:
            obj: The FeaturePython object
        """
        if not App.GuiUp:
            return
        
        if not hasattr(obj, "ViewObject") or not hasattr(obj, "GlassType"):
            return
        
        from freecad.ShowerDesigner.Data.GlassSpecs import (
            getGlassColor,
            getGlassOpacity
        )
        
        vobj = obj.ViewObject
        glass_type = obj.GlassType
        
        # Get glass properties
        color = getGlassColor(glass_type)
        opacity = getGlassOpacity(glass_type)
        
        if color is not None:
            # Set shape color (RGB values 0-1)
            vobj.ShapeColor = color
        
        if opacity is not None:
            # Convert opacity (0=transparent, 1=opaque) to transparency (0=opaque, 100=transparent)
            # For glass, we want high transparency with some opacity for visibility
            if glass_type == "Clear":
                transparency = 85  # Very transparent
            elif glass_type == "Low-Iron":
                transparency = 90  # Ultra transparent
            elif glass_type == "Frosted":
                transparency = 50  # Semi-transparent, more visible
            elif glass_type in ["Bronze", "Grey"]:
                transparency = 60  # Tinted, moderately transparent
            elif glass_type == "Reeded":
                transparency = 55  # Textured appearance
            else:
                transparency = 70  # Default
            
            vobj.Transparency = transparency
        
        # Set display mode to show as a shaded object
        if hasattr(vobj, "DisplayMode"):
            vobj.DisplayMode = "Flat Lines"
        
        # Set line width for edges
        if hasattr(vobj, "LineWidth"):
            vobj.LineWidth = 2.0
        
        # Set line color to a subtle edge color
        if hasattr(vobj, "LineColor"):
            vobj.LineColor = (0.3, 0.3, 0.3, 1.0)  # Dark gray edges
    
    def getDisplayModes(self, vobj):
        """
        Return a list of display modes.
        
        Args:
            vobj: ViewObject
            
        Returns:
            list: Available display modes
        """
        return ["Flat Lines", "Shaded", "Wireframe"]
    
    def getDefaultDisplayMode(self):
        """
        Return the default display mode.
        
        Returns:
            str: Default display mode name
        """
        return "Flat Lines"
    
    def setDisplayMode(self, mode):
        """
        Set the display mode.
        
        Args:
            mode: Display mode name
            
        Returns:
            str: The mode that was set
        """
        return mode
    
    def getIcon(self):
        """
        Return the icon path for this object.
        
        Returns:
            str: Path to icon file
        """
        from freecad.ShowerDesigner.Misc.Resources import asIcon
        return asIcon('Logo')  # TODO: Create specific GlassPanel icon
    
    def __getstate__(self):
        """Return state for serialization"""
        return None
    
    def __setstate__(self, state):
        """Restore state from serialization"""
        return None


def setupViewProvider(obj):
    """
    Setup the view provider for a glass panel object.
    
    Args:
        obj: FreeCAD document object (FeaturePython)
    """
    if not App.GuiUp:
        return
    
    # Create and attach the view provider
    GlassPanelViewProvider(obj.ViewObject)
    
    # Trigger initial visual update
    if hasattr(obj.ViewObject, "Proxy") and obj.ViewObject.Proxy:
        obj.ViewObject.Proxy.updateVisualProperties(obj)
