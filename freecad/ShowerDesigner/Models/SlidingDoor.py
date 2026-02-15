# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Sliding shower door assembly — single App::Part containing glass panel(s),
handle, slider track, rollers, anti-lift pins, and floor guide.

One VarSet owns all user-editable properties. Slider hardware (track,
rollers, pins, floor guide) is built in; no separate SliderHardware
assembly is needed.
"""

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Models.AssemblyBase import AssemblyController
from freecad.ShowerDesigner.Models.ChildProxies import (
    GlassChild,
    HandleChild,
    SliderTrackChild,
    SliderRollerChild,
    SliderFloorGuideChild,
    AntiLiftPinChild,
)
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    HARDWARE_FINISHES,
    SLIDER_SYSTEM_SPECS,
    FLOOR_GUIDE_SPECS,
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


class SlidingDoorAssembly(AssemblyController):
    """
    Assembly controller for a sliding shower door.

    Creates an App::Part containing:
      - VarSet with all user-editable properties
      - 1-2 Glass panel children (single or bypass)
      - Handle child
      - SliderTrack child
      - SliderRoller1..N children (2 per panel)
      - AntiLiftPin1..N children (edge_slider only)
      - SliderFloorGuide child
    """

    def __init__(self, part_obj):
        super().__init__(part_obj)
        vs = self._getOrCreateVarSet(part_obj)
        self._setupVarSetProperties(vs)
        self._addChild(part_obj, "Panel1", GlassChild, _setupGlassVP)

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
            "App::PropertyInteger", "PanelCount", "Door Configuration",
            "Number of panels (1=single, 2=bypass)"
        ).PanelCount = 1
        vs.addProperty(
            "App::PropertyEnumeration", "SlideDirection", "Door Configuration",
            "Direction the door slides when opening"
        )
        vs.SlideDirection = ["Left", "Right"]
        vs.SlideDirection = "Right"
        vs.addProperty(
            "App::PropertyLength", "OverlapWidth", "Door Configuration",
            "Overlap width for bypass doors"
        ).OverlapWidth = 50

        # Slider system
        vs.addProperty(
            "App::PropertyEnumeration", "SliderSystem", "Slider Configuration",
            "Catalogue slider system"
        )
        vs.SliderSystem = list(SLIDER_SYSTEM_SPECS.keys())
        vs.SliderSystem = "edge_slider"

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
        vs.addProperty(
            "App::PropertyEnumeration", "HardwareFinish", "Hardware Display",
            "Finish for all hardware"
        )
        vs.HardwareFinish = HARDWARE_FINISHES[:]
        vs.HardwareFinish = "Chrome"
        vs.addProperty(
            "App::PropertyBool", "ShowHardware", "Hardware Display",
            "Show hardware components"
        ).ShowHardware = True

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
            "App::PropertyString", "SystemValidation", "Calculated",
            "Slider system validation status"
        )
        vs.setEditorMode("SystemValidation", 1)
        vs.addProperty(
            "App::PropertyLength", "TrackLength", "Calculated",
            "Total track length"
        )
        vs.setEditorMode("TrackLength", 1)
        vs.addProperty(
            "App::PropertyLength", "TrackHeight", "Calculated",
            "Track profile height"
        )
        vs.setEditorMode("TrackHeight", 1)
        vs.addProperty(
            "App::PropertyLength", "TravelDistance", "Calculated",
            "How far the door can slide"
        )
        vs.setEditorMode("TravelDistance", 1)
        vs.addProperty(
            "App::PropertyLength", "OpeningWidth", "Calculated",
            "Clear opening when fully open"
        )
        vs.setEditorMode("OpeningWidth", 1)

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

        panel_count = max(1, min(2, vs.PanelCount))
        system_key = vs.SliderSystem
        show_hw = vs.ShowHardware
        finish = vs.HardwareFinish

        # --- Glass panels ---
        self._updatePanels(part_obj, vs, panel_count)

        # --- Handle ---
        if show_hw and vs.HandleType != "None":
            self._updateHandle(part_obj, vs)
        else:
            if self._hasChild(part_obj, "Handle"):
                self._removeChild(part_obj, "Handle")

        # --- Slider hardware ---
        if show_hw:
            self._updateSliderTrack(part_obj, vs, system_key)
            self._updateSliderFloorGuide(part_obj, vs, system_key)
            self._updateSliderRollers(part_obj, vs, system_key, panel_count)
            self._updateAntiLiftPins(part_obj, vs, system_key, panel_count)
        else:
            if self._hasChild(part_obj, "SliderTrack"):
                self._removeChild(part_obj, "SliderTrack")
            if self._hasChild(part_obj, "SliderFloorGuide"):
                self._removeChild(part_obj, "SliderFloorGuide")
            self._syncChildCount(part_obj, "SliderRoller", 0, SliderRollerChild)
            self._syncChildCount(part_obj, "AntiLiftPin", 0, AntiLiftPinChild)

        # --- Finish ---
        self._updateAllHardwareFinish(part_obj, finish)

        # --- Validation & calculated ---
        self._validateSliderSystem(vs, system_key)
        self._updateCalculatedProperties(vs)

    # ------------------------------------------------------------------
    # Panel management
    # ------------------------------------------------------------------

    def _updatePanels(self, part_obj, vs, panel_count):
        width = vs.Width.Value
        height = vs.Height.Value
        thickness = vs.Thickness.Value

        # Panel 1 always exists
        panel1 = self._getChild(part_obj, "Panel1")
        if panel1:
            panel1.Width = width
            panel1.Height = height
            panel1.Thickness = thickness
            if hasattr(panel1, "GlassType"):
                panel1.GlassType = vs.GlassType

        # Panel 2: add or remove based on panel count
        if panel_count == 2:
            if not self._hasChild(part_obj, "Panel2"):
                self._addChild(part_obj, "Panel2", GlassChild, _setupGlassVP)
            panel2 = self._getChild(part_obj, "Panel2")
            if panel2:
                panel2.Width = width
                panel2.Height = height
                panel2.Thickness = thickness
                if hasattr(panel2, "GlassType"):
                    panel2.GlassType = vs.GlassType
                overlap = vs.OverlapWidth.Value
                panel2.Placement = App.Placement(
                    App.Vector(width - overlap, thickness + 25, 0),
                    App.Rotation()
                )
        else:
            if self._hasChild(part_obj, "Panel2"):
                self._removeChild(part_obj, "Panel2")

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

        width = vs.Width.Value
        thickness = vs.Thickness.Value
        handle_height = min(vs.HandleHeight.Value, vs.Height.Value - 100)
        handle_offset = vs.HandleOffset.Value

        if vs.SlideDirection == "Right":
            x_pos = handle_offset
        else:
            x_pos = width - handle_offset

        child.Placement = App.Placement(
            App.Vector(x_pos, thickness / 2, handle_height), App.Rotation()
        )

    # ------------------------------------------------------------------
    # Slider track
    # ------------------------------------------------------------------

    def _updateSliderTrack(self, part_obj, vs, system_key):
        if not self._hasChild(part_obj, "SliderTrack"):
            self._addChild(
                part_obj, "SliderTrack", SliderTrackChild,
                lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
            )

        child = self._getChild(part_obj, "SliderTrack")
        if child is None:
            return

        track_length = _calculateTrackLength(vs)
        child.SliderSystem = system_key
        child.TrackLength = track_length

        # Tube support bracket at fixed panel junction
        if hasattr(child, "TubeSupportX"):
            width = vs.Width.Value
            if vs.SlideDirection == "Right":
                child.TubeSupportX = width - 50
            else:
                child.TubeSupportX = track_length / 2 + 50

        spec = SLIDER_SYSTEM_SPECS[system_key]
        dims = spec["dimensions"]
        height = vs.Height.Value
        thickness = vs.Thickness.Value
        if system_key == "duplo":
            track_y = -dims["fixed_panel_to_door_clearance"]
            track_z = -dims["door_fixed_height_diff"] + dims["lower_tube_to_fixed_panel"]
        elif system_key == "city_slider":
            track_w = dims["track_width"]
            track_h = dims["track_height"]
            track_y = -track_w/2 - dims["fixed_door_clearance_hd"]/2
            track_z = dims["door_top_deduction_hd"] - track_h
        else: #edge slider
            track_w = dims["track_width"]
            track_h = dims["track_height"]
            track_y = -dims["fixed_panel_door_clearance"]/2 - track_w/2
            track_z = -dims["track_center_from_top"] - track_h/2

        child.Placement = App.Placement(
            App.Vector(0, track_y, height + track_z), App.Rotation()
        )

    # ------------------------------------------------------------------
    # Floor guide
    # ------------------------------------------------------------------

    def _updateSliderFloorGuide(self, part_obj, vs, system_key):
        if not self._hasChild(part_obj, "SliderFloorGuide"):
            self._addChild(
                part_obj, "SliderFloorGuide", SliderFloorGuideChild,
                lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
            )

        child = self._getChild(part_obj, "SliderFloorGuide")
        if child is None:
            return

        thickness = vs.Thickness.Value
        guide_w = FLOOR_GUIDE_SPECS["width"]

        if vs.SlideDirection == "Right":
            x_pos = vs.Width.Value - FLOOR_GUIDE_SPECS["length"]
        else:
            x_pos = 0
        y_offset = thickness / 2 - guide_w / 2
        z_offset = -7

        child.Placement = App.Placement(
            App.Vector(x_pos, y_offset, z_offset), App.Rotation()
        )

    # ------------------------------------------------------------------
    # Rollers
    # ------------------------------------------------------------------

    def _updateSliderRollers(self, part_obj, vs, system_key, panel_count):
        roller_count = panel_count * 2
        self._syncChildCount(
            part_obj, "SliderRoller", roller_count, SliderRollerChild,
            lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
        )

        spec = SLIDER_SYSTEM_SPECS[system_key]
        dims = spec["dimensions"]
        width = vs.Width.Value
        height = vs.Height.Value
        thickness = vs.Thickness.Value

        idx = 1
        for panel_idx in range(panel_count):
            if panel_idx == 0:
                if system_key == "duplo":
                    hole_handle = dims["door_wheel_hole_from_handle_side"]
                    hole_fixed = dims["door_wheel_hole_from_fixed_side"]
                    if vs.SlideDirection == "Right":
                        x_positions = [hole_handle, width - hole_fixed]
                    else:
                        x_positions = [hole_fixed, width - hole_handle]
                elif system_key == "edge_slider":
                    from_side = dims["door_wheel_antilift_from_side"]
                    x_positions = [from_side, width - from_side]
                else:  # city_slider
                    from_side = dims["door_runner_hole_from_sides"]
                    x_positions = [from_side, width - from_side]
                if system_key in ("edge_slider", "city_slider"):
                    track_w = dims["track_width"]
                    y_offset = thickness / 2
                else:
                    y_offset = thickness / 2
            else:
                overlap = vs.OverlapWidth.Value
                base_x = width - overlap
                x_positions = [base_x + 20, base_x + width - 20]
                y_offset = thickness / 2 + thickness + 5

            if system_key == "duplo":
                z_pos = (height - dims["door_fixed_height_diff"] + dims["lower_tube_to_fixed_panel"]
                         + dims["tube_spacing_ctc"] / 2)
            elif system_key == "edge_slider":
                z_pos = height - dims["wheel_center_from_top"]
            else:
                z_pos = height - dims.get("wheel_center_from_top", 60)

            for x_pos in x_positions:
                child = self._getChild(part_obj, f"SliderRoller{idx}")
                if child:
                    child.SliderSystem = system_key
                    child.Placement = App.Placement(
                        App.Vector(x_pos, y_offset, z_pos), App.Rotation()
                    )
                idx += 1

    # ------------------------------------------------------------------
    # Anti-lift pins
    # ------------------------------------------------------------------

    def _updateAntiLiftPins(self, part_obj, vs, system_key, panel_count):
        if system_key != "edge_slider":
            self._syncChildCount(part_obj, "AntiLiftPin", 0, AntiLiftPinChild)
            return

        spec = SLIDER_SYSTEM_SPECS[system_key]
        dims = spec["dimensions"]
        pin_count = panel_count * 2
        self._syncChildCount(
            part_obj, "AntiLiftPin", pin_count, AntiLiftPinChild,
            lambda obj: _setupHardwareVP(obj, vs.HardwareFinish)
        )

        width = vs.Width.Value
        height = vs.Height.Value
        from_side = dims["door_wheel_antilift_from_side"]
        ctc_offset = dims["wheel_ctc_to_antilift"]
        track_w = dims["track_width"]
        y_offset = -6 - track_w / 2
        wheel_z = height - dims["wheel_center_from_top"]
        z_pos = wheel_z - ctc_offset

        pin_xs = [from_side, width - from_side]

        idx = 1
        for x_pos in pin_xs:
            child = self._getChild(part_obj, f"AntiLiftPin{idx}")
            if child:
                child.Placement = App.Placement(
                    App.Vector(x_pos, y_offset, z_pos), App.Rotation()
                )
            idx += 1

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validateSliderSystem(self, vs, system_key):
        from freecad.ShowerDesigner.Data.HardwareSpecs import validateSliderSystem

        width = vs.Width.Value
        thickness = vs.Thickness.Value

        area = (width / 1000.0) * (vs.Height.Value / 1000.0)
        thickness_key = f"{int(thickness)}mm"
        if thickness_key in GLASS_SPECS:
            weight = area * GLASS_SPECS[thickness_key]["weight_kg_m2"]
        else:
            weight = area * 2.5 * thickness

        valid, msg = validateSliderSystem(system_key, width, weight, thickness)
        if hasattr(vs, "SystemValidation"):
            vs.SystemValidation = msg
        if not valid:
            App.Console.PrintWarning(f"Slider system warning: {msg}\n")

    # ------------------------------------------------------------------
    # Calculated properties
    # ------------------------------------------------------------------

    def _updateCalculatedProperties(self, vs):
        try:
            width = vs.Width.Value
            height = vs.Height.Value
            thickness = vs.Thickness.Value
            panel_count = max(1, min(2, vs.PanelCount))
            overlap = vs.OverlapWidth.Value

            # Glass weight & area
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

            # Track length
            track_length = _calculateTrackLength(vs)
            if hasattr(vs, "TrackLength"):
                vs.TrackLength = track_length

            # Track height
            system_key = vs.SliderSystem
            spec = SLIDER_SYSTEM_SPECS.get(system_key)
            if spec and hasattr(vs, "TrackHeight"):
                dims = spec["dimensions"]
                if system_key == "duplo":
                    vs.TrackHeight = dims["tube_diameter"]
                else:
                    vs.TrackHeight = dims["track_height"]

            # Travel distance & opening width
            if panel_count == 1:
                travel = width
                opening = width
            else:
                travel = width - overlap
                opening = width - overlap
            if hasattr(vs, "TravelDistance"):
                vs.TravelDistance = travel
            if hasattr(vs, "OpeningWidth"):
                vs.OpeningWidth = opening

        except Exception as e:
            App.Console.PrintWarning(
                f"Error updating calculated properties: {e}\n"
            )

    def assemblyOnChanged(self, part_obj, prop):
        pass


# ======================================================================
# Helpers
# ======================================================================

def _calculateTrackLength(vs):
    """Calculate total track length based on panel configuration."""
    width = vs.Width.Value
    panel_count = max(1, min(2, vs.PanelCount))
    clearance = 0

    if panel_count == 1:
        return width * 2 + clearance * 2
    else:
        overlap = vs.OverlapWidth.Value
        return width * 3 - overlap + clearance * 2


# ======================================================================
# Factory function
# ======================================================================

def createSlidingDoor(name="SlidingDoor"):
    """
    Create a new sliding door assembly in the active document.

    Creates a single App::Part containing glass panel(s), handle,
    slider track, rollers, anti-lift pins, and floor guide.

    Args:
        name: Name for the assembly (default: "SlidingDoor")

    Returns:
        App::Part assembly object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    part = doc.addObject("App::Part", name)
    SlidingDoorAssembly(part)

    doc.recompute()
    App.Console.PrintMessage(f"Sliding door '{name}' created\n")
    return part
