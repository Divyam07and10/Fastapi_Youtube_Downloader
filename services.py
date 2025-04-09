import os
import time
import yt_dlp
from pytube import YouTube
from schemas import DownloadRequest
from utils import build_format_selector, format_duration
from fastapi import HTTPException

DOWNLOAD_DIR = "downloads"
RETRY_ATTEMPTS = 3

# Main function triggered in background
def start_download_task(request: DownloadRequest):
    output_basename = f"download_{int(time.time())}"
    final_path = os.path.join(DOWNLOAD_DIR, f"{output_basename}.{request.format}")

    # Retry with yt-dlp before falling back to pytube
    for attempt in range(RETRY_ATTEMPTS):
        try:
            download_with_ytdlp(request, os.path.join(DOWNLOAD_DIR, output_basename))
            return
        except Exception:
            time.sleep(1)

    # Fallback to pytube after failed attempts
    for attempt in range(RETRY_ATTEMPTS):
        try:
            download_with_pytube(request, final_path)
            return
        except Exception:
            time.sleep(1)

    # If all fail
    raise HTTPException(status_code=500, detail="Download failed using both yt-dlp and pytube.")

def download_with_ytdlp(request: DownloadRequest, output_path: str):
    format_selector = build_format_selector(request.format, request.quality)
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
            "preferedformat": request.format,
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([request.url])

def download_with_pytube(request: DownloadRequest, final_path: str):
    yt = YouTube(request.url)
    if request.format == "mp3":
        stream = yt.streams.filter(only_audio=True).first()
    else:
        stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()

    if not stream:
        raise Exception("No stream found.")

    stream.download(output_path=DOWNLOAD_DIR, filename=os.path.basename(final_path))

def extract_video_metadata(url: str) -> dict:
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "forcejson": True,
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "duration": format_duration(info.get("duration", 0)),
                "views": info.get("view_count"),
                "likes": info.get("like_count"),
                "channel": info.get("uploader"),
                "thumbnail_url": info.get("thumbnail"),
                "published_date": info.get("upload_date")
            }
    except Exception:
        # Fallback to pytube
        yt = YouTube(url)
        return {
            "title": yt.title,
            "duration": format_duration(yt.length),
            "views": yt.views,
            "likes": None,
            "channel": yt.author,
            "thumbnail_url": yt.thumbnail_url,
            "published_date": yt.publish_date.strftime("%Y-%m-%d") if yt.publish_date else None
        }