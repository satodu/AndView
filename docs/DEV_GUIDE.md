# Development Guide - AndView

This guide is for developers who want to contribute or modify AndView.

## Initial Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AndView
```

### 2. Quick Setup

```bash
# Installs everything automatically
./scripts/install.sh

# Or manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Development

### Development Script

The `dev` script (or `scripts/dev.sh`) makes development easier with several options:

```bash
# Normal execution (dev mode)
./dev

# With debug enabled
./dev --debug

# With verbose output
./dev --verbose

# Code analysis (pylint)
./dev --lint

# Automatic code formatting (black)
./dev --format

# Clean temporary files
./dev --clean

# Install development tools
./dev --install-dev

# Show help
./dev --help
```

### Project Structure

```
AndView/
├── main.py                    # Entry point
├── src/
│   ├── __init__.py
│   ├── adb_manager.py         # ADB management
│   ├── scrcpy_manager.py      # scrcpy management
│   └── ui/
│       ├── main_window.py     # Main window
│       └── widgets/
│           ├── device_list.py    # Device list
│           └── control_panel.py  # Control panel
├── dev                        # Wrapper for dev mode
├── andview                    # Wrapper to run app
├── scripts/
│   ├── dev.sh                 # Development script
│   ├── build_appimage.sh      # Script to create AppImage
│   └── install.sh             # Installation script
└── docs/                      # All documentation
```

## Development Workflow

### 1. Making Changes

```bash
# 1. Create a branch
git checkout -b feature/my-feature

# 2. Make your changes
# Edit the necessary files

# 3. Test your changes
./dev

# 4. Check the code
./dev --lint
./dev --format

# 5. Commit
git add .
git commit -m "Add my feature"

# 6. Push
git push origin feature/my-feature
```

### 2. Testing

```bash
# Basic test
./dev

# Test with debug to see more details
./dev --debug

# Clean temporary files before testing
./dev --clean
./dev
```

### 3. Quality Check

```bash
# Install dev tools (first time)
./dev --install-dev

# Run linter
./dev --lint

# Format the code
./dev --format
```

## Adding New Features

### Example: New ADB Function

1. **Edit `src/adb_manager.py`**:

```python
def new_function(self, serial: str) -> Tuple[bool, str]:
    """Description of the new function"""
    try:
        result = subprocess.run(
            [self.adb_path, "-s", serial, "shell", "command"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except FileNotFoundError:
        return False, "ADB not found"
```

2. **Add to UI in `src/ui/widgets/control_panel.py`**:

```python
# In setup_ui or in the appropriate tab
new_btn = QPushButton("🔧 New Function")
new_btn.clicked.connect(self._on_new_function)

# Add the handler
def _on_new_function(self):
    if not self.current_device:
        QMessageBox.warning(self, "Warning", "No device!")
        return
    
    # Emit a signal or call directly
    self.new_function.emit()
```

3. **Connect in the main window in `src/ui/main_window.py`**:

```python
# In __init__ or _setup_ui
self.control_panel.new_function.connect(self._on_new_function)

# Add the handler
def _on_new_function(self):
    success, message = self.adb_manager.new_function(
        self.current_device.serial
    )
    
    if success:
        QMessageBox.information(self, "Success", message)
    else:
        QMessageBox.critical(self, "Error", message)
```

4. **Test**:

```bash
./dev --debug
```

## Debugging

### Debug with prints

```python
# Use prints for quick debug
print(f"DEBUG: device={device.serial}")

# Or use the logging module
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Device: {device.serial}")
```

### Debug with PyQt5

```bash
# Run with QT_DEBUG_PLUGINS to see Qt issues
QT_DEBUG_PLUGINS=1 ./dev --debug
```

### Debug scrcpy/ADB

```bash
# Test commands manually
adb devices -l
scrcpy --version

# See what AndView is executing
./dev --verbose
```

## Creating Releases

### 1. Update Version

Edit in the following files:
- `src/__init__.py` → `__version__`
- `build_appimage.sh` → `APP_VERSION`
- `CHANGELOG.md` → New section

### 2. Create the AppImage

```bash
./scripts/build_appimage.sh
```

### 3. Test the AppImage

```bash
./build/AppImage/AndView-1.0.0-x86_64.AppImage
```

### 4. Create the Release

```bash
# Create a tag
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0

# Upload the AppImage on GitHub Releases
# Or use gh CLI
gh release create v1.0.0 \
    build/AppImage/AndView-1.0.0-x86_64.AppImage \
    --title "AndView v1.0.0" \
    --notes "Release notes here"
```

## Development Troubleshooting

### PyQt5 not found

```bash
source venv/bin/activate
pip install --upgrade PyQt5
```

### Imports not working

```bash
# Make sure you're in the correct directory
cd /home/panda/Projects/satodu/AndView

# And that the virtual environment is active
source venv/bin/activate
```

### Changes don't appear

```bash
# Clean compiled files
./dev --clean

# Or manually
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
```

## Best Practices

### Code

- ✅ Follow PEP 8
- ✅ Use type hints when possible
- ✅ Docstrings in all functions/classes
- ✅ Descriptive variable names
- ✅ Keep functions small and focused

### Git

- ✅ Small and focused commits
- ✅ Descriptive messages
- ✅ Test before committing
- ✅ Use branches for features

### UI

- ✅ Clear messages to the user
- ✅ Proper error handling
- ✅ Visual feedback of actions
- ✅ Accessibility (font sizes, contrast)

## Useful Resources

- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [ADB Documentation](https://developer.android.com/studio/command-line/adb)
- [scrcpy GitHub](https://github.com/Genymobile/scrcpy)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [AppImage Documentation](https://docs.appimage.org/)

## Help

If you need help:
1. See the documentation in the `.md` files
2. Open an issue on GitHub
3. Check the examples in the existing code

Happy coding! 🚀
