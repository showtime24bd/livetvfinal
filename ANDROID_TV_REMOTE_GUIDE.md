# 📱 Android TV Remote Control Guide

Android TV remote দিয়ে আপনার Live TV app control করার complete guide।

## 🎮 Remote Control Features

### ✅ সক্রিয় Features

আপনার Android TV remote এর নিচের buttons এখন কাজ করবে:

#### 🔢 Number Keys (0-9)
- **Direct Channel Selection**: যেকোনো number key চাপুন (1-9) channel number select করতে
- **Multi-digit Support**: একাধিক number চাপুন 2-3 digit channel number এর জন্য
- **Auto-switch**: Number select করার 2 seconds পরে automatically সেই channel এ switch হবে
- **Visual Preview**: Screen এ একটি overlay দেখাবে কোন channel select হচ্ছে

**উদাহরণ:**
- `1` চাপুন → Channel 1 এ যাবে
- `2` `5` চাপুন → Channel 25 এ যাবে
- `1` `0` `8` চাপুন → Channel 108 এ যাবে

#### ⬆️⬇️ Channel Navigation
- **Channel Up**: `Page Up` button অথবা `▲ Arrow Up` চাপুন
- **Channel Down**: `Page Down` button অথবা `▼ Arrow Down` চাপুন
- **Continuous Navigation**: Repeatedly চাপলে পরের/আগের channel এ যাবে
- **Wrap Around**: শেষ channel এর পরে প্রথম channel এ ফিরে যাবে

#### 🎬 Playback Control
- **Play/Pause**: `Space` অথবা `Play/Pause` button
- **Volume Up/Down**: `↑/↓` arrow keys (fullscreen mode এ)
- **Mute**: `M` key
- **Fullscreen**: `F` key toggle করবে

#### 🔙 Navigation Controls
- **Back Button**: Sidebar close করবে অথবা fullscreen থেকে exit করবে
- **OK/Enter**: Channel list sidebar open করবে
- **Escape**: Sidebar close অথবা fullscreen exit

## 🎯 Quick Start Guide

### Android TV তে Setup

1. **আপনার Android TV Browser খুলুন** (Chrome, Firefox, etc.)
2. **App URL এ যান**: `http://your-server-ip:5000`
3. **যেকোনো channel এ click করুন** watch page এ যেতে
4. **Remote control ready!** এখন আপনার remote এর buttons কাজ করবে

### প্রথমবার ব্যবহার

1. **Channel List Load হতে দিন**
2. **Number `1` চাপুন** প্রথম channel দেখতে
3. **Arrow keys ব্যবহার করুন** navigate করতে
4. **`F` key চাপুন** fullscreen mode এর জন্য

## 🎨 Visual Feedback

### Channel Number Overlay
যখন আপনি number key চাপবেন, screen এর মাঝখানে একটি overlay দেখাবে:
- **বড় number display**: আপনি কোন number চাপলেন
- **Channel name preview**: সেই number এর channel এর নাম
- **Auto-hide**: 2 seconds পরে automatically channel switch হবে

### Channel Change Notification
যখন আপনি arrow keys দিয়ে channel change করবেন, screen এর ডান দিকে একটি notification দেখাবে:
- **Current channel name**
- **Channel position** (e.g., "5/42")
- **Direction arrow** (▲ previous, ▼ next)
- **Auto-hide**: 3 seconds পরে

## 🔧 Advanced Features

### Keyboard Shortcuts (সব Remote Keys)

| Key | Action | Description |
|-----|--------|-------------|
| `0-9` | Direct Channel | Channel number select |
| `↑` | Previous Channel | আগের channel |
| `↓` | Next Channel | পরের channel |
| `Page Up` | Channel Up | Same as ↑ |
| `Page Down` | Channel Down | Same as ↓ |
| `Enter` | Channel List | Sidebar open/close |
| `Space` | Play/Pause | Video control |
| `F` | Fullscreen | Toggle fullscreen |
| `M` | Mute | Toggle mute |
| `Escape` | Back | Close sidebar/exit fullscreen |
| `Backspace` | Back | Android TV back button |
| `←` | Seek Back | 10 seconds পেছনে (fullscreen এ) |
| `→` | Seek Forward | 10 seconds সামনে (fullscreen এ) |

### Smart Features

