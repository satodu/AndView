# Installation on Python 3.13

## About PyQt5 and Python 3.13

PyQt5 available on **PyPI (pip)** is not yet fully compatible with **Python 3.13**, presenting compilation errors. 

Therefore, this project has been configured to use **PyQt5 from the system repository**, which is already compiled and working perfectly with Python 3.13.

## ✅ Implemented Solution

Instead of using a virtual environment (venv) with PyQt5 from pip, AndView now:

1. **Uses system Python** (Python 3.13)
2. **Uses PyQt5 from repository** (installed via dnf/apt)
3. **Doesn't require virtual environment** (simpler!)

## 📦 Installation

### Fedora/Nobara (Python 3.13)

```bash
# 1. Install system PyQt5
sudo dnf install python3-qt5

# 2. Install ADB and scrcpy
sudo dnf install android-tools scrcpy

# 3. Run the project installer
./scripts/install.sh

# 4. Run the app
./andview
```

### Ubuntu/Debian

```bash
# 1. Install system PyQt5
sudo apt install python3-pyqt5

# 2. Install ADB and scrcpy
sudo apt install android-tools-adb scrcpy

# 3. Run the project installer
./scripts/install.sh

# 4. Run the app
./andview
```

### Arch/Manjaro

```bash
# 1. Install system PyQt5
sudo pacman -S python-pyqt5

# 2. Install ADB and scrcpy
sudo pacman -S android-tools scrcpy

# 3. Run the project installer
./scripts/install.sh

# 4. Run the app
./andview
```

## 🔍 Verifying Installation

To verify if PyQt5 is installed correctly:

```bash
python3 -c "from PyQt5.QtCore import PYQT_VERSION_STR; print('PyQt5:', PYQT_VERSION_STR)"
```

Should show something like: `PyQt5: 5.15.11`

## ❓ Why not use venv?

### Before (with venv and PyQt5 from pip):
```bash
python3 -m venv venv
source venv/bin/activate
pip install PyQt5  # ❌ Fails to compile on Python 3.13
```

**Typical error:**
```
error: assignment to 'sipSimpleWrapper *' from incompatible pointer type 'PyObject *'
error: command '/usr/bin/gcc' failed with exit code 1
```

### Now (without venv, system PyQt5):
```bash
sudo dnf install python3-qt5  # ✅ Already compiled!
python3 main.py                # ✅ Works directly!
```

## 🎯 Advantages of New Approach

✅ **Simpler** - No venv to manage  
✅ **Faster** - PyQt5 already compiled  
✅ **More reliable** - Package tested by distribution  
✅ **Compatible** - Works with Python 3.13  
✅ **Less space** - Doesn't duplicate PyQt5  

## 🔄 Migration from Old Versions

If you already had the project installed with venv:

```bash
# 1. Remove old virtual environment
rm -rf venv

# 2. Install system PyQt5
sudo dnf install python3-qt5

# 3. Done! Now it works directly
./andview
```

## 📝 Development

For development, the `./dev` script has been updated to work without venv:

```bash
./dev              # Runs normally
./dev --debug      # Debug mode
./dev --lint       # Code analysis
```

## 🚀 AppImage

The AppImage has also been updated to include system PyQt5.

```bash
./scripts/build_appimage.sh
```

The resulting AppImage will include PyQt5 and work on any Linux distribution.

## ⚠️ Important Notes

1. **Python 3.12 and earlier**: Also work with this approach
2. **Future PyQt5**: When pip's PyQt5 supports Python 3.13, we can go back to using venv if desired
3. **Other dependencies**: If you add other Python libs, you can install via pip without problems:
   ```bash
   # Global installation
   pip3 install --user package-name
   
   # Or create venv only for other dependencies
   python3 -m venv venv --system-site-packages
   ```

## 🆘 Problems?

If you encounter any errors:

1. Check if PyQt5 is installed:
   ```bash
   python3 -c "import PyQt5"
   ```

2. Check Python version:
   ```bash
   python3 --version
   ```

3. Reinstall system PyQt5:
   ```bash
   sudo dnf reinstall python3-qt5
   ```

4. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more solutions

---

**Configuration optimized for Python 3.13! 🎉**
