from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import os, time
from app.schemas.download import DownloadRequest
from app.db.database import get_db
from app.db.models import DownloadHistory
from app.services.downloader import start_download
from app.utils.validators import is_valid_youtube_url, validate_video_constraints
from app.core.rate_limit import check_rate_limit
from app.core.security import validate_api_key

router = APIRouter()

DOWNLOADS_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

ALLOWED_FORMATS = ['mp4', 'webm', 'mkv', 'mp3']
ALLOWED_QUALITIES = ['360p', '480p', '720p', '1080p', '4k']

@router.post("/download")
async def download_video(
    request: DownloadRequest,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(validate_api_key),
    req: Request = None
):
    if not is_valid_youtube_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL format.")
    
    if request.format not in ALLOWED_FORMATS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported format. Allowed: {ALLOWED_FORMATS}")
    if request.quality.lower() not in ALLOWED_QUALITIES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported quality. Allowed: {ALLOWED_QUALITIES}")

    ip = req.client.host
    await check_rate_limit(ip)
    
    # ✅ Check size and duration limits BEFORE proceeding
    await validate_video_constraints(request.url, db)

    timestamp = int(time.time())
    file_root = f"download_{timestamp}"
    output_path = os.path.join(DOWNLOADS_DIR, file_root)
    final_file = f"{output_path}.{request.format}"
    download_url = f"/files/{os.path.basename(final_file)}"

    history = DownloadHistory(
        url=request.url,
        status="Started",
        downloaded_at=datetime.utcnow(),
        download_url=download_url
    )
    db.add(history)
    await db.commit()
    await db.refresh(history)

    start_download(request, output_path, final_file, history.id)

    return {"status": "success", "message": "Download started"}
