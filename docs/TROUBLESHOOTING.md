# Troubleshooting - AndView

Troubleshooting guide for common issues.

## Installation Problems

### Error: "Python.h: No such file or directory"

**Cause**: Missing Python development tools.

**Solution**:

```bash
# Ubuntu/Debian
sudo apt install python3-dev build-essential

# Fedora/Nobara
sudo dnf install python3-devel gcc gcc-c++

# Arch/Manjaro
sudo pacman -S base-devel
```

Then run again:
```bash
./install.sh
```

### Error compiling PyQt5-sip

**Cause**: Missing compilers or development libraries.

**Solution**:

```bash
# Ubuntu/Debian
sudo apt install build-essential python3-dev

# Fedora/Nobara  
sudo dnf install gcc gcc-c++ python3-devel

# Arch/Manjaro
sudo pacman -S base-devel
```

### PyQt5 won't install

**Alternative**: Use the system repository version:

```bash
# Ubuntu/Debian
sudo apt install python3-pyqt5

# Fedora/Nobara
sudo dnf install python3-qt5

# Arch/Manjaro
sudo pacman -S python-pyqt5
```

Then, use system Python without venv:
```bash
python3 main.py
```

## ADB Problems

### ADB doesn't detect device

**Checks**:

1. **USB debugging enabled?**
   - Settings → Developer options → USB debugging

2. **Device authorized?**
   ```bash
   adb devices
   # Should show "device", not "unauthorized"
   ```
   
   If it shows "unauthorized", unlock the phone and accept.

3. **ADB server stuck?**
   ```bash
   adb kill-server
   adb start-server
   adb devices
   ```

4. **USB cable working?**
   - Try another cable
   - Test another USB port
   - Some cables are charge-only

5. **udev rules (Linux)?**
   ```bash
   # Create rules file
   sudo nano /etc/udev/rules.d/51-android.rules
   
   # Add (replace XXXX with your device's vendor ID):
   SUBSYSTEM=="usb", ATTR{idVendor}=="XXXX", MODE="0666", GROUP="plugdev"
   
   # Reload rules
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   
   # Reconnect the device
   ```
   
   Common vendor IDs:
   - Google: 18d1
   - Samsung: 04e8
   - Xiaomi: 2717
   - Motorola: 22b8
   - LG: 1004

### Permission denied when using ADB

**Solution**:

```bash
# Add your user to plugdev group
sudo usermod -aG plugdev $USER

# Logout and login again
```

### ADB very slow

**Solutions**:

1. Restart ADB server:
   ```bash
   adb kill-server
   adb start-server
   ```

2. Use another USB cable (prefer USB 3.0)

3. Disable other tools using ADB

## scrcpy Problems

### Black screen in scrcpy

**Causes and solutions**:

1. **Device screen locked**
   - Unlock the screen

2. **Screen saver active**
   - Disable temporarily

3. **App in foreground blocking**
   - Return to home screen

4. **Codec not supported**
   ```bash
   # Try with different codec
   scrcpy --video-codec=h264
   ```

5. **Resolution too high**
   - Use a lower resolution:
   ```bash
   scrcpy -m 1024
   ```

### scrcpy freezing/lagging

**Solutions**:

1. **Reduce resolution**:
   - In AndView: use "Performance" preset
   - Or set max resolution: 720

2. **Reduce bitrate**:
   - Try 4M or 2M

3. **Reduce FPS**:
   - Set to 30 FPS

4. **Use USB cable**:
   - Wireless connection has more latency

5. **Close other applications**:
   - Free resources on PC and phone

### Audio doesn't work

**Note**: Audio in scrcpy requires version 2.0+

**Check**:
```bash
scrcpy --version
```

**If version < 2.0**:
```bash
# Ubuntu/Debian (may need PPA)
sudo add-apt-repository ppa:sicklylife/scrcpy
sudo apt update
sudo apt install scrcpy

# Fedora/Nobara
sudo dnf update scrcpy

# Arch
sudo pacman -Syu scrcpy
```

