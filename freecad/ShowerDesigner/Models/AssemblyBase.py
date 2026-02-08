# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Base class for assembly controllers (App::Part proxies).

An assembly controller manages an App::Part container that holds:
  - A hidden Part::FeaturePython controller (this class's Proxy target)
  - An App::VarSet with user-facing properties
  - Child Part::FeaturePython objects (glass panels, hardware)

Because App::Part does not support the Proxy attribute, the assembly
logic lives on a hidden controller Part::FeaturePython inside the Part.
The controller stores:
  - _AssemblyName (PropertyString) — parent Part name; must be a string,
    NOT a PropertyLink, because linking a child to its parent creates a
    cyclic dependency in FreeCAD's dependency graph.
  - _VarSetLink (PropertyLink) — sibling VarSet; safe as a link because
    it's a sibling relationship, and it ensures FreeCAD recomputes the
    controller when VarSet properties change.

Subclasses implement assemblyExecute() to define
the specific assembly behavior.
"""

import FreeCAD as App


class AssemblyController:
    """
    Base proxy class for a controller Part::FeaturePython inside an
    App::Part assembly container.

    Provides shared logic for managing VarSet, creating/removing child
    objects, and synchronizing hardware finish across children.
    """

    def __init__(self, part_obj):
        self._manifest = {}

        # Create hidden controller inside the App::Part
        doc = part_obj.Document
        ctrl = doc.addObject("Part::FeaturePython", "_Controller")
        ctrl.Proxy = self

        # Store parent name as string (NOT a Link, to avoid cyclic dependency)
        ctrl.addProperty(
            "App::PropertyString", "_AssemblyName", "Internal",
            "Parent assembly object name"
        )
        ctrl._AssemblyName = part_obj.Name
        ctrl.setEditorMode("_AssemblyName", 2)  # Hidden

        # VarSet link for dependency tracking (populated by _getOrCreateVarSet).
        # This is a sibling link (controller → VarSet), NOT a parent link,
        # so it does not create cyclic dependencies.
        ctrl.addProperty(
            "App::PropertyLink", "_VarSetLink", "Internal",
            "VarSet dependency link"
        )
        ctrl.setEditorMode("_VarSetLink", 2)  # Hidden

        # Hide controller from 3D view
        if App.GuiUp:
            ctrl.ViewObject.Proxy = 0
            ctrl.ViewObject.Visibility = False

        part_obj.addObject(ctrl)
        self._manifest["_Controller"] = ctrl.Name

    # ------------------------------------------------------------------
    # VarSet management
    # ------------------------------------------------------------------

    def _getOrCreateVarSet(self, part_obj):
        """Find or create the App::VarSet child inside this Part."""
        for child in part_obj.Group:
            if child.TypeId == "App::VarSet":
                self._linkVarSet(part_obj, child)
                return child

        doc = part_obj.Document
        vs = doc.addObject("App::VarSet", "VarSet")
        part_obj.addObject(vs)
        self._manifest["VarSet"] = vs.Name
        self._linkVarSet(part_obj, vs)
        return vs

    def _linkVarSet(self, part_obj, vs):
        """Link the VarSet to the controller for dependency tracking."""
        ctrl_name = self._manifest.get("_Controller")
        if ctrl_name:
            ctrl = part_obj.Document.getObject(ctrl_name)
            if ctrl and hasattr(ctrl, "_VarSetLink"):
                ctrl._VarSetLink = vs

    def _getVarSet(self, part_obj):
        """Get the VarSet child, or None if it doesn't exist yet."""
        # Primary: follow the PropertyLink on the controller
        ctrl_name = self._manifest.get("_Controller")
        if ctrl_name:
            ctrl = part_obj.Document.getObject(ctrl_name)
            if ctrl and hasattr(ctrl, "_VarSetLink"):
                vs = ctrl._VarSetLink
                if vs is not None:
                    return vs
        # Fallback: manifest name
        name = self._manifest.get("VarSet")
        if name:
            obj = part_obj.Document.getObject(name)
            if obj:
                return obj
        # Final fallback: search by type
        for child in part_obj.Group:
            if child.TypeId == "App::VarSet":
                self._manifest["VarSet"] = child.Name
                return child
        return None

    # ------------------------------------------------------------------
    # Child object management
    # ------------------------------------------------------------------

    def _addChild(self, part_obj, role, proxy_class, vp_setup_fn=None,
                  **proxy_kwargs):
        """
        Create a Part::FeaturePython child, attach its proxy and VP,
        and add it to the Part container.

        Args:
            part_obj: The App::Part container
            role: Display name / role for the child (e.g. "Glass", "WallClamp1")
            proxy_class: Class to instantiate as the child's Proxy
            vp_setup_fn: Optional callable(obj, **kw) to set up the ViewProvider
            **proxy_kwargs: Extra keyword args passed to proxy_class.__init__

        Returns:
            The newly created child object
        """
        doc = part_obj.Document
        child = doc.addObject("Part::FeaturePython", role)
        proxy_class(child, **proxy_kwargs)

        if App.GuiUp and vp_setup_fn is not None:
            vp_setup_fn(child)

        part_obj.addObject(child)
        self._manifest[role] = child.Name
        return child

    def _removeChild(self, part_obj, role):
        """Remove a child object by its role name."""
        name = self._manifest.pop(role, None)
        if name is None:
            return
        doc = part_obj.Document
        obj = doc.getObject(name)
        if obj is None:
            return
        part_obj.removeObject(obj)
        doc.removeObject(name)

    def _getChild(self, part_obj, role):
        """Get a child object by its role name, or None."""
        name = self._manifest.get(role)
        if name:
            return part_obj.Document.getObject(name)
        return None

    def _hasChild(self, part_obj, role):
        """Check whether a child with this role currently exists."""
        name = self._manifest.get(role)
        if name is None:
            return False
        return part_obj.Document.getObject(name) is not None

    def _syncChildCount(self, part_obj, prefix, desired_count,
                        proxy_class, vp_setup_fn=None, **proxy_kwargs):
        """
        Ensure exactly `desired_count` children whose role starts with
        `prefix` exist. Roles are named prefix1, prefix2, ...

        Adds missing children and removes excess ones.
        """
        existing = sorted(
            [k for k in self._manifest if k.startswith(prefix)
             and k[len(prefix):].isdigit()]
        )
        current_count = len(existing)

        # Remove excess (from the end)
        for i in range(current_count, desired_count, -1):
            self._removeChild(part_obj, f"{prefix}{i}")

        # Add missing
        for i in range(current_count + 1, desired_count + 1):
            self._addChild(
                part_obj, f"{prefix}{i}",
                proxy_class, vp_setup_fn,
                **proxy_kwargs
            )

    # ------------------------------------------------------------------
    # Hardware finish propagation
    # ------------------------------------------------------------------

    def _updateAllHardwareFinish(self, part_obj, finish):
        """
        Update the finish on all hardware ViewProviders in this assembly.
        Skips the VarSet, controller, and any glass children.
        """
        if not App.GuiUp:
            return
        from freecad.ShowerDesigner.Models.HardwareViewProvider import (
            HardwareViewProvider,
        )
        for child in part_obj.Group:
            if child.TypeId == "App::VarSet":
                continue
            if child.Label == "_Controller":
                continue
            vp = getattr(child, "ViewObject", None)
            if vp is None:
                continue
            proxy = getattr(vp, "Proxy", None)
            if isinstance(proxy, HardwareViewProvider):
                proxy.updateFinish(vp, finish)

    # ------------------------------------------------------------------
    # FreeCAD callbacks (on the controller Part::FeaturePython)
    # ------------------------------------------------------------------

    def execute(self, obj):
        """
        Called by FreeCAD on the controller Part::FeaturePython.
        Extracts the parent App::Part and delegates to assemblyExecute(),
        then recomputes all children so their shapes reflect updated properties.
        """
        import Part
        obj.Shape = Part.Compound([])  # Controller has no visible geometry

        assembly_name = getattr(obj, "_AssemblyName", "")
        if not assembly_name:
            return
        part_obj = obj.Document.getObject(assembly_name)
        if part_obj is None:
            return
        self.assemblyExecute(part_obj)
        self._recomputeChildren(part_obj)

    def _recomputeChildren(self, part_obj):
        """Force recompute of all children after assemblyExecute().

        Children created or modified during assemblyExecute() won't be
        recomputed in the same document recompute cycle, so we explicitly
        trigger their execute() here to generate/update their shapes.
        For nested App::Part assemblies, recurse into their children so
        nested controllers also fire.
        """
        ctrl_name = self._manifest.get("_Controller")
        for child in part_obj.Group:
            if child.TypeId == "App::VarSet":
                continue
            if child.Name == ctrl_name:
                continue
            if child.TypeId == "App::Part":
                # Nested assembly — recompute its children so its
                # controller fires assemblyExecute + _recomputeChildren
                for grandchild in child.Group:
                    if grandchild.TypeId != "App::VarSet":
                        grandchild.recompute()
            else:
                child.recompute()

    def assemblyExecute(self, part_obj):
        """Override in subclasses to implement assembly logic."""
        pass

    def onChanged(self, obj, prop):
        """Called by FreeCAD when a controller property changes."""
        if prop in ("_AssemblyName", "_VarSetLink", "Shape"):
            return
        assembly_name = getattr(obj, "_AssemblyName", "")
        if not assembly_name:
            return
        part_obj = obj.Document.getObject(assembly_name)
        if part_obj is None:
            return
        self.assemblyOnChanged(part_obj, prop)

    def assemblyOnChanged(self, part_obj, prop):
        """Override in subclasses if needed."""
        pass

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def __getstate__(self):
        return {"manifest": self._manifest}

    def __setstate__(self, state):
        if state:
            self._manifest = state.get("manifest", {})
        else:
            self._manifest = {}
