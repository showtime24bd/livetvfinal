"""
Add Sample Featured Sports Events
"""
from app import app, db
from models import FeaturedSportsEvent, Channel
from datetime import datetime, timedelta

def add_sample_events():
    with app.app_context():
        # Get first channel (or create a default one)
        channel = Channel.query.first()
        
        if not channel:
            print("❌ No channels found! Please add channels first from admin panel.")
            print("   Go to: http://localhost:5000/admin/login")
            return
        
        # Clear existing events (optional)
        print("Clearing old events...")
        FeaturedSportsEvent.query.delete()
        
        # Sample upcoming sports events
        now = datetime.now()
        
        events = [
            {
                'event_title': '🏆 Premier League: Manchester United vs Liverpool',
                'teams_playing': 'Man United vs Liverpool',
                'category': 'Football',
                'event_description': 'Epic clash between two football giants',
                'start_time': now + timedelta(hours=2),
                'end_time': now + timedelta(hours=4),
                'thumbnail_url': '',
                'order': 1,
                'is_active': True
            },
            {
                'event_title': '🏏 India vs Australia - T20 World Cup',
                'teams_playing': 'India vs Australia',
                'category': 'Cricket',
                'event_description': 'Thrilling T20 cricket match',
                'start_time': now + timedelta(days=1, hours=5),
                'end_time': now + timedelta(days=1, hours=8),
                'thumbnail_url': '',
                'order': 2,
                'is_active': True
            },
            {
                'event_title': '⚽ UEFA Champions League Final',
                'teams_playing': 'Real Madrid vs Bayern Munich',
                'category': 'Football',
                'event_description': 'The ultimate European club football championship',
                'start_time': now + timedelta(days=2, hours=8),
                'end_time': now + timedelta(days=2, hours=10),
                'thumbnail_url': '',
                'order': 3,
                'is_active': True
            },
            {
                'event_title': '🎾 Wimbledon Finals - Men\'s Singles',
                'teams_playing': 'Djokovic vs Alcaraz',
                'category': 'Tennis',
                'event_description': 'Epic tennis showdown at Wimbledon',
                'start_time': now + timedelta(days=3, hours=6),
                'end_time': now + timedelta(days=3, hours=10),
                'thumbnail_url': '',
                'order': 4,
                'is_active': True
            },
            {
                'event_title': '🏀 NBA Finals - Game 7',
                'teams_playing': 'Lakers vs Celtics',
                'category': 'Basketball',
                'event_description': 'Championship deciding game',
                'start_time': now + timedelta(days=4, hours=9),
                'end_time': now + timedelta(days=4, hours=12),
                'thumbnail_url': '',
                'order': 5,
                'is_active': True
            },
            {
                'event_title': '🏏 Pakistan vs Bangladesh - ODI Series',
                'teams_playing': 'Pakistan vs Bangladesh',
                'category': 'Cricket',
                'event_description': 'One Day International cricket match',
                'start_time': now + timedelta(days=5, hours=3),
                'end_time': now + timedelta(days=5, hours=9),
                'thumbnail_url': '',
                'order': 6,
                'is_active': True
            }
        ]
        
        print(f"\n✅ Adding {len(events)} sample events...")
        
        for event_data in events:
            event = FeaturedSportsEvent(
                channel_id=channel.id,
                **event_data
            )
            db.session.add(event)
            print(f"   ✓ {event_data['event_title']}")
        
        db.session.commit()
        
        print(f"\n🎉 Successfully added {len(events)} featured sports events!")
        print(f"📺 All events are linked to channel: {channel.name}")
        print(f"\n📱 Now restart your backend server and open Menu in Android TV app!")
        print(f"   Backend: python run.py")
        print(f"   Android: Press Menu button to see events")

if __name__ == '__main__':
    add_sample_events()
