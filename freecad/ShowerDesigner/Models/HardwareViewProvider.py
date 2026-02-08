# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
ViewProvider for hardware objects — handles finish-based coloring.

All hardware pieces (hinges, clamps, handles, support bars, tracks, etc.)
share this ViewProvider so they display with a consistent metallic finish.
"""

import FreeCAD as App


# Finish → RGB color mapping (values 0-1)
FINISH_COLORS = {
    "Chrome": (0.75, 0.75, 0.80),
    "Brushed-Nickel": (0.65, 0.63, 0.58),
    "Matte-Black": (0.10, 0.10, 0.10),
    "Gold": (0.83, 0.69, 0.22),
}


class HardwareViewProvider:
    """
    ViewProvider for hardware objects inside assemblies.

    Colors the object based on its hardware finish (Chrome, Brushed-Nickel, etc.).
    """

    def __init__(self, vobj, finish="Chrome"):
        vobj.Proxy = self
        self.Object = vobj.Object
        self._finish = finish
        self._applyFinish(vobj)

    def attach(self, vobj):
        self.Object = vobj.Object

    def updateData(self, obj, prop):
        pass

    def onChanged(self, vobj, prop):
        pass

    def updateFinish(self, vobj, finish):
        self._finish = finish
        self._applyFinish(vobj)

    def _applyFinish(self, vobj):
        color = FINISH_COLORS.get(self._finish, FINISH_COLORS["Chrome"])
        vobj.ShapeColor = color
        vobj.Transparency = 0
        if hasattr(vobj, "DisplayMode"):
            vobj.DisplayMode = "Shaded"
        if hasattr(vobj, "LineWidth"):
            vobj.LineWidth = 1.0

    def getDisplayModes(self, vobj):
        return ["Shaded", "Flat Lines", "Wireframe"]

    def getDefaultDisplayMode(self):
        return "Shaded"

    def setDisplayMode(self, mode):
        return mode

    def getIcon(self):
        from freecad.ShowerDesigner.Misc.Resources import asIcon
        return asIcon('Logo')

    def __getstate__(self):
        return {"finish": self._finish}

    def __setstate__(self, state):
        if state:
            self._finish = state.get("finish", "Chrome")
        else:
            self._finish = "Chrome"


def setupHardwareViewProvider(obj, finish="Chrome"):
    """
    Setup the hardware view provider for a Part::FeaturePython object.

    Args:
        obj: FreeCAD document object
        finish: Hardware finish name (Chrome, Brushed-Nickel, Matte-Black, Gold)
    """
    if not App.GuiUp:
        return
    HardwareViewProvider(obj.ViewObject, finish)
