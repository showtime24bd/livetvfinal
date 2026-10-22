# 📱 Mobile Access - Quick Visual Guide

## 🚀 3 Minute Setup

---

## Method 1: One-Click Setup ⚡ (Easiest)

### Step 1: Run Setup File
```
📁 Project Folder
   └─ 🖱️ Double-click: setup_mobile_quick.bat
```

**কি হবে:**
- ✅ আপনার IP automatically খুঁজবে
- ✅ Firewall rule create করবে  
- ✅ Flask app চালু করবে
- ✅ Mobile access URL দেখাবে

### Step 2: Copy the URL
```
Setup complete!

Access from Mobile/Android TV:
    http://192.168.1.100:5000
```

### Step 3: Open on Mobile
- Mobile browser open করুন
- URL paste করুন
- Done! 🎉

---

## Method 2: PowerShell Script (Advanced)

### Step 1: Right-click PowerShell
```
Windows Search → PowerShell
Right-click → "Run as Administrator"
```

### Step 2: Navigate & Run
```powershell
cd "C:\Users\Admin\Documents\live tv epg proxy"
.\setup_mobile_access.ps1
```

### Step 3: Follow On-Screen Instructions
Script automatically:
- ✅ Detects network
- ✅ Configures firewall
- ✅ Tests connectivity
- ✅ Provides access URL

---

## Method 3: Manual Setup (If Scripts Don't Work)

### Step 1: Find Your IP 🔍

**Open Command Prompt or PowerShell:**
```
Windows + R → cmd → Enter
```

**Type:**
```
ipconfig
```

**Look for:**
```
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.1.100
                                       ↑↑↑↑↑↑↑↑↑↑↑↑↑↑
                                       This is your IP!
```

**✏️ Write it down:** `192.168.1.___`

---

### Step 2: Open Firewall 🔥

**Method A: Using Command**

**Open PowerShell as Administrator:**
```
Windows Search → PowerShell
Right-click → Run as Administrator
```

**Copy & Paste this command:**
```powershell
New-NetFirewallRule -DisplayName "Flask Live TV" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

**Press Enter**

**Should see:**
```
Name                  : {GUID}
DisplayName           : Flask Live TV
Enabled               : True
```

---

**Method B: Using Windows GUI**

1. **Windows Search:** `Windows Defender Firewall`

2. **Click:** "Advanced settings" (left sidebar)

3. **Click:** "Inbound Rules" (left sidebar)

4. **Click:** "New Rule..." (right sidebar)

5. **Select:** "Port" → Next

6. **Select:** "TCP"
   - **Type:** `5000` in "Specific local ports"
   - **Click:** Next

7. **Select:** "Allow the connection" → Next

8. **Check ALL three:**
   - ☑️ Domain
   - ☑️ Private  
   - ☑️ Public
   - **Click:** Next

9. **Name:** `Flask Live TV` → Finish

✅ **Done!**

---

### Step 3: Start Flask App 🚀

**Navigate to project folder:**
```
cd "C:\Users\Admin\Documents\live tv epg proxy"
```

**Start app:**
```
python app.py
```

**Should see:**
```
* Running on http://0.0.0.0:5000
* Running on http://192.168.1.100:5000
```

**✅ Leave this window OPEN!**

---

### Step 4: Connect from Mobile 📱

**On your mobile device:**

1. **Connect to SAME Wi-Fi** as computer
   - Settings → Wi-Fi
   - Select same network

2. **Open Browser** (Chrome recommended)

3. **Type URL:**
   ```
   http://192.168.1.100:5000
   ```
   *(Replace with YOUR IP from Step 1)*

4. **Press Go/Enter**

5. **✅ Should load!**

---

## 🎯 Android TV Setup

### For Android TV / Smart TV:

1. **Open TV Browser**
   - Apps → Internet/Browser

2. **Use Remote to Type URL:**
   ```
   http://192.168.1.100:5000
   ```

3. **Bookmark it!** (for easy access)

4. **Use Remote Control:**
   - Number keys: Direct channel
   - Arrow keys: Navigate
   - Enter: Channel list
   - See full guide: `ANDROID_TV_REMOTE_GUIDE.md`

---

## 🔍 Verification Checklist

Test করুন যে সব ঠিক আছে:

### ✅ Computer Side:

- [ ] Flask app running (console window open)
- [ ] No error messages in console
- [ ] Firewall rule created
- [ ] Know your IP address

**Quick Test:**
```powershell
# Check Flask is running
netstat -ano | findstr ":5000"
# Should show: LISTENING

