from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
import uuid

from app.db.base import get_db
from app.services.file_service import FileService
from app.schemas.file import File, FileCreate, FileUpdate
from app.models.folder import Folder
from app.models.file import File as FileModel

router = APIRouter()


@router.post("/upload/")
async def upload_file(
    folder_id: int = Query(..., description="ID of the folder to upload to"),
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db)
):
    """
    Upload a file to a specific folder
    """
    try:
        # Print debug information
        print(f"Uploading file: {file.filename} to folder_id: {folder_id}")
        print(f"Content type: {file.content_type}")
        
        # Check if folder exists
        folder = db.query(Folder).filter(Folder.id == folder_id).first()
        if not folder:
            print(f"Folder with id {folder_id} not found")
            return JSONResponse(
                status_code=404,
                content={"detail": f"Folder with id {folder_id} not found"}
            )
        
        print(f"Found folder: {folder.name}, path: {folder.path}, storage_path: {folder.storage_path}")
        
        # Generate unique filename to avoid collisions
        file_ext = os.path.splitext(file.filename)[1] if file.filename and "." in file.filename else ""
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        
        # Create storage path
        storage_path = os.path.join(folder.storage_path, unique_filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        
        print(f"Saving file to: {storage_path}")
        
        # Save file to disk
        try:
            with open(storage_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"detail": f"Failed to save file: {str(e)}"}
            )
        
        # Get file size
        file_size = os.path.getsize(storage_path)
        
        # Create database record
        db_file = FileModel(
            name=file.filename,
            path=os.path.join(folder.path, file.filename),
            storage_path=storage_path,
            mime_type=file.content_type,
            size=file_size,
            folder_id=folder_id
        )
        
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        
        print(f"File saved successfully: {db_file.id}")
        
        # Return response as JSONResponse to avoid validation
        return JSONResponse(content={
            "id": db_file.id,
            "name": db_file.name,
            "mime_type": db_file.mime_type,
            "size": db_file.size,
            "folder_id": db_file.folder_id,
            "path": db_file.path,
            "created_at": db_file.created_at.isoformat(),
            "updated_at": db_file.updated_at.isoformat(),
            "download_url": f"/files/{db_file.storage_path.split('storage/')[-1]}"
        })
    except Exception as e:
        print(f"Exception in upload_file: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )


@router.get("/info/{file_id}", response_model=File)
async def get_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    """
    Get file details by ID
    """
    db_file = FileService.get_file(db, file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Add download URL to response
    result = File.from_orm(db_file)
    result.download_url = f"/files/{db_file.storage_path.split('storage/')[-1]}"
    
    return result


@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a file
    """
    success = FileService.delete_file(db, file_id)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"message": "File deleted successfully"}


@router.patch("/{file_id}", response_model=File)
async def update_file(
    file_id: int,
    file_update: FileUpdate,
    db: Session = Depends(get_db)
):
    """
    Update file details (rename or move)
    """
    try:
        if file_update.name:
            db_file = FileService.rename_file(db, file_id, file_update.name)
            if not db_file:
                raise HTTPException(status_code=404, detail="File not found")
            
            # Add download URL to response
            result = File.from_orm(db_file)
            result.download_url = f"/files/{db_file.storage_path.split('storage/')[-1]}"
            
            return result
        else:
            raise HTTPException(status_code=400, detail="No update parameters provided")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
