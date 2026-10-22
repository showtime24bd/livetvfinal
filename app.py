from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, stream_with_context, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Channel, Category, Admin, FeaturedSportsEvent, StreamQuality
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os, hashlib, base64, json, hmac, secrets, socket, ipaddress
import re
import requests as req_lib
import tempfile
from urllib.parse import urljoin, urlparse
from cryptography.fernet import Fernet, InvalidToken
from sqlalchemy import or_, and_
from sqlalchemy.engine import URL
from sqlalchemy.orm import joinedload, selectinload
from threading import local

load_dotenv()

app = Flask(__name__)
DEFAULT_SECRET_KEY = 'change-this-secret-key'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', DEFAULT_SECRET_KEY)
database_url = os.getenv('DATABASE_URL')
app.config['PERSISTENT_DATABASE_CONFIGURED'] = (
    os.getenv('VERCEL') != '1' or bool(database_url)
)
if not database_url:
    if os.getenv('VERCEL') == '1':
        database_url = URL.create(
            'sqlite',
            database=os.path.join(tempfile.gettempdir(), 'livetv.db'),
        )
    else:
        database_url = 'sqlite:///livetv.db'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
CHANNELS_PER_PAGE = 48
FEATURED_LIVE_GRACE = timedelta(hours=6)
DEFAULT_STREAM_UA = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    'Chrome/120.0.0.0 Safari/537.36'
)
BLOCKED_UPSTREAM_HOSTS = frozenset({
    'localhost', 'metadata', 'metadata.google.internal', 'metadata.internal',
})
MAX_UPSTREAM_REDIRECTS = 5

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    admin = Admin.query.get(int(user_id))
    if admin:
        return User(admin.id, admin.username)
    return None

# ==================== STREAM PROXY & TOKEN SYSTEM ====================

PROXY_SECRET = app.config['SECRET_KEY'].encode()
PROXY_ENCRYPTION_KEY = base64.urlsafe_b64encode(hashlib.sha256(PROXY_SECRET).digest())
PROXY_CIPHER = Fernet(PROXY_ENCRYPTION_KEY)
TOKEN_EXPIRY  = 3600  # 1 hour
_upstream_state = local()


def _upstream_session():
    """Reuse upstream HTTP connections within each WSGI thread."""
    http_session = getattr(_upstream_state, 'session', None)
    if http_session is None:
        http_session = req_lib.Session()
        adapter = req_lib.adapters.HTTPAdapter(pool_connections=16, pool_maxsize=16)
        http_session.mount('http://', adapter)
        http_session.mount('https://', adapter)
        _upstream_state.session = http_session
    return http_session


def _ip_is_unsafe(ip):
    return (
        ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_unspecified
        or ip.is_reserved
    )


def _hostname_is_unsafe(hostname, resolve=False):
    if not hostname:
        return True
    host = hostname.lower().rstrip('.')
    if host in BLOCKED_UPSTREAM_HOSTS or host.endswith('.localhost'):
        return True
    try:
        return _ip_is_unsafe(ipaddress.ip_address(host))
    except ValueError:
        pass
    if not resolve:
        return False
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if _ip_is_unsafe(ip):
            return True
    return False


def _is_blocked_upstream_url(url, resolve=False):
    parsed = urlparse(url)
    if parsed.scheme.lower() not in ('http', 'https') or not parsed.hostname:
        return True
    return _hostname_is_unsafe(parsed.hostname, resolve=resolve)


def _raw_token(real_url, stream_type, user_agent=None, referer=None):
    """Build an opaque, authenticated, expiring token (no url_for)."""
    payload = {'url': real_url, 'stream_type': stream_type}
    if user_agent:
        payload['ua'] = user_agent
    if referer:
        payload['ref'] = referer
    return PROXY_CIPHER.encrypt(
        json.dumps(payload, separators=(',', ':')).encode()
    ).decode()


def make_stream_token(real_url, stream_type='m3u8', user_agent=None, referer=None):
    """Return a /stream/<token> URL that hides the real stream URL."""
    token = _raw_token(real_url, stream_type, user_agent, referer)
    return url_for('stream_proxy', token=token, _external=False)


def channel_api_data(channel):
    """Return channel data with all playable URLs routed through the proxy."""
    data = channel.to_dict()
    data.pop('user_agent', None)
    data.pop('referer', None)
    ua = channel.user_agent or None
    ref = channel.referer or None
    data['stream_url'] = make_stream_token(
        channel.stream_url, channel.stream_type, ua, ref
    )
    data['stream_url_backup'] = (
        make_stream_token(channel.stream_url_backup, channel.stream_type, ua, ref)
        if channel.stream_url_backup else ''
    )
    for quality in data.get('stream_qualities', []):
        if quality.get('stream_url'):
            quality['stream_url'] = make_stream_token(
                quality['stream_url'], channel.stream_type, ua, ref
            )
    return data


