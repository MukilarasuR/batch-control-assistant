"""
Database connection and session management
"""
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker  # Updated import for SQLAlchemy 2.0+

# Now import settings
try:
    from app.config import settings

    print("✅ Successfully imported settings")
except ImportError as e:
    print(f"❌ Import error: {e}")


    # Fallback configuration
    class FallbackSettings:
        DATABASE_URL = "postgresql://postgres:2309@localhost:5432/chatbot_db"
        DEBUG = True


    settings = FallbackSettings()

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Set to True to see SQL queries in console
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300  # Recycle connections every 5 minutes
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create Base class for our models
Base = declarative_base()


# Dependency to get database session
def get_db():
    """
    Database session dependency for FastAPI
    Yields a database session and ensures it's closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to create all tables
def create_tables():
    """
    Create all database tables
    Call this function to initialize your database
    """
    Base.metadata.create_all(bind=engine)
    print("✅ All database tables created successfully!")


# Function to test database connection
def test_connection():
    """
    Test database connection
    """
    try:
        db = SessionLocal()
        # Use text() for raw SQL in SQLAlchemy 2.0+
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


# Optional: Add a main section to test when running directly
if __name__ == "__main__":  # Fixed: double underscores
    print("Testing database connection...")
    test_connection()
