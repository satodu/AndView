# AndView Project Structure

Documentation about file and directory organization of the project.

## 📁 Directory Structure

```
AndView/
├── andview                    # Wrapper to run the app
├── dev                        # Wrapper for development mode
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── LICENSE                    # MIT License
├── README.md                  # Main documentation
├── .gitignore                # Files ignored by Git
│
├── src/                       # Main source code
│   ├── __init__.py
│   ├── adb_manager.py         # ADB command management
│   ├── scrcpy_manager.py      # scrcpy management
│   └── ui/                    # Graphical interface
│       ├── __init__.py
│       ├── main_window.py     # Main window
│       └── widgets/           # Custom widgets
│           ├── __init__.py
│           ├── device_list.py    # Device list
│           └── control_panel.py  # Control panel
│
├── scripts/                   # Automation scripts
│   ├── install.sh             # Complete installation
│   ├── dev.sh                 # Development mode
│   └── build_appimage.sh      # Create AppImage
│
├── docs/                      # Complete documentation
│   ├── START_HERE.md          # Getting started guide
│   ├── README.md              # Detailed overview
│   ├── QUICKSTART.md          # Quick guide
│   ├── DEV_GUIDE.md           # Development guide
│   ├── APPIMAGE.md            # Create AppImage
│   ├── TROUBLESHOOTING.md     # Troubleshooting
│   ├── CONTRIBUTING.md        # How to contribute
│   ├── CHANGELOG.md           # Version history
│   └── STRUCTURE.md           # This file
│
└── venv/                      # Python virtual environment (created on install)
    ├── bin/
    ├── include/
    └── lib/
```

## 📄 File Descriptions

### Project Root

| File | Description |
|------|-------------|
| `andview` | Wrapper script to run the application |
| `dev` | Wrapper script for development mode |
| `main.py` | Python application entry point |
| `requirements.txt` | List of Python dependencies (PyQt5, etc.) |
| `LICENSE` | MIT project license |
| `README.md` | Main documentation and overview |
| `.gitignore` | Files and directories ignored by Git |

### `src/` Directory

Contains all application source code.

| File | Responsibility |
|------|----------------|
| `adb_manager.py` | `ADBManager` class - manages ADB commands, lists devices, installs APKs, etc. |
| `scrcpy_manager.py` | `ScrcpyManager` class - manages scrcpy, starts/stops mirroring, configuration options |
| `ui/main_window.py` | `MainWindow` class - main application window, integrates all components |
| `ui/widgets/device_list.py` | Connected device list widget |
| `ui/widgets/control_panel.py` | Control panel widget with tabs (mirroring, tools, commands) |

### `scripts/` Directory

Automation scripts for installation, development and building.

| Script | Function |
|--------|----------|
| `install.sh` | Complete installation: checks dependencies, creates venv, installs packages, creates shortcuts |
| `dev.sh` | Development mode with various options (debug, lint, format, clean, etc.) |
| `build_appimage.sh` | Creates AppImage for distribution |

### `docs/` Directory

All project documentation.

| Document | Content |
|----------|---------|
| `START_HERE.md` | **Start here!** Quick initial guide |
| `README.md` | Detailed project overview (complete version) |
| `QUICKSTART.md` | Quick usage guide |
| `DEV_GUIDE.md` | Complete guide for developers |
| `APPIMAGE.md` | How to create and distribute AppImage |
| `TROUBLESHOOTING.md` | Common problem solving |
| `CONTRIBUTING.md` | Guide for contributors |
| `CHANGELOG.md` | Version history and changes |
| `STRUCTURE.md` | This file - project structure |

## 🔄 Execution Flow

### Normal Execution

```
./andview
  ↓
Activates venv
  ↓
Executes main.py
  ↓
Imports MainWindow from src/ui/
  ↓
MainWindow imports ADBManager and ScrcpyManager
  ↓
MainWindow creates widgets (DeviceList, ControlPanel)
  ↓
Application starts
```

### Development Mode

```
./dev [options]
  ↓
Executes scripts/dev.sh
  ↓
Checks/creates venv
  ↓
Installs dependencies if needed
  ↓
Processes options (--debug, --lint, etc.)
  ↓
Executes main.py with appropriate settings
```

