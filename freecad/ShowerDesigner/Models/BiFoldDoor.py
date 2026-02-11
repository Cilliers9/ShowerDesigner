# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Bi-fold shower door assembly — App::Part containing two glass panels,
wall hinges, fold hinges, handle, and optional folded-position ghost.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.AssemblyBase import AssemblyController
from freecad.ShowerDesigner.Models.ChildProxies import (
    GlassChild,
    HingeChild,
    HandleChild,
    GhostChild,
    MonzaWallHingeChild,
    MonzaFoldHingeChild,
)
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    BIFOLD_HINGE_SPECS,
    HINGE_SPECS,
    HINGE_PLACEMENT_DEFAULTS,
    HARDWARE_FINISHES,
    MONZA_BIFOLD_HINGE_SPECS,
    MONZA_FINISHES,
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


def _setupGhostVP(obj):
    """Set up a semi-transparent VP for the folded-position ghost."""
    if not App.GuiUp:
        return
    obj.ViewObject.Proxy = 0
    obj.ViewObject.Transparency = 80
    obj.ViewObject.ShapeColor = (0.5, 0.5, 0.5)


class BiFoldDoorAssembly(AssemblyController):
    """
    Assembly controller for a bi-fold shower door.

    Creates an App::Part containing:
      - VarSet with all user-editable properties
      - WallPanel glass child (wall-side half)
      - FreePanel glass child (free-side half)
      - 2 WallHinge children (attach wall panel to wall)
      - 2-3 FoldHinge children (at center fold joint)
      - Handle child
      - Optional Ghost child (folded position)
    """

    def __init__(self, part_obj):
        super().__init__(part_obj)
        vs = self._getOrCreateVarSet(part_obj)
        self._setupVarSetProperties(vs)
        self._addChild(part_obj, "WallPanel", GlassChild, _setupGlassVP)
        self._addChild(part_obj, "FreePanel", GlassChild, _setupGlassVP)

    # ------------------------------------------------------------------
    # VarSet property setup
    # ------------------------------------------------------------------

    def _setupVarSetProperties(self, vs):
        # Dimensions
        vs.addProperty(
            "App::PropertyLength", "Width", "Dimensions", "Total door width"
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
            "App::PropertyEnumeration", "FoldDirection", "Door Configuration",
            "Direction the door folds when opening"
        )
        vs.FoldDirection = ["Inward", "Outward"]
        vs.FoldDirection = "Inward"
        vs.addProperty(
            "App::PropertyEnumeration", "HingeSide", "Door Configuration",
            "Which side is attached to the wall"
        )
        vs.HingeSide = ["Left", "Right"]
        vs.HingeSide = "Left"
        vs.addProperty(
            "App::PropertyAngle", "FoldAngle", "Door Configuration",
            "Current fold angle (0=closed)"
        ).FoldAngle = 0

        # Hinge hardware
        vs.addProperty(
            "App::PropertyEnumeration", "HingeModel", "Hinge Hardware",
            "Hinge product line (Legacy = simple box, Monza = self-rising)"
        )
        vs.HingeModel = ["Legacy", "Monza"]
        vs.HingeModel = "Legacy"
        vs.addProperty(
            "App::PropertyInteger", "HingeCount", "Hinge Hardware",
            "Number of bi-fold hinges at fold joint (2-3)"
        ).HingeCount = 2

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
            "Length of bar handle"
        ).HandleLength = 300

        # Hardware display
        all_finishes = HARDWARE_FINISHES[:] + [
            f for f in MONZA_FINISHES if f not in HARDWARE_FINISHES
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
            "App::PropertyBool", "ShowFoldedPosition", "Hardware Display",
            "Show folded position ghost"
        ).ShowFoldedPosition = False

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
            "App::PropertyLength", "PanelWidth", "Calculated",
            "Width of each panel"
        )
        vs.setEditorMode("PanelWidth", 1)
        vs.addProperty(
            "App::PropertyLength", "FoldedWidth", "Calculated",
            "Width of folded stack"
        )
        vs.setEditorMode("FoldedWidth", 1)
        vs.addProperty(
            "App::PropertyLength", "OpeningWidth", "Calculated",
            "Clear opening when folded"
        )
        vs.setEditorMode("OpeningWidth", 1)
        vs.addProperty(
            "App::PropertyLength", "ClearanceDepth", "Calculated",
            "Depth clearance for folding"
        )
        vs.setEditorMode("ClearanceDepth", 1)
        vs.addProperty(
            "App::PropertyAngle", "MaxFoldAngle", "Calculated",
            "Max fold angle in primary direction"
        )
        vs.setEditorMode("MaxFoldAngle", 1)

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
        if width < 400 or height <= 0 or thickness <= 0:
            App.Console.PrintError(
                "Invalid bi-fold door dimensions (min width: 400mm)\n"
            )
            return

        panel_width = width / 2

        # --- Update glass children ---
        wall_panel = self._getChild(part_obj, "WallPanel")
        if wall_panel:
            wall_panel.Width = panel_width
            wall_panel.Height = height
            wall_panel.Thickness = thickness
            if hasattr(wall_panel, "GlassType"):
                wall_panel.GlassType = vs.GlassType

        free_panel = self._getChild(part_obj, "FreePanel")
        if free_panel:
            free_panel.Width = panel_width
            free_panel.Height = height
            free_panel.Thickness = thickness
            if hasattr(free_panel, "GlassType"):
                free_panel.GlassType = vs.GlassType
            free_panel.Placement = App.Placement(
                App.Vector(panel_width, 0, 0), App.Rotation()
            )

        show_hw = vs.ShowHardware
        finish = vs.HardwareFinish
        use_monza = hasattr(vs, "HingeModel") and vs.HingeModel == "Monza"

        # --- Wall hinges (always 2, top and bottom) ---
        if show_hw:
            if use_monza:
                # Remove legacy wall hinges if present, then use Monza
                self._syncChildCount(part_obj, "WallHinge", 0, HingeChild)
                self._updateWallHingesMonza(part_obj, vs)
            else:
                # Remove Monza wall hinges if present, then use legacy
                self._syncChildCount(
                    part_obj, "MonzaWallHinge", 0, MonzaWallHingeChild
                )
                self._updateWallHinges(part_obj, vs)
        else:
            self._syncChildCount(part_obj, "WallHinge", 0, HingeChild)
            self._syncChildCount(
                part_obj, "MonzaWallHinge", 0, MonzaWallHingeChild
            )

        # --- Fold hinges ---
        if show_hw:
            if use_monza:
                self._syncChildCount(part_obj, "FoldHinge", 0, HingeChild)
                self._updateFoldHingesMonza(part_obj, vs)
            else:
                self._syncChildCount(
                    part_obj, "MonzaFoldHinge", 0, MonzaFoldHingeChild
                )
                self._updateFoldHinges(part_obj, vs)
        else:
            self._syncChildCount(part_obj, "FoldHinge", 0, HingeChild)
            self._syncChildCount(
                part_obj, "MonzaFoldHinge", 0, MonzaFoldHingeChild
            )

        # --- Handle ---
        if show_hw and vs.HandleType != "None":
            self._updateHandle(part_obj, vs)
        else:
            if self._hasChild(part_obj, "Handle"):
                self._removeChild(part_obj, "Handle")

        # --- Ghost ---
        if vs.ShowFoldedPosition:
            self._updateGhost(part_obj, vs)
        else:
            if self._hasChild(part_obj, "Ghost"):
                self._removeChild(part_obj, "Ghost")

        # --- Finish ---
        self._updateAllHardwareFinish(part_obj, finish)

        # --- Calculated properties ---
        self._updateCalculatedProperties(vs)

    # ------------------------------------------------------------------
    # Wall hinges (attach wall panel to wall)
    # ------------------------------------------------------------------

    def _updateWallHinges(self, part_obj, vs):
        width = vs.Width.Value
        height = vs.Height.Value
        thickness = vs.Thickness.Value
        hinge_side = vs.HingeSide

        hinge_dims = HINGE_SPECS["standard_wall_mount"]["dimensions"]
        hinge_w = hinge_dims["width"]
        hinge_d = hinge_dims["depth"]
        hinge_h = hinge_dims["height"]

        positions = _calculateHingePositions(height, 2)
        # Wall hinges: only top and bottom
        wall_z = [positions[0], positions[-1]]

        self._syncChildCount(
            part_obj, "WallHinge", 2, HingeChild,
            lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
        )

        y_pos = thickness / 2 - hinge_d / 2
        for i, z_pos in enumerate(wall_z):
            child = self._getChild(part_obj, f"WallHinge{i + 1}")
            if child is None:
                continue
            z_offset = z_pos - hinge_h / 2
            if hinge_side == "Left":
                x_pos = -hinge_w / 2
            else:
                x_pos = width - hinge_w / 2
            child.Placement = App.Placement(
                App.Vector(x_pos, y_pos, z_offset), App.Rotation()
            )

    # ------------------------------------------------------------------
    # Fold hinges (center fold joint)
    # ------------------------------------------------------------------

    def _updateFoldHinges(self, part_obj, vs):
        width = vs.Width.Value
        height = vs.Height.Value
        thickness = vs.Thickness.Value
        hinge_count = max(2, min(3, vs.HingeCount))
        panel_width = width / 2

        hinge_dims = HINGE_SPECS["standard_wall_mount"]["dimensions"]
        hinge_w = hinge_dims["width"]
        hinge_d = hinge_dims["depth"]
        hinge_h = hinge_dims["height"]

        positions = _calculateHingePositions(height, hinge_count)

        self._syncChildCount(
            part_obj, "FoldHinge", hinge_count, HingeChild,
            lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
        )

        center_x = panel_width - hinge_w / 2
        y_pos = thickness / 2 - hinge_d / 2

        for i, z_pos in enumerate(positions):
            child = self._getChild(part_obj, f"FoldHinge{i + 1}")
            if child is None:
                continue
            z_offset = z_pos - hinge_h / 2
            child.Placement = App.Placement(
                App.Vector(center_x, y_pos, z_offset), App.Rotation()
            )

    # ------------------------------------------------------------------
    # Monza wall hinges (self-rising, wall-to-glass)
    # ------------------------------------------------------------------

    def _updateWallHingesMonza(self, part_obj, vs):
        width = vs.Width.Value
        height = vs.Height.Value
        thickness = vs.Thickness.Value
        hinge_side = vs.HingeSide

        dims = MONZA_BIFOLD_HINGE_SPECS["monza_90_wall_to_glass"]["dimensions"]
        body_h = dims["body_height"]

        positions = _calculateHingePositions(height, 2)
        wall_z = [positions[0], positions[-1]]

        self._syncChildCount(
            part_obj, "MonzaWallHinge", 2, MonzaWallHingeChild,
            lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
        )

        for i, z_pos in enumerate(wall_z):
            child = self._getChild(part_obj, f"MonzaWallHinge{i + 1}")
            if child is None:
                continue
            if hasattr(child, "GlassThickness"):
                child.GlassThickness = thickness

            # Origin at wall-side face, hinge-side edge of door
            if hinge_side == "Left":
                x_pos = 0
                y_pos = 0
                rot = App.Rotation()
            else:
                x_pos = width
                y_pos = thickness
                rot = App.Rotation(App.Vector(0, 0, 1), 180)

            child.Placement = App.Placement(
                App.Vector(x_pos, y_pos, z_pos - body_h / 2), rot
            )

    # ------------------------------------------------------------------
    # Monza fold hinges (self-rising, glass-to-glass)
    # ------------------------------------------------------------------

    def _updateFoldHingesMonza(self, part_obj, vs):
        width = vs.Width.Value
        height = vs.Height.Value
        thickness = vs.Thickness.Value
        hinge_count = max(2, min(3, vs.HingeCount))
        panel_width = width / 2

        dims = MONZA_BIFOLD_HINGE_SPECS["monza_180_glass_to_glass"]["dimensions"]
        body_h = dims["body_height"]

        positions = _calculateHingePositions(height, hinge_count)

        self._syncChildCount(
            part_obj, "MonzaFoldHinge", hinge_count, MonzaFoldHingeChild,
            lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
        )

        for i, z_pos in enumerate(positions):
            child = self._getChild(part_obj, f"MonzaFoldHinge{i + 1}")
            if child is None:
                continue
            if hasattr(child, "GlassThickness"):
                child.GlassThickness = thickness

            # Origin at knuckle center, positioned at fold joint
            x_pos = panel_width
            y_pos = thickness / 2

            child.Placement = App.Placement(
                App.Vector(x_pos, y_pos, z_pos - body_h / 2), App.Rotation()
            )

    # ------------------------------------------------------------------
    # Handle
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

        width = vs.Width.Value
        thickness = vs.Thickness.Value
        handle_height = min(vs.HandleHeight.Value, vs.Height.Value - 100)
        handle_offset = vs.HandleOffset.Value

        if vs.HingeSide == "Left":
            x_pos = width - handle_offset
        else:
            x_pos = handle_offset

        child.Placement = App.Placement(
            App.Vector(x_pos, thickness / 2, handle_height), App.Rotation()
        )

    # ------------------------------------------------------------------
    # Folded position ghost
    # ------------------------------------------------------------------

    def _updateGhost(self, part_obj, vs):
        if not self._hasChild(part_obj, "Ghost"):
            self._addChild(part_obj, "Ghost", GhostChild, _setupGhostVP)

        child = self._getChild(part_obj, "Ghost")
        if child is None:
            return

        width = vs.Width.Value
        height = vs.Height.Value
        thickness = vs.Thickness.Value
        panel_width = width / 2
        folded_width = panel_width + thickness

        child.GhostWidth = folded_width
        child.GhostDepth = thickness * 2 + 5
        child.GhostHeight = height

        if vs.HingeSide == "Left":
            x_pos = 0
        else:
            x_pos = width - folded_width

        child.Placement = App.Placement(
            App.Vector(x_pos, -thickness - 5, 0), App.Rotation()
        )

    # ------------------------------------------------------------------
    # Calculated properties
    # ------------------------------------------------------------------

    def _updateCalculatedProperties(self, vs):
        try:
            width = vs.Width.Value
            height = vs.Height.Value
            thickness = vs.Thickness.Value
            panel_width = width / 2

            width_m = width / 1000.0
            height_m = height / 1000.0
            area = width_m * height_m
            if hasattr(vs, "Area"):
                vs.Area = area

            thickness_key = f"{int(thickness)}mm"
            if thickness_key in GLASS_SPECS:
                weight_per_m2 = GLASS_SPECS[thickness_key]["weight_kg_m2"]
                weight = area * weight_per_m2
            else:
                weight = area * 2.5 * thickness
            if hasattr(vs, "Weight"):
                vs.Weight = weight

            # Map FoldDirection to BIFOLD_HINGE_SPECS key
            fold_key = "Left" if vs.FoldDirection == "Inward" else "Right"
            spec = BIFOLD_HINGE_SPECS.get(fold_key, {})

            if hasattr(vs, "PanelWidth"):
                vs.PanelWidth = panel_width
            folded_width = panel_width + thickness
            if hasattr(vs, "FoldedWidth"):
                vs.FoldedWidth = folded_width
            if hasattr(vs, "OpeningWidth"):
                vs.OpeningWidth = width - folded_width
            if hasattr(vs, "ClearanceDepth"):
                vs.ClearanceDepth = panel_width
            if hasattr(vs, "MaxFoldAngle"):
                vs.MaxFoldAngle = spec.get("primary_angle", 180)

        except Exception as e:
            App.Console.PrintWarning(
                f"Error updating calculated properties: {e}\n"
            )

    def assemblyOnChanged(self, part_obj, prop):
        pass


# ======================================================================
# Helper
# ======================================================================

def _calculateHingePositions(height, count):
    offset_top = HINGE_PLACEMENT_DEFAULTS["offset_top"]
    offset_bottom = HINGE_PLACEMENT_DEFAULTS["offset_bottom"]
    count = max(2, min(3, count))
    positions = [offset_bottom, height - offset_top]
    if count >= 3:
        middle = (offset_bottom + (height - offset_top)) / 2
        positions.insert(1, middle)
    return sorted(positions)


# ======================================================================
# Factory function
# ======================================================================

def createBiFoldDoor(name="BiFoldDoor"):
    """
    Create a new bi-fold door assembly in the active document.

    Args:
        name: Name for the assembly (default: "BiFoldDoor")

    Returns:
        App::Part assembly object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    part = doc.addObject("App::Part", name)
    BiFoldDoorAssembly(part)

    doc.recompute()
    App.Console.PrintMessage(f"Bi-fold door '{name}' created\n")
    return part
