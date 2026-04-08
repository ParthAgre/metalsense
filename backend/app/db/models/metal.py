from sqlalchemy import Column, Integer, String, Float
from app.db.base_class import Base

class HeavyMetal(Base):
    __tablename__ = "heavy_metals"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    standard_limit = Column(Float, nullable=True)
    health_effects = Column(String, nullable=True)
