# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ShowerDesigner is a parametric shower enclosure design workbench for FreeCAD (>= 1.0.2, Python >= 3.10). It creates customizable shower designs with glass panels, hardware, and manufacturing-ready outputs.

## Build/Lint/Test Commands

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Format and lint
black .
ruff check --fix .

# Run tests (requires FreeCAD accessible)
pytest freecad/ShowerDesigner/Tests/

# Run single test
pytest freecad/ShowerDesigner/Tests/test_glass_panel.py
```

## Installation for Development

Windows symlink (run as admin):
```cmd
mklink /D "%APPDATA%\FreeCAD\Mod\ShowerDesigner" "C:\path\to\repo"
```

## Architecture

### Workbench Structure
- **init_gui.py**: Registers `ShowerDesignerWorkbench` with FreeCAD, defines toolbars (Enclosures, Components, Tools)
- **Commands/__init__.py**: All FreeCAD commands using pattern `GetResources()`, `Activated()`, `IsActive()`

### Models (`Models/`)
FreeCAD Part::FeaturePython objects:
- **GlassPanel**: Base parametric glass with type, thickness, tempering, color
- **FixedPanel**: Extends GlassPanel with wall/floor clamp & channel hardware
- **CornerEnclosure**, **AlcoveEnclosure**, **WalkInEnclosure**, **CustomEnclosure**: Compound shapes from panels

Model pattern:
```python
class MyModel:
    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyLength", "Width", "Dimensions", "Panel width")

    def execute(self, obj):
        # Generate geometry here

    def onChanged(self, obj, prop):
        # Handle property changes
```

### Data Layer (`Data/`)
- **GlassSpecs.py**: Glass thickness, types, colors, edge finishes, tempering with validation
- **PanelConstraints.py**: Panel spacing validation, collision detection, alignment utilities

### Qt Compatibility (`Qt/`)
Abstraction for PySide vs PySide6:
```python
if TYPE_CHECKING:
    from PySide6.QtCore import *
else:
    from PySide.QtCore import *
```

## Code Style

- **Line length**: 100 chars
- **Naming**: Classes=PascalCase, methods=camelCase (FreeCAD convention), constants=UPPER_SNAKE_CASE
- Import FreeCAD as `App` for document operations
- Use `App.Console.PrintError()` for error visibility

### Required License Headers
All Python files must include:
```python
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.
```

## Key Files

| File | Purpose |
|------|---------|
| `freecad/ShowerDesigner/init_gui.py` | Workbench registration & toolbars |
| `freecad/ShowerDesigner/Commands/__init__.py` | All command definitions |
| `freecad/ShowerDesigner/Models/GlassPanel.py` | Base glass panel class |
| `freecad/ShowerDesigner/Data/GlassSpecs.py` | Glass specifications database |
| `Documentation/Dev_Plan/PHASE1-PLAN.md` | Development roadmap |
| `AGENTS.md` | Full AI agent guidelines |
