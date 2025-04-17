from app.db.models import VideoMetadata
from app.utils.helpers import format_duration
from pytube import YouTube
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from functools import lru_cache
import yt_dlp

@lru_cache(maxsize=128)
def extract_metadata_yt_dlp(url: str):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "forcejson": True,
        "noplaylist": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        metadata = {
            "title": info.get("title"),
            "duration": format_duration(info.get("duration", 0)),
            "views": info.get("view_count"),
            "likes": info.get("like_count"),
            "channel": info.get("uploader"),
            "thumbnail_url": info.get("thumbnail"),
            "published_date": None
        }
        if info.get("upload_date"):
            try:
                dt = datetime.strptime(info["upload_date"], "%Y%m%d")
                metadata["published_date"] = dt.strftime("%Y-%m-%d")
            except:
                pass
        return metadata

async def extract_and_store_metadata(url: str, db: AsyncSession):
    try:
        metadata = extract_metadata_yt_dlp(url)
    except Exception as e:
        try:
            yt = YouTube(url)
            metadata = {
                "title": yt.title,
                "duration": format_duration(yt.length),
                "views": yt.views,
                "likes": None,
                "channel": yt.author,
                "thumbnail_url": yt.thumbnail_url,
                "published_date": yt.publish_date.strftime("%Y-%m-%d") if yt.publish_date else None
            }
        except Exception as fallback_e:
            raise Exception(f"yt-dlp error: {e}, pytube error: {fallback_e}")

    entry = VideoMetadata(url=url, **metadata)
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry
