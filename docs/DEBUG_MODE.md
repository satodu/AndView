# 🔧 How to Enable Debug Mode on Android

To use AndView, you **MUST** enable debug mode on your Android device. This guide shows how to do it step by step.

## ⚠️ Important

**Without debug mode enabled, AndView will not be able to:**
- ❌ Detect your device
- ❌ Connect via USB or WiFi
- ❌ Mirror the screen
- ❌ Execute ADB commands

## 📱 Step by Step

### 1. Enable Developer Options

1. **Open Android Settings**
2. **Go to "About phone"** or "About device"
3. **Find "Build number"** or "Software version"
4. **Tap 7 times** on the build number
5. You'll see the message: **"You are now a developer!"**

### 2. Enable USB Debugging

1. **Return to Settings**
2. **Look for "Developer options"** or "For developers"
3. **Enable the option** (may be in Advanced settings)
4. **Enable "USB debugging"**

### 3. Authorize the Computer

1. **Connect the device via USB** to the computer
2. **A notification will appear** on Android
3. **Tap the notification**
4. **Check "Always allow from this computer"**
5. **Tap "OK"** or "Allow"

## 🔍 How to Check if It's Working

### Via Terminal (Linux):

```bash
# Check if the device appears
adb devices

# Should show something like:
# List of devices attached
# ABC123DEF456    device
```

### Via AndView:

1. **Open AndView**
2. **Go to the "Devices" tab**
3. **Click "Refresh"**
4. **Your device should appear** in the list

## 🚨 Common Problems

### ❌ "Device doesn't appear"

**Solutions:**
- Check if USB debugging is enabled
- Reconnect the USB cable
- Try another USB cable
- Restart the Android device
- Restart the ADB service: `sudo adb kill-server && adb start-server`

### ❌ "Device appears as 'unauthorized'"

**Solutions:**
- Disconnect and reconnect the USB
- On Android, tap the notification and authorize again
- Check "Always allow from this computer"

### ❌ "ADB not found"

**Solutions:**
- Use the AppImage (includes ADB)
- Or install manually:
  ```bash
  # Ubuntu/Debian
  sudo apt install android-tools-adb
  
  # Fedora
  sudo dnf install android-tools
  
  # Arch Linux
  sudo pacman -S android-tools
  ```

## 📶 WiFi Connection (Optional)

After setting up via USB, you can connect via WiFi:

1. **Connect via USB first** (for setup)
2. **In AndView, go to the "WiFi" tab**
3. **Configure the WiFi connection**
4. **Disconnect the USB**
5. **Continue using via WiFi**

## 🔐 Security

### ⚠️ Important Warnings:

- **USB debugging** allows full access to the device
- **Only authorize trusted computers**
- **Disable when not using** AndView
- **Never leave debugging enabled** on production devices

### 🛡️ How to Disable:

1. **Settings → Developer options**
2. **Disable "USB debugging"**
3. **Or completely disable "Developer options"**

## 📱 Different Android Versions

### Android 11+ (latest):
- Options may be in **"System settings"**
- Look for **"Developer options"**

### Android 10 and earlier:
- Usually in **"About phone"**
- Then in **"Developer options"**

### Samsung:
- May be in **"Developer settings"**
- Or in **"Software information"**

### Xiaomi/MIUI:
- Look for **"Additional settings"**
- Or **"For developers"**

## 🆘 Still Not Working?

If it still doesn't work after following this guide:

1. **Check if the USB cable supports data** (not just charging)
2. **Try another USB cable**
3. **Restart the Android device**
4. **Restart the computer**
5. **Check for device-specific drivers**
6. **Consult the device-specific documentation**

## 📞 Support

- **GitHub Issues:** [AndView Issues](https://github.com/satodu/AndView/issues)
- **Complete documentation:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**💡 Tip:** Keep this guide saved! You'll need it whenever you connect a new device or after Android updates.
