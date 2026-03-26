# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
STEP/STL/3MF batch export dialog.

Provides a Qt dialog for exporting enclosure assemblies and individual
parts to common CAD interchange formats.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont
    from PySide6.QtWidgets import (
        QAbstractItemView,
        QCheckBox,
        QComboBox,
        QDialog,
        QFileDialog,
        QGroupBox,
        QHBoxLayout,
        QHeaderView,
        QLabel,
        QLineEdit,
        QMessageBox,
        QPushButton,
        QTableWidget,
        QTableWidgetItem,
        QVBoxLayout,
    )
else:
    from PySide.QtCore import Qt
    from PySide.QtGui import QFont
    from PySide.QtWidgets import (
        QAbstractItemView,
        QCheckBox,
        QComboBox,
        QDialog,
        QFileDialog,
        QGroupBox,
        QHBoxLayout,
        QHeaderView,
        QLabel,
        QLineEdit,
        QMessageBox,
        QPushButton,
        QTableWidget,
        QTableWidgetItem,
        QVBoxLayout,
    )

import FreeCAD as App
import Part


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FORMATS = {
    "STEP (.step)": ".step",
    "STL (.stl)": ".stl",
    "3MF (.3mf)": ".3mf",
    "IGES (.iges)": ".iges",
    "OBJ (.obj)": ".obj",
}


def _sanitize(name: str) -> str:
    """Replace characters that are invalid in file paths."""
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in name)


def _autoName(obj, parent_label: str | None = None) -> str:
    """Generate a descriptive file stem from an object.

    Pattern: {Enclosure}_{Component}_{WxHxT}
    Falls back to the object Label if dimensions aren't available.
    """
    parts: list[str] = []
    if parent_label:
        parts.append(_sanitize(parent_label))
    parts.append(_sanitize(obj.Label))

    # Try to pull dimensions from a sibling VarSet
    vs = _findVarSet(obj)
    if vs:
        w = getattr(vs, "Width", None)
        h = getattr(vs, "Height", None)
        t = getattr(vs, "Thickness", None) or getattr(vs, "GlassThickness", None)
        dims = []
        if w:
            dims.append(f"{w.Value:.0f}")
        if h:
            dims.append(f"{h.Value:.0f}")
        if t:
            dims.append(f"{t.Value:.0f}")
        if dims:
            parts.append("x".join(dims))

    return "_".join(parts)


def _findVarSet(obj):
    """Find a VarSet sibling inside the same App::Part container."""
    parent = None
    for p in getattr(obj, "InList", []):
        if p.TypeId == "App::Part":
            parent = p
            break
    if parent is None and obj.TypeId == "App::Part":
        parent = obj
    if parent is None:
        return None
    for child in getattr(parent, "Group", []):
        if child.TypeId == "App::VarSet":
            return child
    return None


def collectExportables(targets: list) -> list[dict]:
    """Walk assembly trees and collect objects with exportable shapes.

    Returns a list of dicts:
        {"obj": FreeCAD object, "label": display name, "parent": parent label or ""}
    """
    results = []
    seen = set()

    def _walk(obj, parent_label=""):
        if obj.Name in seen:
            return
        seen.add(obj.Name)

        if obj.TypeId == "App::Part":
            for child in getattr(obj, "Group", []):
                if child.TypeId == "App::VarSet":
                    continue
                # Skip hidden controller objects
                if child.Label.startswith("_"):
                    continue
                _walk(child, parent_label=obj.Label)
            # Also offer the fused assembly itself
            shape = getattr(obj, "Shape", None)
            if shape and not shape.isNull() and shape.Volume > 0:
                results.append({
                    "obj": obj,
                    "label": obj.Label,
                    "parent": parent_label,
                    "is_assembly": True,
                })
        else:
            shape = getattr(obj, "Shape", None)
            if shape and not shape.isNull() and shape.Volume > 0:
                results.append({
                    "obj": obj,
                    "label": obj.Label,
                    "parent": parent_label,
                    "is_assembly": False,
                })

    for t in targets:
        _walk(t)
    return results