def _decrypt_stream_payload(token):
    try:
        payload = json.loads(
            PROXY_CIPHER.decrypt(token.encode(), ttl=TOKEN_EXPIRY).decode()
        )
        if not isinstance(payload, dict):
            return None
        real_url = payload.get('url')
        stream_type = payload.get('stream_type')
        if not isinstance(real_url, str) or not real_url:
            return None
        if not isinstance(stream_type, str) or not stream_type:
            return None
        user_agent = payload.get('ua')
        referer = payload.get('ref')
        return {
            'url': real_url,
            'stream_type': stream_type,
            'ua': user_agent if isinstance(user_agent, str) and user_agent else None,
            'ref': referer if isinstance(referer, str) and referer else None,
        }
    except (InvalidToken, ValueError, TypeError, UnicodeDecodeError, json.JSONDecodeError):
        return None


def verify_stream_token(token):
    """Decode and verify token → (url, stream_type) or (None, None)."""
    payload = _decrypt_stream_payload(token)
    if not payload:
        return None, None
    return payload['url'], payload['stream_type']


def generate_csrf_token():
    token = session.get('_csrf_token')
    if not token:
        token = secrets.token_hex(32)
        session['_csrf_token'] = token
    return token


@app.context_processor
def inject_csrf_token():
    return {'csrf_token': generate_csrf_token}


@app.before_request
def csrf_protect():
    if request.method not in ('POST', 'PUT', 'PATCH', 'DELETE'):
        return
    expected = session.get('_csrf_token')
    submitted = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token', '')
    if (
        not expected
        or not submitted
        or not hmac.compare_digest(str(expected), str(submitted))
    ):
        if request.is_json:
            return jsonify(error='Your session expired. Reload the page and try again.'), 400
        flash('Your admin session expired or the form is stale. Please sign in again and retry.', 'error')
        return redirect(url_for('admin_login'))


@app.before_request
def prevent_writes_without_persistent_vercel_database():
    if (
        not app.config['PERSISTENT_DATABASE_CONFIGURED']
        and request.method in ('POST', 'PUT', 'PATCH', 'DELETE')
        and request.endpoint
        and request.endpoint.startswith('admin_')
        and request.endpoint != 'admin_login'
    ):
        flash(
            'Saving is disabled because this Vercel deployment has no persistent database. '
            'Configure DATABASE_URL and redeploy before managing channels or events.',
            'error',
        )
        return redirect(url_for('admin_dashboard'))


def _visible_featured_sports_query(now):
    return FeaturedSportsEvent.query.filter_by(is_active=True)\
        .options(joinedload(FeaturedSportsEvent.channel))\
        .filter(
            or_(
                FeaturedSportsEvent.end_time > now,
                and_(
                    FeaturedSportsEvent.end_time.is_(None),
                    FeaturedSportsEvent.start_time > now - FEATURED_LIVE_GRACE,
                ),
            )
        )\
        .order_by(FeaturedSportsEvent.order, FeaturedSportsEvent.start_time)


@app.route('/stream/<token>')
def stream_proxy(token):
    """Proxy the stream — real URL never reaches the browser."""
    payload = _decrypt_stream_payload(token)
    if not payload:
        return Response('Stream link expired or invalid', status=403)
    if _is_blocked_upstream_url(payload['url']):
        return Response('Stream link expired or invalid', status=403)

    if payload['stream_type'] in ('m3u8', 'hls', 'ts'):
        return _proxy_hls(payload)
    return _proxy_passthrough(payload)


def _proxy_request_headers(url, payload, include_range=True):
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    referer = payload.get('ref') or (origin + '/')
    referer_origin = urlparse(referer)
    headers = {
        'User-Agent': payload.get('ua') or DEFAULT_STREAM_UA,
        'Referer': referer,
        'Origin': (
            f"{referer_origin.scheme}://{referer_origin.netloc}"
            if referer_origin.scheme and referer_origin.netloc else origin
        ),
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'identity',
    }
    if include_range:
        range_header = request.headers.get('Range')
        if range_header:
            headers['Range'] = range_header
    return headers


def _upstream_get(url, headers, timeout):
    http_session = _upstream_session()
    current = url
    response = None
    for _ in range(MAX_UPSTREAM_REDIRECTS + 1):
        if _is_blocked_upstream_url(current, resolve=True):
            raise req_lib.RequestException('Blocked upstream URL')
        response = http_session.get(
            current, headers=headers, timeout=timeout, stream=True, allow_redirects=False
        )
        if getattr(response, 'is_redirect', False) or response.status_code in (
            301, 302, 303, 307, 308
        ):
            location = response.headers.get('Location')
            response.close()
            if not location:
                raise req_lib.RequestException('Redirect without Location')
            current = urljoin(current, location)
            continue
        response.raise_for_status()
        return response
    if response is not None:
        response.close()
    raise req_lib.RequestException('Too many redirects')


