# Creating AndView AppImage

This guide explains how to create an AppImage of AndView for distribution.

## What is AppImage?

AppImage is a universal package format for Linux that allows you to distribute applications as single executable files, without requiring installation.

## Prerequisites

### 1. Install appimagetool

```bash
# Download appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage

# Make it executable
chmod +x appimagetool-x86_64.AppImage

# Move to /usr/local/bin
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
```

### 2. Install ImageMagick (optional, to create icon)

```bash
# Ubuntu/Debian
sudo apt install imagemagick

# Fedora/Nobara
sudo dnf install ImageMagick

# Arch
sudo pacman -S imagemagick
```

## Creating the AppImage

### Automated Method (Recommended)

Run the build script:

```bash
./build_appimage.sh
```

The AppImage will be created in `build/AppImage/AndView-1.0.0-x86_64.AppImage`

> A versão atual do script empacota automaticamente Python, PySide6, `adb` e `scrcpy` 3.3.3 (com suas bibliotecas FFmpeg/SDL), garantindo que o AppImage funcione mesmo em sistemas sem essas dependências instaladas.

### Testing the AppImage

```bash
./build/AppImage/AndView-1.0.0-x86_64.AppImage
```

## AppImage Structure

```
AndView.AppDir/
├── AppRun                    # Main execution script
├── andview.desktop          # Desktop file (symbolic link)
├── andview.png             # Icon (symbolic link)
└── usr/
    ├── bin/
    │   ├── andview         # Wrapper script
    │   ├── main.py         # Main code
    │   └── src/            # Source code
    ├── lib/
    │   └── python-packages/  # Python dependencies
    └── share/
        ├── applications/
        │   └── andview.desktop
        └── icons/
            └── hicolor/256x256/apps/
                └── andview.png
```

## Customizing the Icon

To use a custom icon:

1. Create or get a 256x256 pixel PNG icon
2. Replace the file in:
   ```bash
   cp your-icon.png build/AppImage/AndView.AppDir/usr/share/icons/hicolor/256x256/apps/andview.png
   ```
3. Rebuild the AppImage

## Distribution

### 1. Upload to GitHub Releases

```bash
# After creating a release on GitHub
gh release upload v1.0.0 build/AppImage/AndView-1.0.0-x86_64.AppImage
```

### 2. AppImageHub

To list on AppImageHub:
1. Fork the repository: https://github.com/AppImage/appimage.github.io
2. Add your AppImage in `database/`
3. Create a pull request

### 3. Direct Distribution

Simply share the `.AppImage` file. Users can:

```bash
# Download
wget https://your-site.com/AndView-1.0.0-x86_64.AppImage

# Make executable
chmod +x AndView-1.0.0-x86_64.AppImage

# Run
./AndView-1.0.0-x86_64.AppImage
```

## System Integration

To integrate the AppImage into the application menu:

### Option 1: AppImageLauncher (Recommended)

Install AppImageLauncher which does the integration automatically:

```bash
# Ubuntu/Debian
sudo add-apt-repository ppa:appimagelauncher-team/stable
sudo apt update
sudo apt install appimagelauncher

# Other distros: download from GitHub
# https://github.com/TheAssassin/AppImageLauncher/releases
```

### Option 2: Manual

```bash
# Copy to ~/Applications
mkdir -p ~/Applications
cp AndView-1.0.0-x86_64.AppImage ~/Applications/

# Create desktop file
cat > ~/.local/share/applications/andview.desktop << EOF
[Desktop Entry]
Type=Application
Name=AndView
Comment=GUI for scrcpy and ADB
Exec=$HOME/Applications/AndView-1.0.0-x86_64.AppImage
Icon=phone
Categories=Utility;Development;
Terminal=false
EOF
```

## Updates

To create a new version:

1. Update version in `build_appimage.sh`
2. Run `./build_appimage.sh`
3. Distribute the new AppImage

## Troubleshooting

### Error: "cannot open shared object file"

O AppImage inclui `adb` e `scrcpy` (v3.3.3), portanto não é necessário instalá-los no sistema hospedeiro.

### Error on run: "No such file or directory"

```bash
# Make sure the AppImage is executable
chmod +x AndView-1.0.0-x86_64.AppImage

# Check if FUSE is installed
sudo apt install fuse libfuse2  # Ubuntu/Debian
```

### AppImage too large

To reduce size:

1. Use `--no-cache-dir` when installing Python packages
2. Remove unnecessary files (.pyc, __pycache__)
3. Use compression:
   ```bash
   appimagetool --comp gzip AndView.AppDir
   ```

## Additional Resources

- [AppImage Documentation](https://docs.appimage.org/)
- [AppImageKit GitHub](https://github.com/AppImage/AppImageKit)
- [Best Practices](https://github.com/AppImage/AppImageSpec/blob/master/draft.md)
