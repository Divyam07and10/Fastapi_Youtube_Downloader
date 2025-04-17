from pydantic import BaseModel, HttpUrl
from typing import Optional

class MetadataRequest(BaseModel):
    url: HttpUrl

class MetadataResponse(BaseModel):
    url: str
    title: Optional[str]
    duration: Optional[str]
    views: Optional[int]
    likes: Optional[int]
    channel: Optional[str]
    thumbnail_url: Optional[str]
    published_date: Optional[str]

    class Config:
        from_attributes = True
