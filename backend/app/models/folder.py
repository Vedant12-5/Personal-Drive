from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    path = Column(String, unique=True, index=True)  # Virtual path for API
    storage_path = Column(String, unique=True)  # Actual path on disk
    parent_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    files = relationship("File", back_populates="folder", cascade="all, delete-orphan")
    children = relationship("Folder", 
                        back_populates="parent",
                        cascade="all, delete-orphan")
    parent = relationship("Folder", back_populates="children", remote_side=[id])
    def __repr__(self):
        return f"<Folder {self.name}>"
