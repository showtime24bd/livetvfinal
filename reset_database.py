#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Reset database - Use this when you update models
WARNING: This will delete all existing data!
"""
import os
from app import app, db, init_db

def reset_database():
    with app.app_context():
        # Check if database exists
        db_path = 'instance/livetv.db'
        if os.path.exists(db_path):
            response = input("WARNING: This will delete all existing data! Continue? (yes/no): ")
            if response.lower() != 'yes':
                print("Operation cancelled.")
                return
            
            # Drop all tables
            print("Dropping all tables...")
            db.drop_all()
            print("Tables dropped!")
        
        # Create all tables
        print("Creating new tables...")
        db.create_all()
        print("Tables created!")
        
        # Initialize with default data
        print("Adding default data...")
        init_db()
        print("\nDatabase reset complete!")
        print("\nDefault admin credentials:")
        print("  Username: admin")
        print("  Password: admin123")

if __name__ == '__main__':
    reset_database()
