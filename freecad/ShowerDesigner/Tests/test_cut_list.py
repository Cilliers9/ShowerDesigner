# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for Cut List / Bill of Materials.

Pure data tests (no FreeCAD required) plus integration tests.

Run:
    pytest freecad/ShowerDesigner/Tests/test_cut_list.py
"""

import sys
sys.path.insert(
    0, r"C:\Users\tclou\AppData\Roaming\FreeCAD\v1-1\Mod\ShowerDesigner"
)

from freecad.ShowerDesigner.Data.CutList import (
    CutListItem,
    aggregateItems,
    toCSV,
    toConsoleTable,
    toTable,
)


# ======================================================================
# Pure data tests — no FreeCAD required
# ======================================================================


class TestCutListItem:
    """Test CutListItem dataclass defaults."""

    def test_defaults(self):
        item = CutListItem(
            category="Glass",
            component="Test Panel",
            description="Clear 10mm",
        )
        assert item.product_code == ""
        assert item.width == 0.0
        assert item.height == 0.0
        assert item.quantity == 1
        assert item.unit == "pc"
        assert item.notes == ""

    def test_full_construction(self):
        item = CutListItem(
            category="Hinge",
            component="Hinged Door",
            description="Bevel 90° Wall to Glass Hinge — Full Plate",
            product_code="SDH-201-90",
            quantity=2,
            unit="pc",
            notes="Bright Polished",
        )
        assert item.category == "Hinge"
        assert item.product_code == "SDH-201-90"
        assert item.quantity == 2


class TestAggregateItems:
    """Test aggregateItems merges identical items."""

    def test_identical_items_merge(self):
        items = [
            CutListItem("Hinge", "Door A", "Bevel 90°", "SDH-201-90"),
            CutListItem("Hinge", "Door A", "Bevel 90°", "SDH-201-90"),
        ]
        result = aggregateItems(items)
        assert len(result) == 1
        assert result[0].quantity == 2

    def test_different_items_stay_separate(self):
        items = [
            CutListItem("Hinge", "Door A", "Bevel 90°", "SDH-201-90"),
            CutListItem("Handle", "Door A", "Mushroom Knob", "DK-201"),
        ]
        result = aggregateItems(items)
        assert len(result) == 2

    def test_different_codes_stay_separate(self):
        items = [
            CutListItem("Hinge", "Door A", "Bevel 90°", "SDH-201-90"),
            CutListItem("Hinge", "Door A", "Bevel 90°", "SDH-291-90"),
        ]
        result = aggregateItems(items)
        assert len(result) == 2

    def test_same_item_different_component_merges(self):
        """Same item from different components → merge, join component names."""
        items = [
            CutListItem("Clamp", "Fixed Panel L", "L Clamp (Wall)", "GC-402"),
            CutListItem("Clamp", "Fixed Panel R", "L Clamp (Wall)", "GC-402"),
        ]
        result = aggregateItems(items)
        assert len(result) == 1
        assert result[0].quantity == 2
        assert "Fixed Panel L" in result[0].component
        assert "Fixed Panel R" in result[0].component

    def test_empty_list(self):
        assert aggregateItems([]) == []

    def test_does_not_mutate_originals(self):
        item = CutListItem("Glass", "Panel", "Clear 10mm", quantity=1)
        aggregateItems([item, CutListItem("Glass", "Panel", "Clear 10mm")])
        assert item.quantity == 1  # original unchanged

    def test_glass_different_dims_stay_separate(self):
        items = [
            CutListItem("Glass", "A", "Clear 10mm", width=900, height=2000),
            CutListItem("Glass", "B", "Clear 10mm", width=800, height=2000),
        ]
        result = aggregateItems(items)
        assert len(result) == 2

    def test_glass_same_dims_merge(self):
        items = [
            CutListItem("Glass", "A", "Clear 10mm", width=900, height=2000),
            CutListItem("Glass", "B", "Clear 10mm", width=900, height=2000),
        ]
        result = aggregateItems(items)
        assert len(result) == 1
        assert result[0].quantity == 2


class TestToCSV:
    """Test CSV output formatting."""

    def test_header_row(self):
        csv_text = toCSV([])
        lines = csv_text.strip().split("\n")
        assert len(lines) == 1  # header only
        assert "Category" in lines[0]
        assert "Product Code" in lines[0]

    def test_single_item(self):
        items = [
            CutListItem(
                category="Glass",
                component="Hinged Door",
                description="Clear 10mm",
                width=900,
                height=2000,
            )
        ]
        csv_text = toCSV(items)
        lines = csv_text.strip().split("\n")
        assert len(lines) == 2
        assert "Glass" in lines[1]
        assert "900" in lines[1]
        assert "2000" in lines[1]

    def test_product_code_in_output(self):
        items = [
            CutListItem(
                category="Hinge",
                component="Door",
                description="Bevel 90°",
                product_code="SDH-201-90",
            )
        ]
        csv_text = toCSV(items)
        assert "SDH-201-90" in csv_text

    def test_hardware_no_dims(self):
        """Hardware items with width/height=0 should show empty dim columns."""
        items = [
            CutListItem(
                category="Handle",
                component="Door",
                description="Mushroom Knob",
                product_code="DK-201",
            )
        ]
        csv_text = toCSV(items)
        # The CSV line should not have "0" in the width/height fields
        lines = csv_text.strip().split("\n")
        data_line = lines[1]
        # Width and Height should be empty strings, not "0"
        parts = data_line.split(",")
        # Index 4 = Width, 5 = Height
        assert parts[4].strip() == ""
        assert parts[5].strip() == ""


class TestToTable:
    """Test table output formatting."""

    def test_header_row(self):
        rows = toTable([])
        assert len(rows) == 1  # header only
        assert rows[0][0] == "Category"

    def test_data_rows(self):
        items = [
            CutListItem("Glass", "Panel", "Clear 10mm", width=900, height=2000),
            CutListItem("Hinge", "Door", "Bevel 90°", product_code="SDH-201-90"),
        ]
        rows = toTable(items)
        assert len(rows) == 3  # header + 2 data


class TestToConsoleTable:
    """Test console table formatting."""

    def test_empty_items(self):
        text = toConsoleTable([])
        assert "no items" in text

    def test_formatted_output(self):
        items = [
            CutListItem("Glass", "Panel", "Clear 10mm", width=900, height=2000),
        ]
        text = toConsoleTable(items)
        assert "Glass" in text
        assert "Clear 10mm" in text
        assert "---" in text  # separator line


# ======================================================================
# Integration tests — require FreeCAD
# ======================================================================

try:
    import FreeCAD as App
    HAS_FREECAD = True
except ImportError:
    HAS_FREECAD = False

import pytest


@pytest.mark.skipif(not HAS_FREECAD, reason="FreeCAD not available")
class TestCutListExtractorIntegration:
    """Integration tests that create real FreeCAD objects."""

    def _makeDoc(self):
        doc = App.newDocument("CutListTest")
        return doc

    def _closeDoc(self, doc):
        App.closeDocument(doc.Name)

    def test_extract_glass_child(self):
        from freecad.ShowerDesigner.Models.ChildProxies import GlassChild
        from freecad.ShowerDesigner.Models.CutListExtractor import CutListExtractor

        doc = self._makeDoc()
        try:
            part = doc.addObject("App::Part", "TestPanel")
            glass = doc.addObject("Part::FeaturePython", "Glass")
            GlassChild(glass)
            glass.Width = 900
            glass.Height = 2000
            glass.Thickness = 10
            glass.GlassType = "Clear"
            part.addObject(glass)
            doc.recompute()

            extractor = CutListExtractor()
            items = extractor.extract(part)

            assert len(items) == 1
            assert items[0].category == "Glass"
            assert items[0].width == 900
            assert items[0].height == 2000
            assert "Clear" in items[0].description
            assert "10" in items[0].description
        finally:
            self._closeDoc(doc)

    def test_extract_hinge_child(self):
        from freecad.ShowerDesigner.Models.ChildProxies import HingeChild
        from freecad.ShowerDesigner.Models.CutListExtractor import CutListExtractor

        doc = self._makeDoc()
        try:
            part = doc.addObject("App::Part", "TestDoor")
            hinge = doc.addObject("Part::FeaturePython", "Hinge")
            HingeChild(hinge)
            hinge.HingeType = "bevel_90_wall_to_glass_full"
            part.addObject(hinge)
            doc.recompute()

            extractor = CutListExtractor()
            items = extractor.extract(part)

            assert len(items) == 1
            assert items[0].category == "Hinge"
            assert "SDH-201-90" in items[0].product_code
            assert "Bevel 90" in items[0].description
        finally:
            self._closeDoc(doc)

    def test_extract_handle_child(self):
        from freecad.ShowerDesigner.Models.ChildProxies import HandleChild
        from freecad.ShowerDesigner.Models.CutListExtractor import CutListExtractor

        doc = self._makeDoc()
        try:
            part = doc.addObject("App::Part", "TestDoor")
            handle = doc.addObject("Part::FeaturePython", "Handle")
            HandleChild(handle)
            handle.HandleType = "mushroom_knob_b2b"
            part.addObject(handle)
            doc.recompute()

            extractor = CutListExtractor()
            items = extractor.extract(part)

            assert len(items) == 1
            assert items[0].category == "Handle"
            assert items[0].product_code == "DK-201"
            assert "Mushroom" in items[0].description
        finally:
            self._closeDoc(doc)

    def test_extract_clamp_child(self):
        from freecad.ShowerDesigner.Models.ChildProxies import ClampChild
        from freecad.ShowerDesigner.Models.CutListExtractor import CutListExtractor

        doc = self._makeDoc()
        try:
            part = doc.addObject("App::Part", "TestPanel")
            clamp = doc.addObject("Part::FeaturePython", "Clamp")
            ClampChild(clamp)
            clamp.ClampType = "L_Clamp"
            part.addObject(clamp)
            doc.recompute()

            extractor = CutListExtractor()
            items = extractor.extract(part)

            assert len(items) == 1
            assert items[0].category == "Clamp"
            assert items[0].product_code == "GC-402"
        finally:
            self._closeDoc(doc)

    def test_extract_channel_child(self):
        from freecad.ShowerDesigner.Models.ChildProxies import ChannelChild
        from freecad.ShowerDesigner.Models.CutListExtractor import CutListExtractor

        doc = self._makeDoc()
        try:
            part = doc.addObject("App::Part", "TestPanel")
            ch = doc.addObject("Part::FeaturePython", "Channel")
            ChannelChild(ch)
            ch.ChannelLocation = "wall"
            ch.ChannelLength = 1800
            part.addObject(ch)
            doc.recompute()

            extractor = CutListExtractor()
            items = extractor.extract(part)

            assert len(items) == 1
            assert items[0].category == "Channel"
            assert items[0].width == 1800
        finally:
            self._closeDoc(doc)

    def test_skip_visualization_children(self):
        from freecad.ShowerDesigner.Models.ChildProxies import SwingArcChild
        from freecad.ShowerDesigner.Models.CutListExtractor import CutListExtractor

        doc = self._makeDoc()
        try:
            part = doc.addObject("App::Part", "TestDoor")
            arc = doc.addObject("Part::FeaturePython", "SwingArc")
            SwingArcChild(arc)
            part.addObject(arc)
            doc.recompute()

            extractor = CutListExtractor()
            items = extractor.extract(part)

            assert len(items) == 0
        finally:
            self._closeDoc(doc)

    def test_skip_varset_and_controller(self):
        from freecad.ShowerDesigner.Models.CutListExtractor import CutListExtractor

        doc = self._makeDoc()
        try:
            part = doc.addObject("App::Part", "TestAssembly")
            vs = doc.addObject("App::VarSet", "VarSet")
            part.addObject(vs)
            doc.recompute()

            extractor = CutListExtractor()
            items = extractor.extract(part)

            assert len(items) == 0
        finally:
            self._closeDoc(doc)

    def test_nested_parts_recurse(self):
        from freecad.ShowerDesigner.Models.ChildProxies import GlassChild
        from freecad.ShowerDesigner.Models.CutListExtractor import CutListExtractor

        doc = self._makeDoc()
        try:
            enclosure = doc.addObject("App::Part", "CornerEnclosure")
            sub_panel = doc.addObject("App::Part", "FixedPanel")
            glass = doc.addObject("Part::FeaturePython", "Glass")
            GlassChild(glass)
            glass.Width = 600
            glass.Height = 2000
            glass.Thickness = 8
            sub_panel.addObject(glass)
            enclosure.addObject(sub_panel)
            doc.recompute()

            extractor = CutListExtractor()
            items = extractor.extract(enclosure)

            assert len(items) == 1
            assert items[0].component == "FixedPanel"
            assert items[0].width == 600
        finally:
            self._closeDoc(doc)

    def test_full_assembly_multiple_children(self):
        """Assembly with glass + hinge + handle → 3 BOM items."""
        from freecad.ShowerDesigner.Models.ChildProxies import (
            GlassChild,
            HandleChild,
            HingeChild,
        )
        from freecad.ShowerDesigner.Models.CutListExtractor import CutListExtractor

        doc = self._makeDoc()
        try:
            part = doc.addObject("App::Part", "HingedDoor")

            glass = doc.addObject("Part::FeaturePython", "Glass")
            GlassChild(glass)
            glass.Width = 800
            glass.Height = 2000
            glass.Thickness = 10
            part.addObject(glass)

            h1 = doc.addObject("Part::FeaturePython", "Hinge1")
            HingeChild(h1)
            h1.HingeType = "bevel_90_wall_to_glass_full"
            part.addObject(h1)

            h2 = doc.addObject("Part::FeaturePython", "Hinge2")
            HingeChild(h2)
            h2.HingeType = "bevel_90_wall_to_glass_full"
            part.addObject(h2)

            handle = doc.addObject("Part::FeaturePython", "Handle")
            HandleChild(handle)
            handle.HandleType = "mushroom_knob_b2b"
            part.addObject(handle)

            doc.recompute()

            extractor = CutListExtractor()
            items = extractor.extract(part)

            assert len(items) == 4  # 1 glass + 2 hinges + 1 handle
            categories = [i.category for i in items]
            assert categories.count("Glass") == 1
            assert categories.count("Hinge") == 2
            assert categories.count("Handle") == 1

            # After aggregation, hinges should merge
            from freecad.ShowerDesigner.Data.CutList import aggregateItems
            agg = aggregateItems(items)
            hinge_items = [i for i in agg if i.category == "Hinge"]
            assert len(hinge_items) == 1
            assert hinge_items[0].quantity == 2
        finally:
            self._closeDoc(doc)


# ======================================================================
# Console runner (for FreeCAD console)
# ======================================================================

def run_all_tests():
    """Run all tests from the FreeCAD console."""
    import traceback

    test_classes = [
        TestCutListItem,
        TestAggregateItems,
        TestToCSV,
        TestToTable,
        TestToConsoleTable,
    ]

    if HAS_FREECAD:
        test_classes.append(TestCutListExtractorIntegration)

    passed = 0
    failed = 0
    errors = []

    for cls in test_classes:
        instance = cls()
        for name in dir(instance):
            if not name.startswith("test_"):
                continue
            method = getattr(instance, name)
            try:
                method()
                passed += 1
                print(f"  PASS: {cls.__name__}.{name}")
            except Exception as e:
                failed += 1
                errors.append(f"  FAIL: {cls.__name__}.{name}: {e}")
                traceback.print_exc()

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    if errors:
        print("\nFailures:")
        for e in errors:
            print(e)

    return failed == 0


if __name__ == "__main__":
    run_all_tests()
