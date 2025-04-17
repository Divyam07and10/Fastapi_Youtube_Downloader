from pydantic import BaseModel

class DownloadRequest(BaseModel):
    url: str
    format: str = "mp4"
    quality: str = "720p"

class DownloadResponse(BaseModel):
    message: str
    filepath: str
