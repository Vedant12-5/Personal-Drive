from app.db.base import SessionLocal, Base, engine
from app.models.folder import Folder
from app.models.file import File
from app.core.config import settings
import os

def debug_database():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if root folder exists
        root_folders = db.query(Folder).filter(Folder.parent_id == None).all()
        print(f"Root folders: {root_folders}")
        
        if not root_folders:
            print("Creating root folder...")
            # Create root folder
            root_folder = Folder(
                name="Root",
                path="/",
                storage_path=settings.STORAGE_DIR,
                parent_id=None
            )
            db.add(root_folder)
            db.commit()
            db.refresh(root_folder)
            print(f"Created root folder: {root_folder}")
        else:
            root_folder = root_folders[0]
            print(f"Root folder exists: {root_folder.name}, ID: {root_folder.id}")
            
            # Check if storage path exists
            if not os.path.exists(root_folder.storage_path):
                print(f"Storage path {root_folder.storage_path} does not exist, creating...")
                os.makedirs(root_folder.storage_path, exist_ok=True)
            else:
                print(f"Storage path exists: {root_folder.storage_path}")
        
        # List all folders
        all_folders = db.query(Folder).all()
        print(f"All folders: {len(all_folders)}")
        for folder in all_folders:
            print(f"  - {folder.id}: {folder.name}, path: {folder.path}, storage_path: {folder.storage_path}")
            
        # List all files
        all_files = db.query(File).all()
        print(f"All files: {len(all_files)}")
        for file in all_files:
            print(f"  - {file.id}: {file.name}, folder_id: {file.folder_id}")
            
    finally:
        db.close()

if __name__ == "__main__":
    debug_database()
