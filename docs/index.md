---
layout: default
title: AndView
description: Mirror and control your Android device from Linux - No dependencies required!
---

<div class="hero">
  <img src="{{ '/assets/logo.png' | relative_url }}" alt="AndView Logo" class="logo">
  <h1>📱 AndView</h1>
  <p class="description">Mirror and control your Android device from Linux<br><strong>Zero dependencies required!</strong></p>
</div>

## 🎯 What is AndView?

AndView is a modern, user-friendly GUI application that allows you to mirror and control your Android device directly from your Linux desktop. Built with PySide6, it provides an intuitive interface for Android device management.

<div class="features">
  <div class="feature-card">
    <h3>🖥️ Screen Mirroring</h3>
    <ul>
      <li>Real-time Android screen display</li>
      <li>High-quality video streaming</li>
      <li>Multiple quality presets</li>
      <li>Low latency performance</li>
    </ul>
  </div>

  <div class="feature-card">
    <h3>📱 Device Control</h3>
    <ul>
      <li>Mouse and keyboard control</li>
      <li>Touch gestures support</li>
      <li>Volume and power buttons</li>
      <li>File drag & drop</li>
    </ul>
  </div>

  <div class="feature-card">
    <h3>🔧 Advanced Features</h3>
    <ul>
      <li>APK installation via GUI</li>
      <li>Instant screenshot capture</li>
      <li>ADB shell integration</li>
      <li>Device information display</li>
    </ul>
  </div>
</div>

<div class="download-section">
  <h2>🚀 Ready to Start?</h2>
  <p>Download the latest version and start mirroring in seconds!</p>
  <a href="https://github.com/satodu/AndView/releases/latest/download/AndView-x86_64.AppImage" class="download-button">
    📥 Download Latest Release
  </a>
  <a href="{{ '/releases' | relative_url }}" class="download-button">
    📋 View All Releases
  </a>
</div>

## ⚡ Quick Setup

### 1. Download & Run

```bash
# Download the latest AppImage
wget https://github.com/satodu/AndView/releases/latest/download/AndView-x86_64.AppImage

# Make it executable and run
chmod +x AndView-x86_64.AppImage
./AndView-x86_64.AppImage
```

### 2. Enable USB Debugging

Before connecting your Android device:

1. **Settings** → **About Phone** → Tap **Build Number** 7 times
2. **Settings** → **Developer Options** → Enable **USB Debugging**
3. Connect your device via USB cable
4. Allow USB debugging when prompted on your phone

## 🎊 Why Choose AndView?

<div class="features">
  <div class="feature-card">
    <h3>🚀 100% Independent</h3>
    <ul>
      <li>No Python installation required</li>
      <li>No system dependencies</li>
      <li>Everything bundled in AppImage</li>
      <li>Works out of the box</li>
    </ul>
  </div>

  <div class="feature-card">
    <h3>⚡ Always Latest</h3>
    <ul>
      <li>Includes scrcpy v3.3.3</li>
      <li>Latest ADB tools</li>
      <li>Modern PySide6 GUI</li>
      <li>Regular updates</li>
    </ul>
  </div>

  <div class="feature-card">
    <h3>🌍 Universal Compatibility</h3>
    <ul>
      <li>Works on any Linux distro</li>
      <li>No package conflicts</li>
      <li>Portable and reliable</li>
      <li>No root access needed</li>
    </ul>
  </div>
</div>

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
