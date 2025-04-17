from urllib.parse import quote_plus
from app.core.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Build the database URL using the credentials from the config
DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD)
DATABASE_URL = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Creating the asynchronous engine for SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True for debugging SQL queries

# SessionLocal is used to create session objects tied to the database engine
SessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for all ORM models
Base = declarative_base()

# Database dependency to be injected into FastAPI routes
async def get_db():
    async with SessionLocal() as db:
        yield db
        