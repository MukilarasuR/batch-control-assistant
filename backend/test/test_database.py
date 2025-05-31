"""
Test script to verify database connection and operations
Run this to test your setup
"""
import sys, os

# Insert the project’s root (backend/) into sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


from database.database import test_connection, create_tables, SessionLocal
from services.crud_service import get_batch_by_code, get_batch_statistics
from models import *
from datetime import date, datetime


def test_database_setup():
    """Test database connection and basic operations"""
    print("🧪 Testing Database Setup...")

    # Test 1: Database Connection
    print("\n1️⃣ Testing database connection...")
    if not test_connection():
        print("❌ Database connection failed. Check your config.py settings.")
        return False

    # Test 2: Create Tables
    print("\n2️⃣ Creating database tables...")
    try:
        create_tables()
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

    # Test 3: Basic CRUD Operations
    print("\n3️⃣ Testing CRUD operations...")
    db = SessionLocal()

    try:
        # Test getting a batch (should return None if no data)
        batch = get_batch_by_code(db, "VDT-052025-A")
        if batch:
            print(f"✅ Found batch: {batch.batch_code}")
        else:
            print("ℹ️ No sample batch found (normal if database is empty)")

        # Test statistics
        stats = get_batch_statistics(db)
        print(f"✅ Batch statistics: {stats}")

        print("\n✅ All database tests passed!")
        return True

    except Exception as e:
        print(f"❌ CRUD test failed: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    test_database_setup()
