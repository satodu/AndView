# AndView - GUI for scrcpy and ADB

A modern Python GUI for managing Android devices using scrcpy and ADB (Android Debug Bridge).

## Credits

This project uses the following tools:

- **[scrcpy](https://github.com/Genymobile/scrcpy)** - Mirror Android devices
- **[ADB (Android Debug Bridge)](https://developer.android.com/studio/command-line/adb)** - Android Debug Bridge

Developed by **Eduardo Sato** ([@satodu](https://github.com/satodu))

## Features

- 🔍 Automatic detection of connected Android devices
- 📱 Screen mirroring with scrcpy
- 🎮 Remote device control
- 📊 Detailed device information
- 🔧 Common ADB operations (APK installation, screenshots, etc.)
- 🎨 Modern and intuitive interface with PyQt5

## Prerequisites

### Installation on Linux

1. **ADB (Android Debug Bridge)**
   ```bash
   sudo apt install android-tools-adb android-tools-fastboot  # Ubuntu/Debian
   # or
   sudo dnf install android-tools  # Fedora/Nobara
   ```

2. **scrcpy**
   ```bash
   sudo apt install scrcpy  # Ubuntu/Debian
   # or
   sudo dnf install scrcpy  # Fedora/Nobara
   ```

3. **Python 3.8+**
   ```bash
   python3 --version
   ```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AndView
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Normal Mode

1. Connect your Android device via USB
2. Enable USB debugging in developer options
3. Run the application:
   ```bash
   ./andview
   ```
   
   Or manually:
   ```bash
   source venv/bin/activate
   python3 main.py
   ```

### Development Mode

For testing during development:

```bash
./dev.sh              # Normal execution
./dev.sh --debug      # Debug mode
./dev.sh --verbose    # Verbose output
./dev.sh --lint       # Code analysis
./dev.sh --format     # Format code
./dev.sh --clean      # Clean temp files
./dev.sh --help       # Show help
```

## Features

- **Device List**: View all connected Android devices
- **Screen Mirroring**: Start scrcpy with different configuration options
- **Device Information**: Model, Android version, battery, etc.
- **APK Installation**: Drag and drop or select APKs to install
- **Screenshots**: Capture device screenshots
- **File Transfer**: Send and receive files from device
- **ADB Shell**: Execute custom ADB commands

## Project Structure

```
AndView/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── README.md           # Documentation
├── src/
│   ├── __init__.py
│   ├── adb_manager.py  # ADB command management
│   ├── scrcpy_manager.py  # scrcpy management
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py  # Main window
│       └── widgets/
│           ├── __init__.py
│           ├── device_list.py
│           └── control_panel.py
└── resources/
    └── icons/
```

## License

MIT License

## Creating AppImage

To create an AppImage for distribution:

1. Install `appimagetool`:
   ```bash
   wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
   chmod +x appimagetool-x86_64.AppImage
   sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
   ```

2. Run the build script:
   ```bash
   ./build_appimage.sh
   ```

3. The AppImage will be created in `build/AppImage/AndView-1.0.0-x86_64.AppImage`

See [APPIMAGE.md](APPIMAGE.md) for more details.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

Feel free to open issues or pull requests.
