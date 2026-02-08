# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Lightweight proxy classes for child objects inside assembly containers.

Each class generates its own shape using the existing shared shape
functions from the standalone hardware models. These proxies are simpler
than the standalone models — they have minimal properties since the
assembly controller manages dimensions and positioning.
"""

import FreeCAD as App
import Part

from freecad.ShowerDesigner.Data.HardwareSpecs import (
    HINGE_SPECS,
    HANDLE_SPECS,
    CLAMP_SPECS,
    SUPPORT_BAR_SPECS,
    TRACK_PROFILES,
    ROLLER_SPECS,
    BOTTOM_GUIDE_SPECS,
    CHANNEL_SPECS,
)


# ======================================================================
# Glass
# ======================================================================

class GlassChild:
    """Proxy for a glass panel child inside an assembly."""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyLength", "Width", "Dimensions", "Panel width"
        ).Width = 900
        obj.addProperty(
            "App::PropertyLength", "Height", "Dimensions", "Panel height"
        ).Height = 2000
        obj.addProperty(
            "App::PropertyLength", "Thickness", "Dimensions", "Glass thickness"
        ).Thickness = 8
        obj.addProperty(
            "App::PropertyEnumeration", "GlassType", "Glass", "Glass type"
        )
        obj.GlassType = ["Clear", "Frosted", "Bronze", "Grey", "Reeded", "Low-Iron"]
        obj.GlassType = "Clear"

    def execute(self, obj):
        w = obj.Width.Value
        t = obj.Thickness.Value
        h = obj.Height.Value
        if w <= 0 or t <= 0 or h <= 0:
            return
        obj.Shape = Part.makeBox(w, t, h)

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


# ======================================================================
# Hinge
# ======================================================================

class HingeChild:
    """Proxy for a hinge child inside an assembly."""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyEnumeration", "HingeType", "Hinge", "Hinge type"
        )
        obj.HingeType = list(HINGE_SPECS.keys())
        obj.HingeType = "standard_wall_mount"

    def execute(self, obj):
        from freecad.ShowerDesigner.Models.Hinge import createHingeShape
        spec = HINGE_SPECS.get(obj.HingeType)
        if spec is None:
            return
        dims = spec["dimensions"]
        obj.Shape = createHingeShape(dims["width"], dims["depth"], dims["height"])

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


# ======================================================================
# Handle
# ======================================================================

class HandleChild:
    """Proxy for a handle child inside an assembly."""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyEnumeration", "HandleType", "Handle", "Handle type"
        )
        obj.HandleType = list(HANDLE_SPECS.keys())
        obj.HandleType = "Bar"
        obj.addProperty(
            "App::PropertyLength", "HandleLength", "Handle", "Handle length"
        ).HandleLength = 300

    def execute(self, obj):
        from freecad.ShowerDesigner.Models.Handle import createHandleShape
        shape = createHandleShape(obj.HandleType, obj.HandleLength.Value)
        if shape is None:
            shape = Part.makeSphere(5)
        obj.Shape = shape

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


# ======================================================================
# Clamp
# ======================================================================

class ClampChild:
    """Proxy for a clamp child inside an assembly."""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyEnumeration", "ClampType", "Clamp", "Clamp type"
        )
        obj.ClampType = list(CLAMP_SPECS.keys())
        obj.ClampType = "L_Clamp"

    def execute(self, obj):
        from freecad.ShowerDesigner.Models.Clamp import createClampShape
        obj.Shape = createClampShape(obj.ClampType)

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


# ======================================================================
# Support Bar
# ======================================================================

class SupportBarChild:
    """Proxy for a support bar child inside an assembly."""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyEnumeration", "BarType", "SupportBar", "Bar type"
        )
        obj.BarType = list(SUPPORT_BAR_SPECS.keys())
        obj.BarType = "Horizontal"
        obj.addProperty(
            "App::PropertyLength", "Length", "SupportBar", "Bar length"
        ).Length = 500
        obj.addProperty(
            "App::PropertyLength", "Diameter", "SupportBar", "Bar diameter"
        ).Diameter = 16

    def execute(self, obj):
        from freecad.ShowerDesigner.Models.SupportBar import createSupportBarShape
        length = obj.Length.Value
        diameter = obj.Diameter.Value
        if length <= 0 or diameter <= 0:
            return
        obj.Shape = createSupportBarShape(obj.BarType, length, diameter)

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


# ======================================================================
# Channel (wall / floor U-channel)
# ======================================================================

class ChannelChild:
    """Proxy for a wall or floor channel child inside an assembly."""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyEnumeration", "ChannelLocation", "Channel",
            "Channel location"
        )
        obj.ChannelLocation = ["wall", "floor"]
        obj.ChannelLocation = "wall"
        obj.addProperty(
            "App::PropertyLength", "ChannelLength", "Channel",
            "Length of the channel"
        ).ChannelLength = 2000

    def execute(self, obj):
        loc = obj.ChannelLocation
        spec = CHANNEL_SPECS.get(loc, CHANNEL_SPECS["wall"])
        cw = spec["width"]
        cd = spec["depth"]
        length = obj.ChannelLength.Value
        if length <= 0:
            return
        # Create U-channel profile: outer box minus inner box
        outer = Part.makeBox(cw, cd, length)
        inner = Part.makeBox(cw - 4, cd - 2, length)
        inner.translate(App.Vector(2, 2, 0))
        obj.Shape = outer.cut(inner)

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


# ======================================================================
# Track (sliding door top track)
# ======================================================================

class TrackChild:
    """Proxy for a sliding door top track child."""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyEnumeration", "TrackType", "Track", "Track profile type"
        )
        obj.TrackType = list(TRACK_PROFILES.keys())
        obj.TrackType = "Edge"
        obj.addProperty(
            "App::PropertyLength", "TrackLength", "Track", "Total track length"
        ).TrackLength = 1900

    def execute(self, obj):
        spec = TRACK_PROFILES.get(obj.TrackType)
        if spec is None:
            return
        length = obj.TrackLength.Value
        if length <= 0:
            return
        obj.Shape = Part.makeBox(length, spec["width"], spec["height"])

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


# ======================================================================
# Guide (sliding door bottom guide)
# ======================================================================

class GuideChild:
    """Proxy for a sliding door bottom guide child."""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyLength", "GuideLength", "Guide", "Total guide length"
        ).GuideLength = 1900

    def execute(self, obj):
        length = obj.GuideLength.Value
        if length <= 0:
            return
        obj.Shape = Part.makeBox(
            length, BOTTOM_GUIDE_SPECS["width"], BOTTOM_GUIDE_SPECS["height"]
        )

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


# ======================================================================
# Roller (sliding door roller)
# ======================================================================

class RollerChild:
    """Proxy for a sliding door roller child."""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyEnumeration", "RollerType", "Roller", "Roller type"
        )
        obj.RollerType = list(ROLLER_SPECS.keys())
        obj.RollerType = "Standard"

    def execute(self, obj):
        spec = ROLLER_SPECS.get(obj.RollerType)
        if spec is None:
            return
        obj.Shape = Part.makeCylinder(
            spec["radius"], spec["height"],
            App.Vector(0, 0, 0), App.Vector(0, 0, 1)
        )

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


# ======================================================================
# Swing Arc (hinged door clearance visualization)
# ======================================================================

class SwingArcChild:
    """Proxy for a hinged door swing arc visualization."""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyLength", "Radius", "Arc", "Arc radius (door width)"
        ).Radius = 900
        obj.addProperty(
            "App::PropertyAngle", "StartAngle", "Arc", "Arc start angle"
        ).StartAngle = 0
        obj.addProperty(
            "App::PropertyAngle", "EndAngle", "Arc", "Arc end angle"
        ).EndAngle = 90

    def execute(self, obj):
        radius = obj.Radius.Value
        if radius <= 0:
            return
        start = obj.StartAngle.Value
        end = obj.EndAngle.Value
        if abs(end - start) < 0.1:
            return
        arc = Part.makeCircle(
            radius, App.Vector(0, 0, 0), App.Vector(0, 0, 1), start, end
        )
        obj.Shape = arc

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


# ======================================================================
# Ghost (bi-fold folded position visualization)
# ======================================================================

class GhostChild:
    """Proxy for a bi-fold door folded position ghost."""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty(
            "App::PropertyLength", "GhostWidth", "Ghost", "Folded stack width"
        ).GhostWidth = 100
        obj.addProperty(
            "App::PropertyLength", "GhostDepth", "Ghost", "Folded stack depth"
        ).GhostDepth = 21
        obj.addProperty(
            "App::PropertyLength", "GhostHeight", "Ghost", "Folded stack height"
        ).GhostHeight = 2000

    def execute(self, obj):
        w = obj.GhostWidth.Value
        d = obj.GhostDepth.Value
        h = obj.GhostHeight.Value
        if w <= 0 or d <= 0 or h <= 0:
            return
        obj.Shape = Part.makeBox(w, d, h)

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None
