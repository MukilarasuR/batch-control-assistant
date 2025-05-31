"""
Configuration settings for the ERP Chatbot application
"""
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Database Configuration Components
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "chatbot_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "2309")  # Your actual password

    # Properly encode password for URL (handles special characters like @)
    _encoded_password = quote_plus(DB_PASSWORD)

    # Construct DATABASE_URL with proper encoding
    DATABASE_URL = f"postgresql://{DB_USER}:{_encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Alternative: You can also set DATABASE_URL directly from environment
    # DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{DB_USER}:{_encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    # Application Settings
    APP_NAME = "ERP Chatbot - Batch Control"
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # API Configuration
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("API_PORT", "8000"))

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")

    # AI/ML Settings (for later phases)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # Redis Settings (optional - for Phase 6)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Create settings instance
settings = Settings()

# Debug print to verify DATABASE_URL (remove in production)
if __name__ == "__main__":
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"App name: {settings.APP_NAME}")