def _proxy_hls(payload):
    """Fetch m3u8 manifest and rewrite every URL — supports Xtream Codes, MAG/Stalker, root-relative paths."""
    url = payload['url']
    headers = _proxy_request_headers(url, payload)

    r = None
    try:
        r = _upstream_get(url, headers, timeout=15)
    except req_lib.RequestException:
        if r is not None:
            r.close()
        app.logger.exception('Failed to fetch proxied HLS stream')
        return Response('Failed to fetch stream', status=502)

    content_type = r.headers.get('Content-Type', 'application/x-mpegURL')
    chunks = r.iter_content(chunk_size=65536)

    # After redirects, use the FINAL URL's origin for resolving relative paths
    # This fixes MAG/Stalker portals that redirect to a different IP/server
    # Detect if this is actually a manifest
    final_path = urlparse(r.url).path.lower()
    is_manifest = (
        'mpegurl' in content_type.lower()
        or final_path.endswith(('.m3u8', '.m3u'))
    )
    first_chunk = b''
    if not is_manifest and not final_path.endswith(
        ('.ts', '.mp4', '.m4s', '.aac', '.key', '.bin')
    ):
        try:
            first_chunk = next(chunks, b'')
        except req_lib.RequestException:
            r.close()
            app.logger.exception('Failed to read proxied HLS response')
            return Response('Failed to fetch stream', status=502)
        is_manifest = first_chunk.lstrip()[:7] == b'#EXTM3U'

    if not is_manifest:
        return _stream_upstream_response(r, chunks, first_chunk, content_type)

    # Rewrite every segment / sub-playlist URL using FINAL origin
    try:
        content = first_chunk + b''.join(chunks)
        playlist = content.decode(r.encoding or 'utf-8', errors='replace')
        lines = []
        for line in playlist.splitlines():
            stripped = line.strip()

            if not stripped:
                lines.append(line)
                continue

            if stripped.startswith('#'):
                lines.append(_rewrite_hls_uri_attributes(line, r.url, payload))
            else:
                lines.append(_proxy_child_url(stripped, r.url, payload))
    except req_lib.RequestException:
        app.logger.exception('Failed to read proxied HLS playlist')
        return Response('Failed to fetch stream', status=502)
    finally:
        r.close()

    return Response(
        '\n'.join(lines),
        content_type='application/x-mpegURL',
        headers={
            'Access-Control-Allow-Origin': '*',
            'Cache-Control': 'no-cache, no-store',
        }
    )


def _stream_upstream_response(upstream, chunks, first_chunk, content_type):
    headers = {
        'Content-Type': content_type,
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-cache',
    }
    for name in (
        'Content-Length', 'Content-Range', 'Accept-Ranges', 'ETag', 'Last-Modified'
    ):
        if name in upstream.headers and not (
            name == 'Content-Length' and upstream.headers.get('Content-Encoding')
        ):
            headers[name] = upstream.headers[name]

    def generate():
        try:
            if first_chunk:
                yield first_chunk
            yield from chunks
        finally:
            upstream.close()

    response = Response(
        stream_with_context(generate()),
        status=upstream.status_code,
        headers=headers,
    )
    response.call_on_close(upstream.close)
    return response


def _proxy_passthrough(payload):
    """Stream binary content (ts segments, mp4) through the server."""
    url = payload['url']
    headers = _proxy_request_headers(url, payload)

    r = None
    try:
        r = _upstream_get(url, headers, timeout=20)
        return _stream_upstream_response(
            r,
            r.iter_content(chunk_size=65536),
            b'',
            r.headers.get('Content-Type', 'video/MP2T'),
        )
    except req_lib.RequestException:
        if r is not None:
            r.close()
        app.logger.exception('Failed to fetch proxied stream')
        return Response('Failed to fetch stream', status=502)


def _proxy_child_url(reference, final_url, payload=None):
    """Resolve one playlist URI and return an opaque proxy URL for it."""
    parsed = urlparse(reference)
    if parsed.scheme and parsed.scheme.lower() not in ('http', 'https'):
        return reference

    absolute_url = urljoin(final_url, reference)
    if _is_blocked_upstream_url(absolute_url):
        return ''
    path_clean = urlparse(absolute_url).path.lower()
    stream_type = 'm3u8' if path_clean.endswith(('.m3u8', '.m3u')) else 'ts'
    extra = payload or {}
    token = _raw_token(
        absolute_url, stream_type, extra.get('ua'), extra.get('ref')
    )
    return url_for('stream_proxy', token=token, _external=False)


