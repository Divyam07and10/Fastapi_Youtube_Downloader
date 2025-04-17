from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base

class DownloadHistory(Base):
    __tablename__ = "download_history"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    status = Column(String, nullable=False)
    downloaded_at = Column(DateTime, default=datetime.utcnow)
    download_url = Column(String, nullable=False)

class VideoMetadata(Base):
    __tablename__ = "video_metadata"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String)
    duration = Column(String)
    views = Column(Integer)
    likes = Column(Integer, nullable=True)
    channel = Column(String)
    thumbnail_url = Column(String)
    published_date = Column(String)
    fetched_at = Column(DateTime, default=datetime.utcnow)