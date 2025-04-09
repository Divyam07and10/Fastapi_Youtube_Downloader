from fastapi import FastAPI
from routes import router as api_router
from utils import create_download_directory

# Ensure downloads directory exists
create_download_directory("downloads")

# Create FastAPI instance
app = FastAPI(title="YouTube Downloader API",)

# Register API routes
app.include_router(api_router)
