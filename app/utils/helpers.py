def build_format_selector(format: str, target_height: int) -> str:
    if format == "mp4":
        return f"bestvideo[height<={target_height}][ext=mp4]+bestaudio[acodec^=mp4a]/best[height<={target_height}][ext=mp4]"
    elif format == "webm":
        return f"bestvideo[height<={target_height}][ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best"
    elif format == "mkv":
        return f"bestvideo[height<={target_height}]+bestaudio/acodec!*=av01/best[height<={target_height}]"
    elif format == "mp3":
        return "bestaudio[acodec^=mp4a]/bestaudio"
    else:
        return "best"

def format_duration(seconds: int) -> str:
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}h {minutes}m {sec}s"
    else:
        return f"{minutes}m {sec}s"