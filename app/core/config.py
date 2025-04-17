import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# API Key for authentication
API_KEY = os.getenv("KEY", "default_api_key")

# Redis connection URLs
REDIS_BROKER_URL = os.getenv("REDIS_BROKER_URL", "redis://localhost:6379/0")
REDIS_BACKEND_URL = os.getenv("REDIS_BACKEND_URL", "redis://localhost:6379/0")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")

# Database connection details
DB_USERNAME = os.getenv("DB_USERNAME", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME", "youtube_db")

# Max downloads per day and rate limit expiry time (in seconds)
MAX_DOWNLOADS_PER_DAY = os.getenv("MAX_DOWNLOADS_PER_DAY", 100)
RATE_LIMIT_EXPIRY = os.getenv("RATE_LIMIT_EXPIRY", 86400) # 86400 seconds = 1 day

MAX_VIDEO_SIZE = int(os.getenv("MAX_VIDEO_SIZE", 3 * 1024 * 1024 * 1024))
MAX_VIDEO_DURATION = int(os.getenv("MAX_VIDEO_DURATION", 5 * 60 * 60))     # 5 hours