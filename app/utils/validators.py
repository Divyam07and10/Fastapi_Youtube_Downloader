import re
from yt_dlp import YoutubeDL
from fastapi import HTTPException
from datetime import datetime
from app.db.models import DownloadHistory
from app.core.config import MAX_VIDEO_SIZE, MAX_VIDEO_DURATION

async def validate_video_constraints(request_url: str, session):
    """
    Validates video size and duration.
    Rejects videos >3GB or >5 hours long.
    Saves failure in history if invalid.
    """
    with YoutubeDL({'quiet': True, 'noplaylist': True}) as ydl:
        info = ydl.extract_info(request_url, download=False)
        size = info.get("filesize") or info.get("filesize_approx") or 0
        duration = info.get("duration") or 0

        if size and size > MAX_VIDEO_SIZE:
            await log_failure(session, request_url, "Video exceeds 3GB limit")
            raise HTTPException(
                status_code=413,
                detail=f"Video size exceeds 3GB limit. Size: {round(size / (1024 ** 3), 2)} GB"
            )

        if duration and duration > MAX_VIDEO_DURATION:
            await log_failure(session, request_url, "Video exceeds 5 hour duration")
            raise HTTPException(
                status_code=400,
                detail=f"Video duration exceeds 5 hour limit. Duration: {round(duration / 3600, 2)} hours"
            )

        return info


async def log_failure(session, url: str, reason: str):
    """Logs a failed download attempt in history."""
    history = DownloadHistory(
        url=url,
        status="Failed",
        downloaded_at=datetime.utcnow(),
        download_url=""
    )
    session.add(history)
    await session.commit()

def is_valid_youtube_url(url: str) -> bool:
    if url.count("http://") > 1 or url.count("https://") > 1:
        return False
    if url.count("www.") > 1:
        return False
    pattern = (
        r'^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|(?:v|e(?:mbed)?)\/|.*[?&]v=|.*[?&]embed\/|.*/)([a-zA-Z0-9_-]{11})'
    )
    return bool(re.match(pattern, url.strip()))
