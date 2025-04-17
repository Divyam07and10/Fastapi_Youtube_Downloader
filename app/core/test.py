import os
from dotenv import load_dotenv

load_dotenv()


MAX_VIDEO_SIZE = int(os.getenv("MAX_VIDEO_SIZE", 3 * 1024 * 1024 * 1024))
print("DEBUG: MAX_VIDEO_SIZE =", MAX_VIDEO_SIZE)