# Check firewall rule
Get-NetFirewallRule -DisplayName "Flask*"
# Should show: Enabled : True
```

### ✅ Mobile Side:

- [ ] Connected to same Wi-Fi
- [ ] Browser can access URL
- [ ] Homepage loads
- [ ] Can click channels
- [ ] Videos play

---

## ❌ Troubleshooting

### Problem: "This site can't be reached"

**Possible Causes:**

1. **❌ Different Wi-Fi Networks**
   
   **Fix:**
   - Check computer Wi-Fi: Settings → Network
   - Check mobile Wi-Fi: Settings → Wi-Fi
   - Must be SAME network name!

2. **❌ Firewall Blocking**
   
   **Fix:**
   - Re-run firewall command (Step 2)
   - Or temporarily disable to test:
   ```powershell
   Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False
   ```
   - If works, firewall was issue
   - Re-enable firewall:
   ```powershell
   Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
   ```
   - Then properly configure firewall rule

3. **❌ Flask Not Running**
   
   **Fix:**
   - Check console window still open
   - No error messages?
   - Restart: `python app.py`

4. **❌ Wrong IP Address**
   
   **Fix:**
   - Re-check IP: `ipconfig`
   - IPs can change on restart
   - Use exact IP from ipconfig

---

### Problem: "Connection Timed Out"

**Usually means:** Computer and mobile can't talk

**Fix:**

1. **Test Computer is Reachable**
   
   On mobile, install "Ping Tools" app:
   - Ping: `192.168.1.100` (your IP)
   - If fails → Network issue
   - If succeeds → Firewall issue

2. **Check Router AP Isolation**
   
   Some routers block device-to-device communication:
   - Login to router (usually `192.168.1.1`)
   - Look for "AP Isolation" or "Client Isolation"
   - Disable it
   - Save and restart router

3. **Check Antivirus**
   
   - Temporarily disable antivirus
   - Test mobile access
   - If works → antivirus was blocking
   - Add exception for port 5000

---

### Problem: Works for 5 Minutes Then Stops

**Cause:** Computer went to sleep or IP changed

**Fix:**

1. **Disable Sleep:**
   - Settings → System → Power & Sleep
   - Set "Sleep" to "Never" (while streaming)

2. **Set Static IP:**
   - Control Panel → Network → Adapter Settings
   - Right-click Wi-Fi → Properties
   - IPv4 → Properties
   - "Use the following IP address:"
   - IP: `192.168.1.100`
   - Subnet: `255.255.255.0`
   - Gateway: `192.168.1.1`
   - DNS: `8.8.8.8`
   - Save

---

### Problem: Video Plays on Computer But Not Mobile

**Possible Causes:**

1. **Mobile Browser Issue**
   
   **Try:**
   - Clear browser cache
   - Use Chrome/Firefox
   - Try incognito mode

2. **Stream Format Issue**
   
   **Check:**
   - Does video play on computer browser?
   - Try different channel
   - Some streams may be DRM protected

3. **Network Speed**
   
   **Test:**
   - Check mobile Wi-Fi signal strength
   - Try moving closer to router
   - Check internet speed

---

## 💡 Pro Tips

### 1. Create QR Code 📷

**Steps:**
1. Go to: https://www.qr-code-generator.com/
2. Enter URL: `http://192.168.1.100:5000`
3. Generate QR code
4. Print it
5. Scan from mobile → Instant access!