### Installation

```
./scripts/install.sh
  ↓
Detects operating system
  ↓
Checks ADB, scrcpy, Python
  ↓
Offers to install missing dependencies
  ↓
Creates virtual environment (venv/)
  ↓
Installs Python packages
  ↓
Creates wrappers (andview, dev)
  ↓
Optionally creates menu shortcut
```

## 🎯 Organization Patterns

### Python Code

- **Modularity**: Each class in its own file
- **Separation of Concerns**: 
  - `adb_manager.py` - only ADB
  - `scrcpy_manager.py` - only scrcpy  
  - `ui/` - only GUI
- **Type Hints**: Used in all functions
- **Docstrings**: All classes and functions documented

### Shell Scripts

- **Portability**: Compatible with bash
- **Validation**: Check dependencies before executing
- **Feedback**: Clear messages with emojis
- **Error Handling**: Appropriate exit codes

### Documentation

- **Hierarchy**: From general (README) to specific (DEV_GUIDE)
- **Markdown**: Consistent formatting
- **Examples**: Code and commands always with examples
- **Accessibility**: Clear language in English

## 🚀 Adding New Components

### New UI Widget

1. Create file in `src/ui/widgets/new_widget.py`
2. Import in `src/ui/widgets/__init__.py`
3. Use in `src/ui/main_window.py`

### New ADB Feature

1. Add method in `src/adb_manager.py`
2. Add button/action in `src/ui/widgets/control_panel.py`
3. Connect signal in `src/ui/main_window.py`

### New Script

1. Create script in `scripts/new_script.sh`
2. Make executable: `chmod +x scripts/new_script.sh`
3. (Optional) Create wrapper in root

### New Documentation

1. Create file in `docs/NEW_DOC.md`
2. Add link in README.md
3. Add link in START_HERE.md if important

## 📦 Build and Distribution

### AppImage Structure

When you create an AppImage with `./scripts/build_appimage.sh`:

```
build/
└── AppImage/
    ├── AndView.AppDir/          # Build directory
    │   ├── AppRun               # Execution script
    │   ├── andview.desktop      # Desktop file
    │   ├── andview.png          # Icon
    │   └── usr/
    │       ├── bin/             # Application code
    │       ├── lib/             # Python dependencies
    │       └── share/           # Resources
    │
    └── AndView-1.0.0-x86_64.AppImage  # Final AppImage
```

## 🔐 Ignored Files (.gitignore)

Not versioned:

- `venv/` - Virtual environment
- `__pycache__/` - Python cache
- `build/` - Build artifacts
- `*.pyc`, `*.pyo` - Python bytecode
- `.vscode/`, `.idea/` - IDE settings
- `*.log` - Logs
- `andview` (generated) - Generated wrapper script
- `*.AppImage` - Generated binaries

## 📊 Project Metrics

- **Python Lines of Code**: ~2000
- **Python Files**: 6
- **Shell Scripts**: 3
- **Documents**: 9
- **Python Dependencies**: 3 (PyQt5, PyQt5-Qt5, PyQt5-sip)
- **System Dependencies**: 2 (adb, scrcpy)

## 🔗 Dependencies

### Internal (between modules)

```
main.py
  └── ui/main_window.py
      ├── ui/widgets/device_list.py
      ├── ui/widgets/control_panel.py
      ├── adb_manager.py
      └── scrcpy_manager.py
```

### External

- **PyQt5** - GUI
- **adb** - Communication with Android
- **scrcpy** - Screen mirroring
- **Python 3.8+** - Runtime

## 📝 Conventions

### Naming

- **Python files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/methods**: `snake_case()`
- **Constants**: `UPPER_CASE`
- **Scripts**: `kebab-case.sh`

### Git

- **Branches**: `feature/feature-name`
- **Commits**: Descriptive messages in English
- **Tags**: `v1.0.0` (semantic versioning)

### Documentation

- **Files**: `UPPER_CASE.md`
- **Sections**: Headers with emojis
- **Code**: Always in blocks ```bash or ```python
- **Links**: Relative when possible

---

**Structure kept simple, clear and scalable! 🚀**
