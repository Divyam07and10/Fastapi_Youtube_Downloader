from pydantic import BaseModel

class DownloadHistoryResponse(BaseModel):
    url: str
    status: str
    downloaded_at: str
    download_url: str