### 2. Create Phone Shortcut 📱

**On Android:**
1. Open URL in Chrome
2. Menu (⋮) → "Add to Home screen"
3. Now it's like an app!

**On iOS:**
1. Open URL in Safari
2. Share button
3. "Add to Home Screen"

### 3. Auto-Start on Computer Boot 🖥️

**Create startup shortcut:**

1. Press `Windows + R`
2. Type: `shell:startup`
3. Create shortcut to `setup_mobile_quick.bat`
4. Now Flask starts automatically!

### 4. Keep Screen On (Mobile) 📱

**While watching:**
- Settings → Display → Screen timeout
- Set to "10 minutes" or more
- Or use "Stay awake" in Developer options

---

## 📊 Network Diagram

```
        🌐 Wi-Fi Router
        192.168.1.1
              |
      ________|________
      |               |
  💻 Computer    📱 Mobile
  192.168.1.100  192.168.1.150
      |               |
  🐍 Flask App ←→ 🌐 Browser
  Port 5000      http://...
```

**Requirements:**
- ✅ Same Wi-Fi network
- ✅ Computer running Flask
- ✅ Firewall allows port 5000
- ✅ No AP Isolation

---

## 🎓 Understanding the Setup

### Why 0.0.0.0?

```python
app.run(host='0.0.0.0', port=5000)
```

**Means:**
- Listen on ALL network interfaces
- Accessible from other devices
- Not just `localhost` (127.0.0.1)

### Why Firewall Rule?

**Without rule:**
- Windows blocks incoming connections
- Mobile can't reach Flask app
- Security feature

**With rule:**
- Allows port 5000 specifically
- Other ports still protected
- Safe for home network

### Why Same Wi-Fi?

**Network routing:**
- Devices on same Wi-Fi can talk
- Different networks = isolated
- Router manages local IPs

---

## ✅ Success Indicators

**You'll know it's working when:**

1. **Console shows:**
   ```
   * Running on http://0.0.0.0:5000
   192.168.1.150 - - [timestamp] "GET / HTTP/1.1" 200
   ```
   *(Mobile IP shows in logs)*

2. **Mobile shows:**
   - Homepage loads
   - Channel list visible
   - Videos clickable

3. **Playback:**
   - Video player appears
   - Stream starts playing
   - Controls work

**🎉 Congratulations! You're streaming!**

---

## 📞 Still Need Help?

### Files to Check:

1. **`NETWORK_SETUP_GUIDE.md`** - Detailed troubleshooting
2. **`ANDROID_TV_REMOTE_GUIDE.md`** - Remote control help
3. **Console logs** - Error messages
4. **Flask debug output** - Connection attempts

### Run Diagnostic:

```powershell
# All-in-one check
.\setup_mobile_access.ps1
```

Shows:
- ✅ IP address
- ✅ Flask status
- ✅ Firewall status
- ✅ Network profile
- ✅ Port availability

---

## 🎬 Video Tutorial (Manual Steps)

**If you prefer video tutorial:**

1. Screen record yourself following this guide
2. Or follow along with screenshots
3. Pause at each step
4. Verify before proceeding

**Key screenshots to take:**
- [ ] ipconfig output (IP address)
- [ ] Firewall rule creation
- [ ] Flask console (running)
- [ ] Mobile browser (loaded page)

---

**Happy Streaming!** 📺✨📱

---

## Quick Reference Commands

```powershell
# Find IP
ipconfig

# Create Firewall Rule
New-NetFirewallRule -DisplayName "Flask Live TV" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow

# Start Flask
python app.py

# Check Flask Running
netstat -ano | findstr ":5000"

# Test Port
Test-NetConnection -ComputerName localhost -Port 5000

# Get Firewall Rules
Get-NetFirewallRule -DisplayName "Flask*"

# Disable Firewall (TEST ONLY)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# Enable Firewall (IMPORTANT)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

**Copy-paste এই commands সরাসরি PowerShell এ!**
