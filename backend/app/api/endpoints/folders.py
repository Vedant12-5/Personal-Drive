from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.base import get_db
from app.services.folder_service import FolderService
from app.schemas.folder import Folder, FolderCreate, FolderUpdate, FolderContents
from app.models.folder import Folder as FolderModel
from app.models.file import File

router = APIRouter()


@router.post("/", response_model=Folder)
async def create_folder(
    folder: FolderCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new folder
    """
    try:
        db_folder = FolderService.create_folder(db, folder.name, folder.parent_id)
        return db_folder
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Folder])
async def get_root_folders(
    db: Session = Depends(get_db)
):
    """
    Get all root folders
    """
    return FolderService.get_root_folders(db)


@router.get("/{folder_id}", response_model=Folder)
async def get_folder(
    folder_id: int,
    db: Session = Depends(get_db)
):
    """
    Get folder details by ID
    """
    db_folder = FolderService.get_folder(db, folder_id)
    if not db_folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return db_folder


@router.get("/{folder_id}/contents")
async def get_folder_contents(
    folder_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all contents of a folder (files and subfolders)
    """
    try:
        print(f"Getting contents for folder_id: {folder_id}")
        
        # Check if folder exists
        folder = db.query(FolderModel).filter(FolderModel.id == folder_id).first()
        if not folder:
            print(f"Folder with id {folder_id} not found in database")
            raise ValueError(f"Folder with id {folder_id} not found")
            
        print(f"Found folder: {folder.name}, path: {folder.path}")
        
        # Get subfolders
        subfolders = db.query(FolderModel).filter(FolderModel.parent_id == folder_id).all()
        print(f"Found {len(subfolders)} subfolders")
        
        # Get files
        files = db.query(File).filter(File.folder_id == folder_id).all()
        print(f"Found {len(files)} files")
        
        # Create response manually
        result = {
            "id": folder.id,
            "name": folder.name,
            "path": folder.path,
            "parent_id": folder.parent_id,
            "created_at": folder.created_at,
            "updated_at": folder.updated_at,
            "files": [],
            "subfolders": []
        }
        
        # Add subfolders
        for subfolder in subfolders:
            result["subfolders"].append({
                "id": subfolder.id,
                "name": subfolder.name,
                "path": subfolder.path,
                "parent_id": subfolder.parent_id,
                "created_at": subfolder.created_at,
                "updated_at": subfolder.updated_at
            })
        
        # Add files with download URLs
        for file in files:
            file_dict = {
                "id": file.id,
                "name": file.name,
                "mime_type": file.mime_type,
                "size": file.size,
                "folder_id": file.folder_id,
                "path": file.path,
                "created_at": file.created_at,
                "updated_at": file.updated_at,
                "download_url": f"/files/{file.storage_path.split('storage/')[-1]}"
            }
            result["files"].append(file_dict)
        
        return result
    except ValueError as e:
        print(f"ValueError in get_folder_contents: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        print(f"Error in get_folder_contents: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))



@router.delete("/{folder_id}")
async def delete_folder(
    folder_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a folder and all its contents
    """
    try:
        success = FolderService.delete_folder(db, folder_id)
        if not success:
            raise HTTPException(status_code=404, detail="Folder not found")
        return {"message": "Folder deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{folder_id}", response_model=Folder)
async def update_folder(
    folder_id: int,
    folder_update: FolderUpdate,
    db: Session = Depends(get_db)
):
    """
    Update folder details (rename)
    """
    try:
        if folder_update.name:
            db_folder = FolderService.rename_folder(db, folder_id, folder_update.name)
            if not db_folder:
                raise HTTPException(status_code=404, detail="Folder not found")
            return db_folder
        else:
            raise HTTPException(status_code=400, detail="No update parameters provided")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
