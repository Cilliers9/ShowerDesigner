# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Test script for 3D Dimension annotations.

Pure data tests (no FreeCAD required) plus integration tests.

Run:
    pytest freecad/ShowerDesigner/Tests/test_dimensions.py
"""

import sys
sys.path.insert(
    0, r"C:\Users\tclou\AppData\Roaming\FreeCAD\v1-1\Mod\ShowerDesigner"
)

from freecad.ShowerDesigner.Data.DimensionSpecs import (
    DIM_COLORS,
    DIM_OFFSET_HARDWARE,
    DIM_OFFSET_OVERALL,
    DIM_OFFSET_PANEL,
    DimensionItem,
)


# ======================================================================
# Pure data tests — no FreeCAD required
# ======================================================================


class TestDimensionItem:
    """Test DimensionItem dataclass."""

    def test_construction(self):
        item = DimensionItem(
            category="Overall",
            label="Width",
            p1=(0.0, 0.0, 0.0),
            p2=(900.0, 0.0, 0.0),
            offset_direction=(0.0, -1.0, 0.0),
            offset_distance=150.0,
        )
        assert item.category == "Overall"
        assert item.label == "Width"
        assert item.p1 == (0.0, 0.0, 0.0)
        assert item.p2 == (900.0, 0.0, 0.0)
        assert item.offset_direction == (0.0, -1.0, 0.0)
        assert item.offset_distance == 150.0

    def test_hardware_item(self):
        item = DimensionItem(
            category="Hardware",
            label="Hinge1 Height",
            p1=(100.0, 0.0, 0.0),
            p2=(100.0, 0.0, 250.0),
            offset_direction=(1.0, 0.0, 0.0),
            offset_distance=DIM_OFFSET_HARDWARE,
        )
        assert item.category == "Hardware"
        assert item.offset_distance == 50.0


class TestDimensionConstants:
    """Test dimension spec constants."""

    def test_offset_values(self):
        assert DIM_OFFSET_OVERALL == 150.0
        assert DIM_OFFSET_PANEL == 80.0
        assert DIM_OFFSET_HARDWARE == 50.0

    def test_color_categories(self):
        assert "Overall" in DIM_COLORS
        assert "Panel" in DIM_COLORS
        assert "Hardware" in DIM_COLORS

    def test_color_format(self):
        for category, color in DIM_COLORS.items():
            assert len(color) == 3, f"{category} color must be RGB tuple"
            for component in color:
                assert 0.0 <= component <= 1.0, (
                    f"{category} color component out of range"
                )


# ======================================================================
# Integration tests — require FreeCAD
# ======================================================================

try:
    import FreeCAD as App

    _HAS_FREECAD = True
except ImportError:
    _HAS_FREECAD = False

import pytest


@pytest.mark.skipif(not _HAS_FREECAD, reason="FreeCAD not available")
class TestDimensionExtractorCorner:
    """Integration tests: extract dimensions from a CornerEnclosure."""

    @pytest.fixture(autouse=True)
    def setup_corner(self):
        from freecad.ShowerDesigner.Models.CornerEnclosure import (
            createCornerEnclosure,
        )

        self.doc = App.newDocument("TestDimCorner")
        self.enc = createCornerEnclosure("TestCorner")
        self.doc.recompute()
        yield
        App.closeDocument(self.doc.Name)

    def test_extracts_overall_dimensions(self):
        from freecad.ShowerDesigner.Models.DimensionExtractor import (
            DimensionExtractor,
        )

        extractor = DimensionExtractor()
        items = extractor.extract(self.enc)

        overall = [i for i in items if i.category == "Overall"]
        labels = {i.label for i in overall}
        assert "Width" in labels
        assert "Height" in labels
        assert "Depth" in labels

    def test_extracts_panel_dimensions(self):
        from freecad.ShowerDesigner.Models.DimensionExtractor import (
            DimensionExtractor,
        )

        extractor = DimensionExtractor()
        items = extractor.extract(self.enc)

        panels = [i for i in items if i.category == "Panel"]
        assert len(panels) > 0
        # Each panel should have width and height
        width_dims = [i for i in panels if "Width" in i.label]
        height_dims = [i for i in panels if "Height" in i.label]
        assert len(width_dims) > 0
        assert len(height_dims) > 0

    def test_overall_width_value(self):
        from freecad.ShowerDesigner.Models.DimensionExtractor import (
            DimensionExtractor,
        )

        extractor = DimensionExtractor()
        items = extractor.extract(self.enc)

        width_dim = next(
            i for i in items if i.category == "Overall" and i.label == "Width"
        )
        # Default CornerEnclosure width is 900
        measured = abs(width_dim.p2[0] - width_dim.p1[0])
        assert abs(measured - 900.0) < 0.1

    def test_overall_height_value(self):
        from freecad.ShowerDesigner.Models.DimensionExtractor import (
            DimensionExtractor,
        )

        extractor = DimensionExtractor()
        items = extractor.extract(self.enc)

        height_dim = next(
            i for i in items
            if i.category == "Overall" and i.label == "Height"
        )
        # Default CornerEnclosure height is 2000
        measured = abs(height_dim.p2[2] - height_dim.p1[2])
        assert abs(measured - 2000.0) < 0.1

    def test_extracts_hardware_dimensions(self):
        from freecad.ShowerDesigner.Models.DimensionExtractor import (
            DimensionExtractor,
        )

        extractor = DimensionExtractor()
        items = extractor.extract(self.enc)

        hardware = [i for i in items if i.category == "Hardware"]
        # Corner enclosure has hinges and possibly support bar
        assert len(hardware) > 0


@pytest.mark.skipif(not _HAS_FREECAD, reason="FreeCAD not available")
class TestDimensionExtractorAlcove:
    """Integration tests: extract dimensions from an AlcoveEnclosure."""

    @pytest.fixture(autouse=True)
    def setup_alcove(self):
        from freecad.ShowerDesigner.Models.AlcoveEnclosure import (
            createAlcoveEnclosure,
        )

        self.doc = App.newDocument("TestDimAlcove")
        self.enc = createAlcoveEnclosure("TestAlcove")
        self.doc.recompute()
        yield
        App.closeDocument(self.doc.Name)

    def test_extracts_overall_dimensions(self):
        from freecad.ShowerDesigner.Models.DimensionExtractor import (
            DimensionExtractor,
        )

        extractor = DimensionExtractor()
        items = extractor.extract(self.enc)

        overall = [i for i in items if i.category == "Overall"]
        labels = {i.label for i in overall}
        assert "Width" in labels
        assert "Height" in labels

    def test_overall_width_value(self):
        from freecad.ShowerDesigner.Models.DimensionExtractor import (
            DimensionExtractor,
        )

        extractor = DimensionExtractor()
        items = extractor.extract(self.enc)

        width_dim = next(
            i for i in items if i.category == "Overall" and i.label == "Width"
        )
        # Default AlcoveEnclosure width is 1200
        measured = abs(width_dim.p2[0] - width_dim.p1[0])
        assert abs(measured - 1200.0) < 0.1


# ======================================================================
# Console runner
# ======================================================================


def run_all_tests():
    """Run all tests — call from FreeCAD console."""
    passed = 0
    failed = 0

    # Pure data tests
    for cls in (TestDimensionItem, TestDimensionConstants):
        instance = cls()
        for name in dir(instance):
            if not name.startswith("test_"):
                continue
            try:
                getattr(instance, name)()
                App.Console.PrintMessage(f"  PASS: {cls.__name__}.{name}\n")
                passed += 1
            except Exception as e:
                App.Console.PrintError(
                    f"  FAIL: {cls.__name__}.{name}: {e}\n"
                )
                failed += 1

    App.Console.PrintMessage(
        f"\nDimension tests: {passed} passed, {failed} failed\n"
    )
    return failed == 0
