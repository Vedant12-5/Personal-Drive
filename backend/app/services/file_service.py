import os
import shutil
import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.file import File
from app.models.folder import Folder
from app.core.config import settings


class FileService:
    @staticmethod
    def create_file(db: Session, folder_id: int, file: UploadFile) -> File:
        """
        Save an uploaded file to storage and create a database record
        """
        # Check if folder exists
        folder = db.query(Folder).filter(Folder.id == folder_id).first()
        if not folder:
            raise ValueError("Folder not found")
        
        # Generate unique filename to avoid collisions
        file_ext = os.path.splitext(file.filename)[1] if file.filename and "." in file.filename else ""
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        
        # Create storage path
        folder_storage_path = folder.storage_path if hasattr(folder, 'storage_path') else os.path.join(settings.STORAGE_DIR, str(folder_id))
        storage_path = os.path.join(folder_storage_path, unique_filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        
        # Save file to disk
        try:
            with open(storage_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise ValueError(f"Failed to save file: {str(e)}")
        
        # Get file size
        file_size = os.path.getsize(storage_path)
        
        # Create database record
        db_file = File(
            name=file.filename,
            path=os.path.join(folder.path if hasattr(folder, 'path') else f"/folder/{folder_id}", file.filename),
            storage_path=storage_path,
            mime_type=file.content_type,
            size=file_size,
            folder_id=folder_id
        )
        
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        
        return db_file
    
    @staticmethod
    def get_file(db: Session, file_id: int) -> Optional[File]:
        """
        Get file by ID
        """
        return db.query(File).filter(File.id == file_id).first()
    
    @staticmethod
    def get_files_in_folder(db: Session, folder_id: int) -> List[File]:
        """
        Get all files in a folder
        """
        return db.query(File).filter(File.folder_id == folder_id).all()
    
    @staticmethod
    def delete_file(db: Session, file_id: int) -> bool:
        """
        Delete a file from storage and database
        """
        file = db.query(File).filter(File.id == file_id).first()
        if not file:
            return False
        
        # Delete from storage
        try:
            if os.path.exists(file.storage_path):
                os.remove(file.storage_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")
        
        # Delete from database
        db.delete(file)
        db.commit()
        
        return True
    
    @staticmethod
    def rename_file(db: Session, file_id: int, new_name: str) -> Optional[File]:
        """
        Rename a file
        """
        file = db.query(File).filter(File.id == file_id).first()
        if not file:
            return None
        
        # Update database record
        file.name = new_name
        file.path = os.path.join(os.path.dirname(file.path), new_name)
        
        db.commit()
        db.refresh(file)
        
        return file
