# AGENTS.md - ShowerDesigner Workbench

Guidelines for AI agents working in the ShowerDesigner FreeCAD workbench repository.

## Project Overview

ShowerDesigner is a parametric shower enclosure design workbench for FreeCAD. It creates customizable shower designs with glass panels, hardware, and manufacturing-ready outputs.

- **Python**: >= 3.10
- **FreeCAD**: >= 1.0.2
- **License**: LGPL-3.0-or-later (code), CC-BY-SA-4.0 (icons)

## Build/Lint/Test Commands

```bash
# Install development dependencies
pip install -e ".[dev]"
# or with uv: uv sync

# Format code with Black
black .

# Lint with Ruff
ruff check .
ruff check --fix .

# Run all tests
pytest

# Run single test file
pytest tests/test_file.py

# Run single test function
pytest tests/test_file.py::test_function_name

# Run with verbose output
pytest -v
```

## Code Style Guidelines

### Formatting
- **Line length**: 100 characters maximum
- **Indentation**: 4 spaces (no tabs)
- **End of line**: LF (Unix-style)
- **No trailing whitespace** (except Markdown)
- **No final newline** in files
- Use **Black** for automatic formatting

### License Headers
All new Python files MUST include SPDX headers at the top:

```python
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.
```

For SVG icons, include Creative Commons metadata in the file.

### Imports
- Group imports: stdlib, third-party, local
- Use `from typing import TYPE_CHECKING` for type-only imports
- FreeCAD/PySide compatibility pattern:
  ```python
  from typing import TYPE_CHECKING
  if TYPE_CHECKING:
      from PySide6.QtCore import *
  else:
      from PySide.QtCore import *
  ```
- Import FreeCAD as `App` for document operations

### Type Hints
- Use type hints where appropriate
- Use `from __future__ import annotations` for forward references if needed
- Function signatures should include types for public APIs

### Naming Conventions
- **Classes**: PascalCase (e.g., `AlcoveEnclosure`, `GlassPanel`)
- **Functions/Methods**: camelCase for FreeCAD integration (e.g., `createAlcoveEnclosure`, `onChanged`)
- **Constants**: UPPER_SNAKE_CASE
- **Private members**: Prefix with underscore `_`
- **Modules**: lowercase with underscores (e.g., `alcove_enclosure.py`)

### Documentation
- Use docstrings for all public classes and methods
- Follow Google-style docstrings or standard Python conventions
- Document property changes in FreeCAD feature objects

### Error Handling
- Use try/except with specific exception types
- Log errors using `App.Console.PrintError()` for FreeCAD visibility
- Handle missing documents gracefully (create if none active)

### FreeCAD Patterns
- Feature objects inherit from `object` and set `obj.Proxy = self`
- Implement `execute(self, obj)` for geometry regeneration
- Implement `onChanged(self, obj, prop)` for property change handling
- Add properties using `obj.addProperty(type, name, group, tooltip)`
- Set `obj.ViewObject.Proxy = 0` for GUI mode

### Git Workflow
- Use clear, descriptive commit messages starting with a verb
- Reference issue numbers when applicable
- Branch naming: `feature/description` or `fix/description`

## Project Structure

```
freecad/ShowerDesigner/
├── __init__.py           # Module initialization
├── init_gui.py          # GUI initialization
├── Models/              # Parametric enclosure models
│   ├── AlcoveEnclosure.py
│   ├── CornerEnclosure.py
│   ├── WalkInEnclosure.py
│   └── CustomEnclosure.py
├── Qt/                  # Qt compatibility layer
│   ├── Core.py
│   ├── Gui.py
│   └── Widget.py
├── Commands/            # FreeCAD commands
├── Gui/                 # GUI components
└── Misc/                # Utilities
    └── Resources.py
Resources/
├── Icons/               # SVG icons
└── Documents/           # Documentation
```

## VS Code Extensions (Recommended)

- ms-python.python
- ms-python.vscode-pylance
- streetsidesoftware.code-spell-checker
- editorconfig.editorconfig
- theqtcompany.qt-ui
- aaron-bond.better-comments
- redhat.vscode-xml
- astral-sh.ruff

## Testing Notes

- No test suite exists yet; tests should be added in a `tests/` directory
- Test manually in FreeCAD after code changes
- Verify workbench loads without errors in FreeCAD Addon Manager

## Dependencies

**Runtime:**
- freecad-stubs>=1.0.21
- pyside6>=6.9.2
- numpy>=2.4.0 (FreeCAD internal)

**Development:**
- pytest>=7.0.0
- black>=23.0.0
- ruff>=0.1.0