def _rewrite_hls_uri_attributes(line, final_url, payload=None):
    """Rewrite URI attributes embedded in HLS comment/tag lines."""
    return re.sub(
        r'URI=(["\'])(.*?)\1',
        lambda match: f'URI={match.group(1)}{_proxy_child_url(match.group(2), final_url, payload)}'
        f'{match.group(1)}',
        line,
    )


# ==================== DB INIT ====================

def init_db(seed_admin=True):
    with app.app_context():
        db.create_all()
        for model in (Channel, StreamQuality, FeaturedSportsEvent):
            for index in model.__table__.indexes:
                index.create(bind=db.engine, checkfirst=True)
        if seed_admin and Admin.query.count() == 0:
            admin_username = os.getenv('ADMIN_USERNAME', 'admin')
            admin_password = os.getenv('ADMIN_PASSWORD')
            if not admin_password:
                admin_password = 'admin123'
                print('WARNING: ADMIN_PASSWORD is not set. Default password is in use; change it immediately.')
            admin = Admin(username=admin_username,
                          password_hash=generate_password_hash(admin_password))
            db.session.add(admin)
            for cat_name in ['News', 'Sports', 'Entertainment', 'Movies', 'Music']:
                if not Category.query.filter_by(name=cat_name).first():
                    db.session.add(Category(name=cat_name))
            db.session.commit()
            print(f"Default admin created: {admin_username}")


# Vercel imports app.py directly and does not run run.py's database setup.
if os.getenv('VERCEL') == '1':
    init_db(seed_admin=bool(os.getenv('ADMIN_PASSWORD')))


# ==================== FRONTEND ROUTES ====================

@app.route('/')
def index():
    categories = Category.query.all()
    page = max(request.args.get('page', 1, type=int), 1)
    channel_page = Channel.query.options(joinedload(Channel.category))\
        .filter_by(is_active=True)\
        .order_by(Channel.order, Channel.name)\
        .paginate(page=page, per_page=CHANNELS_PER_PAGE, error_out=False)
    channels = channel_page.items
    epg_channels = [
        {'id': channel.id, 'name': channel.name}
        for channel in channels if channel.epg_channel_id
    ]
    now = datetime.now()
    featured_sports = _visible_featured_sports_query(now).limit(24).all()

    return render_template(
        'index.html', channels=channels, channel_page=channel_page,
        categories=categories,
        epg_channels=epg_channels, featured_sports=featured_sports, now=now
    )


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/watch')
@app.route('/watch/<int:channel_id>')
def watch_channel(channel_id=None):
    if channel_id is None:
        channel = Channel.query.options(
            joinedload(Channel.category), selectinload(Channel.stream_qualities)
        ).filter_by(is_active=True).order_by(Channel.order, Channel.name).first()
        if not channel:
            flash('No channels available', 'error')
            return redirect(url_for('index'))
    else:
        channel = Channel.query.options(
            joinedload(Channel.category), selectinload(Channel.stream_qualities)
        ).filter_by(id=channel_id).first_or_404()
        if not channel.is_active:
            flash('This channel is not available', 'error')
            return redirect(url_for('index'))

    all_channels = Channel.query.options(joinedload(Channel.category))\
        .filter_by(is_active=True).order_by(Channel.order, Channel.name).all()
    categories   = Category.query.all()
    channel_dict = channel_api_data(channel)
    featured_event = None
    event_id = request.args.get('event_id', type=int)
    if event_id:
        candidate_event = FeaturedSportsEvent.query.get(event_id)
        if candidate_event and any(
            broadcast_channel.id == channel.id
            for broadcast_channel in candidate_event.broadcast_channels
        ):
            featured_event = candidate_event

    return render_template('watch.html',
                           channel=channel,
                           channel_data=channel_dict,
                           all_channels=all_channels,
                           categories=categories,
                           featured_event=featured_event)


@app.route('/category/<int:category_id>')
def category_channels(category_id):
    category   = Category.query.get_or_404(category_id)
    categories = Category.query.all()
    page = max(request.args.get('page', 1, type=int), 1)
    channel_page = Channel.query.options(joinedload(Channel.category))\
        .filter_by(category_id=category_id, is_active=True)\
        .order_by(Channel.order, Channel.name)\
        .paginate(page=page, per_page=CHANNELS_PER_PAGE, error_out=False)
    channels = channel_page.items
    epg_channels = [
        {'id': channel.id, 'name': channel.name}
        for channel in channels if channel.epg_channel_id
    ]
    return render_template(
        'index.html', channels=channels, channel_page=channel_page,
        categories=categories,
        selected_category=category, epg_channels=epg_channels
    )