def exportShape(obj, filepath: str, fmt_ext: str):
    """Export a single object's shape to the given file path."""
    shape = obj.Shape
    if shape is None or shape.isNull():
        raise ValueError(f"Object '{obj.Label}' has no valid shape.")

    ext = fmt_ext.lower()
    if ext == ".step":
        shape.exportStep(filepath)
    elif ext == ".iges":
        shape.exportIges(filepath)
    elif ext == ".stl":
        shape.exportStl(filepath)
    elif ext == ".3mf":
        Part.export([obj], filepath)
    elif ext == ".obj":
        Part.export([obj], filepath)
    else:
        raise ValueError(f"Unsupported export format: {ext}")


# ---------------------------------------------------------------------------
# Dialog
# ---------------------------------------------------------------------------

_TABLE_HEADERS = ["Export", "Parent", "Component", "Type"]


class ExportDialog(QDialog):
    """Modal dialog for batch-exporting enclosure parts."""

    def __init__(self, targets: list, parent=None):
        super().__init__(parent)
        self._targets = targets
        self._exportables = collectExportables(targets)
        self.setWindowTitle("Export Parts")
        self.setMinimumSize(750, 500)
        self._buildUI()
        self._populateTable()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _buildUI(self):
        layout = QVBoxLayout(self)

        # --- Options group ---
        opts = QGroupBox("Export Options")
        opts_layout = QVBoxLayout(opts)

        # Format
        fmt_row = QHBoxLayout()
        fmt_row.addWidget(QLabel("Format:"))
        self._fmtCombo = QComboBox()
        self._fmtCombo.addItems(list(_FORMATS.keys()))
        fmt_row.addWidget(self._fmtCombo)
        fmt_row.addStretch()
        opts_layout.addLayout(fmt_row)

        # Output directory
        dir_row = QHBoxLayout()
        dir_row.addWidget(QLabel("Output:"))
        self._dirEdit = QLineEdit()
        default_dir = os.path.expanduser("~/ShowerDesigner_Export")
        self._dirEdit.setText(default_dir)
        dir_row.addWidget(self._dirEdit)
        self._browseBtn = QPushButton("Browse...")
        self._browseBtn.clicked.connect(self._onBrowse)
        dir_row.addWidget(self._browseBtn)
        opts_layout.addLayout(dir_row)

        # Prefix
        prefix_row = QHBoxLayout()
        prefix_row.addWidget(QLabel("Prefix:"))
        self._prefixEdit = QLineEdit()
        self._prefixEdit.setPlaceholderText("Optional filename prefix")
        prefix_row.addWidget(self._prefixEdit)
        prefix_row.addStretch()
        opts_layout.addLayout(prefix_row)

        layout.addWidget(opts)

        # --- Parts table ---
        self._table = QTableWidget(0, len(_TABLE_HEADERS))
        self._table.setHorizontalHeaderLabels(_TABLE_HEADERS)
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        header = self._table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        layout.addWidget(self._table)

        # --- Select all / none ---
        sel_row = QHBoxLayout()
        self._selectAllBtn = QPushButton("Select All")
        self._selectAllBtn.clicked.connect(self._onSelectAll)
        sel_row.addWidget(self._selectAllBtn)
        self._selectNoneBtn = QPushButton("Select None")
        self._selectNoneBtn.clicked.connect(self._onSelectNone)
        sel_row.addWidget(self._selectNoneBtn)
        sel_row.addStretch()
        sel_row.addWidget(QLabel(""))
        self._countLabel = QLabel("")
        font = QFont()
        font.setBold(True)
        self._countLabel.setFont(font)
        sel_row.addWidget(self._countLabel)
        layout.addLayout(sel_row)

        # --- Action buttons ---
        btn_row = QHBoxLayout()
        self._exportBtn = QPushButton("Export")
        self._exportBtn.clicked.connect(self._onExport)
        btn_row.addWidget(self._exportBtn)
        btn_row.addStretch()
        self._closeBtn = QPushButton("Close")
        self._closeBtn.clicked.connect(self.reject)
        btn_row.addWidget(self._closeBtn)
        layout.addLayout(btn_row)

    # ------------------------------------------------------------------
    # Table population
    # ------------------------------------------------------------------

    def _populateTable(self):
        self._checkboxes: list[QCheckBox] = []
        self._table.setRowCount(len(self._exportables))
        for row, entry in enumerate(self._exportables):
            cb = QCheckBox()
            cb.setChecked(True)
            cb.stateChanged.connect(self._updateCount)
            self._checkboxes.append(cb)
            self._table.setCellWidget(row, 0, cb)

            parent_item = QTableWidgetItem(entry["parent"])
            parent_item.setFlags(parent_item.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(row, 1, parent_item)

            label_item = QTableWidgetItem(entry["label"])
            label_item.setFlags(label_item.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(row, 2, label_item)

            type_str = "Assembly" if entry.get("is_assembly") else "Part"
            type_item = QTableWidgetItem(type_str)
            type_item.setFlags(type_item.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(row, 3, type_item)

        self._updateCount()

    def _updateCount(self, _=None):
        checked = sum(1 for cb in self._checkboxes if cb.isChecked())
        self._countLabel.setText(f"{checked} of {len(self._exportables)} selected")

    # ------------------------------------------------------------------
    # Button handlers
    # ------------------------------------------------------------------

    def _onBrowse(self):
        path = QFileDialog.getExistingDirectory(
            self, "Select Export Directory", self._dirEdit.text()
        )
        if path:
            self._dirEdit.setText(path)

    def _onSelectAll(self):
        for cb in self._checkboxes:
            cb.setChecked(True)

    def _onSelectNone(self):
        for cb in self._checkboxes:
            cb.setChecked(False)

    def _onExport(self):
        fmt_key = self._fmtCombo.currentText()
        ext = _FORMATS[fmt_key]
        out_dir = self._dirEdit.text().strip()
        prefix = self._prefixEdit.text().strip()

        if not out_dir:
            QMessageBox.warning(self, "Export", "Please specify an output directory.")
            return

        # Collect checked items
        selected = []
        for i, entry in enumerate(self._exportables):
            if self._checkboxes[i].isChecked():
                selected.append(entry)

        if not selected:
            QMessageBox.warning(self, "Export", "No parts selected for export.")
            return

        # Create output directory
        os.makedirs(out_dir, exist_ok=True)

        exported = []
        errors = []
        for entry in selected:
            stem = _autoName(entry["obj"], entry["parent"] or None)
            if prefix:
                stem = f"{_sanitize(prefix)}_{stem}"
            filepath = os.path.join(out_dir, stem + ext)

            try:
                exportShape(entry["obj"], filepath, ext)
                exported.append(filepath)
                App.Console.PrintMessage(f"Exported: {filepath}\n")
            except Exception as e:
                errors.append(f"{entry['label']}: {e}")
                App.Console.PrintError(f"Export failed for {entry['label']}: {e}\n")

        # Write manifest
        if exported:
            manifest_path = os.path.join(out_dir, "export_manifest.txt")
            with open(manifest_path, "w", encoding="utf-8") as f:
                f.write(f"ShowerDesigner Export Manifest\n")
                f.write(f"Format: {fmt_key}\n")
                f.write(f"Files: {len(exported)}\n")
                f.write("-" * 40 + "\n")
                for fp in exported:
                    f.write(os.path.basename(fp) + "\n")
            App.Console.PrintMessage(f"Manifest written: {manifest_path}\n")

        # Summary
        msg = f"Exported {len(exported)} file(s) to:\n{out_dir}"
        if errors:
            msg += f"\n\n{len(errors)} error(s):\n" + "\n".join(errors)
            QMessageBox.warning(self, "Export Complete", msg)
        else:
            QMessageBox.information(self, "Export Complete", msg)
            self.accept()
