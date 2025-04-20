import os
import shutil
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.models.folder import Folder
from app.core.config import settings


class FolderService:
    @staticmethod
    def create_folder(db: Session, name: str, parent_id: Optional[int] = None) -> Folder:
        """
        Create a new folder
        """
        # Handle root folder case
        if parent_id is None:
            parent_path = ""
            parent_storage_path = settings.STORAGE_DIR
        else:
            # Get parent folder
            parent = db.query(Folder).filter(Folder.id == parent_id).first()
            if not parent:
                raise ValueError("Parent folder not found")
            parent_path = parent.path
            parent_storage_path = parent.storage_path
        
        # Create virtual path
        path = os.path.join(parent_path, name)
        
        # Create storage path
        storage_path = os.path.join(parent_storage_path, name)
        
        # Create directory on disk
        os.makedirs(storage_path, exist_ok=True)
        
        # Create database record
        db_folder = Folder(
            name=name,
            path=path,
            storage_path=storage_path,
            parent_id=parent_id
        )
        
        db.add(db_folder)
        db.commit()
        db.refresh(db_folder)
        
        return db_folder
    
    @staticmethod
    def get_folder(db: Session, folder_id: int) -> Optional[Folder]:
        """
        Get folder by ID
        """
        return db.query(Folder).filter(Folder.id == folder_id).first()
    
    @staticmethod
    def get_folder_by_path(db: Session, path: str) -> Optional[Folder]:
        """
        Get folder by path
        """
        return db.query(Folder).filter(Folder.path == path).first()
    
    @staticmethod
    def get_root_folders(db: Session) -> List[Folder]:
        """
        Get all root folders (folders with no parent)
        """
        return db.query(Folder).filter(Folder.parent_id == None).all()
    
    @staticmethod
    def get_subfolders(db: Session, parent_id: int) -> List[Folder]:
        """
        Get all subfolders of a folder
        """
        return db.query(Folder).filter(Folder.parent_id == parent_id).all()
    
    @staticmethod
    def delete_folder(db: Session, folder_id: int) -> bool:
        """
        Delete a folder and all its contents
        """
        folder = db.query(Folder).filter(Folder.id == folder_id).first()
        if not folder:
            return False
        
        # Delete from storage
        try:
            if os.path.exists(folder.storage_path):
                shutil.rmtree(folder.storage_path)
        except Exception as e:
            raise ValueError(f"Failed to delete folder: {str(e)}")
        
        # Delete from database (cascade will handle children)
        db.delete(folder)
        db.commit()
        
        return True
    
    @staticmethod
    def rename_folder(db: Session, folder_id: int, new_name: str) -> Optional[Folder]:
        """
        Rename a folder
        """
        folder = db.query(Folder).filter(Folder.id == folder_id).first()
        if not folder:
            return None
        
        # Get parent path
        parent_path = os.path.dirname(folder.path)
        parent_storage_path = os.path.dirname(folder.storage_path)
        
        # Create new paths
        new_path = os.path.join(parent_path, new_name)
        new_storage_path = os.path.join(parent_storage_path, new_name)
        
        # Rename directory on disk
        try:
            os.rename(folder.storage_path, new_storage_path)
        except Exception as e:
            raise ValueError(f"Failed to rename folder: {str(e)}")
        
        # Update database record
        folder.name = new_name
        folder.path = new_path
        folder.storage_path = new_storage_path
        
        db.commit()
        db.refresh(folder)
        
        return folder
    
    @staticmethod
    def get_folder_contents(db: Session, folder_id: int) -> Dict[str, Any]:
        """
        Get all contents of a folder (files and subfolders)
        """
        folder = db.query(Folder).filter(Folder.id == folder_id).first()
        if not folder:
            raise ValueError("Folder not found")
        
        # Get subfolders
        subfolders = db.query(Folder).filter(Folder.parent_id == folder_id).all()
        
        # Get files
        files = folder.files
        
        return {
            "folder": folder,
            "subfolders": subfolders,
            "files": files
        }
