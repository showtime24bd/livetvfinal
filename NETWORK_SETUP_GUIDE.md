# 🌐 Mobile/Android TV Network Access Setup Guide

## সমস্যা: Mobile বা Android TV তে Local IP দিয়ে website access হচ্ছে না

---

## ✅ Solution Steps

### Step 1: আপনার Computer এর Local IP খুঁজুন

#### Windows PowerShell এ:
```powershell
ipconfig
```

**দেখুন:**
```
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.1.100
```

অথবা:
```
Ethernet adapter Ethernet:
   IPv4 Address. . . . . . . . . . . : 192.168.0.105
```

> 💡 আপনার IP হবে `192.168.x.x` অথবা `10.0.x.x` format এ

---

### Step 2: Windows Firewall Configure করুন

#### Option A: Quick Method (Recommended)
PowerShell **Administrator** হিসেবে চালু করুন এবং এই command run করুন:

```powershell
# Port 5000 এর জন্য inbound rule create করুন
New-NetFirewallRule -DisplayName "Flask Live TV App" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow

# Verify করুন rule created হয়েছে
Get-NetFirewallRule -DisplayName "Flask Live TV App"
```

#### Option B: GUI Method

1. **Windows Security** open করুন
2. **Firewall & network protection** এ যান
3. **Advanced settings** click করুন
4. **Inbound Rules** → **New Rule** click করুন
5. **Port** select করুন → **Next**
6. **TCP** select করুন
7. **Specific local ports** select করুন → `5000` লিখুন → **Next**
8. **Allow the connection** select করুন → **Next**
9. সব profiles (Domain, Private, Public) check করুন → **Next**
10. Name দিন: `Flask Live TV` → **Finish**

---

### Step 3: Network Verification

#### Check করুন same Wi-Fi network এ আছেন কিনা:

**Computer এ:**
```powershell
ipconfig | findstr "IPv4"
```

**Mobile এ:**
- Settings → Wi-Fi → Connected network এর details দেখুন
- IP address যদি same subnet এ থাকে (e.g., `192.168.1.x`)

> ⚠️ **Important:** Computer এবং Mobile/TV **same Wi-Fi network** এ থাকতে হবে!

---

### Step 4: Flask App Properly চালু করুন

#### Method 1: Direct Python
```powershell
python app.py
```

Output দেখবেন:
```
* Running on http://0.0.0.0:5000
* Running on http://192.168.1.100:5000
```

#### Method 2: Using run.py
```powershell
python run.py
```

---

### Step 5: Mobile/Android TV থেকে Access করুন

**Browser এ open করুন:**
```
http://192.168.1.100:5000
```

> 🔴 **Replace করুন:** `192.168.1.100` আপনার actual IP দিয়ে

---

## 🔍 Troubleshooting

### Problem 1: "Site can't be reached"

**Solution:**
```powershell
# Test করুন port open আছে কিনা
Test-NetConnection -ComputerName localhost -Port 5000
```

Expected output:
```
TcpTestSucceeded : True
```

যদি `False` হয়:
- App চালু আছে কিনা check করুন
- Port 5000 অন্য কিছু use করছে কিনা check করুন

**Port check:**
```powershell
netstat -ano | findstr :5000
```

### Problem 2: "Connection timed out"

**Causes:**
1. ❌ Different Wi-Fi networks
2. ❌ Firewall blocking
3. ❌ Router isolation enabled

**Solutions:**

#### A. Check Wi-Fi Network
```powershell
# Computer IP subnet
ipconfig

# দেখুন: 192.168.1.x নাকি 192.168.0.x নাকি 10.0.0.x?
```

Mobile এর IP same subnet এ আছে কিনা verify করুন।

#### B. Temporarily Disable Firewall (Test Only)
```powershell
# Disable Windows Firewall (Admin PowerShell)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# Test করুন mobile থেকে

# Re-enable Firewall (IMPORTANT!)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

> ⚠️ **Security Warning:** শুধুমাত্র testing এর জন্য disable করুন!

#### C. Check Router AP Isolation

কিছু routers "AP Isolation" বা "Client Isolation" enable করে রাখে।

**Fix:**
1. Router admin panel এ login করুন (`192.168.1.1` বা `192.168.0.1`)
2. Wireless settings খুঁজুন
3. "AP Isolation" / "Client Isolation" disable করুন
4. Save এবং router restart করুন

### Problem 3: "Refused to connect"

**Solution:**
```powershell
# Check app actually 0.0.0.0 এ running কিনা
netstat -ano | findstr :5000 | findstr LISTENING
```

Output should show:
```
TCP    0.0.0.0:5000    0.0.0.0:0    LISTENING    [PID]
```

If not, check `app.py` এ:
```python
app.run(host='0.0.0.0', port=5000)  # ✅ Correct
# NOT: app.run(host='localhost')     # ❌ Wrong
```

### Problem 4: Works on Computer but not Mobile

**Solution:**

1. **Antivirus Check**
   - Windows Defender
   - Third-party antivirus
   - Temporarily disable এবং test করুন

2. **Network Profile**
   ```powershell
   # Set network to Private
   Get-NetConnectionProfile
   Set-NetConnectionProfile -NetworkCategory Private
   ```

3. **Mobile Browser Cache**
   - Clear browser cache
   - Try incognito mode
   - Try different browser

---

## 🚀 Quick Test Commands

### One-Liner Setup (PowerShell Admin)
```powershell
# Create firewall rule
New-NetFirewallRule -DisplayName "Flask Live TV" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow; python app.py
```

### Network Test Script
Save as `test_network.ps1`:

```powershell
# Get Computer IP
$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"}).IPAddress
Write-Host "Your IP: $ip" -ForegroundColor Green