# ==================== API ROUTES ====================

@app.route('/api/channels')
def api_channels():
    channels = Channel.query.options(
        joinedload(Channel.category), selectinload(Channel.stream_qualities)
    ).filter_by(is_active=True).order_by(Channel.order, Channel.name).all()
    return jsonify([channel_api_data(channel) for channel in channels])


@app.route('/api/channels/<int:channel_id>')
def api_channel_detail(channel_id):
    channel = Channel.query.options(
        joinedload(Channel.category), selectinload(Channel.stream_qualities)
    ).filter_by(id=channel_id, is_active=True).first_or_404()
    return jsonify(channel_api_data(channel))


@app.route('/healthz')
def healthz():
    return jsonify({'status': 'ok'})


@app.route('/api/categories')
def api_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])


@app.route('/api/featured-sports')
def api_featured_sports():
    """Get upcoming featured sports events"""
    try:
        events = _visible_featured_sports_query(datetime.now()).limit(10).all()
        
        events_data = []
        for event in events:
            events_data.append({
                'id': event.id,
                'title': event.event_title,
                'channel_id': event.channel_id,
                'channel_name': event.channel.name if event.channel else 'N/A',
                'channel_ids': [channel.id for channel in event.broadcast_channels],
                'channel_names': [channel.name for channel in event.broadcast_channels],
                'event_date': event.start_time.strftime('%B %d, %Y') if event.start_time else '',
                'event_time': event.start_time.strftime('%I:%M %p') if event.start_time else '',
                'description': event.event_description or '',
                'teams': event.teams_playing or '',
                'category': event.category or ''
            })
        
        return jsonify({'events': events_data})
    except Exception as e:
        return jsonify({'error': str(e), 'events': []}), 500


# ==================== EPG API ====================

BD_TIMEZONE = timezone(timedelta(hours=6), 'Asia/Dhaka')


def _parse_epg_datetime(value):
    """Parse an epg.pw JSON timestamp and return it in Bangladesh time."""
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=BD_TIMEZONE)
    return parsed.astimezone(BD_TIMEZONE)


