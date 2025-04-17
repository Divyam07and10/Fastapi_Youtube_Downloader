from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import DownloadHistory
from app.schemas.history import DownloadHistoryResponse
from app.db.database import get_db

router = APIRouter()

@router.get("/history", response_model=list[DownloadHistoryResponse])
async def get_history(
    db: AsyncSession = Depends(get_db)
):
    stmt = select(DownloadHistory).order_by(DownloadHistory.downloaded_at.desc())
    result = await db.execute(stmt)
    records = result.scalars().all()
    return [
        DownloadHistoryResponse(
            url=record.url,
            status=record.status,
            downloaded_at=record.downloaded_at.strftime("%Y-%m-%d %H:%M:%S"),
            download_url=record.download_url
        )
        for record in records
    ]
