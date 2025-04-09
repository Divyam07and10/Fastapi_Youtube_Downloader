import os

def create_download_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def build_format_selector(format: str, quality: str) -> str:
    height = quality.replace("p", "")
    if format == "mp4":
        return f"bestvideo[height<={height}][vcodec!*=av01][ext=mp4]+bestaudio[acodec^=mp4a]/best"
    elif format == "webm":
        return f"bestvideo[height<={height}][ext=webm]+bestaudio[ext=webm]/best"
    elif format == "mkv":
        return f"bestvideo[height<={height}]+bestaudio/merge"
    elif format == "mp3":
        return "bestaudio[acodec^=mp4a]/bestaudio"
    return "best"

def format_duration(seconds: int) -> str:
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m {sec}s"
    return f"{minutes}m {sec}s"
