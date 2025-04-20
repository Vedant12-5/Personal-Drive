from fastapi import APIRouter

from app.api.endpoints import files, folders

api_router = APIRouter()
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(folders.router, prefix="/folders", tags=["folders"])
