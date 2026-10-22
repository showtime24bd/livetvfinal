from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

featured_event_channels = db.Table(
    'featured_event_channels',
    db.Column('event_id', db.Integer, db.ForeignKey('featured_sports_events.id'), primary_key=True),
    db.Column('channel_id', db.Integer, db.ForeignKey('channels.id'), primary_key=True),
)

class Category(db.Model):
    """Category model for organizing channels"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Channels stay in the catalog when a category is deleted.
    channels = db.relationship('Channel', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Channel(db.Model):
    """Channel model for storing live TV channel information"""
    __tablename__ = 'channels'
    __table_args__ = (
        db.Index('ix_channels_active_order_name', 'is_active', 'order', 'name'),
        db.Index('ix_channels_category_active_order', 'category_id', 'is_active', 'order'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    stream_url = db.Column(db.String(500), nullable=False)
    stream_url_backup = db.Column(db.String(500))  # Backup/alternative stream URL
    stream_type = db.Column(db.String(20), nullable=False)  # m3u8, mpd, ts, mp4, flv
    logo_url = db.Column(db.String(500))
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    user_agent = db.Column(db.String(500))  # Custom user agent for streams that require it
    referer = db.Column(db.String(500))  # Custom referer for streams that require it
    epg_channel_id = db.Column(db.String(100))  # EPG channel ID (epg.pw)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship for multiple stream qualities
    stream_qualities = db.relationship('StreamQuality', backref='channel', lazy=True, cascade='all, delete-orphan')
    featured_events = db.relationship(
        'FeaturedSportsEvent', backref='channel', lazy=True, cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<Channel {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'stream_url': self.stream_url,
            'stream_url_backup': self.stream_url_backup,
            'stream_type': self.stream_type,
            'logo_url': self.logo_url,
            'description': self.description,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'is_active': self.is_active,
            'order': self.order,
            'user_agent': self.user_agent,
            'referer': self.referer,
            'epg_channel_id': self.epg_channel_id,
            'stream_qualities': [sq.to_dict() for sq in self.stream_qualities],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class StreamQuality(db.Model):
    """Multiple quality options for a channel"""
    __tablename__ = 'stream_qualities'
    
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False, index=True)
    quality_label = db.Column(db.String(50), nullable=False)  # e.g., "1080p", "720p", "480p", "Auto"
    stream_url = db.Column(db.String(500), nullable=False)
    bitrate = db.Column(db.Integer)  # in kbps
    is_default = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<StreamQuality {self.quality_label} for Channel {self.channel_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'channel_id': self.channel_id,
            'quality_label': self.quality_label,
            'stream_url': self.stream_url,
            'bitrate': self.bitrate,
            'is_default': self.is_default,
            'order': self.order
        }


class FeaturedSportsEvent(db.Model):
    """Featured sports events to display on homepage"""
    __tablename__ = 'featured_sports_events'
    __table_args__ = (
        db.Index('ix_featured_events_active_start_order', 'is_active', 'start_time', 'order'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    event_title = db.Column(db.String(300), nullable=False)
    event_description = db.Column(db.Text)
    thumbnail_url = db.Column(db.String(500))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    category = db.Column(db.String(100))  # e.g., "Football", "Cricket", "Basketball"
    league_tournament = db.Column(db.String(200))  # e.g., "EPL", "IPL", "UEFA Champions League"
    teams_playing = db.Column(db.String(300))  # e.g., "Arsenal vs Chelsea"
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    channels = db.relationship('Channel', secondary=featured_event_channels, lazy='selectin')

    @property
    def broadcast_channels(self):
        return self.channels or ([self.channel] if self.channel else [])
    
    def __repr__(self):
        return f'<FeaturedSportsEvent {self.event_title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'channel_id': self.channel_id,
            'channel_name': self.channel.name if self.channel else None,
            'channel_logo': self.channel.logo_url if self.channel else None,
            'channel_ids': [channel.id for channel in self.broadcast_channels],
            'channel_names': [channel.name for channel in self.broadcast_channels],
            'event_title': self.event_title,
            'event_description': self.event_description,
            'thumbnail_url': self.thumbnail_url,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'category': self.category,
            'league_tournament': self.league_tournament,
            'teams_playing': self.teams_playing,
            'is_active': self.is_active,
            'order': self.order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Admin(db.Model):
    """Admin model for authentication"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Admin {self.username}>'
