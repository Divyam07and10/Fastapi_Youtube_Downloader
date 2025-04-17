from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import download, metadata, history

app = FastAPI()

app.include_router(download.router, tags=["Download"])
app.include_router(metadata.router, tags=["Metadata"])
app.include_router(history.router, tags=["History"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