@app.route('/api/epg/<int:channel_id>')
def api_epg(channel_id):
    """Fetch the current and next three programmes in Bangladesh time."""
    channel = Channel.query.get_or_404(channel_id)

    if not channel.epg_channel_id:
        return jsonify({'error': 'No EPG configured for this channel'}), 404

    now = datetime.now(BD_TIMEZONE)

    def fetch_programmes(date):
        response = req_lib.get(
            'https://epg.pw/api/epg.json',
            params={'lang': 'en', 'date': date, 'channel_id': channel.epg_channel_id},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError('EPG provider returned an invalid JSON response')
        if data.get('error_message'):
            raise ValueError(data['error_message'])

        day_programmes = []
        epg_list = data.get('epg_list', [])
        if not isinstance(epg_list, list):
            raise ValueError('EPG provider response is missing a valid epg_list')
        for prog in epg_list:
            if not isinstance(prog, dict):
                continue
            start_dt = _parse_epg_datetime(prog.get('start_date'))
            if not start_dt:
                continue

            day_programmes.append({
                'title': (prog.get('title') or '').strip(),
                'desc': (prog.get('desc') or '').strip(),
                'category': (prog.get('category') or '').strip(),
                'icon': prog.get('icon', ''),
                'start': start_dt.isoformat(),
                'start_fmt': start_dt.strftime('%H:%M'),
            })

        return day_programmes

    try:
        today = now.strftime('%Y%m%d')
        programmes = []
        if now.hour < 2:
            yesterday = (now - timedelta(days=1)).strftime('%Y%m%d')
            programmes.extend(fetch_programmes(yesterday))
        programmes.extend(fetch_programmes(today))
        upcoming = {
            (p['start'], p['title'])
            for p in programmes
            if datetime.fromisoformat(p['start']) > now
        }
        if len(upcoming) < 3:
            tomorrow = (now + timedelta(days=1)).strftime('%Y%m%d')
            programmes.extend(fetch_programmes(tomorrow))
    except (req_lib.RequestException, ValueError) as e:
        return jsonify({'error': f'Failed to fetch EPG: {e}'}), 502

    programmes = list({
        (p['start'], p['title']): p for p in programmes
    }.values())
    programmes.sort(key=lambda p: p['start'])

    for index, programme in enumerate(programmes):
        if index + 1 >= len(programmes):
            continue
        stop_dt = datetime.fromisoformat(programmes[index + 1]['start'])
        programme['stop'] = stop_dt.isoformat()
        programme['stop_fmt'] = stop_dt.strftime('%H:%M')
        start_dt = datetime.fromisoformat(programme['start'])
        programme['is_live'] = start_dt <= now < stop_dt

    current = next((p for p in programmes if p['is_live']), None)
    upcoming = [
        p for p in programmes
        if datetime.fromisoformat(p['start']) > now
    ][:3]

    return jsonify({
        'channel_id':  channel_id,
        'channel_name': channel.name,
        'timezone': 'Asia/Dhaka',
        'current':  current,
        'upcoming': upcoming,
        'all':      programmes
    })


# ==================== ADMIN ROUTES ====================

@app.route('/admin/login', methods=['GET', 'POST'])
@app.route('/sz-secure-panel-2024', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash, password):
            login_user(User(admin.id, admin.username))
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('admin/login.html')


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin_dashboard():
    channels   = Channel.query.order_by(Channel.order, Channel.name).all()
    categories = Category.query.all()
    featured_sports = FeaturedSportsEvent.query.order_by(FeaturedSportsEvent.order, FeaturedSportsEvent.start_time.desc()).all()
    stats = {
        'total_channels':  Channel.query.count(),
        'active_channels': Channel.query.filter_by(is_active=True).count(),
        'total_categories': Category.query.count(),
        'featured_sports': FeaturedSportsEvent.query.filter_by(is_active=True).count(),
    }
    return render_template('admin/dashboard.html', channels=channels, categories=categories, 
                          featured_sports=featured_sports, stats=stats,
                          persistent_database_configured=app.config['PERSISTENT_DATABASE_CONFIGURED'])


@app.route('/admin/channels/add', methods=['GET', 'POST'])
@login_required
def admin_add_channel():
    if request.method == 'POST':
        from models import StreamQuality
        name             = request.form.get('name')
        stream_url       = request.form.get('stream_url')
        stream_url_backup= request.form.get('stream_url_backup', '')
        stream_type      = request.form.get('stream_type')
        logo_url         = request.form.get('logo_url', '')
        description      = request.form.get('description', '')
        category_id      = request.form.get('category_id')
        user_agent       = request.form.get('user_agent', '')
        referer          = request.form.get('referer', '')
        epg_channel_id   = request.form.get('epg_channel_id', '').strip()
        is_active        = request.form.get('is_active') == 'on'
        order            = request.form.get('order', 0, type=int)

        channel = Channel(name=name, stream_url=stream_url, stream_url_backup=stream_url_backup,
                          stream_type=stream_type, logo_url=logo_url, description=description,
                          category_id=int(category_id) if category_id else None,
                          user_agent=user_agent, referer=referer,
                          epg_channel_id=epg_channel_id or None,
                          is_active=is_active, order=order)
        db.session.add(channel)
        db.session.flush()

        quality_labels   = request.form.getlist('quality_label[]')
        quality_urls     = request.form.getlist('quality_url[]')
        quality_bitrates = request.form.getlist('quality_bitrate[]')
        quality_defaults = request.form.getlist('quality_default[]')

        for idx, (label, url) in enumerate(zip(quality_labels, quality_urls)):
            if label and url:
                bitrate    = int(quality_bitrates[idx]) if idx < len(quality_bitrates) and quality_bitrates[idx] else None
                is_default = str(idx + 1) in quality_defaults
                db.session.add(StreamQuality(channel_id=channel.id, quality_label=label,
                                             stream_url=url, bitrate=bitrate,
                                             is_default=is_default, order=idx))
        db.session.commit()
        flash(f'Channel "{name}" added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    categories = Category.query.all()
    return render_template('admin/add_channel.html', categories=categories)


@app.route('/admin/channels/edit/<int:channel_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_channel(channel_id):
    from models import StreamQuality
    channel = Channel.query.get_or_404(channel_id)

    if request.method == 'POST':
        channel.name             = request.form.get('name')
        channel.stream_url       = request.form.get('stream_url')
        channel.stream_url_backup= request.form.get('stream_url_backup', '')
        channel.stream_type      = request.form.get('stream_type')
        channel.logo_url         = request.form.get('logo_url', '')
        channel.description      = request.form.get('description', '')
        channel.user_agent       = request.form.get('user_agent', '')
        channel.referer          = request.form.get('referer', '')
        channel.epg_channel_id   = request.form.get('epg_channel_id', '').strip() or None
        category_id              = request.form.get('category_id')
        channel.category_id      = int(category_id) if category_id else None
        channel.is_active        = request.form.get('is_active') == 'on'
        channel.order            = request.form.get('order', 0, type=int)

        deleted = request.form.get('deleted_qualities', '')
        for qid in deleted.split(','):
            if qid:
                q = StreamQuality.query.get(int(qid))
                if q and q.channel_id == channel.id:
                    db.session.delete(q)

        quality_ids      = request.form.getlist('quality_id[]')
        quality_labels   = request.form.getlist('quality_label[]')
        quality_urls     = request.form.getlist('quality_url[]')
        quality_bitrates = request.form.getlist('quality_bitrate[]')
        quality_defaults = request.form.getlist('quality_default[]')

        for idx, (qid, label, url) in enumerate(zip(quality_ids, quality_labels, quality_urls)):
            if label and url:
                bitrate    = int(quality_bitrates[idx]) if idx < len(quality_bitrates) and quality_bitrates[idx] else None
                is_default = str(qid) in quality_defaults or f'new-{idx+1}' in quality_defaults
                if qid == 'new':
                    db.session.add(StreamQuality(channel_id=channel.id, quality_label=label,
                                                 stream_url=url, bitrate=bitrate,
                                                 is_default=is_default, order=idx))
                else:
                    q = StreamQuality.query.get(int(qid))
                    if q and q.channel_id == channel.id:
                        q.quality_label = label; q.stream_url = url
                        q.bitrate = bitrate; q.is_default = is_default; q.order = idx

        db.session.commit()
        flash(f'Channel "{channel.name}" updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    categories = Category.query.all()
    return render_template('admin/edit_channel.html', channel=channel, categories=categories)


@app.route('/admin/channels/delete/<int:channel_id>', methods=['POST'])
@login_required
def admin_delete_channel(channel_id):
    channel = Channel.query.get_or_404(channel_id)
    name    = channel.name
    db.session.delete(channel)
    db.session.commit()
    flash(f'Channel "{name}" deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/categories/add', methods=['GET', 'POST'])
@login_required
def admin_add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        if Category.query.filter_by(name=name).first():
            flash('Category already exists!', 'error')
        else:
            db.session.add(Category(name=name))
            db.session.commit()
            flash(f'Category "{name}" added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
    return render_template('admin/add_category.html')


@app.route('/admin/categories/delete/<int:category_id>', methods=['POST'])
@login_required
def admin_delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    name     = category.name
    Channel.query.filter_by(category_id=category.id).update(
        {Channel.category_id: None}, synchronize_session=False
    )
    db.session.delete(category)
    db.session.commit()
    flash(f'Category "{name}" deleted. Channels were left uncategorized.', 'success')
    return redirect(url_for('admin_dashboard'))


# ==================== FEATURED SPORTS ADMIN ROUTES ====================

@app.route('/admin/featured-sports/browse')
@login_required
def admin_browse_sports_epg():
    """Browse EPG data from channels to select sports events"""
    channels_with_epg = Channel.query.filter(Channel.epg_channel_id.isnot(None)).all()
    return render_template('admin/browse_sports_epg.html', channels=channels_with_epg)


@app.route('/admin/epg-test')
@login_required
def admin_epg_test():
    """Simple EPG test page"""
    channels_with_epg = Channel.query.filter(Channel.epg_channel_id.isnot(None)).all()
    return render_template('admin/epg_test.html', channels=channels_with_epg)


@app.route('/admin/featured-sports/add', methods=['GET', 'POST'])
@login_required
def admin_add_featured_sports():
    if request.method == 'POST':
        channel_ids = request.form.getlist('channel_ids', type=int)
        if not channel_ids:
            legacy_channel_id = request.form.get('channel_id', type=int)
            if legacy_channel_id:
                channel_ids = [legacy_channel_id]
        channel_ids = list(dict.fromkeys(channel_ids))
        channels_by_id = {
            channel.id: channel
            for channel in Channel.query.filter(Channel.id.in_(channel_ids)).all()
        } if channel_ids else {}
        if not channel_ids or len(channels_by_id) != len(channel_ids):
            flash('Select at least one valid channel for this event.', 'error')
            return redirect(url_for('admin_add_featured_sports'))
        selected_channels = [channels_by_id[channel_id] for channel_id in channel_ids]
        event_title = request.form.get('event_title')
        event_description = request.form.get('event_description', '')
        thumbnail_url = request.form.get('thumbnail_url', '')
        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time', '')
        category = request.form.get('category', '')
        league_tournament = request.form.get('league_tournament', '')
        teams_playing = request.form.get('teams_playing', '')
        is_active = request.form.get('is_active') == 'on'
        order = request.form.get('order', 0, type=int)
        
        # Parse datetime
        try:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str) if end_time_str else None
        except (TypeError, ValueError):
            flash('Invalid date/time format', 'error')
            return redirect(url_for('admin_add_featured_sports'))
        if end_time and end_time < start_time:
            end_time += timedelta(days=1)
        
        featured_event = FeaturedSportsEvent(
            channel_id=selected_channels[0].id,
            channels=selected_channels,
            event_title=event_title,
            event_description=event_description,
            thumbnail_url=thumbnail_url,
            start_time=start_time,
            end_time=end_time,
            category=category,
            league_tournament=league_tournament,
            teams_playing=teams_playing,
            is_active=is_active,
            order=order
        )
        db.session.add(featured_event)
        db.session.commit()
        flash(f'Featured sports event "{event_title}" added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    channels = Channel.query.order_by(Channel.name).all()
    selected_channel_ids = request.args.getlist('channel_ids', type=int)
    if not selected_channel_ids:
        channel_id = request.args.get('channel_id', type=int)
        if channel_id:
            selected_channel_ids = [channel_id]
    return render_template(
        'admin/add_featured_sports.html',
        channels=channels,
        selected_channel_ids=selected_channel_ids,
    )


@app.route('/admin/featured-sports/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_featured_sports(event_id):
    event = FeaturedSportsEvent.query.get_or_404(event_id)
    
    if request.method == 'POST':
        channel_ids = request.form.getlist('channel_ids', type=int)
        if not channel_ids:
            legacy_channel_id = request.form.get('channel_id', type=int)
            if legacy_channel_id:
                channel_ids = [legacy_channel_id]
        channel_ids = list(dict.fromkeys(channel_ids))
        channels_by_id = {
            channel.id: channel
            for channel in Channel.query.filter(Channel.id.in_(channel_ids)).all()
        } if channel_ids else {}
        if not channel_ids or len(channels_by_id) != len(channel_ids):
            flash('Select at least one valid channel for this event.', 'error')
            return redirect(url_for('admin_edit_featured_sports', event_id=event_id))
        selected_channels = [channels_by_id[channel_id] for channel_id in channel_ids]
        event.channel_id = selected_channels[0].id
        event.channels = selected_channels
        event.event_title = request.form.get('event_title')
        event.event_description = request.form.get('event_description', '')
        event.thumbnail_url = request.form.get('thumbnail_url', '')
        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time', '')
        event.category = request.form.get('category', '')
        event.league_tournament = request.form.get('league_tournament', '')
        event.teams_playing = request.form.get('teams_playing', '')
        event.is_active = request.form.get('is_active') == 'on'
        event.order = request.form.get('order', 0, type=int)
        
        # Parse datetime
        try:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str) if end_time_str else None
        except (TypeError, ValueError):
            flash('Invalid date/time format', 'error')
            return redirect(url_for('admin_edit_featured_sports', event_id=event_id))
        if end_time and end_time < start_time:
            end_time += timedelta(days=1)
        event.start_time = start_time
        event.end_time = end_time
        
        db.session.commit()
        flash(f'Featured sports event "{event.event_title}" updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    channels = Channel.query.order_by(Channel.name).all()
    selected_channel_ids = [channel.id for channel in event.broadcast_channels]
    return render_template(
        'admin/edit_featured_sports.html',
        event=event,
        channels=channels,
        selected_channel_ids=selected_channel_ids,
    )


@app.route('/admin/featured-sports/delete/<int:event_id>', methods=['POST'])
@login_required
def admin_delete_featured_sports(event_id):
    event = FeaturedSportsEvent.query.get_or_404(event_id)
    title = event.event_title
    db.session.delete(event)
    db.session.commit()
    flash(f'Featured sports event "{title}" deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    original_exception = getattr(error, 'original_exception', None)
    if original_exception:
        app.logger.error(
            'Unhandled server error on %s %s',
            request.method,
            request.path,
            exc_info=(
                type(original_exception),
                original_exception,
                original_exception.__traceback__,
            ),
        )
    else:
        app.logger.error(
            'HTTP 500 while handling %s %s: %s',
            request.method,
            request.path,
            error,
        )
    db.session.rollback()
    return render_template('500.html'), 500


# ==================== RUN ====================

if __name__ == '__main__':
    init_db()
    if app.config['SECRET_KEY'] == DEFAULT_SECRET_KEY:
        print('WARNING: SECRET_KEY is using the default value. Set SECRET_KEY in .env before production use.')
    debug = os.getenv('FLASK_DEBUG', 'false').lower() in ('1', 'true', 'yes')
    if not debug and (
        app.config['SECRET_KEY'] == DEFAULT_SECRET_KEY
        or os.getenv('ADMIN_PASSWORD') is None
    ):
        raise RuntimeError('Refusing to start in production with default SECRET_KEY or ADMIN_PASSWORD')
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    app.run(debug=debug, host=host, port=port)
