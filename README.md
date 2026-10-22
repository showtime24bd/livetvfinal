# 📺 Live TV Streaming Website

A modern Python-based live TV streaming platform with an admin panel for managing channels. Supports M3U8 (HLS), TS, and MP4 stream formats.

## ✨ Features

- **Live TV Streaming**: Watch live channels with support for multiple stream formats
- **Admin Panel**: Complete management interface for channels and categories
- **Stream Format Support**: M3U8 (HLS), TS (MPEG Transport Stream), and MP4
- **Category Management**: Organize channels into categories
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modern UI**: Dark theme with smooth animations and transitions
- **Video Player**: Integrated Video.js player with HLS support
- **Live Match Schedule**: Show today's live cricket, football, and other popular sports from channel EPGs with a start countdown in Bangladesh time; exclude replay and pre-/mid-/post-show segments
- **Authentication**: Secure admin login system
- **🎮 Android TV Remote Control**: Full support for Android TV remotes with number pad channel selection, arrow key navigation, and media controls (NEW!)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
```bash
cd "C:\Users\Admin\Desktop\web-2023"
```

2. **Create a virtual environment:**
```bash
python -m venv venv
```

3. **Activate the virtual environment:**

Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

Windows Command Prompt:
```cmd
venv\Scripts\activate.bat
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Configure environment variables:**

Copy the example environment file:
```bash
copy .env.example .env
```

Edit `.env` file and update the following:
```
SECRET_KEY=your-secret-key-here-change-this
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password
FLASK_DEBUG=False
```

6. **Initialize the database and run the application:**
```bash
python app.py
```

The application will:
- Create the database
- Set up default admin user
- Create default categories
- Start the development server on http://localhost:5000

### Vercel Database

When `DATABASE_URL` is not set, Vercel uses a temporary SQLite database under its writable temp directory so the serverless function can initialize its schema. That database is ephemeral and is not shared reliably between function instances; admin writes are therefore disabled until a persistent `DATABASE_URL` is configured. Vercel does not automatically upload the local `instance/livetv.db`; migrate/import its content after configuring the persistent database. Set `ADMIN_USERNAME` and `ADMIN_PASSWORD` in Vercel's environment variables as well. A new database creates its initial admin only when `ADMIN_PASSWORD` is configured; existing admin passwords are not changed automatically.

## 📖 Usage

### Accessing the Website

- **Homepage**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login

### Default Admin Credentials

- **Username**: admin (or as set in .env)
- **Password**: admin123 (or as set in .env)

**⚠️ IMPORTANT**: Change the default admin password immediately after first login!

## 🔧 Admin Panel Guide

### Adding a Channel

1. Log in to the admin panel
2. Click "Add Channel" button
3. Fill in the channel details:
   - **Channel Name**: Display name (e.g., "CNN News")
   - **Stream URL**: Direct URL to the stream
   - **Stream Type**: Select m3u8, ts, or mp4
   - **Logo URL**: Optional channel logo image URL
   - **Category**: Select a category or leave uncategorized
   - **Description**: Optional channel description
   - **Display Order**: Lower numbers appear first (0 = highest priority)
   - **Active**: Check to make channel visible to users
4. Click "Add Channel"

### Stream URL Examples

**M3U8 (HLS) - Recommended for live streaming:**
```
https://example.com/live/channel.m3u8
```

**TS (MPEG Transport Stream):**
```
https://example.com/live/stream.ts
```

**MP4 (Video file):**
```
https://example.com/videos/channel.mp4
```

### Managing Categories

1. Click "Add Category" to create new categories
2. Categories appear in the filter on the homepage
3. Deleting a category leaves its channels uncategorized; the channels themselves are kept

### Editing Channels

1. Click "Edit" button next to any channel
2. Update the channel information
3. Click "Update Channel"

### Deleting Channels

1. Click "Delete" button next to any channel
2. Confirm the deletion
3. The channel will be permanently removed

## 🎥 Supported Stream Formats

### M3U8 (HLS - HTTP Live Streaming)
- **Best for**: Live TV broadcasts
- **Compatibility**: Excellent browser support via Video.js
- **Adaptive**: Automatically adjusts quality based on connection

### TS (MPEG Transport Stream)
- **Best for**: Direct transport streams
- **Compatibility**: Supported via Video.js

### MP4
- **Best for**: Pre-recorded content
- **Compatibility**: Native HTML5 video support
- **Limitation**: Not ideal for live streaming

## 🎮 Android TV Remote Control

আপনার Android TV remote দিয়ে সম্পূর্ণ app control করতে পারবেন! **বিস্তারিত guide দেখুন: [ANDROID_TV_REMOTE_GUIDE.md](ANDROID_TV_REMOTE_GUIDE.md)**

### Quick Reference:

#### 📱 Number Keys (0-9)
- **Direct channel jump**: `1` চাপুন Channel 1 এ যেতে
- **Multi-digit support**: `2` `5` = Channel 25
- **Visual preview**: Screen এ channel name দেখাবে

#### ⬆️⬇️ Navigation
- **Arrow Up / Page Up**: Previous channel
- **Arrow Down / Page Down**: Next channel
- **Enter/OK**: Channel list open করুন
- **Back/Escape**: Exit fullscreen / Close sidebar

#### 🎬 Playback
- **Space / Play/Pause**: Video pause/play toggle
- **F**: Fullscreen mode
- **M**: Mute toggle
- **Arrow Left/Right**: Seek 10 seconds (fullscreen এ)

### Setup on Android TV:
1. Android TV browser open করুন
2. `http://your-server-ip:5000` এ যান
3. যেকোনো channel click করুন
4. Remote control automatically কাজ করবে! 🎉

