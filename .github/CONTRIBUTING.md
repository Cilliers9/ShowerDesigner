
# Contributing to ShowerDesigner

Thank you for your interest in contributing to ShowerDesigner!

<br/>

## Quick Start

-   Standard PR-based workflow
-   For new files add SPDX license headers
-   Open an issue for larger features or changes

<br/>

## Development Setup

### Prerequisites
- FreeCAD >= 0.20 installed
- Python >= 3.10
- Git

### Setup Steps

1. **Fork & clone the repository**
   ```sh
   git clone https://github.com/Cilliers9/ShowerDesigner.git
   cd ShowerDesigner
   ```

2. **Install development dependencies**
   
   Using [uv](https://docs.astral.sh/uv/):
   ```sh
   uv sync
   ```
   
   Or using pip:
   ```sh
   pip install -e ".[dev]"
   ```

3. **Link to FreeCAD**
   
   Create a symlink from the repository to your FreeCAD `Mod` directory:
   
   - **Linux/macOS**:
     ```sh
     ln -s $(pwd) ~/.local/share/FreeCAD/Mod/ShowerDesigner
     ```
   
   - **Windows** (as Administrator):
     ```cmd
     mklink /D "%APPDATA%\FreeCAD\Mod\ShowerDesigner" "%CD%"
     ```

4. **Test the setup**
   
   Open FreeCAD and verify ShowerDesigner appears in the workbench dropdown.

<br/>

## Code Guidelines

### Python Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use Black for formatting: `black .`

### License Headers
All new Python files must include:
```python
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner addon.
```

For SVG icons, include Creative Commons metadata in the file.

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Reference issue numbers when applicable

Example:
```
Add corner shower template

- Implements parametric corner enclosure
- Adds configurable glass panels
- Includes default hardware positions

Fixes #42
```

<br/>

## Contribution Workflow

1. **Create an issue** (for new features or bugs)
   - Describe the problem or enhancement
   - Wait for feedback before starting major work

2. **Create a branch**
   ```sh
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, documented code
   - Add tests if applicable
   - Update documentation

4. **Test thoroughly**
   - Test in FreeCAD with various scenarios
   - Verify no regressions

5. **Submit a Pull Request**
   - Describe your changes clearly
   - Link related issues
   - Respond to review feedback

<br/>

## Areas for Contribution

### High Priority
- [ ] Shower enclosure templates (corner, alcove, walk-in)
- [ ] Glass panel thickness and spacing calculations
- [ ] Hardware placement tools
- [ ] Manufacturing export formats

### Medium Priority
- [ ] Custom layout designer
- [ ] Material library (glass types, frame finishes)
- [ ] Measurement tools
- [ ] Preview/rendering improvements

### Documentation
- [ ] User tutorials
- [ ] API documentation
- [ ] Example projects
- [ ] Video demonstrations

<br/>

## Questions?

- Open a [discussion](https://github.com/Cilliers9/ShowerDesigner/discussions)
- Check existing [issues](https://github.com/Cilliers9/ShowerDesigner/issues)
- Review the [wiki](https://github.com/Cilliers9/ShowerDesigner/wiki)

<br/>

Thank you for contributing to ShowerDesigner! 🚿
