# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Standalone handle hardware model for shower enclosures.

Provides a Handle Part::FeaturePython object and a shared
createHandleShape() function that loads handle geometry from
pre-exported .brep files in the Handle/ directory (one per model).

The .brep files are generated once from their source .FCStd files using
the export_handle_breps() utility below.  They are committed to version
control so that runtime loading does not require opening any FreeCAD
document.
"""

import os

import FreeCAD as App
import Part
from freecad.ShowerDesigner.Data.HardwareSpecs import (
    HANDLE_SPECS,
    HANDLE_PLACEMENT_DEFAULTS,
    HARDWARE_FINISHES,
)

# Directory containing handle model files (.brep and .FCStd)
_HANDLE_MODEL_DIR = os.path.join(os.path.dirname(__file__), "Handle")

# Cache loaded shapes to avoid re-reading .brep files on every recompute
_shape_cache = {}


def _loadHandleShape(model_file):
    """Load and cache a handle shape from a .brep file.

    The .brep filename is derived from the model_file spec key by replacing
    the .FCStd extension with .brep.  Loading via Part.Shape.read() is
    fast and does not open a FreeCAD document, so it never disturbs
    App.ActiveDocument.
    """
    brep_file = os.path.splitext(model_file)[0] + ".brep"

    if brep_file in _shape_cache:
        return _shape_cache[brep_file].copy()

    filepath = os.path.join(_HANDLE_MODEL_DIR, brep_file)
    if not os.path.isfile(filepath):
        App.Console.PrintError(
            f"Handle .brep model not found: {filepath}\n"
            f"Run Handle.export_handle_breps() once to generate it.\n"
        )
        return None

    shape = Part.Shape()
    shape.read(filepath)
    if shape.isNull():
        App.Console.PrintError(f"Failed to read shape from {filepath}\n")
        return None

    _shape_cache[brep_file] = shape.copy()
    return shape.copy()


def createHandleShape(handle_type, length=None, position=None):
    """
    Create a handle shape at the given position.

    Loads geometry from pre-exported .brep files in the Handle/ directory.

    Args:
        handle_type: Key from HANDLE_SPECS (e.g. "mushroom_knob_b2b")
        length: Unused, kept for API compatibility.
        position: App.Vector for handle center. Defaults to origin.

    Returns:
        Part.Shape or None if handle_type is "None" or unknown
    """
    if handle_type == "None" or handle_type not in HANDLE_SPECS:
        return None

    spec = HANDLE_SPECS[handle_type]
    model_file = spec["model_file"]
    shape = _loadHandleShape(model_file)

    if shape is None:
        return None

    if position is not None:
        shape.translate(position)

    return shape


def export_handle_breps():
    """
    One-time utility: export all handle .FCStd models to .brep files.

    Call this from the FreeCAD Python console whenever the source
    .FCStd files are updated.  The generated .brep files should then
    be committed to version control.

    Example:
        from freecad.ShowerDesigner.Models.Handle import export_handle_breps
        export_handle_breps()
    """
    previous_doc = App.ActiveDocument
    exported = []

    for key, spec in HANDLE_SPECS.items():
        model_file = spec["model_file"]
        fcstd_path = os.path.join(_HANDLE_MODEL_DIR, model_file)
        brep_path = os.path.splitext(fcstd_path)[0] + ".brep"

        if not os.path.isfile(fcstd_path):
            App.Console.PrintWarning(f"Source not found, skipping: {fcstd_path}\n")
            continue

        try:
            doc = App.openDocument(fcstd_path, hidden=True)

            best_shape = None
            for obj in doc.Objects:
                if obj.TypeId == "PartDesign::Body":
                    if hasattr(obj, "Shape") and not obj.Shape.isNull() and obj.Shape.Solids:
                        best_shape = obj.Shape.copy()
                        break

            if best_shape is None:
                for obj in doc.Objects:
                    if (hasattr(obj, "Shape") and not obj.Shape.isNull()
                            and obj.Shape.Solids
                            and obj.TypeId not in ("App::Line", "App::Plane", "App::Point")):
                        if best_shape is None or len(obj.Shape.Solids) > len(best_shape.Solids):
                            best_shape = obj.Shape.copy()

            App.closeDocument(doc.Name)
            if previous_doc is not None:
                try:
                    App.setActiveDocument(previous_doc.Name)
                except Exception:
                    pass

            if best_shape is not None and best_shape.Solids:
                best_shape.exportBrep(brep_path)
                App.Console.PrintMessage(f"Exported: {brep_path}\n")
                exported.append(brep_path)
            else:
                App.Console.PrintError(f"No solid found in {fcstd_path}\n")

        except Exception as e:
            App.Console.PrintError(f"Error exporting {model_file}: {e}\n")

    return exported


class Handle:
    """
    Parametric standalone handle hardware object.

    Properties:
        HandleType: Enum — mushroom_knob_b2b, pull_handle_round, flush_handle_with_plate
        HandleLength: Length (kept for compatibility)
        Finish: Hardware finish
    """

    def __init__(self, obj):
        obj.Proxy = self

        obj.addProperty(
            "App::PropertyEnumeration",
            "HandleType",
            "Handle",
            "Type of handle"
        )
        obj.HandleType = list(HANDLE_SPECS.keys())
        obj.HandleType = "mushroom_knob_b2b"

        obj.addProperty(
            "App::PropertyLength",
            "HandleLength",
            "Handle",
            "Length of bar/pull handle"
        ).HandleLength = 300

        obj.addProperty(
            "App::PropertyEnumeration",
            "Finish",
            "Handle",
            "Hardware finish"
        )
        obj.Finish = HARDWARE_FINISHES[:]
        obj.Finish = "Chrome"

        obj.addProperty(
            "App::PropertyVector",
            "Position",
            "Placement",
            "Position of the handle"
        ).Position = App.Vector(0, 0, 0)

        obj.addProperty(
            "App::PropertyAngle",
            "Rotation",
            "Placement",
            "Rotation angle around Z-axis"
        ).Rotation = 0

    def execute(self, obj):
        handle_type = obj.HandleType
        length = obj.HandleLength.Value

        shape = createHandleShape(handle_type, length, obj.Position)
        if shape is None:
            # Fallback to a small marker shape
            shape = Part.makeSphere(5, obj.Position)

        obj.Shape = shape
        obj.Placement.Base = obj.Position
        obj.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), obj.Rotation)

    def onChanged(self, obj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


def createHandle(name="Handle"):
    """
    Create a standalone handle object in the active document.

    Args:
        name: Name for the object

    Returns:
        FreeCAD document object
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("ShowerDesign")

    obj = doc.addObject("Part::FeaturePython", name)
    Handle(obj)

    if App.GuiUp:
        obj.ViewObject.Proxy = 0

    doc.recompute()
    App.Console.PrintMessage(f"Handle '{name}' created\n")
    return obj
