from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class EducationMaterial(Base):
    __tablename__ = "education_materials"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False) # e.g. "article", "fact"
    title = Column(String, nullable=False)
    content_markdown = Column(Text, nullable=False)
    target_metal_id = Column(Integer, ForeignKey("heavy_metals.id"), nullable=True)

    metal = relationship("HeavyMetal", backref="education_materials")
