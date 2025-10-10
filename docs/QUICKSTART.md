# Quick Start - AndView

## Quick Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd AndView
```

### 2. Run the installer
```bash
chmod +x install.sh
./install.sh
```

The installer will:
- ✅ Check dependencies
- ✅ Offer to install ADB and scrcpy (if needed)
- ✅ Create Python virtual environment
- ✅ Install Python dependencies
- ✅ Create execution script
- ✅ Create menu shortcut (optional)

### 3. Run the application
```bash
./andview
```

Or manually:
```bash
source venv/bin/activate
python3 main.py
```

## Preparing Your Android Device

### 1. Enable Developer Options
1. Go to **Settings** > **About phone**
2. Tap 7 times on **Build number**
3. Return to Settings
4. Enter **Developer options**

### 2. Enable USB Debugging
1. In **Developer options**
2. Enable **USB debugging**

### 3. Connect via USB
1. Connect the device to the computer via USB
2. On the device, authorize the computer when prompted
3. Check "Always allow from this computer"

## Using AndView

### Basic Mirroring
1. Connect your device
2. Select the device in the left list
3. Click "▶️ Start Mirroring"

### Installing APKs
1. Go to the "🛠️ Tools" tab
2. Click "📁 Browse" and select the APK
3. Click "📦 Install APK"

### Capturing Screenshots
1. Go to the "🛠️ Tools" tab
2. Click "📸 Capture Screenshot"
3. Choose where to save

### Running Commands
1. Go to the "⌨️ Commands" tab
2. Type the shell command (e.g., `ls /sdcard/`)
3. Press Enter or click "▶️ Execute"

## Quality Presets

- **Default**: Balanced configuration
- **High Quality**: Best visual quality (more resources)
- **Performance**: Best performance (fewer resources)
- **Low Latency**: Lowest possible delay
- **Recording**: Optimized for video recording

## Keyboard Shortcuts

- `F5` - Refresh device list
- `Ctrl+S` - Capture screenshot
- `Ctrl+Q` - Exit

## Common Problems

### "ADB not found"
```bash
# Ubuntu/Debian
sudo apt install android-tools-adb

# Fedora/Nobara
sudo dnf install android-tools

# Arch
sudo pacman -S android-tools
```

### "scrcpy not found"
```bash
# Ubuntu/Debian
sudo apt install scrcpy

# Fedora/Nobara
sudo dnf install scrcpy

# Arch
sudo pacman -S scrcpy
```

### Device doesn't appear
1. Check if USB debugging is enabled
2. Try another USB cable
3. Run `adb kill-server && adb start-server` in terminal
4. Click "🔄 Refresh" in AndView

### Black screen in scrcpy
1. Unlock the device screen
2. Disable screen saver
3. Check if no other apps are using the screen

## More Help

For complete documentation, see [README.md](README.md)
