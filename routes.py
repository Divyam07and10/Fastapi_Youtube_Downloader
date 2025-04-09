from fastapi import APIRouter, BackgroundTasks, HTTPException, status, Query
from schemas import DownloadRequest
from services import start_download_task, extract_video_metadata
import os

router = APIRouter()

@router.post("/download")
async def download_video_or_audio(request: DownloadRequest, background_tasks: BackgroundTasks):
    # Validate inputs
    allowed_formats = ["mp4", "webm", "mkv", "mp3"]
    allowed_qualities = ["360p", "480p", "720p", "1080p", "4k"]

    if request.format not in allowed_formats:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid format. Allowed: {allowed_formats}")
    if request.format != "mp3" and request.quality not in allowed_qualities:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid quality. Allowed: {allowed_qualities}")

    # Trigger background download
    background_tasks.add_task(start_download_task, request)

    return {
        "status": "success",
        "message": "Download started in background"
    }

@router.get("/metadata")
async def get_metadata(url: str = Query(..., description="YouTube video URL")):
    try:
        return extract_video_metadata(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
