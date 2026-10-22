"""
Database migration script to add FeaturedSportsEvent table
Run this after updating models.py
"""

from app import app, db
from models import FeaturedSportsEvent

def migrate():
    with app.app_context():
        print("Creating featured_sports_events table...")
        db.create_all()
        print("✓ Migration completed successfully!")
        print("\nYou can now:")
        print("  1. Go to admin panel")
        print("  2. Click 'Browse EPG Sports' to see upcoming sports events")
        print("  3. Select events to feature on homepage")
        print("  4. Add thumbnails and additional information")

if __name__ == '__main__':
    migrate()
