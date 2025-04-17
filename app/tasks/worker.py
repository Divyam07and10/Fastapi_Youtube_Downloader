from celery import Celery
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import SessionLocal
from app.db.models import DownloadHistory
from app.schemas.download import DownloadRequest
from app.utils.helpers import build_format_selector
from pytube import YouTube
import yt_dlp
from app.core.config import REDIS_BROKER_URL, REDIS_BACKEND_URL
import os

DOWNLOADS_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

celery_app = Celery(
    "worker",
    broker=REDIS_BROKER_URL,
    backend=REDIS_BACKEND_URL
)

@celery_app.task
def process_download_task(data: dict, output_path: str, final_file: str, history_id: int):
    request = DownloadRequest(**data)
    db: Session = SessionLocal()

    try:
        target_height = int(request.quality.lower().replace("k", "000").replace("p", ""))
    except Exception:
        update_status(db, history_id, "Failed")
        db.close()
        return

    format_selector = build_format_selector(request.format, target_height)

    ydl_opts = {
        "format": format_selector,
        "outtmpl": output_path,
        "quiet": True,
        "noplaylist": True,
        "postprocessors": [],
    }

    if request.format == "mp3":
        ydl_opts["postprocessors"].append({
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        })
    else:
        ydl_opts["merge_output_format"] = request.format
        ydl_opts["postprocessors"].append({
            "key": "FFmpegVideoConvertor",
            "preferedformat": request.format
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([request.url])
        update_status(db, history_id, "Completed")
    except Exception:
        try:
            yt = YouTube(request.url)
            if request.format == "mp3":
                stream = yt.streams.filter(only_audio=True).first()
            else:
                stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()

            stream.download(output_path=DOWNLOADS_DIR, filename=os.path.basename(final_file))
            update_status(db, history_id, "Completed")
        except Exception:
            update_status(db, history_id, "Failed")

    db.close()

async def update_status(db: AsyncSession, history_id: int, status: str):
    result = await db.execute(select(DownloadHistory).filter(DownloadHistory.id == history_id))
    download_history = result.scalars().first()
    if download_history:
        download_history.status = status
        await db.commit()
    else:
        print(f"DownloadHistory entry with ID {history_id} not found.")