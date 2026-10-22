# 🏆 Featured Sports Events - Admin Guide

## Overview
আপনার Live TV platform এ এখন একটি powerful Featured Sports Events management system আছে। আপনি admin panel থেকে সম্পূর্ণভাবে control করতে পারবেন কোন sports events homepage এ দেখাবে।

---

## ✨ Features

### 1️⃣ **EPG থেকে Sports Browse করুন**
- Admin Panel → **"Browse EPG Sports"** button
- যেকোনো channel এর EPG থেকে সব programs দেখুন
- **"Show only Sports programs"** checkbox দিয়ে শুধু খেলার programs filter করুন
- Real-time EPG data থেকে upcoming sports events দেখুন

### 2️⃣ **One-Click Feature করুন**
- যেকোনো sports event এর পাশে **"⭐ Feature on Homepage"** button
- Click করলে সরাসরি event টি featured list এ add হবে
- Automatic data fill হবে EPG থেকে

### 3️⃣ **Manual Add করুন**
- **"Add Manually"** button দিয়ে নিজে থেকে event create করুন
- Custom information add করতে পারবেন

### 4️⃣ **Customize করুন**
প্রতিটি featured event এ add/edit করতে পারবেন:

| Field | Description | Example |
|-------|-------------|---------|
| **Event Title*** | Event এর নাম | "Arsenal vs Chelsea" |
| **Channel*** | কোন channel এ দেখাবে | "Star Sports 1" |
| **Teams/Players** | খেলোয়াড়/দল | "Manchester United vs Liverpool" |
| **Category** | Sports type | "Football", "Cricket", "Basketball" |
| **League/Tournament** | Tournament name | "Premier League", "IPL", "UEFA Champions League" |
| **Description** | Event details | "Exciting match between top teams" |
| **Thumbnail URL** | Event poster/image | "https://example.com/match-poster.jpg" |
| **Start Time*** | Event শুরুর সময় | 2024-10-20 19:00 |
| **End Time** | Event শেষ হওয়ার সময় | 2024-10-20 21:00 |
| **Display Order** | Homepage এ position | 0, 1, 2, 3... (ছোট number আগে দেখাবে) |
| **Active** | Homepage এ দেখাবে কি না | ✅ / ❌ |

*Required fields

---

## 🎯 How to Use

### Step 1: Browse EPG
1. Admin Panel এ যান
2. **"Browse EPG Sports"** click করুন
3. Dropdown থেকে একটা channel select করুন (যেটার EPG আছে)
4. সব programs load হবে
5. "Show only Sports programs" checked রাখুন শুধু sports দেখার জন্য

### Step 2: Feature an Event
1. যেকোনো sports event খুঁজে বের করুন
2. **"⭐ Feature on Homepage"** button এ click করুন
3. Event automatically featured list এ add হবে

### Step 3: Add Thumbnail & Details
1. Dashboard এ ফিরে যান
2. **"Featured Sports Events"** table এ নতুন event দেখবেন
3. **"Edit"** button click করুন
4. **Thumbnail URL** add করুন (event poster এর link)
5. অন্যান্য information customize করুন
6. **"Update Featured Event"** click করুন

### Step 4: Check Homepage
1. Homepage এ যান
2. **"🏆 Live & Upcoming Sports Events"** section দেখবেন
3. Beautiful cards এ সব featured events দেখাবে

---

## 💡 Tips & Best Practices

### ✅ DO:
- **High quality thumbnails** use করুন (recommended: 1280x720 বা 16:9 ratio)
- **Clear event titles** দিন (e.g., "Arsenal vs Chelsea - Premier League")
- **Display Order** use করুন important events আগে দেখানোর জন্য
- Events শেষ হলে **Inactive** করুন বা delete করুন
- **Start Time** correctly set করুন "LIVE NOW" badge দেখানোর জন্য

### ❌ DON'T:
- ❌ Low quality বা broken image links use করবেন না
- ❌ একই event বার বার add করবেন না
- ❌ সব events active রাখবেন না (শুধু upcoming events active রাখুন)