### Test Your Remote:
`REMOTE_CONTROL_TEST.html` file open করুন browser এ test করতে কোন buttons কাজ করছে।

## 📱 Mobile/Android TV Network Access

যদি mobile বা Android TV তে access করতে সমস্যা হয়, **বিস্তারিত guide দেখুন: [NETWORK_SETUP_GUIDE.md](NETWORK_SETUP_GUIDE.md)**

### Quick Setup (Windows):

#### Option 1: Automated Setup (Recommended)
**Double-click করুন:** `setup_mobile_quick.bat`

অথবা **PowerShell Admin** এ চালান:
```powershell
.\setup_mobile_access.ps1
```

#### Option 2: Manual Setup

1. **Find your computer IP:**
```powershell
ipconfig
```
Look for: `IPv4 Address: 192.168.x.x`

2. **Create firewall rule:**
```powershell
New-NetFirewallRule -DisplayName "Flask Live TV" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

3. **Start Flask app:**
```powershell
python app.py
```

4. **Access from mobile/TV:**
```
http://192.168.x.x:5000
```

### Common Issues:

| Problem | Solution |
|---------|----------|
| "Site can't be reached" | Check firewall, run `setup_mobile_quick.bat` |
| "Connection timeout" | Ensure same Wi-Fi network |
| Works on PC, not mobile | Create firewall rule (see above) |
| IP keeps changing | Set static IP in network settings |

**Full troubleshooting guide:** [NETWORK_SETUP_GUIDE.md](NETWORK_SETUP_GUIDE.md)

## 📁 Project Structure

```
live tv/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── static/
│   ├── css/
│   │   └── style.css         # Application styles
│   ├── js/
│   │   └── admin.js          # Admin panel JavaScript
│   └── images/               # Static images
├── templates/
│   ├── base.html             # Base template
│   ├── index.html            # Homepage
│   ├── watch.html            # Video player page
│   ├── 404.html              # Not found error
│   ├── 500.html              # Server error
│   └── admin/
│       ├── login.html        # Admin login
│       ├── dashboard.html    # Admin dashboard
│       ├── add_channel.html  # Add channel form
│       ├── edit_channel.html # Edit channel form
│       └── add_category.html # Add category form
└── instance/
    └── livetv.db             # SQLite database (created automatically)
