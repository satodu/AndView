# Build Guide - AndView

This guide explains how to generate AndView distribution packages (AppImage and Flatpak).

## Prerequisites

### For AppImage:
- `appimagetool` - Tool to create AppImages
- Python 3.8+
- Project dependencies (PyQt5, psutil, etc.)

### For Flatpak:
- `flatpak` and `flatpak-builder`
- Python 3.8+
- KDE Platform SDK

## Installing Tools

### Ubuntu/Debian:
```bash
# AppImage
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool

# Flatpak
sudo apt install flatpak flatpak-builder
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.kde.Platform//5.15-22.08
flatpak install flathub org.kde.Sdk//5.15-22.08
```

### Fedora:
```bash
# AppImage
sudo dnf install appimagetool

# Flatpak
sudo dnf install flatpak flatpak-builder
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.kde.Platform//5.15-22.08
flatpak install flathub org.kde.Sdk//5.15-22.08
```

### Arch Linux:
```bash
# AppImage
sudo pacman -S appimagetool

# Flatpak
sudo pacman -S flatpak flatpak-builder
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.kde.Platform//5.15-22.08
flatpak install flathub org.kde.Sdk//5.15-22.08
```

## Generating Packages

### Complete Build (Recommended):
```bash
./scripts/build_all.sh
```

### Individual Build:

#### AppImage only:
```bash
./scripts/build_appimage.sh
```

#### Flatpak only:
```bash
./scripts/build_flatpak.sh
```

## Generated Files

After a successful build, the following files will be created:

- **AppImage**: `scripts/build/AppImage/AndView-1.0.0-x86_64.AppImage`
- **Flatpak**: `build/flatpak/AndView.flatpak`

## Testing Packages

### AppImage:
```bash
./scripts/build/AppImage/AndView-1.0.0-x86_64.AppImage
```

### Flatpak:
```bash
# Install
flatpak install --bundle build/flatpak/AndView.flatpak

# Run
flatpak run com.satodu.AndView

# Uninstall
flatpak uninstall com.satodu.AndView
```

## Distribution

### GitHub Releases:
1. Go to the releases page on GitHub
2. Create a new release
3. Upload the `.AppImage` and `.flatpak` files

### Flathub (Flatpak):
To submit Flatpak to Flathub:
1. Fork the [flathub](https://github.com/flathub/flathub) repository
2. Add the `com.satodu.AndView.yml` file to the `flathub/` folder
3. Create a pull request

## Troubleshooting

### AppImage doesn't run:
- Check if it has execution permission: `chmod +x AndView-*.AppImage`
- Check system dependencies (ADB, scrcpy)

### Flatpak fails to build:
- Check if KDE SDK is installed
- Clean the cache: `flatpak-builder --repo=repo --force-clean build com.satodu.AndView.yml`

### Missing dependencies:
- Install necessary system dependencies
- For Ubuntu/Debian: `sudo apt install android-tools-adb scrcpy`
- For Fedora: `sudo dnf install android-tools scrcpy`
- For Arch: `sudo pacman -S android-tools scrcpy`

## File Structure

```
scripts/
├── build_all.sh          # Complete build
├── build_appimage.sh     # AppImage build
└── build_flatpak.sh      # Flatpak build

com.satodu.AndView.yml    # Flatpak manifest
com.satodu.AndView.desktop # Desktop file
com.satodu.AndView.png    # Icon
```

## Customization

To modify build settings:

- **AppImage**: Edit `scripts/build_appimage.sh`
- **Flatpak**: Edit `com.satodu.AndView.yml`

To change metadata (name, description, icon):
- Edit `com.satodu.AndView.desktop`
- Replace `com.satodu.AndView.png` with your icon