---

## 🎨 Homepage Display

### What Users See:
- **Section Title**: "🏆 Live & Upcoming Sports Events"
- **Beautiful Cards** with:
  - Large thumbnail (16:9)
  - Event title
  - Teams/Players name
  - League/Tournament badge
  - Channel name with icon
  - Start time
  - Sport category badge
  - **"LIVE NOW"** badge (if event is currently happening)
  - Hover effect with play button

### Card Features:
- ✨ Gradient overlays
- 🎯 Smooth hover animations
- 📱 Fully responsive (mobile/tablet)
- 🖼️ Fallback icon if no thumbnail
- ⚡ Click করলে সরাসরি channel এ redirect

---

## 🔥 Advanced Features

### Auto-detect LIVE Events:
System automatically shows **"LIVE NOW"** badge যদি:
- Current time >= Start Time
- Current time < End Time (if set)

### Display Ordering:
- Events sort হয় **Display Order** অনুযায়ী
- Same order হলে **Start Time** অনুযায়ী sort হয়
- আপনি control করতে পারেন কোন event কোথায় দেখাবে

### Only Upcoming Events:
- Homepage এ শুধু **future events** দেখায় (যেগুলো শুরু হয়নি বা চলছে)
- Past events automatically hide হয়
- Maximum 6 events show হয় homepage এ

---

## 🛠️ Database Management

### Migration:
Database table automatically created হয়েছে `migrate_featured_sports.py` run করার পর।

### Table: `featured_sports_events`
```sql
- id (Primary Key)
- channel_id (Foreign Key → channels.id)
- event_title
- event_description
- thumbnail_url
- start_time
- end_time
- category
- league_tournament
- teams_playing
- is_active
- order
- created_at
- updated_at
```

---

## 📊 Admin Dashboard

### New Stats Card:
Dashboard এ এখন **4টি stat cards** আছে:
1. Total Channels
2. Active Channels
3. Total Categories
4. **Featured Sports** ← নতুন! (shows active featured events count)

### Featured Sports Table:
Admin dashboard এ full table দেখাবে:
- Thumbnail preview
- Event name with teams
- Channel badge
- Start time
- Category badge
- Active/Inactive status
- Edit & Delete buttons

---

## 🚀 Quick Actions

### Browse → Feature → Customize
1. Browse EPG Sports (2 clicks)
2. Feature on Homepage (1 click)
3. Edit & Add Thumbnail (2 clicks)
4. **Total: 5 clicks to feature an event!** ⚡

---

## 📝 Example Workflow

**Scenario**: Premier League match আসছে আগামীকাল

1. **Browse**: Admin Panel → Browse EPG Sports → Select "Star Sports 1"
2. **Find**: "Live: Premier League - Arsenal vs Chelsea" খুঁজে পান
3. **Feature**: "⭐ Feature on Homepage" click করুন
4. **Edit**: Dashboard → Edit button
5. **Customize**:
   - Thumbnail: `https://img.url/arsenal-vs-chelsea.jpg`
   - Teams: "Arsenal vs Chelsea"
   - League: "Premier League"
   - Category: "Football"
6. **Save**: Update button click
7. **Result**: Homepage এ beautiful card দেখাচ্ছে! 🎉

---

## 🎯 Result

এখন আপনার platform এ:
- ✅ **Full control** over featured sports events
- ✅ **Beautiful UI** on homepage
- ✅ **Easy management** from admin panel
- ✅ **No automatic EPG mess** - আপনি যা চান তাই দেখান
- ✅ **Professional look** with thumbnails and details

---

## 🆘 Support

যদি কোনো সমস্যা হয়:
1. Check database migration হয়েছে কি না
2. Check channel এর EPG ID correctly set আছে কি না
3. Check image URLs valid এবং accessible কি না
4. Browser console check করুন errors এর জন্য

---

**Made with ❤️ for StreamZone**
