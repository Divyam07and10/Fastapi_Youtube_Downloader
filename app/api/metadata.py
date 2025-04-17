from fastapi import APIRouter, HTTPException, Query, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import VideoMetadata
from app.db.database import get_db
from app.schemas.metadata import MetadataResponse
from app.services.metadata import extract_and_store_metadata
from app.utils.validators import is_valid_youtube_url

router = APIRouter()

@router.get("/metadata", response_model=MetadataResponse)
async def get_metadata(
    url: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    if not is_valid_youtube_url(url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL format.")

    stmt = select(VideoMetadata).filter_by(url=url)
    result = await db.execute(stmt)
    existing = result.scalars().first()

    if existing:
        return existing

    return await extract_and_store_metadata(url, db)
