from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    path = Column(String, unique=True, index=True)
    storage_path = Column(String, unique=True)  # Actual path on disk
    mime_type = Column(String)
    size = Column(BigInteger)  # File size in bytes
    folder_id = Column(Integer, ForeignKey("folders.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    folder = relationship("Folder", back_populates="files")

    def __repr__(self):
        return f"<File {self.name}>"