# Check Flask is running
$flaskRunning = Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue
if ($flaskRunning) {
    Write-Host "✅ Flask app is running on port 5000" -ForegroundColor Green
} else {
    Write-Host "❌ Flask app is NOT running" -ForegroundColor Red
}

# Check Firewall Rule
$firewallRule = Get-NetFirewallRule -DisplayName "Flask Live TV*" -ErrorAction SilentlyContinue
if ($firewallRule) {
    Write-Host "✅ Firewall rule exists" -ForegroundColor Green
} else {
    Write-Host "❌ Firewall rule NOT found" -ForegroundColor Red
    Write-Host "Creating firewall rule..." -ForegroundColor Yellow
    New-NetFirewallRule -DisplayName "Flask Live TV" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
}

Write-Host "`nAccess from mobile: http://${ip}:5000" -ForegroundColor Cyan
```

**Run করুন:**
```powershell
powershell -ExecutionPolicy Bypass -File test_network.ps1
```

---

## 📱 Mobile Browser Testing

### Recommended Browsers:
1. ✅ **Chrome** (Best compatibility)
2. ✅ **Firefox**
3. ✅ **Edge**
4. ⚠️ Safari (iOS - may have issues)

### Test URL Format:
```
http://[YOUR_COMPUTER_IP]:5000
```

**Examples:**
- `http://192.168.1.100:5000`
- `http://192.168.0.105:5000`
- `http://10.0.0.50:5000`

> 🚫 **DO NOT USE:**
> - `localhost:5000` ❌
> - `127.0.0.1:5000` ❌
> - `https://...` ❌ (no HTTPS setup)

---

## 🔐 Security Considerations

### For Home Network:
✅ Safe to use `0.0.0.0` binding
✅ Firewall allows local network only

### For Public Network:
⚠️ Be careful exposing port 5000
⚠️ Use strong admin password
⚠️ Consider VPN for remote access

### Production Deployment:
```python
# Use environment variable
app.run(
    host=os.getenv('HOST', '0.0.0.0'),
    port=int(os.getenv('PORT', 5000)),
    debug=False  # Important for production!
)
```

---

## 🎯 Android TV Specific

### Smart TV Browser Access:

1. **LG WebOS TV:**
   - Built-in browser → Enter URL
   - May need to enable "Developer Mode"

2. **Samsung Tizen TV:**
   - Internet browser app → Enter URL
   - Ensure TV on same Wi-Fi

3. **Android TV:**
   - Chrome browser / Firefox
   - Or TV's built-in browser
   - URL: `http://192.168.x.x:5000`

### Testing on Android TV:

```
1. Open TV browser
2. Navigate to: http://[YOUR_IP]:5000
3. If works: Bookmark it!
4. Test remote controls
```

---

## 📊 Network Diagram

```
┌─────────────────┐
│   Wi-Fi Router  │
│  192.168.1.1    │
└────────┬────────┘
         │
         ├──────────────────┐
         │                  │
    ┌────▼─────┐      ┌────▼──────┐
    │ Computer │      │  Mobile   │
    │192.168.1.│      │192.168.1. │
    │   100    │      │   150     │
    │          │      │           │
    │ Flask    │◄────►│  Browser  │
    │ :5000    │ HTTP │           │
    └──────────┘      └───────────┘
```

---

## ✅ Success Checklist

- [ ] Computer IP খুঁজেছি (192.168.x.x)
- [ ] Firewall rule create করেছি
- [ ] Flask app `0.0.0.0:5000` এ running
- [ ] Computer এবং Mobile same Wi-Fi এ
- [ ] Mobile browser এ `http://[IP]:5000` test করেছি
- [ ] Page load হচ্ছে
- [ ] Video play হচ্ছে

---

## 🆘 Still Not Working?

### Advanced Debugging:

#### 1. Ping Test (Mobile)
Install "Network Tools" app on mobile:
```
Ping: 192.168.1.100
```
যদি successful হয়, network connectivity OK।

#### 2. Port Scan (Computer)
```powershell
# Check what's listening on port 5000
Get-NetTCPConnection -LocalPort 5000 | Format-Table -AutoSize
```

#### 3. Verbose Flask Logging
In `app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

app.run(host='0.0.0.0', port=5000, debug=True)
```

Check console for connection attempts from mobile.

#### 4. Alternative Port
যদি port 5000 কাজ না করে:
```python
app.run(host='0.0.0.0', port=8080)  # Try different port
```

Then firewall rule update করুন:
```powershell
New-NetFirewallRule -DisplayName "Flask 8080" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
```

---

## 💡 Pro Tips

### 1. Create Desktop Shortcut (Computer)
Save as `Start_LiveTV.bat`:
```batch
@echo off
echo Starting Live TV Server...
python "C:\Users\Admin\Documents\live tv epg proxy\app.py"
pause
```

### 2. Create QR Code for Easy Mobile Access
Use online QR generator:
- URL: `http://192.168.1.100:5000`
- Print QR code
- Scan from mobile!

### 3. Static IP (Optional)
Set static IP on your computer:
- Control Panel → Network → Change Adapter Settings
- Right-click Wi-Fi → Properties
- IPv4 → Properties
- Use static IP (e.g., 192.168.1.100)

Benefits: IP won't change, consistent access

---

## 📞 Need More Help?

Common issues এবং solutions:

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Page not found | Wrong IP/Port | Double-check IP with `ipconfig` |
| Connection timeout | Firewall | Create firewall rule |
| Refused connection | App not running | Start `python app.py` |
| Works 5 min then stops | IP changed | Use static IP |
| Different Wi-Fi | Network mismatch | Connect to same Wi-Fi |

---

**এখন mobile access করতে পারবেন!** 📱✨
