from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    upload_status = Column(String, default="completed")
    created_at = Column(DateTime, default=datetime.utcnow)

    uploader = relationship("User", backref="datasets")
    samples = relationship("Sample", back_populates="dataset", cascade="all, delete-orphan")
