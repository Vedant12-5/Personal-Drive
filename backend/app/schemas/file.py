from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class FileBase(BaseModel):
    name: str
    mime_type: Optional[str] = None
    size: int = 0
    folder_id: Optional[int] = None


class FileCreate(FileBase):
    pass


class FileUpdate(BaseModel):
    name: Optional[str] = None
    folder_id: Optional[int] = None


class FileInDB(FileBase):
    id: int
    path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class File(BaseModel):
    id: int
    name: str
    mime_type: Optional[str] = None
    size: int = 0
    folder_id: Optional[int] = None
    path: str
    created_at: datetime
    updated_at: datetime
    download_url: str
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, obj):
        return cls.model_validate(obj)
