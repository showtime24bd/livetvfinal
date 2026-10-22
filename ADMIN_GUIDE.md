# 🎛️ Admin Panel - Channel Management Guide

## 📝 Channel Add করার সঠিক পদ্ধতি

### 1. **Basic Channel Information** (Required)

#### Channel Name *
```
Example: GTV, Somoy TV, CNN News
- সহজ এবং পরিষ্কার নাম দিন
- Duplicate name avoid করুন
```

#### Primary Stream URL *
```
Example: https://example.com/stream.m3u8
- Direct stream URL দিতে হবে
- M3U8, TS, অথবা MP4 format
- URL টা working কিনা check করুন
```

#### Stream Type *
```
- M3U8 (HLS) → Live streaming এর জন্য best
- TS (Transport Stream) → Direct TS streams
- MP4 → Video files
```

---

## 🎬 Multi-Quality Links Add করা

### কখন ব্যবহার করবেন?
যদি আপনার কাছে **একই channel এর বিভিন্ন quality** এর আলাদা আলাদা stream URL থাকে।

### কিভাবে Add করবেন?

#### Step 1: "➕ Add Quality Option" Button Click করুন

#### Step 2: Quality Details Fill করুন

```
Quality Label: 1080p
Stream URL: https://example.com/1080p.m3u8
Bitrate: 5000 (optional)
Default: ☑ (যদি default quality হিসেবে set করতে চান)
```

#### Step 3: আরো Quality Add করতে পারেন

```
Quality #1:
  - Label: 1080p (Full HD)
  - URL: https://...1080.m3u8
  - Bitrate: 5000
  - Default: ☑

Quality #2:
  - Label: 720p (HD)
  - URL: https://...720.m3u8
  - Bitrate: 3000
  - Default: ☐

Quality #3:
  - Label: 480p (SD)
  - URL: https://...480.m3u8
  - Bitrate: 1500
  - Default: ☐
```

#### Step 4: Submit করুন ✅

---

## ⚠️ Common Errors এবং Solutions

### Error 1: "Failed to add channel"
**Problem:** Database error বা validation failed

**Solution:**
```
1. সব required fields (*) fill করেছেন কিনা check করুন
2. Stream URL valid কিনা verify করুন
3. Browser console (F12) check করুন error message এর জন্য
```

### Error 2: Multi-quality links not showing
**Problem:** Quality options player এ দেখা যাচ্ছে না

**Solution:**
```
1. Quality URL গুলো valid এবং working কিনা test করুন
2. Stream Type সঠিক select করেছেন কিনা check করুন
3. একটা quality কে default set করুন
```

### Error 3: "Quality label required" error
**Problem:** Quality option add করার সময় label বা URL missing

**Solution:**
```
1. Quality Label এবং Stream URL দুটোই required
2. যদি quality add করতে না চান, তাহলে "🗑️ Remove" button click করুন
3. Empty quality field submit করবেন না
```

### Error 4: Channel plays but quality selector not working
**Problem:** Player এ quality change করা যাচ্ছে না

**Solution:**
```
1. প্রতিটা quality এর URL আলাদা হতে হবে
2. Stream format same রাখুন (সব m3u8 বা সব ts)
3. Browser cache clear করুন (Ctrl+Shift+Delete)
```

---

## 💡 Best Practices

### 1. **Stream URL Testing**
Channel add করার আগে VLC Player দিয়ে test করুন:
```
1. VLC Player open করুন
2. Media → Open Network Stream
3. Stream URL paste করুন
4. Play হচ্ছে কিনা check করুন
```

### 2. **Logo Images**
```
✅ Do:
- Small file size (< 100KB)
- Square or 16:9 ratio
- PNG or JPG format
- Direct image URL

❌ Don't:
- Very large images (slow loading)
- Non-image URLs
- Password protected URLs
```

### 3. **Category Organization**
```
✅ Good:
- News
- Sports
- Entertainment
- Movies
- Music

❌ Bad:
- Too many categories (confusing)
- Unclear category names
- Overlapping categories
```

### 4. **Display Order**
```
Important channels → Lower numbers (0, 1, 2, ...)
Less important → Higher numbers (10, 20, 30, ...)

Example:
  0 → Popular Channel 1
  1 → Popular Channel 2
  2 → Popular Channel 3
  10 → Other channels...
```

---

## 🔧 Advanced Options

### Custom User Agent
কিছু streams specific browser identity চায়:
```
Example: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
```

### Custom Referer
কিছু streams specific referer header চায়:
```
Example: https://originaldomain.com
```

### Backup Stream URL
Primary stream fail হলে player automatic backup-এ switch করার চেষ্টা করবে। HEVC/H.265 সব browser/device-এ চলে না, তাই broad support-এর জন্য একই format-এর H.264-encoded backup দিন:
```
Primary: https://main-server.com/stream.m3u8
Backup: https://backup-server.com/stream.m3u8
```

---

## 📊 Quality Options Examples

### Example 1: Simple Channel (No Multi-Quality)
```
Channel Name: GTV
Primary URL: https://stream.com/gtv.m3u8
Stream Type: M3U8
Quality Options: (Leave empty)
```

### Example 2: HD + SD Options
```
Channel Name: Somoy TV
Primary URL: https://stream.com/somoy-auto.m3u8
Stream Type: M3U8

Quality Options:
  #1: Auto (Default) → https://stream.com/somoy-auto.m3u8
  #2: HD → https://stream.com/somoy-hd.m3u8
  #3: SD → https://stream.com/somoy-sd.m3u8
```

### Example 3: Multiple Qualities with Bitrates
```
Channel Name: Sports HD
Primary URL: https://stream.com/sports.m3u8
Stream Type: M3U8

Quality Options:
  #1: 1080p (Default)
      URL: https://stream.com/sports-1080.m3u8
      Bitrate: 5000
  
  #2: 720p
      URL: https://stream.com/sports-720.m3u8
      Bitrate: 3000
  
  #3: 480p
      URL: https://stream.com/sports-480.m3u8
      Bitrate: 1500
  
  #4: 360p
      URL: https://stream.com/sports-360.m3u8
      Bitrate: 800
```

---

## ✅ Success Checklist

Before submitting a new channel:

- [ ] Channel name entered
- [ ] Stream URL tested and working
- [ ] Stream type correctly selected
- [ ] Logo URL added (optional but recommended)
- [ ] Category selected
- [ ] Display order set
- [ ] Active checkbox checked
- [ ] Multi-quality options added (if available)
- [ ] At least one quality set as default (if using multi-quality)
- [ ] All quality URLs tested

---

## 🎯 Quick Tips

1. **Test Everything**: সব URL submit করার আগে test করুন
2. **Use Categories**: Channel organization এর জন্য properly categories use করুন
3. **Add Logos**: Logo থাকলে UI অনেক professional দেখায়
4. **Set Order**: Important channels এর জন্য low order number ব্যবহার করুন
5. **Backup URLs**: যদি possible হয় backup stream URL add করুন
6. **Quality Labels**: Clear labels use করুন (1080p, 720p, SD, HD, etc.)

---

## 🆘 Need Help?

যদি কোনো সমস্যা হয়:

1. Browser console (F12) check করুন
2. Network tab দেখুন request failed হচ্ছে কিনা
3. Stream URL directly browser এ paste করে test করুন
4. VLC Player দিয়ে URL verify করুন

---

**Happy Channel Management! 📺✨**