### scrcpy doesn't connect via WiFi

**Steps**:

1. **Connect first via USB**

2. **Configure TCP/IP port**:
   ```bash
   adb tcpip 5555
   ```

3. **Find device IP**:
   - Settings → About → Status → IP address
   - Or: `adb shell ip addr show wlan0`

4. **Connect**:
   ```bash
   adb connect 192.168.1.XXX:5555
   ```

5. **Disconnect USB and use scrcpy**

**Issues**:
- Computer and phone must be on the same network
- Some routers block communication between devices
- Firewall may be blocking

## GUI Problems

### AndView doesn't open

**Checks**:

1. **PyQt5 installed?**
   ```bash
   python3 -c "import PyQt5"
   ```

2. **Virtual environment activated?**
   ```bash
   source venv/bin/activate
   python3 main.py
   ```

3. **Run with debug**:
   ```bash
   ./dev.sh --debug
   ```

### Error: "cannot import name 'MainWindow'"

**Solution**:
```bash
# Clean compiled files
./dev.sh --clean

# Or manually
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Run again
./dev.sh
```

### GUI too small/large

**Solution**: Edit `main.py` and adjust window size:

```python
self.setGeometry(100, 100, 1400, 800)  # Width, height
```

### Font too small

**Solution**: Adjust DPI in Qt:

```python
# In main.py, before creating the window
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1.5"  # Adjust as needed
```

## AppImage Problems

### "cannot open shared object file"

**Cause**: Missing system library.

**Solution**:
```bash
# Install FUSE for AppImage
sudo apt install fuse libfuse2  # Ubuntu/Debian
sudo dnf install fuse fuse-libs  # Fedora/Nobara
```

### AppImage doesn't run

**Checks**:

1. **Is it executable?**
   ```bash
   chmod +x AndView-*.AppImage
   ```

2. **FUSE installed?**
   ```bash
   sudo apt install fuse libfuse2
   ```

3. **Run manually**:
   ```bash
   ./AndView-*.AppImage --appimage-extract-and-run
   ```

### AppImage too large

**To reduce size**:

1. Edit `build_appimage.sh`
2. Add compression:
   ```bash
   appimagetool --comp gzip AndView.AppDir
   ```

## Performance Problems

### High CPU usage

**Causes**:

1. **Automatic device updates**
   - Normal, updates every 5 seconds
   - To disable, edit `main_window.py` and comment:
   ```python
   # self.update_timer.start(5000)
   ```

2. **scrcpy in high quality**
   - Use "Performance" preset
   - Reduce resolution and FPS

### High memory usage

**Solutions**:

1. Close and reopen the application periodically
2. Don't keep multiple windows open
3. Use lower resolution in scrcpy

## Other Problems

### Code changes don't appear

```bash
# Clean Python cache
./dev.sh --clean

# Recreate virtual environment
rm -rf venv
./install.sh
```

### Import error

```bash
# Make sure you're in the correct directory
cd /home/panda/Projects/satodu/AndView

# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### AndView freezes

**Possible causes**:

1. **Long ADB operation**
   - Installing large APK
   - Normal, wait

2. **scrcpy stuck**
   - Close scrcpy manually
   - Click "Stop"

3. **Device disconnected**
   - Reconnect
   - Click "Refresh"

## Getting More Help

If the problem persists:

1. **See the logs**:
   ```bash
   ./dev.sh --debug 2>&1 | tee andview.log
   ```

2. **Test components individually**:
   ```bash
   adb devices       # Test ADB
   scrcpy --version  # Test scrcpy
   python3 -c "import PyQt5"  # Test PyQt5
   ```

3. **Open an issue** on GitHub with:
   - Problem description
   - Steps to reproduce
   - Complete error log
   - Operating system and versions:
     ```bash
     uname -a
     python3 --version
     adb version
     scrcpy --version
     ```

4. **Ask the community**:
   - Reddit: r/linux
   - Your distro forums
   - Stack Overflow