```

## 🔒 Security Considerations

1. **Change Default Credentials**: Always change the default admin username and password
2. **Use Strong SECRET_KEY**: Generate a secure random secret key for production
3. **HTTPS in Production**: Always use HTTPS in production environments
4. **Environment Variables**: Never commit `.env` file to version control
5. **Database Backups**: Regularly backup your `livetv.db` database
6. **CSRF**: Admin forms require a session CSRF token; keep `SECRET_KEY` stable
7. **Stream proxy**: Loopback and link-local origins are blocked. LAN stream URLs still work. This is not DRM.

## 🌐 API Endpoints

The application provides REST API endpoints:

- `GET /api/channels` - Get all active channels with encrypted, expiring proxy stream links
- `GET /api/categories` - Get all categories
- `GET /api/epg/<channel_id>` - Get the current programme and next 3 programmes in Bangladesh time
- `GET /api/channels/<channel_id>` - Get one channel with encrypted, expiring proxy stream links

Example:
```bash
curl http://localhost:5000/api/channels
```

### Android TV

This tree serves the web player with Android TV remote support (number keys, D-pad, media keys). Open the site in the TV browser at `http://your-server-ip:5000`. A native APK is not included in this folder; use the web app on the TV for now.

The server now encrypts proxy tokens and never returns the origin stream URL through the channel APIs. Keep `SECRET_KEY` private and stable in Railway; changing it invalidates existing playback tokens. This hides origin URLs from ordinary API responses and token decoding, but is not DRM: a viewer can still copy a proxy link or capture the video being played.

## 🐛 Troubleshooting

### Video Won't Play

1. **Check Stream URL**: Ensure the stream URL is accessible and correct
2. **Check Stream Type**: Verify the stream type matches the actual format
3. **CORS Issues**: Some streams require proper CORS headers
4. **Browser Console**: Check browser console for error messages

### Can't Access Admin Panel

1. Ensure you're using the correct URL: http://localhost:5000/admin/login
2. Check credentials match those in `.env` file
3. Verify database was initialized (check for `livetv.db` in instance folder)

### Database Errors

Delete the database and restart:
```bash
Remove-Item instance\livetv.db
python app.py
```

## 🚀 Production Deployment

For production deployment, consider:

1. **Use a Production WSGI Server**: Gunicorn (Linux) or Waitress (Windows)
```bash
pip install waitress
waitress-serve --threads=8 --port=8000 app:app
```
Tune the thread count to the host's available resources; each proxied stream occupies a request thread while its media is being transferred.

2. **Use PostgreSQL or MySQL**: Instead of SQLite for better performance
```python
# In .env
DATABASE_URL=postgresql://user:password@localhost/livetv
```

3. **Set Environment Variables Properly**:
```
FLASK_ENV=production
FLASK_DEBUG=False
```

4. **Use a Reverse Proxy**: Nginx or Apache for serving static files

5. **Enable HTTPS**: Use Let's Encrypt for free SSL certificates

### Handling many channels and concurrent viewers

- The home page and category pages load at most 48 channels at a time. Database queries eager-load channel relationships and use indexes for the channel and featured-event listing paths.
- HLS playlists remain small and are rewritten by the app, but video segments and direct streams are sent to the browser as streamed responses instead of being buffered in app memory.
- Every proxied video byte still passes through this app. Estimate required outbound capacity as `concurrent viewers × average stream bitrate`; for example, 500 viewers at 4 Mbps need roughly 2 Gbps of video egress before protocol overhead. A larger worker/thread count cannot remove this bandwidth limit.
- For large audiences, serve HLS segments from an HLS-capable CDN or streaming origin close to viewers. If origin URLs must remain private, use short-lived signed CDN URLs or an edge proxy rather than routing every segment through the Flask application.
- Use PostgreSQL for production and apply schema/index changes by running the app's `init_db()` setup before deploying workers. Keep the development Flask server disabled in production; run behind a production WSGI server and reverse proxy.
- After deploying these index changes to an existing database, run the setup once before starting the WSGI workers:
```bash
python -c "from app import init_db; init_db()"
```

## 📝 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

Feel free to fork this project and customize it for your needs!

## 📧 Support

For issues or questions, please refer to the troubleshooting section above.

---

**Happy Streaming! 📺🎉**
