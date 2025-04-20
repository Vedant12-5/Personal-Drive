from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api.api import api_router
from app.core.config import settings
from app.db.base import SessionLocal
from app.db.init_db import init_db

app = FastAPI(title=settings.PROJECT_NAME)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files for file downloads
if os.path.exists(settings.STORAGE_DIR):
    app.mount("/files", StaticFiles(directory=settings.STORAGE_DIR), name="files")

# Initialize database
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
