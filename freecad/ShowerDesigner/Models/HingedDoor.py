# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Hinged shower door assembly — App::Part containing glass + hinges + handle.

Each hinge and the handle are individual Part::FeaturePython children
with their own ViewProviders for independent display control.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.AssemblyBase import AssemblyController
from freecad.ShowerDesigner.Models.ChildProxies import (
    GlassChild,
    HingeChild,
    HandleChild,
    SwingArcChild,
)
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    HINGE_SPECS,
    BEVEL_HINGE_SPECS,
    BEVEL_FINISHES,
    HINGE_PLACEMENT_DEFAULTS,
    HARDWARE_FINISHES,
    DOOR_MOUNTING_VARIANTS,
    getHingeModelsForVariant,
)
from freecad.ShowerDesigner.Data.GlassSpecs import GLASS_SPECS


def _setupGlassVP(obj):
    from freecad.ShowerDesigner.Models.GlassPanelViewProvider import setupViewProvider
    setupViewProvider(obj)


def _setupHardwareVP(obj, finish="Chrome"):
    from freecad.ShowerDesigner.Models.HardwareViewProvider import (
        setupHardwareViewProvider,
    )
    setupHardwareViewProvider(obj, finish)


class HingedDoorAssembly(AssemblyController):
    """
    Assembly controller for a hinged shower door.

    Creates an App::Part containing:
      - VarSet with all user-editable properties
      - Glass child (Part::FeaturePython + GlassPanelViewProvider)
      - 2-3 Hinge children (Part::FeaturePython + HardwareViewProvider)
      - Handle child (Part::FeaturePython + HardwareViewProvider)
      - Optional SwingArc child for clearance visualization
    """

    def __init__(self, part_obj):
        super().__init__(part_obj)
        vs = self._getOrCreateVarSet(part_obj)
        self._setupVarSetProperties(vs)
        self._addChild(part_obj, "Glass", GlassChild, _setupGlassVP)

    # ------------------------------------------------------------------
    # VarSet property setup
    # ------------------------------------------------------------------

    def _setupVarSetProperties(self, vs):
        # Dimensions
        vs.addProperty(
            "App::PropertyLength", "Width", "Dimensions", "Door width"
        ).Width = 900
        vs.addProperty(
            "App::PropertyLength", "Height", "Dimensions", "Door height"
        ).Height = 2000
        vs.addProperty(
            "App::PropertyLength", "Thickness", "Dimensions", "Glass thickness"
        ).Thickness = 8

        # Glass
        vs.addProperty(
            "App::PropertyEnumeration", "GlassType", "Glass", "Type of glass"
        )
        vs.GlassType = ["Clear", "Frosted", "Bronze", "Grey", "Reeded", "Low-Iron"]
        vs.GlassType = "Clear"
        vs.addProperty(
            "App::PropertyEnumeration", "EdgeFinish", "Glass", "Edge finish type"
        )
        vs.EdgeFinish = ["Bright_Polish", "Dull_Polish"]
        vs.EdgeFinish = "Bright_Polish"
        vs.addProperty(
            "App::PropertyEnumeration", "TemperType", "Glass", "Tempering type"
        )
        vs.TemperType = ["Tempered", "Laminated", "None"]
        vs.TemperType = "Tempered"

        # Door configuration
        vs.addProperty(
            "App::PropertyEnumeration", "MountingType", "Door Configuration",
            "How the door is mounted (Wall, Glass-to-Glass, or Pivot)"
        )
        vs.MountingType = list(DOOR_MOUNTING_VARIANTS.keys())
        vs.MountingType = "Wall Mounted"
        vs.addProperty(
            "App::PropertyEnumeration", "SwingDirection", "Door Configuration",
            "Direction the door swings when opening"
        )
        vs.SwingDirection = ["Inward", "Outward"]
        vs.SwingDirection = "Inward"
        vs.addProperty(
            "App::PropertyEnumeration", "HingeSide", "Door Configuration",
            "Which side the hinges are mounted"
        )
        vs.HingeSide = ["Left", "Right"]
        vs.HingeSide = "Left"
        vs.addProperty(
            "App::PropertyAngle", "OpeningAngle", "Door Configuration",
            "Maximum opening angle"
        ).OpeningAngle = 90

        # Hinge hardware
        _initial_models = getHingeModelsForVariant("Wall Mounted")
        vs.addProperty(
            "App::PropertyEnumeration", "HingeModel", "Hinge Hardware",
            "Hinge product line (Legacy = simple box hinges)"
        )
        vs.HingeModel = _initial_models
        vs.HingeModel = _initial_models[0]
        vs.addProperty(
            "App::PropertyInteger", "HingeCount", "Hinge Hardware",
            "Number of hinges (2-3)"
        ).HingeCount = 2
        vs.addProperty(
            "App::PropertyLength", "HingeOffsetTop", "Hinge Hardware",
            "Distance from top edge to top hinge"
        ).HingeOffsetTop = HINGE_PLACEMENT_DEFAULTS["offset_top"]
        vs.addProperty(
            "App::PropertyLength", "HingeOffsetBottom", "Hinge Hardware",
            "Distance from bottom edge to bottom hinge"
        ).HingeOffsetBottom = HINGE_PLACEMENT_DEFAULTS["offset_bottom"]

        # Handle hardware
        vs.addProperty(
            "App::PropertyEnumeration", "HandleType", "Handle Hardware",
            "Type of door handle"
        )
        vs.HandleType = ["None", "Knob", "Bar", "Pull"]
        vs.HandleType = "Bar"
        vs.addProperty(
            "App::PropertyLength", "HandleHeight", "Handle Hardware",
            "Height of handle from floor"
        ).HandleHeight = 1050
        vs.addProperty(
            "App::PropertyLength", "HandleOffset", "Handle Hardware",
            "Distance from handle to door edge"
        ).HandleOffset = 75
        vs.addProperty(
            "App::PropertyLength", "HandleLength", "Handle Hardware",
            "Length of bar handle (for Bar type)"
        ).HandleLength = 300

        # Hardware display
        all_finishes = HARDWARE_FINISHES[:] + [
            f for f in BEVEL_FINISHES if f not in HARDWARE_FINISHES
        ]
        vs.addProperty(
            "App::PropertyEnumeration", "HardwareFinish", "Hardware Display",
            "Finish for all hardware"
        )
        vs.HardwareFinish = all_finishes
        vs.HardwareFinish = "Chrome"
        vs.addProperty(
            "App::PropertyBool", "ShowHardware", "Hardware Display",
            "Show hardware in 3D view"
        ).ShowHardware = True
        vs.addProperty(
            "App::PropertyBool", "ShowSwingArc", "Hardware Display",
            "Show swing arc on floor plane"
        ).ShowSwingArc = False

        # Calculated (read-only)
        vs.addProperty(
            "App::PropertyFloat", "Weight", "Calculated",
            "Weight of the door in kg"
        )
        vs.setEditorMode("Weight", 1)
        vs.addProperty(
            "App::PropertyFloat", "Area", "Calculated",
            "Area of the door in m²"
        )
        vs.setEditorMode("Area", 1)
        vs.addProperty(
            "App::PropertyInteger", "RecommendedHingeCount", "Calculated",
            "Recommended hinge count based on door weight"
        )
        vs.setEditorMode("RecommendedHingeCount", 1)

    # ------------------------------------------------------------------
    # execute
    # ------------------------------------------------------------------

    def assemblyExecute(self, part_obj):
        vs = self._getVarSet(part_obj)
        if vs is None:
            return

        width = vs.Width.Value
        height = vs.Height.Value
        thickness = vs.Thickness.Value
        if width <= 0 or height <= 0 or thickness <= 0:
            App.Console.PrintError("Invalid door dimensions\n")
            return

        # --- Sync HingeModel choices to current MountingType ---
        mounting = vs.MountingType if hasattr(vs, "MountingType") else "Wall Mounted"
        available = getHingeModelsForVariant(mounting)
        current_model = vs.HingeModel
        vs.HingeModel = available
        if current_model in available:
            vs.HingeModel = current_model
        else:
            vs.HingeModel = available[0]

        # --- Pivot forces HingeCount to 2 ---
        if mounting == "Pivot":
            vs.HingeCount = 2
            vs.setEditorMode("HingeCount", 1)  # Read-only
        else:
            vs.setEditorMode("HingeCount", 0)  # Editable

        # --- Update Glass child ---
        glass = self._getChild(part_obj, "Glass")
        if glass:
            glass.Width = width
            glass.Height = height
            glass.Thickness = thickness
            if hasattr(glass, "GlassType"):
                glass.GlassType = vs.GlassType

        show_hw = vs.ShowHardware
        finish = vs.HardwareFinish

        # --- Hinges ---
        if show_hw:
            self._updateHinges(part_obj, vs)
        else:
            self._syncChildCount(part_obj, "Hinge", 0, HingeChild)

        # --- Handle ---
        if show_hw and vs.HandleType != "None":
            self._updateHandle(part_obj, vs)
        else:
            if self._hasChild(part_obj, "Handle"):
                self._removeChild(part_obj, "Handle")

        # --- Swing Arc ---
        if vs.ShowSwingArc:
            self._updateSwingArc(part_obj, vs)
        else:
            if self._hasChild(part_obj, "SwingArc"):
                self._removeChild(part_obj, "SwingArc")

        # --- Hardware finish ---
        self._updateAllHardwareFinish(part_obj, finish)

        # --- Calculated properties ---
        self._updateCalculatedProperties(vs)

    # ------------------------------------------------------------------
    # Hinge management
    # ------------------------------------------------------------------

    def _updateHinges(self, part_obj, vs):
        mounting = vs.MountingType if hasattr(vs, "MountingType") else "Wall Mounted"
        if mounting == "Pivot":
            self._updateHingesPivot(part_obj, vs)
        elif mounting == "Glass Mounted":
            self._updateHingesGlassMounted(part_obj, vs)
        else:
            self._updateHingesWallMounted(part_obj, vs)

    # ------------------------------------------------------------------
    # Wall Mounted hinges (original logic)
    # ------------------------------------------------------------------

    def _updateHingesWallMounted(self, part_obj, vs):
        width = vs.Width.Value
        height = vs.Height.Value
        thickness = vs.Thickness.Value
        hinge_count = max(2, min(3, vs.HingeCount))
        hinge_side = vs.HingeSide

        hinge_model = "Legacy"
        if hasattr(vs, "HingeModel"):
            hinge_model = vs.HingeModel

        positions = _calculateHingePositions(
            height, hinge_count,
            vs.HingeOffsetTop.Value, vs.HingeOffsetBottom.Value
        )

        self._syncChildCount(
            part_obj, "Hinge", hinge_count, HingeChild,
            lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
        )

        use_bevel = hinge_model != "Legacy" and hinge_model in BEVEL_HINGE_SPECS

        if use_bevel:
            bevel_dims = BEVEL_HINGE_SPECS[hinge_model]["dimensions"]
        else:
            hinge_dims = HINGE_SPECS["standard_wall_mount"]["dimensions"]
            hinge_w = hinge_dims["width"]
            hinge_d = hinge_dims["depth"]
            hinge_h = hinge_dims["height"]

        for i, z_pos in enumerate(positions):
            child = self._getChild(part_obj, f"Hinge{i + 1}")
            if child is None:
                continue

            if use_bevel:
                child.HingeType = hinge_model
                if hasattr(child, "GlassThickness"):
                    child.GlassThickness = thickness

                if hinge_side == "Left":
                    x_pos = 0
                else:
                    x_pos = width

                y_pos = 0
                z_offset = z_pos

                if hinge_side == "Right":
                    rot = App.Rotation(App.Vector(0, 0, 1), 180)
                    y_pos = thickness
                else:
                    rot = App.Rotation()

                child.Placement = App.Placement(
                    App.Vector(x_pos, y_pos, z_offset), rot
                )
            else:
                child.HingeType = "standard_wall_mount"

                if hinge_side == "Left":
                    x_pos = -10
                else:
                    x_pos = width - hinge_w + 10

                y_pos = thickness / 2 - hinge_d / 2
                z_offset = z_pos - hinge_h / 2

                child.Placement = App.Placement(
                    App.Vector(x_pos, y_pos, z_offset), App.Rotation()
                )

    # ------------------------------------------------------------------
    # Glass Mounted hinges (Glass-to-Glass)
    # ------------------------------------------------------------------

    def _updateHingesGlassMounted(self, part_obj, vs):
        width = vs.Width.Value
        height = vs.Height.Value
        thickness = vs.Thickness.Value
        hinge_count = max(2, min(3, vs.HingeCount))
        hinge_side = vs.HingeSide

        hinge_model = "Legacy"
        if hasattr(vs, "HingeModel"):
            hinge_model = vs.HingeModel

        positions = _calculateHingePositions(
            height, hinge_count,
            vs.HingeOffsetTop.Value, vs.HingeOffsetBottom.Value
        )

        self._syncChildCount(
            part_obj, "Hinge", hinge_count, HingeChild,
            lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
        )

        use_bevel = hinge_model != "Legacy" and hinge_model in BEVEL_HINGE_SPECS

        if use_bevel:
            bevel_dims = BEVEL_HINGE_SPECS[hinge_model]["dimensions"]
        else:
            hinge_dims = HINGE_SPECS["standard_glass_to_glass"]["dimensions"]
            hinge_w = hinge_dims["width"]
            hinge_d = hinge_dims["depth"]
            hinge_h = hinge_dims["height"]

        for i, z_pos in enumerate(positions):
            child = self._getChild(part_obj, f"Hinge{i + 1}")
            if child is None:
                continue

            if use_bevel:
                child.HingeType = hinge_model
                if hasattr(child, "GlassThickness"):
                    child.GlassThickness = thickness

                # Glass-to-Glass bevel: origin at knuckle center,
                # positioned at the hinge-side glass edge
                if hinge_side == "Left":
                    x_pos = 0
                    y_pos = thickness / 2
                    rot = App.Rotation()
                else:
                    x_pos = width
                    y_pos = thickness / 2
                    rot = App.Rotation(App.Vector(0, 0, 1), 180)

                child.Placement = App.Placement(
                    App.Vector(x_pos, y_pos, z_pos), rot
                )
            else:
                child.HingeType = "standard_glass_to_glass"

                # Legacy glass-to-glass: centered on glass edge
                if hinge_side == "Left":
                    x_pos = -hinge_w / 2
                else:
                    x_pos = width - hinge_w / 2

                y_pos = thickness / 2 - hinge_d / 2
                z_offset = z_pos - hinge_h / 2

                child.Placement = App.Placement(
                    App.Vector(x_pos, y_pos, z_offset), App.Rotation()
                )

    # ------------------------------------------------------------------
    # Pivot hinges (top + bottom)
    # ------------------------------------------------------------------

    def _updateHingesPivot(self, part_obj, vs):
        width = vs.Width.Value
        height = vs.Height.Value
        thickness = vs.Thickness.Value
        hinge_side = vs.HingeSide

        hinge_model = vs.HingeModel if hasattr(vs, "HingeModel") else ""

        # Pivot always uses exactly 2 hinges: bottom and top
        hinge_count = 2
        self._syncChildCount(
            part_obj, "Hinge", hinge_count, HingeChild,
            lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
        )

        if hinge_model not in BEVEL_HINGE_SPECS:
            return

        bevel_dims = BEVEL_HINGE_SPECS[hinge_model]["dimensions"]
        body_h = bevel_dims["body_height"]
        floor_offset = bevel_dims.get("floor_offset", 15)

        # Pivot positions: bottom near floor, top near ceiling
        positions = [floor_offset, height - floor_offset - body_h]

        for i, z_pos in enumerate(positions):
            child = self._getChild(part_obj, f"Hinge{i + 1}")
            if child is None:
                continue

            child.HingeType = hinge_model
            if hasattr(child, "GlassThickness"):
                child.GlassThickness = thickness

            if hinge_side == "Left":
                x_pos = 0
                y_pos = thickness / 2
                rot = App.Rotation()
            else:
                x_pos = width
                y_pos = thickness / 2
                rot = App.Rotation(App.Vector(0, 0, 1), 180)

            child.Placement = App.Placement(
                App.Vector(x_pos, y_pos, z_pos), rot
            )

    # ------------------------------------------------------------------
    # Handle management
    # ------------------------------------------------------------------

    def _updateHandle(self, part_obj, vs):
        if not self._hasChild(part_obj, "Handle"):
            self._addChild(
                part_obj, "Handle", HandleChild,
                lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
            )

        child = self._getChild(part_obj, "Handle")
        if child is None:
            return

        child.HandleType = vs.HandleType
        child.HandleLength = vs.HandleLength.Value

        # Calculate handle position (opposite side from hinges)
        width = vs.Width.Value
        thickness = vs.Thickness.Value
        handle_height = min(vs.HandleHeight.Value, vs.Height.Value - 100)
        handle_offset = vs.HandleOffset.Value

        if vs.HingeSide == "Left":
            x_pos = width - handle_offset
        else:
            x_pos = handle_offset

        y_pos = thickness / 2
        z_pos = handle_height

        child.Placement = App.Placement(
            App.Vector(x_pos, y_pos, z_pos), App.Rotation()
        )

    # ------------------------------------------------------------------
    # Swing Arc management
    # ------------------------------------------------------------------

    def _updateSwingArc(self, part_obj, vs):
        if not self._hasChild(part_obj, "SwingArc"):
            self._addChild(part_obj, "SwingArc", SwingArcChild, None)

        child = self._getChild(part_obj, "SwingArc")
        if child is None:
            return

        width = vs.Width.Value
        thickness = vs.Thickness.Value
        opening_angle = vs.OpeningAngle.Value

        child.Radius = width

        if vs.HingeSide == "Left":
            center = App.Vector(0, thickness / 2, 0)
            if vs.SwingDirection == "Inward":
                child.StartAngle = 0
                child.EndAngle = opening_angle
            else:
                child.StartAngle = -opening_angle
                child.EndAngle = 0
        else:
            center = App.Vector(width, thickness / 2, 0)
            if vs.SwingDirection == "Inward":
                child.StartAngle = 180 - opening_angle
                child.EndAngle = 180
            else:
                child.StartAngle = 180
                child.EndAngle = 180 + opening_angle

        child.Placement = App.Placement(center, App.Rotation())

    # ------------------------------------------------------------------
    # Calculated properties
    # ------------------------------------------------------------------

    def _updateCalculatedProperties(self, vs):
        try:
            width_m = vs.Width.Value / 1000.0
            height_m = vs.Height.Value / 1000.0
            area = width_m * height_m
            if hasattr(vs, "Area"):
                vs.Area = area

            thickness_key = f"{int(vs.Thickness.Value)}mm"
            if thickness_key in GLASS_SPECS:
                weight_per_m2 = GLASS_SPECS[thickness_key]["weight_kg_m2"]
                weight = area * weight_per_m2
            else:
                weight = area * 2.5 * vs.Thickness.Value
            if hasattr(vs, "Weight"):
                vs.Weight = weight

            # Recommended hinge count
            if hasattr(vs, "RecommendedHingeCount"):
                threshold = HINGE_PLACEMENT_DEFAULTS["weight_threshold_3_hinges"]
                vs.RecommendedHingeCount = 2 if weight <= threshold else 3

        except Exception as e:
            App.Console.PrintWarning(
                f"Error updating calculated properties: {e}\n"
            )

    # ------------------------------------------------------------------
    # onChanged
    # ------------------------------------------------------------------

    def assemblyOnChanged(self, part_obj, prop):
        pass


# ======================================================================
# Helper
# ======================================================================

def _calculateHingePositions(height, count, offset_top, offset_bottom):
    """Calculate evenly-spaced hinge Z positions along a door."""
    count = max(2, min(3, count))
    positions = [offset_bottom, height - offset_top]
    if count >= 3:
        middle = (offset_bottom + (height - offset_top)) / 2
        positions.insert(1, middle)
    return sorted(positions)


# ======================================================================
# Factory function
# ======================================================================

def createHingedDoor(name="HingedDoor"):
    """
    Create a new hinged door assembly in the active document.

    Args:
        name: Name for the assembly (default: "HingedDoor")

    Returns:
        App::Part assembly object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    part = doc.addObject("App::Part", name)
    HingedDoorAssembly(part)

    doc.recompute()
    App.Console.PrintMessage(f"Hinged door '{name}' created\n")
    return part