#### 1. **Auto-detect Channel List**
- Automatically সব channels detect করে
- Real-time update যখন admin panel থেকে channel add/remove করা হয়

#### 2. **Circular Navigation**
- শেষ channel থেকে আবার প্রথম channel এ wrap করে
- কোনো "end of list" error নেই

#### 3. **Input Detection**
- Input field এ type করার সময় remote keys disable থাকে
- Video player controls এর সাথে conflict করে না

#### 4. **Multi-digit Channel Entry**
- 3-digit পর্যন্ত channel number support
- Smart timeout: 2 seconds পরে auto-switch

## 🖥️ TV-Optimized Interface

### Mobile/Touch vs Remote
- **Touch devices**: Tap এবং swipe gestures
- **Remote control**: Directional navigation
- **Automatic detection**: Device এর উপর based করে best interface দেখায়

### Fullscreen Experience
- Video player fullscreen mode এ সব controls accessible
- Visual indicators বড় এবং readable
- High contrast colors better visibility এর জন্য

## 🐛 Troubleshooting

### Remote Keys কাজ করছে না?

1. **Browser check করুন**
   - Chrome/Firefox recommended
   - Browser TV remote keys support করে কিনা verify করুন

2. **Page refresh করুন**
   - Sometimes JavaScript initialization হতে একটু সময় লাগে
   - Hard refresh: `Ctrl + Shift + R` (Android TV browser এ)

3. **Input field থেকে বের হন**
   - যদি search box active থাকে, remote keys কাজ করবে না
   - `Escape` অথবা `Back` button চাপুন

4. **Console log check করুন**
   - Browser developer tools open করুন
   - Console এ "Android TV Remote Control initialized" message দেখুন

### Channel List Empty?

1. **Admin panel check করুন**
   - Ensure কিছু channels added আছে
   - Channel status "active" আছে কিনা verify করুন

2. **Page fully load হয়েছে কিনা**
   - Sidebar এ channels visible হওয়া পর্যন্ত অপেক্ষা করুন
   - Slow network এ একটু সময় লাগতে পারে

### Number Keys অন্য কিছু করছে?

- আপনার Android TV browser এর built-in shortcuts override করতে পারে
- Arrow keys ব্যবহার করুন as alternative
- Browser settings check করুন keyboard shortcuts disable করার জন্য

## 💡 Tips & Best Practices

### 1. **Fullscreen Mode ব্যবহার করুন**
- Better viewing experience
- সব controls easily accessible
- `F` key চাপুন toggle করতে

### 2. **Channel Numbers মনে রাখুন**
- আপনার favorite channels এর numbers note করে রাখুন
- Quick access এর জন্য directly number চাপুন

### 3. **Arrow Keys for Browsing**
- জানা নেই কোন channel ভালো হবে? Arrow keys দিয়ে browse করুন
- Visual notification দেখাবে কি আসছে

### 4. **Sidebar Quick Access**
- `Enter` চাপুন full channel list দেখতে
- Category filter এবং search ব্যবহার করুন

### 5. **Backup Stream**
- Primary stream fail করলে configured backup স্বয়ংক্রিয়ভাবে চেষ্টা হবে
- প্রয়োজনে `🔄 Backup` button দিয়ে backup manual-ও চালু করা যাবে

## 🚀 Performance Tips

### Smooth Playback এর জন্য

1. **Stable Internet Connection**
   - Minimum 5 Mbps recommended
   - Wi-Fi better than mobile data

2. **Close অন্য Apps**
   - Android TV তে background apps close করুন
   - Memory free করুন better performance এর জন্য

3. **Regular Cache Clear**
   - Browser cache clear করুন occasionally
   - Settings → Apps → Browser → Clear Cache

## 🔄 Future Enhancements

Upcoming features planning করা হচ্ছে:

- [ ] Voice control integration
- [ ] Gesture controls (swipe on touchpad)
- [ ] Custom channel favorites list
- [ ] EPG grid view with remote navigation
- [ ] Picture-in-Picture (PiP) mode
- [ ] Sleep timer function

## 📞 Support

যদি কোনো problem face করেন:

1. GitHub repository তে issue create করুন
2. Console logs attach করুন
3. Android TV model এবং browser version mention করুন
4. Detailed steps describe করুন reproduce করার জন্য

---

**Enjoy your Android TV Live TV experience!** 📺✨
