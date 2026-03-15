# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Cut List / Bill of Materials dialog.

Displays extracted BOM items in a sortable table with copy-to-clipboard
and CSV export functionality.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtCore import Qt, QSortFilterProxyModel
    from PySide6.QtGui import QFont
    from PySide6.QtWidgets import (
        QAbstractItemView,
        QApplication,
        QDialog,
        QFileDialog,
        QHBoxLayout,
        QHeaderView,
        QLabel,
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
        QApplication,
        QDialog,
        QFileDialog,
        QHBoxLayout,
        QHeaderView,
        QLabel,
        QPushButton,
        QTableWidget,
        QTableWidgetItem,
        QVBoxLayout,
    )

import FreeCAD as App

from freecad.ShowerDesigner.Data.CutList import CutListItem, toCSV

_HEADERS = [
    "Category",
    "Component",
    "Description",
    "Product Code",
    "Width (mm)",
    "Height (mm)",
    "Qty",
    "Unit",
    "Notes",
]


class CutListDialog(QDialog):
    """Modal dialog showing a cut list / BOM table."""

    def __init__(self, items: list[CutListItem], parent=None):
        super().__init__(parent)
        self._items = items
        self.setWindowTitle("Cut List / Bill of Materials")
        self.setMinimumSize(900, 500)
        self._buildUI()
        self._populateTable()

    def _buildUI(self):
        layout = QVBoxLayout(self)

        # Summary label
        total_qty = sum(item.quantity for item in self._items)
        unique = len(self._items)
        self._summaryLabel = QLabel(
            f"{unique} line items, {total_qty} total pieces"
        )
        font = QFont()
        font.setBold(True)
        self._summaryLabel.setFont(font)
        layout.addWidget(self._summaryLabel)

        # Table
        self._table = QTableWidget(len(self._items), len(_HEADERS))
        self._table.setHorizontalHeaderLabels(_HEADERS)
        self._table.setAlternatingRowColors(True)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setSortingEnabled(True)
        header = self._table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        layout.addWidget(self._table)

        # Buttons
        btn_layout = QHBoxLayout()

        self._copyBtn = QPushButton("Copy to Clipboard")
        self._copyBtn.clicked.connect(self._onCopy)
        btn_layout.addWidget(self._copyBtn)

        self._exportBtn = QPushButton("Export CSV...")
        self._exportBtn.clicked.connect(self._onExportCSV)
        btn_layout.addWidget(self._exportBtn)

        btn_layout.addStretch()

        self._closeBtn = QPushButton("Close")
        self._closeBtn.clicked.connect(self.accept)
        btn_layout.addWidget(self._closeBtn)

        layout.addLayout(btn_layout)

    def _populateTable(self):
        self._table.setSortingEnabled(False)
        for row, item in enumerate(self._items):
            cells = [
                item.category,
                item.component,
                item.description,
                item.product_code,
                f"{item.width:.0f}" if item.width else "",
                f"{item.height:.0f}" if item.height else "",
                str(item.quantity),
                item.unit,
                item.notes,
            ]
            for col, text in enumerate(cells):
                tw = QTableWidgetItem(text)
                # Right-align numeric columns (width, height, qty)
                if col in (4, 5, 6):
                    tw.setTextAlignment(
                        int(Qt.AlignRight) | int(Qt.AlignVCenter)
                    )
                    # Store numeric value for proper sorting
                    try:
                        tw.setData(Qt.UserRole, float(text) if text else 0.0)
                    except ValueError:
                        pass
                self._table.setItem(row, col, tw)
        self._table.setSortingEnabled(True)

    def _onCopy(self):
        csv_text = toCSV(self._items)
        clipboard = QApplication.clipboard()
        clipboard.setText(csv_text)
        App.Console.PrintMessage("Cut list CSV copied to clipboard.\n")
        self._copyBtn.setText("Copied!")
        # Reset button text after a moment — use a single-shot timer
        try:
            from PySide.QtCore import QTimer
        except ImportError:
            from PySide6.QtCore import QTimer
        QTimer.singleShot(1500, lambda: self._copyBtn.setText("Copy to Clipboard"))

    def _onExportCSV(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Cut List as CSV",
            os.path.expanduser("~/ShowerDesigner_CutList.csv"),
            "CSV Files (*.csv);;All Files (*)",
        )
        if not path:
            return
        csv_text = toCSV(self._items)
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write(csv_text)
        App.Console.PrintMessage(f"Cut list exported to {path}\n")
