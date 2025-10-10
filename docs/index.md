---
layout: default
title: AndView
description: Mirror and control your Android device from Linux - No dependencies required!
---

# 📱 AndView

**Mirror and control your Android device from Linux - Zero dependencies!**

![AndView Logo]({{ '/assets/logo.png' | relative_url }}){: .logo}

## 🎯 What is AndView?

AndView is a modern, user-friendly GUI application that allows you to mirror and control your Android device directly from your Linux desktop. Built with PySide6, it provides an intuitive interface for Android device management.

### ✨ Key Features

- 🖥️ **Screen Mirroring** - View your Android screen on Linux
- 📱 **Device Control** - Use your mouse/keyboard to control Android
- 📦 **APK Installation** - Install apps directly from your desktop
- 📸 **Screenshot Capture** - Take screenshots with one click
- 🔧 **ADB Shell** - Execute commands directly on your device
- 📊 **Device Info** - View detailed device information
- 🎛️ **Quality Presets** - Optimize mirroring for your needs

## 🚀 Quick Start

### 1. Download the AppImage

Get the latest release from our [releases page]({{ '/releases' | relative_url }}):

```bash
# Download the latest AppImage
wget https://github.com/satodu/AndView/releases/latest/download/AndView-x86_64.AppImage

# Make it executable
chmod +x AndView-x86_64.AppImage

# Run it
./AndView-x86_64.AppImage
```

### 2. Enable USB Debugging

Before connecting your Android device, you need to enable Developer Options and USB Debugging:

1. Go to **Settings** → **About Phone**
2. Tap **Build Number** 7 times
3. Go back to **Settings** → **Developer Options**
4. Enable **USB Debugging**
5. Connect your device via USB

## 🎊 Why AndView?

### ✅ **100% Independent**
- No Python installation required
- No PyQt5/PySide6 dependencies
- No ADB or scrcpy setup needed
- Everything is bundled in the AppImage!

### ✅ **Always Up-to-Date**
- Includes latest scrcpy v3.3.3
- Latest ADB tools
- Modern PySide6 GUI framework

### ✅ **Cross-Distribution**
- Works on Ubuntu, Fedora, Arch, openSUSE, etc.
- No package manager conflicts
- Portable and reliable

## 📖 Documentation

- 📚 [Quick Start Guide]({{ '/quickstart' | relative_url }})
- 🔧 [Troubleshooting]({{ '/troubleshooting' | relative_url }})
- 🛠️ [Development Guide]({{ '/development' | relative_url }})
- 📦 [Build Instructions]({{ '/build' | relative_url }})

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide]({{ '/contributing' | relative_url }}) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/satodu/AndView/blob/main/LICENSE) file for details.

## 🙏 Acknowledgments

- [scrcpy](https://github.com/Genymobile/scrcpy) - Screen mirroring tool
- [Android Debug Bridge (ADB)](https://developer.android.com/studio/command-line/adb) - Device communication
- [PySide6](https://doc.qt.io/qtforpython/) - GUI framework

---

**Open source, feito com ❤️ no Linux.**

*by [Panda](https://www.linkedin.com/in/eduardo-sato-panda)*
