# ✅ Quick Test Guide - Browse EPG & Feature Sports

## 🔧 Fix Applied

আমি Browse EPG Sports page এ JavaScript error fix করেছি। এখন button click properly কাজ করবে!

---

## 🧪 How to Test

### Step 1: Login to Admin
```
URL: http://localhost:5000/admin
Username: admin (or your username)
Password: admin123 (or your password)
```

### Step 2: Click "Browse EPG Sports"
Dashboard থেকে blue button "Browse EPG Sports" click করুন

### Step 3: Select a Channel
Dropdown থেকে যেকোনো channel select করুন:
- STAR SPORTS 1
- STAR SPORTS 2
- WILLOW HD

### Step 4: Wait for EPG to Load
"Loading EPG data... ⏳" দেখাবে, তারপর programs দেখাবে

### Step 5: Check Programs
- "Show only Sports programs" checkbox checked থাকবে
- শুধু sports programs দেখাবে (orange border)
- প্রতিটিতে "⭐ Feature on Homepage" button দেখাবে

### Step 6: Feature an Event
1. যেকোনো sports event এ "⭐ Feature on Homepage" click করুন
2. Confirmation dialog দেখাবে event এর নাম সহ
3. "OK" click করুন
4. Button text change হবে: "⏳ Adding..."
5. Redirect হবে dashboard এ
6. Success message দেখাবে
7. Featured Sports table এ নতুন event দেখাবে!

### Step 7: Verify on Homepage
```
URL: http://localhost:5000/
```
- "🏆 Live & Upcoming Sports Events" section এ নতুন event দেখাবে
- Click করলে channel watch page এ যাবে

---

## 🐛 If Button Doesn't Work

### Check Browser Console:
1. Press F12 (Developer Tools)
2. Go to "Console" tab
3. Click "⭐ Feature on Homepage" button
4. দেখুন কোনো error আসে কিনা

### Common Issues:

**Issue 1: No programs showing**
- ✓ Check "Show only Sports programs" unchecked করে দেখুন
- ✓ সব programs দেখাবে

**Issue 2: "Failed to load EPG"**
- ✓ Internet connection check করুন
- ✓ EPG API (epg.pw) down হতে পারে
- ✓ Browser থেকে direct test করুন: http://localhost:5000/api/epg/1

**Issue 3: Button click না হলে**
- ✓ Browser cache clear করুন (Ctrl+Shift+R)
- ✓ Console এ JavaScript error check করুন

**Issue 4: Form submit হচ্ছে না**
- ✓ Browser console check করুন
- ✓ Flask server log check করুন
- ✓ CSRF token issue হতে পারে

---

## 🎯 Expected Behavior

### When You Click "⭐ Feature on Homepage":

1. **Confirmation Dialog:**
   ```
   Feature this event on homepage?
   
   [Event Title]
   
   Start: [Time]
   
   [OK] [Cancel]
   ```

2. **Button Changes:**
   ```
   ⭐ Feature on Homepage  →  ⏳ Adding...
   ```

3. **Form Submits:**
   - POST to /admin/featured-sports/add
   - With fields: channel_id, event_title, description, start_time, end_time, category

4. **Redirect:**
   - Goes to admin dashboard
   - Flash message: "Featured sports event added successfully!"

5. **Event Appears:**
   - In Featured Sports Events table
   - With event details
   - Edit and Delete buttons

6. **Homepage Updates:**
   - Event shows in featured section
   - With all details
   - Clickable to watch

---

## 📊 Test Checklist

- [ ] ✓ Can login to admin panel
- [ ] ✓ "Browse EPG Sports" button visible
- [ ] ✓ Channel dropdown has 3 channels
- [ ] ✓ EPG data loads when channel selected
- [ ] ✓ Sports programs showing (with orange border)
- [ ] ✓ "Show only Sports" filter works
- [ ] ✓ "⭐ Feature on Homepage" button visible
- [ ] ✓ Click shows confirmation dialog
- [ ] ✓ Clicking OK submits form
- [ ] ✓ Redirects to dashboard
- [ ] ✓ Success message shown
- [ ] ✓ Event in Featured Sports table
- [ ] ✓ Event shows on homepage
- [ ] ✓ Can edit event
- [ ] ✓ Can delete event

---

## 🚀 What I Fixed

### Before (Problem):
```javascript
// JSON stringify in onclick attribute = syntax error
onclick="featureEvent(..., ${JSON.stringify(prog)})"
```

### After (Fixed):
```javascript
// Data attributes + event listeners = clean & working
<button data-program-index="${index}" data-channel-id="${channelId}">
```

```javascript
// Proper event handling
document.querySelectorAll('.btn-feature').forEach(btn => {
  btn.addEventListener('click', function() {
    const index = parseInt(this.dataset.programIndex);
    const channelId = parseInt(this.dataset.channelId);
    featureEvent(channelId, programs[index]);
  });
});
```

### Changes Made:
1. ✅ Removed inline onclick with JSON
2. ✅ Added data-attributes for program index
3. ✅ Added event listeners properly
4. ✅ Added HTML escaping for safety
5. ✅ Added confirmation dialog
6. ✅ Added loading state on button
7. ✅ Improved error handling
8. ✅ Store programs in global variable

---

## 🎉 Result

এখন আপনি:
1. ✅ EPG browse করতে পারবেন
2. ✅ Sports programs দেখতে পারবেন
3. ✅ One-click এ feature করতে পারবেন
4. ✅ Homepage এ দেখাতে পারবেন
5. ✅ Edit করতে পারবেন
6. ✅ Thumbnail add করতে পারবেন

---

## 🔍 Debug URLs

Test these URLs in browser:

**EPG API Test:**
- http://localhost:5000/api/epg/1 (STAR SPORTS 1)
- http://localhost:5000/api/epg/2 (STAR SPORTS 2)
- http://localhost:5000/api/epg/3 (WILLOW HD)

**Admin Pages:**
- http://localhost:5000/admin (Dashboard)
- http://localhost:5000/admin/featured-sports/browse (Browse EPG)
- http://localhost:5000/admin/featured-sports/add (Manual Add)
- http://localhost:5000/admin/epg-test (Simple Test Page)

**Homepage:**
- http://localhost:5000/ (Featured sports visible here)

---

## 💡 Pro Tip

**Test Page আছে!**

যদি Browse EPG page এ problem হয়, simple test page try করুন:
```
http://localhost:5000/admin/epg-test
```

এটা একটা simplified version যেখানে:
- All programs দেখায় (sports + non-sports)
- Console এ log দেখায়
- Same "Feature This" functionality
- Easy debugging

---

**Server Running:** http://localhost:5000/ ✅
**Ready to Test!** 🚀
