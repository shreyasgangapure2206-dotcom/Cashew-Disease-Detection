"""
Database Initialization Script for Cashew Disease Detection
Run this script to initialize the database with tables.
"""

import os
import sys
from app import app, db
from models import Prediction, DiseaseInfo

def init_database():
    """Initialize the database with all tables"""
    with app.app_context():
        print("[DB] Creating database tables...")
        db.create_all()
        print("[DB] ✓ Database tables created successfully")
        
        # Count existing predictions
        prediction_count = Prediction.query.count()
        print(f"[DB] Total predictions in database: {prediction_count}")
        
        print("\n[DB] ✓ Database initialization complete!")
        print("[DB] You can now run: python app.py")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}")
        sys.exit(1)
