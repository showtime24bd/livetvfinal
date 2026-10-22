# 🚀 Quick Start Guide

## শুরু করার আগে (Before Starting)

1. **Python installed আছে কিনা check করুন:**
   ```
   python --version
   ```
   (Python 3.8+ প্রয়োজন)

2. **Virtual environment তৈরি করুন (প্রথমবার only):**
   ```
   python -m venv venv
   ```

3. **Virtual environment activate করুন:**
   
   **PowerShell:**
   ```
   .\venv\Scripts\Activate.ps1
   ```
   
   **Command Prompt:**
   ```
   venv\Scripts\activate.bat
   ```

4. **Dependencies install করুন (প্রথমবার only):**
   ```
   pip install -r requirements.txt
   ```

## 🎯 Application চালানো (Start Application)

### সহজ পদ্ধতি (Easy Way):
Double-click করুন: **`start.bat`**

### Manual পদ্ধতি (Manual Way):
```bash
python run.py
```

## 🌐 Application Access করা

Application চালু হলে browser এ যান:

- **Homepage:** http://localhost:5000
- **Admin Panel:** http://localhost:5000/admin/login

## 🔑 Default Login Credentials

```
Username: admin
Password: admin123
```

**⚠️ IMPORTANT:** প্রথম login এর পর password change করুন!

## 📝 Channel Add করা

1. Admin panel এ login করুন
2. "Add Channel" button এ click করুন
3. Form fill করুন:
   - **Channel Name:** চ্যানেলের নাম
   - **Primary Stream URL:** মূল stream URL (m3u8/ts/mp4)
   - **Backup Stream URL:** (Optional) backup stream
   - **Stream Type:** m3u8, ts, বা mp4 select করুন
   - **Multiple Quality Links:** বিভিন্ন quality এর জন্য আলাদা URL add করুন
   - **Logo URL:** Channel logo এর URL
   - **Category:** Channel category select করুন
   - **User Agent/Referer:** (Optional) কিছু stream এর জন্য দরকার হতে পারে
4. "Add Channel" এ click করুন

## 🎬 Player Features

### Keyboard Shortcuts:
- **Space:** Play/Pause
- **F:** Fullscreen toggle
- **M:** Mute/Unmute
- **Arrow Up:** Volume up
- **Arrow Down:** Volume down
- **Arrow Right:** Forward 10 seconds
- **Arrow Left:** Backward 10 seconds

### Player Features:
- ✅ HLS (M3U8) streaming support
- ✅ Multi-quality selection
- ✅ Backup stream switching
- ✅ Picture-in-picture mode
- ✅ Speed control (0.5x to 2x)
- ✅ Keyboard shortcuts
- ✅ Auto-recovery on errors
- ✅ Responsive design

## 🔧 Database Reset করা

যদি model update করার পর error আসে:

```bash
python reset_database.py
```

অথবা manually:
```bash
# Delete old database
Remove-Item instance\livetv.db -Force

# Run app again (will create new database)
python run.py
```

## ❌ Common Problems & Solutions

### Problem 1: "Port 5000 already in use"
**Solution:** অন্য কোন application port 5000 ব্যবহার করছে।
```bash
# Kill the process using port 5000
netstat -ano | findstr :5000
# Note the PID and kill it
taskkill /PID <PID> /F
```

### Problem 2: Database error "no such column"
**Solution:** Database reset করুন:
```bash
python reset_database.py
```

### Problem 3: Stream not playing
**Solutions:**
1. Stream URL সঠিক আছে কিনা check করুন
2. Stream type সঠিক select করেছেন কিনা check করুন
3. Browser console check করুন (F12)
4. Backup stream try করুন (যদি add করা থাকে)

### Problem 4: "Module not found" error
**Solution:** Dependencies install করুন:
```bash
pip install -r requirements.txt
```

### Problem 5: Virtual environment activate হচ্ছে না
**Solution:** PowerShell execution policy change করুন:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📚 Stream URL Examples

### M3U8 (HLS) - Recommended:
```
https://example.com/live/channel.m3u8
https://cdn.example.com/hls/stream/index.m3u8
```

### TS (Transport Stream):
```
https://example.com/live/stream.ts
```

### MP4 (Video File):
```
https://example.com/videos/movie.mp4
```

## 🎨 Multi-Quality Setup

1. Primary URL এ main/auto quality দিন
2. "Add Quality Option" button click করুন
3. প্রতিটি quality এর জন্য:
   - Quality Label: "1080p", "720p", "480p" etc.
   - Stream URL: সেই quality এর URL
   - Bitrate: (Optional) kbps এ
   - Default checkbox: default quality হলে check করুন

## 📱 Mobile/Tablet Access

Same network এ থাকলে:

1. আপনার computer এর IP address জানুন:
   ```
   ipconfig
   ```
2. Mobile browser এ যান:
   ```
   http://<YOUR-IP>:5000
   ```

Example:
```
http://192.168.1.100:5000
```

## 🔒 Production Deployment

Production এ deploy করার জন্য:

1. `.env` file edit করুন:
   ```
   SECRET_KEY=<generate-a-strong-random-key>
   FLASK_ENV=production
   FLASK_DEBUG=False
   ADMIN_PASSWORD=<strong-password>
   ```

2. Production server ব্যবহার করুন:
   ```bash
   pip install waitress
   waitress-serve --port=8000 app:app
   ```

## 💡 Tips

1. **Stream URL testing:** VLC player দিয়ে URL test করুন add করার আগে
2. **Logo images:** Fast loading এর জন্য ছোট size এর logo ব্যবহার করুন
3. **Categories:** Channel গুলো organize করার জন্য proper categories তৈরি করুন
4. **Display Order:** Important channels এর জন্য কম number ব্যবহার করুন (0, 1, 2...)
5. **Backup URLs:** Important channels এর জন্য always backup URL add করুন

## 📞 Support

কোন সমস্যা হলে:
1. README.md পড়ুন
2. FIXES.md দেখুন known issues এর জন্য
3. Browser console (F12) check করুন error messages দেখার জন্য

---

**Happy Streaming! 📺**
