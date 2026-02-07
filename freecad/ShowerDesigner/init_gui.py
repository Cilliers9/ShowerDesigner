# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner addon.

import FreeCADGui as Gui
from freecad.ShowerDesigner.Misc.Resources import asIcon


class ShowerDesignerWorkbench(Gui.Workbench):
    """ShowerDesigner workbench for FreeCAD"""

    MenuText = "ShowerDesigner"
    ToolTip = "Parametric shower enclosure design"
    Icon = asIcon('Logo')

    def Initialize(self):
        """Initialize workbench - set up toolbars and menus"""

        # Import commands to register them
        import freecad.ShowerDesigner.Commands

        # Define command lists
        enclosure_commands = [
            'ShowerDesigner_CornerEnclosure',
            'ShowerDesigner_AlcoveEnclosure',
            'ShowerDesigner_WalkInEnclosure',
            'ShowerDesigner_CustomEnclosure'
        ]

        component_commands = [
            'ShowerDesigner_GlassPanel',
            'ShowerDesigner_FixedPanel',
            'ShowerDesigner_HingedDoor',
            'ShowerDesigner_SlidingDoor',
            'ShowerDesigner_BiFoldDoor',
            'ShowerDesigner_Hinge',
            'ShowerDesigner_Clamp',
            'ShowerDesigner_SupportBar',
        ]

        tool_commands = [
            'ShowerDesigner_Measure',
            'ShowerDesigner_CutList',
            'ShowerDesigner_Export'
        ]

        # Create toolbars
        self.appendToolbar("ShowerDesigner Enclosures", enclosure_commands)
        self.appendToolbar("ShowerDesigner Components", component_commands)
        self.appendToolbar("ShowerDesigner Tools", tool_commands)

        # Create menus
        self.appendMenu("ShowerDesigner", enclosure_commands + component_commands + tool_commands)
        self.appendMenu(["ShowerDesigner", "Enclosures"], enclosure_commands)
        self.appendMenu(["ShowerDesigner", "Components"], component_commands)
        self.appendMenu(["ShowerDesigner", "Tools"], tool_commands)

    def Activated(self):
        """Called when workbench is activated"""
        import FreeCAD as App
        App.Console.PrintMessage("ShowerDesigner workbench activated\n")

    def Deactivated(self):
        """Called when workbench is deactivated"""
        import FreeCAD as App
        App.Console.PrintMessage("ShowerDesigner workbench deactivated\n")

    def ContextMenu(self, recipient):
        """Define context menu items (optional)"""
        pass

    def GetClassName(self):
        """Return the C++ class name (for backwards compatibility)"""
        return "Gui::PythonWorkbench"


# Register the workbench
Gui.addWorkbench(ShowerDesignerWorkbench())