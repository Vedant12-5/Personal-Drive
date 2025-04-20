from sqlalchemy.orm import Session
from app.db.base import Base, engine
from app.models.folder import Folder
from app.core.config import settings
import os

def init_db(db: Session) -> None:
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Check if root folder exists
    root_folder = db.query(Folder).filter(Folder.parent_id == None).first()
    if not root_folder:
        # Create root folder
        root_folder = Folder(
            name="Root",
            path="/",
            storage_path=settings.STORAGE_DIR,
            parent_id=None
        )
        db.add(root_folder)
        db.commit()
        
        # Create storage directory if it doesn't exist
        os.makedirs(settings.STORAGE_DIR, exist_ok=True)
