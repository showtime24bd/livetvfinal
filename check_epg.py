"""Check which channels have EPG IDs configured"""

from app import app, db
from models import Channel

def check_epg():
    with app.app_context():
        channels = Channel.query.all()
        
        print("\n" + "="*60)
        print("CHANNELS EPG STATUS")
        print("="*60)
        
        has_epg = []
        no_epg = []
        
        for channel in channels:
            if channel.epg_channel_id:
                has_epg.append(channel)
                print(f"✓ {channel.name}")
                print(f"  EPG ID: {channel.epg_channel_id}")
            else:
                no_epg.append(channel)
                print(f"✗ {channel.name}")
                print(f"  EPG ID: NOT SET")
            print()
        
        print("="*60)
        print(f"Summary:")
        print(f"  Channels with EPG: {len(has_epg)}")
        print(f"  Channels without EPG: {len(no_epg)}")
        print("="*60)
        
        if no_epg:
            print("\n⚠️  To enable EPG browsing:")
            print("   1. Go to admin panel")
            print("   2. Edit each channel")
            print("   3. Add EPG Channel ID")
            print("\n📝 How to find EPG IDs:")
            print("   1. Visit: https://epg.pw/")
            print("   2. Search for your channel")
            print("   3. Copy the channel ID")
            print("\n   Example EPG IDs:")
            print("   - Star Sports 1: starsports1hd.in")
            print("   - Sony Ten 1: sonyten1hd.in")
            print("   - Sky Sports: skysportspremierleague.uk")

if __name__ == '__main__':
    check_epg()
