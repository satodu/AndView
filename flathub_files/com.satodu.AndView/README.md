# AndView

Android Device Manager with WiFi Connection Support

## Description

AndView is a modern GUI for managing Android devices using ADB and scrcpy. It provides an intuitive interface for developers and users who need to interact with Android devices from their desktop.

## Features

- Device list and management
- WiFi connection support  
- Screen mirroring with scrcpy
- Quality settings and options
- Multi-language support
- Modern Qt interface

## Screenshots

Please add screenshots to the `screenshots/` directory:
- `1.png` - Main interface
- `2.png` - Device list
- `3.png` - Settings

## Build Instructions

```bash
flatpak-builder --install-deps-from=flathub --repo=repo build com.satodu.AndView.yml
flatpak build-bundle repo com.satodu.AndView.flatpak com.satodu.AndView
```

## Installation

```bash
flatpak install --bundle com.satodu.AndView.flatpak
```
