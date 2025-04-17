from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import API_KEY

API_KEY_NAME = "X-API-Key"
VALID_API_KEY = API_KEY
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def validate_api_key(api_key: str = Depends(api_key_header)):
    if api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )