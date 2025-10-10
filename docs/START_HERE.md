# 🚀 Start Here - AndView

Welcome to **AndView** - GUI for scrcpy and ADB!

## ⚡ Quick Start

### 1️⃣ First, install system dependencies

If you're on **Nobara/Fedora**, run:

```bash
# Install development tools (REQUIRED!)
sudo dnf install python3-devel gcc gcc-c++

# Install ADB and scrcpy
sudo dnf install android-tools scrcpy
```

### 2️⃣ Run the project installation

```bash
cd /home/panda/Projects/satodu/AndView
./scripts/install.sh
```

This will:
- ✅ Create Python virtual environment
- ✅ Install PyQt5 and dependencies
- ✅ Create execution script
- ✅ (Optional) Create menu shortcut

### 3️⃣ Run the application

```bash
./andview
```

## 🛠️ Development Mode

For testing and development:

```bash
# Normal dev mode execution
./dev.sh

# With debug enabled (shows more info)
./dev.sh --debug

# With verbose output
./dev.sh --verbose

# Check code (installs pylint if needed)
./dev.sh --lint

# Format code (installs black if needed)
./dev.sh --format

# Clean temporary files
./dev.sh --clean

# Install development tools
./dev.sh --install-dev

# See all options
./dev.sh --help
```

## 📦 Create AppImage (Future)

When you want to distribute the app as AppImage:

### 1. Install appimagetool

```bash
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
```

### 2. Build the AppImage

```bash
./scripts/build_appimage.sh
```

### 3. Test the AppImage

```bash
./build/AppImage/AndView-1.0.0-x86_64.AppImage
```

See [APPIMAGE.md](APPIMAGE.md) for complete details.

## 📚 Documentation

We've created several guides to help you:

### For End Users
- **[README.md](README.md)** - Project overview
- **[QUICKSTART.md](QUICKSTART.md)** - Quick usage guide
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Problem solving

### For Developers
- **[DEV_GUIDE.md](DEV_GUIDE.md)** - Complete development guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[APPIMAGE.md](APPIMAGE.md)** - How to create AppImage

### Others
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[LICENSE](LICENSE)** - MIT License

## 🎯 Project Structure

```
AndView/
├── main.py                    # ← Starts the application
├── src/
│   ├── adb_manager.py         # Manages ADB commands
│   ├── scrcpy_manager.py      # Manages scrcpy
│   └── ui/
│       ├── main_window.py     # Main window
│       └── widgets/
│           ├── device_list.py    # Device list
│           └── control_panel.py  # Control panel
│
├── dev.sh                     # ← Development script
├── install.sh                 # ← Installation script
├── build_appimage.sh          # ← Creates AppImage
│
└── [Documentation in .md]
```

## 🔧 Main Features

✅ **Automatic Detection** of Android devices
✅ **Screen Mirroring** with scrcpy (multiple presets)
✅ **APK Installation** via GUI
✅ **Screenshots Capture**
✅ **Integrated ADB Shell** console
✅ **Detailed Information** about the device

## 🎨 Quality Presets

- **Default**: Balanced configuration (8M bitrate)
- **High Quality**: Best visual (16M, 60 FPS, H265)
- **Performance**: Best performance (720p, 4M, 30 FPS)
- **Low Latency**: Lowest delay (1024p, 8M, 60 FPS, no audio)
- **Recording**: For video recording (16M, 60 FPS)

## 🐛 Common Issues

### Error installing PyQt5
```bash
# Install development tools
sudo dnf install python3-devel gcc gcc-c++
```

### Device doesn't appear
```bash
# Check if USB debugging is enabled
adb devices

# Restart ADB server if needed
adb kill-server
adb start-server
```

### scrcpy with black screen
- Unlock the device screen
- Return to home screen (exit apps)

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more solutions.

## 📱 Preparing Your Android Device

1. **Enable Developer Options**:
   - Settings → About phone
   - Tap 7 times on "Build number"

2. **Enable USB Debugging**:
   - Settings → Developer options
   - Enable "USB debugging"

3. **Connect via USB**:
   - Use a USB data cable (not just charging)
   - Authorize the computer when prompted
   - Check "Always allow"

## 💡 Tips

### Development
```bash
# Always use the dev script for testing
./dev

# Clean cache before testing important changes
./dev --clean
./dev

# Check code quality periodically
./dev --lint
./dev --format
```

### Performance
- Use "Performance" preset for slower devices
- Connect via USB for better quality (WiFi has more latency)
- Close other apps on Android to free resources

### Productivity
- Use `F5` to refresh device list
- Use `Ctrl+S` for quick screenshot
- Keep frequent commands saved to run in console

## 🤝 Contributing

Want to improve AndView?

1. Fork the project
2. Create a branch (`git checkout -b feature/MyFeature`)
3. Make your changes
4. Test with `./dev.sh --debug`
5. Commit (`git commit -m 'Add MyFeature'`)
6. Push (`git push origin feature/MyFeature`)
7. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📞 Need Help?

1. **Read the documentation** in the `.md` files
2. **See troubleshooting** in [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. **Run with debug** to see errors: `./dev.sh --debug`
4. **Open an issue** on GitHub with problem details

## 🎉 Next Steps

Now that you're set up:

1. ✅ Run `./scripts/install.sh` to set everything up
2. ✅ Connect your Android device
3. ✅ Run `./andview` and have fun!
4. ✅ For development, use `./dev`
5. ✅ In the future, create AppImage with `./scripts/build_appimage.sh`

**Happy coding! 🚀**

---

*AndView - GUI for scrcpy and ADB*  
*Developed with ❤️ using Python and PyQt5*
