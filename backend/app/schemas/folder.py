from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class FolderBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class FolderCreate(FolderBase):
    pass


class FolderUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None


class FolderInDB(FolderBase):
    id: int
    path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Folder(FolderInDB):
    pass


class FolderContents(Folder):
    files: List["File"] = []
    subfolders: List["Folder"] = []


# Avoid circular import issues
from app.schemas.file import File
FolderContents.update_forward_refs()
