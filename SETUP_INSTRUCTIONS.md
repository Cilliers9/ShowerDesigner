# ShowerDesigner Setup Instructions

## Quick Start

You now have a complete FreeCAD addon template renamed to "ShowerDesigner"!

## Directory Structure

```
ShowerDesigner/
├── freecad/
│   └── ShowerDesigner/          # Main Python package
│       ├── __init__.py          # Package initializer
│       ├── init_gui.py          # GUI initialization
│       ├── Misc/                # Utility modules
│       │   ├── __init__.py
│       │   └── Resources.py     # Icon/resource loader
│       ├── Qt/                  # Qt compatibility layer
│       │   ├── __init__.py
│       │   ├── Core.py          # QtCore imports
│       │   ├── Gui.py           # QtGui imports
│       │   └── Widget.py        # QtWidgets imports
│       └── Resources/
│           └── Icons/
│               └── Logo.svg     # Workbench icon
├── Documentation/               # User documentation
│   ├── README.md
│   └── Usage/
├── Resources/                   # Repository resources
│   ├── Documents/
│   │   └── Overview.md         # For addon manager
│   ├── Icons/
│   │   └── Logo.svg
│   └── Media/
│       └── Header.svg          # README header
├── .github/
│   ├── CONTRIBUTING.md
│   └── FUNDING.yml
├── .vscode/
│   └── extensions.json
├── package.xml                  # FreeCAD addon metadata
├── pyproject.toml              # Python project config
├── README.md                   # Main README
├── CHANGELOG.md
├── LICENSE-CODE                # LGPL-3.0-or-later
├── LICENSE-ICON                # CC-BY-SA-4.0
├── .gitignore
└── .editorconfig
```

## Next Steps

### 1. Customize Metadata

Edit these files with your information:

**package.xml**
- Update maintainer name and email
- Update author name and email
- Update repository URLs (replace "YourUsername")

**pyproject.toml**
- No changes needed unless adding dependencies

**README.md**
- Update repository URLs
- Add actual feature details as you build them

### 2. Install in FreeCAD

#### Option A: Symlink (Development)
```bash
# Linux/macOS
ln -s /path/to/ShowerDesigner ~/.local/share/FreeCAD/Mod/ShowerDesigner

# Windows (as Administrator in CMD)
mklink /D "%APPDATA%\FreeCAD\Mod\ShowerDesigner" "C:\path\to\ShowerDesigner"
```

#### Option B: Copy
Copy the entire `ShowerDesigner` folder to your FreeCAD `Mod` directory.

### 3. Verify Installation

1. Open FreeCAD
2. The ShowerDesigner workbench should appear in the workbench dropdown
3. Check the Python console for the init messages

### 4. Start Development

Key files to modify:

**init_gui.py** - Add workbench GUI initialization:
```python
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner addon.

import FreeCADGui as Gui


class ShowerDesignerWorkbench(Gui.Workbench):
    """ShowerDesigner workbench for FreeCAD"""
    
    MenuText = "ShowerDesigner"
    ToolTip = "Parametric shower enclosure design"
    Icon = """paste the icon SVG content here or use a path"""
    
    def Initialize(self):
        """Initialize workbench"""
        # Add toolbars, menus, etc.
        pass
    
    def Activated(self):
        """Called when workbench is activated"""
        pass
    
    def Deactivated(self):
        """Called when workbench is deactivated"""
        pass
 

Gui.addWorkbench(ShowerDesignerWorkbench())
```

### 5. Run unit tests (optional)

- Ensure FreeCAD is accessible or run in CI environment.
- From repo root: `pytest` (or `pytest -v` for verbose)
- If tests require GUI, consider headless FreeCAD in CI or skip locally.

### 6. Lint and format (optional)

- `ruff check .` and fix with `ruff check --fix .`
- `black .`

### 7. Packaging / Release (optional)

- If using setuptools: `python -m build` or `python -m pip install build` then `python -m build`
- Ensure `package.xml` and `pyproject.toml` reflect metadata
- Create a git tag and push release artifacts

**Create new modules** in `freecad/ShowerDesigner/`:
- `Commands.py` - Define FreeCAD commands
- `Models.py` - Parametric shower models
- `Panels.py` - Property panels and task panels
- `Templates.py` - Shower enclosure templates

### 5. Add Icons

Replace `freecad/ShowerDesigner/Resources/Icons/Logo.svg` with your custom icon.

Add command icons to the same directory.

### 6. Update Documentation

Fill in the documentation files in the `Documentation/` folder with actual usage instructions.

### 7. Convert Header Image

The header is currently SVG. For better README display, convert to WebP:
```bash
# Using ImageMagick or similar
convert Resources/Media/Header.svg Resources/Media/Header.webp
```

### 8. Initialize Git Repository

```bash
cd ShowerDesigner
git init
git add .
git commit -m "Initial commit: ShowerDesigner workbench structure"

# If you have a GitHub repo:
git remote add origin https://github.com/YourUsername/ShowerDesigner.git
git push -u origin main
```

## Development Tools

### Install Development Dependencies
```bash
uv sync
# or
pip install -e ".[dev]"
```

### Code Formatting
```bash
black freecad/
```

### Linting
```bash
ruff check freecad/
```

## Testing in FreeCAD

1. Make changes to your code
2. Restart FreeCAD (or reload the module in the Python console)
3. Test the changes
4. Iterate

## Publishing

When ready to share:

1. Update version in `package.xml` and `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a GitHub release
4. Submit to FreeCAD Addon Manager repository

## Need Help?

- FreeCAD Forum: https://forum.freecad.org/
- FreeCAD Wiki: https://wiki.freecad.org/
- Python API Docs: https://freecad.github.io/SourceDoc/

## License

- Code: LGPL-3.0-or-later
- Icons: CC-BY-SA-4.0

Make sure all new files include the appropriate SPDX headers!
